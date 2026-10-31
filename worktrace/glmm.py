"""Random-intercept logistic regression (GLMM) by maximum likelihood with adaptive Gauss-Hermite quadrature.

Pre-registered H3 model (amendment A11.5): logit P(y = 1) = X @ beta + u_g, u_g ~ N(0, sigma^2), one random intercept
per group (configuration). Observations may carry weights (tied selections, A7). Written here because lme4 is not
available; checked against simulated data in tests/test_glmm.py.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import optimize, special

_NODES, _WEIGHTS = np.polynomial.hermite.hermgauss(25)


def _cluster_loglik(eta: np.ndarray, y: np.ndarray, w: np.ndarray, sigma: float) -> float:
    """log of the integral over u of prod_i Bernoulli(y_i | eta_i + u)^w_i * N(u; 0, sigma^2), adaptive GH."""
    def g(u):
        z = eta + u
        return float(np.sum(w * (y * z - np.logaddexp(0.0, z)))) - u * u / (2 * sigma * sigma)
    # mode of g by damped Newton (g is strictly concave): halve the step until g does not decrease
    u, gu = 0.0, g(0.0)
    for _ in range(200):
        p = special.expit(eta + u)
        d1 = float(np.sum(w * (y - p))) - u / sigma ** 2
        d2 = -float(np.sum(w * p * (1 - p))) - 1 / sigma ** 2
        step = d1 / d2
        t = 1.0
        while t > 1e-8:
            gn = g(u - t * step)
            if gn >= gu:
                break
            t /= 2
        u, gu = u - t * step, gn
        if abs(t * step) < 1e-12:
            break
    p = special.expit(eta + u)
    h = float(np.sum(w * p * (1 - p))) + 1 / sigma ** 2
    s = math.sqrt(2.0 / h)
    vals = np.array([g(u + s * x) for x in _NODES]) + _NODES ** 2
    m = vals.max()
    integral_log = m + math.log(float(np.sum(_WEIGHTS * np.exp(vals - m)))) + math.log(s)
    return integral_log - 0.5 * math.log(2 * math.pi * sigma * sigma)


def negloglik(theta: np.ndarray, X: np.ndarray, y: np.ndarray, w: np.ndarray, groups: list[np.ndarray]) -> float:
    beta, sigma = theta[:-1], math.exp(theta[-1])
    eta = X @ beta
    return -sum(_cluster_loglik(eta[idx], y[idx], w[idx], sigma) for idx in groups)


def _hessian(f, x: np.ndarray, eps: float = 1e-4) -> np.ndarray:
    k = len(x)
    H = np.zeros((k, k))
    for i in range(k):
        for j in range(i, k):
            ei, ej = np.zeros(k), np.zeros(k)
            ei[i], ej[j] = eps, eps
            H[i, j] = H[j, i] = (f(x + ei + ej) - f(x + ei - ej) - f(x - ei + ej) + f(x - ei - ej)) / (4 * eps * eps)
    return H


def fit(X: np.ndarray, y: np.ndarray, group: list, w: np.ndarray | None = None, names: list[str] | None = None) -> dict:
    """Fit the model; returns estimates, Wald standard errors (observed information) and sigma."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    w = np.ones(len(y)) if w is None else np.asarray(w, float)
    labels = sorted(set(group), key=str)
    groups = [np.array([i for i, g in enumerate(group) if g == lab]) for lab in labels]
    f = lambda t: negloglik(t, X, y, w, groups)
    theta0 = np.zeros(X.shape[1] + 1)
    theta0[-1] = math.log(0.5)
    # Nelder-Mead is robust to the flat likelihood when some groups have no events; BFGS then polishes
    nm = optimize.minimize(f, theta0, method="Nelder-Mead",
                           options={"xatol": 1e-7, "fatol": 1e-9, "maxiter": 40000, "maxfev": 80000})
    res = optimize.minimize(f, nm.x, method="BFGS", options={"gtol": 1e-6, "maxiter": 500})
    if res.fun > nm.fun:
        res = nm
    H = _hessian(f, res.x, eps=1e-3)
    try:
        cov = np.linalg.inv(H)
        se = np.sqrt(np.clip(np.diag(cov), 0, None))
    except np.linalg.LinAlgError:
        se = np.full(len(res.x), float("nan"))
    names = names or [f"b{i}" for i in range(X.shape[1])]
    # BFGS with numerical gradients often stops with "precision loss" at the optimum; judge convergence by the gradient
    grad_norm = float(np.linalg.norm(optimize.approx_fprime(res.x, f, 1e-5)))
    out = {"converged": bool(res.success) or grad_norm < 1e-2, "grad_norm": grad_norm, "loglik": -float(res.fun), "sigma": math.exp(res.x[-1]),
           "n_obs": int(len(y)), "n_groups": len(groups), "coef": {}}
    for i, nm in enumerate(names):
        b, s = float(res.x[i]), float(se[i])
        z = b / s if s > 0 else float("nan")
        out["coef"][nm] = {"est": b, "se": s, "z": z, "p_lower": float(special.ndtr(z)) if s > 0 else float("nan")}
    return out
