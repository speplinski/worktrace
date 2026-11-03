"""Revocation e-process of §4.6: false-revocation rate at the boundary and the median detection delay when the true
rate doubles. Betting e-process M_t = prod(1 + lambda (X_t - alpha')), revoke at M_t >= 1/delta_rev; lambda is the
Kelly bet for the alternative p = 2 alpha', capped below 1/alpha'. Monte Carlo, fixed seed. Run: python paper/pilot/revocation_delay.py"""
import numpy as np

DELTA_REV, N, T, SEED = 0.05, 50_000, 4_000, 20261103


def simulate(alpha_p, p_true, rng):
    lam = min((2 * alpha_p - alpha_p) / (alpha_p * (1 - alpha_p)), 0.999 / alpha_p)
    x = (rng.random((N, T)) < p_true).astype(float)
    m = np.cumprod(1 + lam * (x - alpha_p), axis=1)
    hit = m >= 1 / DELTA_REV
    ever = hit.any(axis=1)
    t = np.where(ever, hit.argmax(axis=1) + 1, T + 1)
    return ever.mean(), float(np.median(t[ever])) if ever.any() else float("inf"), lam


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    print(f"delta_rev = {DELTA_REV}; {N:,} paths of {T:,} audited episodes each; lambda = Kelly bet for p = 2 alpha'")
    for ap in (0.05, 0.10, 0.15, 0.20):
        fr, _, lam = simulate(ap, ap, rng)
        _, md, _ = simulate(ap, 2 * ap, rng)
        print(f"alpha' = {ap:.2f} (lambda = {lam:.2f}): false-revocation rate at p = alpha' {fr:.3f}; "
              f"median delay at p = 2 alpha' {md:.0f} audited episodes")
