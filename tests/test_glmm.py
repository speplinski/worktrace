import numpy as np

from worktrace import glmm


def test_recovers_simulated_parameters():
    rng = np.random.default_rng(7)
    G, n = 40, 150
    b0, b1, sigma = -1.0, -0.8, 0.7
    X, y, g = [], [], []
    for j in range(G):
        u = rng.normal(0, sigma)
        x = rng.integers(0, 2, n)
        p = 1 / (1 + np.exp(-(b0 + b1 * x + u)))
        X += [[1.0, float(v)] for v in x]
        y += list(rng.random(n) < p)
        g += [j] * n
    r = glmm.fit(np.array(X), np.array(y, float), g, names=["intercept", "x"])
    assert r["converged"]
    assert abs(r["coef"]["x"]["est"] - b1) < 3 * r["coef"]["x"]["se"]
    assert abs(r["coef"]["intercept"]["est"] - b0) < 0.4
    assert 0.4 < r["sigma"] < 1.1
    assert r["coef"]["x"]["p_lower"] < 0.01


def test_weights_equal_duplicated_rows():
    rng = np.random.default_rng(3)
    X = np.column_stack([np.ones(200), rng.integers(0, 2, 200)])
    y = (rng.random(200) < 0.3).astype(float)
    g = list(rng.integers(0, 5, 200))
    a = glmm.fit(np.vstack([X, X]), np.concatenate([y, y]), g + g)
    b = glmm.fit(X, y, g, w=np.full(200, 2.0))
    assert abs(a["coef"]["b1"]["est"] - b["coef"]["b1"]["est"]) < 1e-3


def test_likelihood_matches_brute_force_integration():
    """Adaptive Gauss-Hermite cluster log-likelihood vs scipy quad, incl. a group with no events and fractional weights."""
    import math
    from scipy import integrate, special
    rng = np.random.default_rng(11)
    for sigma in (0.05, 0.7, 3.0):
        for events in (True, False):
            eta = rng.normal(-1.5, 1.0, 30)
            y = (rng.random(30) < 0.3).astype(float) if events else np.zeros(30)
            w = rng.choice([0.5, 1.0, 2.0], 30)
            f = lambda u: math.exp(float(np.sum(w * (y * (eta + u) - np.logaddexp(0, eta + u))))) \
                * math.exp(-u * u / (2 * sigma ** 2)) / math.sqrt(2 * math.pi * sigma ** 2)
            ref = math.log(integrate.quad(f, -12 * sigma - 10, 12 * sigma + 10, limit=400, epsabs=0, epsrel=1e-11)[0])
            assert abs(glmm._cluster_loglik(eta, y, w, sigma) - ref) < 1e-4
