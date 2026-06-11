from os import path

from Src.Utils.Utils import default_checkpoint_metadata


# Parent to all algorithm
class Agent:

    def __init__(self, config):      
        self.config = config
        self.checkpoint_metadata = getattr(
            config,
            "checkpoint_metadata",
            default_checkpoint_metadata(
                status="not_requested",
                checkpoint_path=getattr(config, "checkpoint_path", ""),
                run_mode=getattr(config, "run_mode", "smoke"),
                checkpoint_required=getattr(config, "require_checkpoint", False),
                checkpoint_intentional_mismatch=getattr(config, "allow_checkpoint_mismatch", False),
                run_id=getattr(config, "run_id", ""),
            ),
        )

        # Abstract class variables
        self.modules = None

    def init(self):
         for name, m in self.modules:
             m.to(self.config.device)

    def clear_gradients(self):
        for _, module in self.modules:
            module.optim.zero_grad()
            
    def clear_actor_gradients(self):
        self.modules[0][1].optim.zero_grad()

    def clear_critic_gradients(self):
        self.modules[1][1].optim.zero_grad()

    def save(self):
        if self.config.save_model:
            for name, module in self.modules:
                module.save(self.config.paths['checkpoint'] + name+'.pt')

    def load_checkpoint(
        self,
        checkpoint_path=None,
        require_checkpoint=None,
        allow_checkpoint_mismatch=None,
        run_mode=None,
    ):
        checkpoint_path = checkpoint_path if checkpoint_path is not None else getattr(self.config, "checkpoint_path", "")
        run_mode = run_mode or getattr(self.config, "run_mode", "smoke")
        require_checkpoint = (
            bool(require_checkpoint)
            if require_checkpoint is not None
            else bool(getattr(self.config, "require_checkpoint", False))
        )
        allow_checkpoint_mismatch = (
            bool(allow_checkpoint_mismatch)
            if allow_checkpoint_mismatch is not None
            else bool(getattr(self.config, "allow_checkpoint_mismatch", False))
        )
        run_id = getattr(self.config, "run_id", "")
        settings_summary = {
            "algo_name": getattr(self.config, "algo_name", ""),
            "run_mode": run_mode,
            "require_checkpoint": require_checkpoint,
            "allow_checkpoint_mismatch": allow_checkpoint_mismatch,
        }

        if allow_checkpoint_mismatch and run_mode in ("pilot", "formal"):
            raise ValueError("checkpoint mismatch is diagnostic-only and cannot be used in pilot/formal mode")

        if not checkpoint_path:
            metadata = default_checkpoint_metadata(
                status="not_requested",
                checkpoint_path="",
                checkpoint_required=require_checkpoint,
                checkpoint_intentional_mismatch=False,
                checkpoint_model_type=self.__class__.__name__,
                checkpoint_compatibility_reason="checkpoint not requested",
                run_mode=run_mode,
                run_id=run_id,
                settings_summary=settings_summary,
            )
            self.checkpoint_metadata = metadata
            self.config.checkpoint_metadata = metadata.copy()
            return metadata

        module_status = {}
        statuses = []
        for name, module in self.modules or []:
            module_path = checkpoint_path
            if path.isdir(str(checkpoint_path)):
                module_path = path.join(str(checkpoint_path), name + ".pt")
            status = module.load(
                module_path,
                required=require_checkpoint,
                allow_mismatch=allow_checkpoint_mismatch,
                run_mode=run_mode,
                run_id=run_id,
                settings_summary=settings_summary,
            )
            module_status[name] = status
            statuses.append(status.get("checkpoint_load_status", "failed"))

        if not statuses:
            aggregate_status = "not_requested"
        elif all(status == "loaded" for status in statuses):
            aggregate_status = "loaded"
        elif any(status == "intentional_mismatch" for status in statuses):
            aggregate_status = "intentional_mismatch"
        else:
            aggregate_status = "failed"

        first = next(iter(module_status.values()), {})
        metadata = default_checkpoint_metadata(
            status=aggregate_status,
            checkpoint_path=str(checkpoint_path),
            checkpoint_required=require_checkpoint,
            checkpoint_intentional_mismatch=(aggregate_status == "intentional_mismatch"),
            checkpoint_load_error=first.get("checkpoint_load_error", ""),
            checkpoint_hash=first.get("checkpoint_hash", ""),
            checkpoint_model_type=self.__class__.__name__,
            checkpoint_compatibility_reason=first.get("checkpoint_compatibility_reason", ""),
            run_mode=run_mode,
            run_id=run_id,
            settings_summary=settings_summary,
        )
        metadata["modules"] = module_status
        self.checkpoint_metadata = metadata
        self.config.checkpoint_metadata = metadata.copy()
        return metadata

    def step(self, loss, clip_norm=False):
        self.clear_gradients()
        loss.backward()
        for _, module in self.modules:
            module.step(clip_norm)
            
    def actor_step(self, loss, clip_norm=False):
        self.clear_actor_gradients()
        loss.backward()
        self.modules[0][1].step(clip_norm)
    def critic_step(self, loss, clip_norm=False):
        self.clear_actor_gradients()
        loss.backward()
        self.modules[1][1].step(clip_norm)

    def reset(self):
        for _, module in self.modules:
            module.reset()
