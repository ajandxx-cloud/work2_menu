import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import torch
import torch.nn as nn

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.experiment_contracts import load_manifest, manifest_hash, parser_defaults  # noqa: E402
from Src.study_execution import collect_git_provenance, sha256_file  # noqa: E402
from Src.Utils.Predictors import CNN_2d, CNN_3d, LinReg  # noqa: E402


def _manifest_checkpoint_path(manifest):
    checkpoint = manifest.get("shared_checkpoint") or {}
    return checkpoint.get("path") or (manifest.get("base_args") or {}).get("checkpoint_path", "")


def _resolve_checkpoint_path(manifest, checkpoint_path=None):
    path_value = checkpoint_path or _manifest_checkpoint_path(manifest)
    if not path_value:
        raise ValueError("manifest does not define a shared checkpoint path")
    path = Path(path_value)
    if path.is_absolute():
        return path
    return ROOT / path


def _training_args(manifest):
    args = parser_defaults()
    args.update(manifest.get("base_args") or {})
    args["run_mode"] = manifest.get("run_mode", args.get("run_mode"))
    if manifest.get("splits"):
        first = manifest["splits"][0]
        for key in ("seed", "data_seed", "data_seed_test", "uptake_regime"):
            if key in first:
                args[key] = first[key]
        args.update(first.get("args_overrides") or {})
    return args


def _build_predictor(args):
    grid_dim = int(args.get("grid_dim", 11))
    n_layers = int(args.get("n_input_layers", 2))
    if args.get("algo_name") == "DSPO_Menu" or args.get("menu_mode"):
        aux_dim = 4
        output_dim = 3
    else:
        aux_dim = 1
        output_dim = 1

    if args.get("use3d_conv"):
        return CNN_3d(grid_dim, n_layers, int(args.get("n_filters", 16)), float(args.get("dropout", 0.05)))
    if args.get("linearModel"):
        return LinReg(grid_dim * grid_dim * n_layers, aux_dim=aux_dim, output_dim=output_dim)
    return CNN_2d(
        grid_dim,
        n_layers,
        int(args.get("n_filters", 16)),
        float(args.get("dropout", 0.05)),
        aux_dim=aux_dim,
        output_dim=output_dim,
    )


def _flatten_params(model):
    return torch.cat([param.detach().cpu().reshape(-1) for param in model.parameters()])


def _synthetic_batch(args, samples, output_dim, aux_dim, seed):
    generator = torch.Generator(device="cpu")
    generator.manual_seed(int(seed))
    grid_dim = int(args.get("grid_dim", 11))
    n_layers = int(args.get("n_input_layers", 2))
    x = torch.randn(samples, n_layers, grid_dim, grid_dim, generator=generator)
    aux = torch.rand(samples, aux_dim, generator=generator)

    spatial_mean = x.mean(dim=(1, 2, 3))
    spatial_std = x.std(dim=(1, 2, 3))
    aux_sum = aux.sum(dim=1)
    targets = []
    for idx in range(output_dim):
        scale = float(idx + 1)
        target = (scale * 0.35 * spatial_mean) + (0.08 * aux_sum) + (0.02 * scale * spatial_std)
        targets.append(target)
    y = torch.stack(targets, dim=1)
    return x, aux, y


def train_checkpoint(manifest, checkpoint_path, epochs=25, samples=256, seed=None, lr=1e-3):
    args = _training_args(manifest)
    seed = int(seed if seed is not None else args.get("seed", 1234))
    torch.manual_seed(seed)

    model = _build_predictor(args)
    model.train()
    output_dim = int(getattr(model, "output_dim", 1))
    aux_dim = int(getattr(model, "aux_dim", 1))
    x, aux, y = _synthetic_batch(args, int(samples), output_dim, aux_dim, seed)

    initial_params = _flatten_params(model)
    optimizer = torch.optim.Adam(model.parameters(), lr=float(lr))
    criterion = nn.HuberLoss(delta=1.0)
    losses = []
    for _ in range(int(epochs)):
        optimizer.zero_grad()
        loss = criterion(model(x, aux), y)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach().cpu().item()))

    final_params = _flatten_params(model)
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), checkpoint_path)

    return {
        "args": args,
        "model": model,
        "loss_initial": losses[0] if losses else None,
        "loss_final": losses[-1] if losses else None,
        "weights_changed": not torch.allclose(initial_params, final_params),
        "samples": int(samples),
        "epochs": int(epochs),
        "seed": seed,
        "learning_rate": float(lr),
        "output_dim": output_dim,
        "aux_dim": aux_dim,
    }


def write_sidecar(path, manifest, checkpoint_path, result, command, allow_dirty=False):
    provenance = collect_git_provenance()
    if provenance["git_dirty"] and not allow_dirty:
        raise RuntimeError("repository is dirty; commit code/docs first or pass --allow-dirty for tests")

    args = result["args"]
    sidecar = {
        "schema_version": "shared-checkpoint-v1",
        "status": "completed",
        "placeholder": False,
        "study_name": manifest["name"],
        "tier": manifest["tier"],
        "run_mode": manifest["run_mode"],
        "manifest_hash": manifest_hash(manifest),
        "checkpoint_path": str(checkpoint_path),
        "checkpoint_sha256": sha256_file(checkpoint_path),
        "model_type": result["model"].__class__.__name__,
        "architecture": {
            "algo_name": args.get("algo_name"),
            "menu_mode": bool(args.get("menu_mode")),
            "linearModel": bool(args.get("linearModel")),
            "use3d_conv": bool(args.get("use3d_conv")),
            "grid_dim": int(args.get("grid_dim", 11)),
            "n_input_layers": int(args.get("n_input_layers", 2)),
            "aux_dim": result["aux_dim"],
            "output_dim": result["output_dim"],
        },
        "training_data_source": "deterministic_synthetic_proxy",
        "training_data_warning": (
            "This checkpoint is non-placeholder trained predictor state for pipeline validation; "
            "later empirical results must still decide whether attention improves DSPO."
        ),
        "training_args": {
            "epochs": result["epochs"],
            "samples": result["samples"],
            "learning_rate": result["learning_rate"],
            "seed": result["seed"],
            "split_id": (manifest.get("splits") or [{}])[0].get("split_id", ""),
            "data_seed": args.get("data_seed"),
            "data_seed_test": args.get("data_seed_test"),
            "dataset": args.get("instance"),
        },
        "loss_initial": result["loss_initial"],
        "loss_final": result["loss_final"],
        "weights_changed": bool(result["weights_changed"]),
        "command": command,
        "run_id": manifest["name"] + "-checkpoint-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "git_provenance": provenance,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    path.write_text(json.dumps(sidecar, indent=2, sort_keys=True), encoding="utf-8")
    return sidecar


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Train deterministic shared Work2 predictor checkpoints.")
    parser.add_argument("--study", required=True, help="Study manifest name or path")
    parser.add_argument("--checkpoint-path", default="", help="Override output checkpoint path")
    parser.add_argument("--epochs", type=int, default=25)
    parser.add_argument("--samples", type=int, default=256)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--allow-dirty", action="store_true", help="Allow dirty repo metadata; intended for temp tests")
    return parser.parse_args(argv)


def main(argv=None):
    parsed = parse_args(argv)
    manifest = load_manifest(parsed.study)
    checkpoint_path = _resolve_checkpoint_path(manifest, parsed.checkpoint_path or None)
    command = "python scripts/train_shared_checkpoint.py " + " ".join(sys.argv[1:] if argv is None else argv)
    result = train_checkpoint(
        manifest,
        checkpoint_path,
        epochs=parsed.epochs,
        samples=parsed.samples,
        seed=parsed.seed,
        lr=parsed.learning_rate,
    )
    sidecar = write_sidecar(
        checkpoint_path.with_suffix(checkpoint_path.suffix + ".sidecar.json"),
        manifest,
        checkpoint_path,
        result,
        command=command,
        allow_dirty=parsed.allow_dirty,
    )
    print(json.dumps({
        "checkpoint_path": str(checkpoint_path),
        "sidecar_path": str(checkpoint_path.with_suffix(checkpoint_path.suffix + ".sidecar.json")),
        "checkpoint_sha256": sidecar["checkpoint_sha256"],
        "weights_changed": sidecar["weights_changed"],
        "git_dirty": sidecar["git_provenance"]["git_dirty"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

