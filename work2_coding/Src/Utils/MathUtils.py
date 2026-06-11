import math


try:
    from scipy.special import lambertw as _scipy_lambertw
except Exception:
    _scipy_lambertw = None


class _LambertWValue(float):
    @property
    def real(self):
        return float(self)


def _lambertw_principal_real(x):
    x = float(x)
    if x < -1.0 / math.e:
        raise ValueError("lambertw principal branch is undefined for x < -1/e")
    if x == 0.0:
        return 0.0

    w = math.log1p(x) if x > -0.25 else -0.5
    for _ in range(40):
        ew = math.exp(w)
        f = w * ew - x
        denom = ew * (w + 1.0) - ((w + 2.0) * f / (2.0 * w + 2.0))
        if abs(denom) < 1e-14:
            break
        step = f / denom
        w -= step
        if abs(step) <= 1e-12 * (1.0 + abs(w)):
            break
    return w


def lambertw(x):
    if _scipy_lambertw is not None:
        return _scipy_lambertw(x)
    return _LambertWValue(_lambertw_principal_real(x))
