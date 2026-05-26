from math import exp, log


def _lambertw_principal_real(x, max_iter=50, tol=1e-12):
    x = float(x)
    if x == 0.0:
        return 0.0
    if x < -0.36787944117144233:
        raise ValueError("Lambert W principal branch is only implemented for x >= -1/e.")

    if x < 1.0:
        w = x
    else:
        w = log(x)
        if x > 3.0:
            w -= log(max(w, 1e-12))

    for _ in range(max_iter):
        e_w = exp(w)
        f = w * e_w - x
        denom = e_w * (w + 1.0)
        if abs(denom) < 1e-12:
            break
        step = f / denom
        w_next = w - step
        if abs(w_next - w) <= tol * max(1.0, abs(w_next)):
            return w_next
        w = w_next
    return w


def lambertw(x):
    try:
        from scipy.special import lambertw as scipy_lambertw

        return scipy_lambertw(x)
    except ModuleNotFoundError:
        return complex(_lambertw_principal_real(x), 0.0)
