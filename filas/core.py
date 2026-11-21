"""
Núcleo de cálculo – Teoria das Filas (P108 – Otimização II, Inatel).

Todas as fórmulas seguem os slides do Prof. Paulo Roberto Maia:
  - "Teoria das filas Modelo MMs.pdf"            -> M/M/1 e M/M/s
  - "Teoria das filas Modelo MMsK e MMsN.pdf"     -> M/M/1/K, M/M/s/K, M/M/1/N, M/M/s/N
  - "Teoria das filas Modelo MG1 e com prioridades.pdf" -> M/G/1 e prioridades

Convenção: λ e μ devem estar na MESMA unidade de tempo (ex.: clientes/hora).
Os tempos (W, Wq) saem nessa mesma unidade.
"""
from __future__ import annotations

import math


class ErroModelo(ValueError):
    """Parâmetros inválidos ou sistema instável."""


def _positivo(**valores):
    for nome, v in valores.items():
        if v is None or v <= 0:
            raise ErroModelo(f"{nome} deve ser maior que zero.")


def _inteiro_positivo(**valores):
    for nome, v in valores.items():
        if v is None or int(v) != v or v < 1:
            raise ErroModelo(f"{nome} deve ser um inteiro maior ou igual a 1.")


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def poisson(x: int, media: float) -> float:
    """P(X = x) = e^(-λ) λ^x / x!   (slide 25 / lista M/M/s ex. 2 j)."""
    return math.exp(-media) * media**x / math.factorial(x)


# ---------------------------------------------------------------------------
# M/M/1  (slides 33–40)
# ---------------------------------------------------------------------------
def mm1(lam: float, mu: float) -> dict:
    _positivo(**{"λ": lam, "μ": mu})
    if lam >= mu:
        raise ErroModelo("Sistema instável: é necessário λ < μ.")
    rho = lam / mu
    return {
        "modelo": "M/M/1",
        "lam": lam, "mu": mu, "s": 1,
        "rho": rho,
        "P0": 1 - rho,
        "L": lam / (mu - lam),
        "Lq": lam**2 / (mu * (mu - lam)),
        "W": 1 / (mu - lam),
        "Wq": lam / (mu * (mu - lam)),
    }


def mm1_pn(lam: float, mu: float, n: int) -> float:
    """P(n) = (1-ρ) ρ^n"""
    rho = lam / mu
    return (1 - rho) * rho**n


def mm1_p_maior(lam: float, mu: float, r: int) -> float:
    """P(n > r) = (λ/μ)^(r+1)"""
    return (lam / mu) ** (r + 1)


def mm1_p_w(lam: float, mu: float, t: float) -> float:
    """P(W > t) = e^(-μ(1-ρ)t)"""
    rho = lam / mu
    return math.exp(-mu * (1 - rho) * t)


def mm1_p_wq(lam: float, mu: float, t: float) -> float:
    """P(Wq > t) = ρ e^(-μ(1-ρ)t)"""
    rho = lam / mu
    return rho * math.exp(-mu * (1 - rho) * t)


# ---------------------------------------------------------------------------
# M/M/s>1  (slides 44–48)
# ---------------------------------------------------------------------------
def _mms_p0(lam: float, mu: float, s: int) -> float:
    r = lam / mu
    soma = sum(r**n / math.factorial(n) for n in range(s))
    return 1 / (soma + r**s / math.factorial(s) * 1 / (1 - lam / (s * mu)))


def mms(lam: float, mu: float, s: int) -> dict:
    _positivo(**{"λ": lam, "μ": mu})
    _inteiro_positivo(s=s)
    s = int(s)
    rho = lam / (s * mu)
    if rho >= 1:
        raise ErroModelo("Sistema instável: é necessário λ < s·μ.")
    r = lam / mu
    p0 = _mms_p0(lam, mu, s)
    lq = p0 * r**s * rho / (math.factorial(s) * (1 - rho) ** 2)
    wq = lq / lam
    return {
        "modelo": f"M/M/{s}",
        "lam": lam, "mu": mu, "s": s,
        "rho": rho,
        "P0": p0,
        "Lq": lq,
        "Wq": wq,
        "L": lq + r,
        "W": wq + 1 / mu,
    }


def mms_pn(lam: float, mu: float, s: int, n: int) -> float:
    r = lam / mu
    p0 = _mms_p0(lam, mu, s)
    if n <= s:
        return r**n / math.factorial(n) * p0
    return r**n / (math.factorial(s) * s ** (n - s)) * p0


def mms_p_w(lam: float, mu: float, s: int, t: float) -> float:
    """P(W > t) = e^(-μt) [1 + P0 (λ/μ)^s / (s!(1-ρ)) · (1 - e^(-μt(s-1-λ/μ))) / (s-1-λ/μ)]"""
    r = lam / mu
    rho = lam / (s * mu)
    p0 = _mms_p0(lam, mu, s)
    a = s - 1 - r
    if abs(a) < 1e-12:
        fracao = mu * t  # limite de (1 - e^(-μt·a))/a quando a -> 0
    else:
        fracao = (1 - math.exp(-mu * t * a)) / a
    return math.exp(-mu * t) * (1 + p0 * r**s / (math.factorial(s) * (1 - rho)) * fracao)


def mms_p_wq(lam: float, mu: float, s: int, t: float) -> float:
    """P(Wq > t) = [1 - P(Wq = 0)] e^(-sμ(1-ρ)t),  P(Wq = 0) = Σ_{n=0}^{s-1} Pn"""
    rho = lam / (s * mu)
    p_wq0 = sum(mms_pn(lam, mu, s, n) for n in range(s))
    return (1 - p_wq0) * math.exp(-s * mu * (1 - rho) * t)


def mms_p_maior(lam: float, mu: float, s: int, r: int) -> float:
    """P(n > r) = 1 - Σ_{n=0}^{r} Pn"""
    return 1 - sum(mms_pn(lam, mu, s, n) for n in range(r + 1))


# ---------------------------------------------------------------------------
# M/M/1/K  (slides 3–6, MMsK)
# ---------------------------------------------------------------------------
def mm1k(lam: float, mu: float, K: int) -> dict:
    _positivo(**{"λ": lam, "μ": mu})
    _inteiro_positivo(K=K)
    K = int(K)
    rho = lam / mu
    if abs(rho - 1) < 1e-12:
        # limite ρ -> 1 (fórmula do slide indeterminada 0/0)
        p0 = 1 / (K + 1)
        pn = [p0] * (K + 1)
        L = K / 2
    else:
        p0 = (1 - rho) / (1 - rho ** (K + 1))
        pn = [p0 * rho**n for n in range(K + 1)]
        L = rho / (1 - rho) - (K + 1) * rho ** (K + 1) / (1 - rho ** (K + 1))
    lq = L - (1 - p0)
    lam_ef = lam * (1 - pn[K])
    return {
        "modelo": f"M/M/1/{K}",
        "lam": lam, "mu": mu, "s": 1, "K": K,
        "rho": rho,
        "P0": p0,
        "L": L,
        "Lq": lq,
        "lam_ef": lam_ef,
        "W": L / lam_ef,
        "Wq": lq / lam_ef,
        "Pn": pn,
        "PK": pn[K],
    }


# ---------------------------------------------------------------------------
# M/M/s>1/K  (slides 9–12, MMsK)
# ---------------------------------------------------------------------------
def mmsk(lam: float, mu: float, s: int, K: int) -> dict:
    _positivo(**{"λ": lam, "μ": mu})
    _inteiro_positivo(s=s, K=K)
    s, K = int(s), int(K)
    if K < s:
        raise ErroModelo("A capacidade K deve ser maior ou igual ao número de servidores s.")
    if s == 1:
        res = mm1k(lam, mu, K)
        return res
    r = lam / mu
    rho = lam / (s * mu)
    soma1 = sum(r**n / math.factorial(n) for n in range(s + 1))
    soma2 = r**s / math.factorial(s) * sum(rho ** (n - s) for n in range(s + 1, K + 1))
    p0 = 1 / (soma1 + soma2)

    def pn_(n):
        if n <= s:
            return r**n / math.factorial(n) * p0
        if n <= K:
            return r**n / (math.factorial(s) * s ** (n - s)) * p0
        return 0.0

    pn = [pn_(n) for n in range(K + 1)]
    if abs(rho - 1) < 1e-12:
        # limite ρ -> 1: Lq = Σ (n-s) Pn
        lq = sum((n - s) * pn[n] for n in range(s, K + 1))
    else:
        lq = (p0 * r**s * rho / (math.factorial(s) * (1 - rho) ** 2)
              * (1 - rho ** (K - s) - (K - s) * rho ** (K - s) * (1 - rho)))
    soma_npn = sum(n * pn[n] for n in range(s))
    soma_pn = sum(pn[n] for n in range(s))
    L = soma_npn + lq + s * (1 - soma_pn)
    lam_ef = lam * (1 - pn[K])
    return {
        "modelo": f"M/M/{s}/{K}",
        "lam": lam, "mu": mu, "s": s, "K": K,
        "rho": rho,
        "P0": p0,
        "L": L,
        "Lq": lq,
        "lam_ef": lam_ef,
        "W": L / lam_ef,
        "Wq": lq / lam_ef,
        "Pn": pn,
        "PK": pn[K],
    }


# ---------------------------------------------------------------------------
# M/M/1/N – população finita  (slides 15–17, MMsK e MMsN)
# ---------------------------------------------------------------------------
def mm1n(lam: float, mu: float, N: int) -> dict:
    _positivo(**{"λ": lam, "μ": mu})
    _inteiro_positivo(N=N)
    N = int(N)
    r = lam / mu
    termos = [math.factorial(N) / math.factorial(N - n) * r**n for n in range(N + 1)]
    p0 = 1 / sum(termos)
    pn = [t * p0 for t in termos]
    L = N - mu / lam * (1 - p0)
    lq = N - (lam + mu) / lam * (1 - p0)
    lam_ef = lam * (N - L)
    return {
        "modelo": f"M/M/1/N={N}",
        "lam": lam, "mu": mu, "s": 1, "N": N,
        "rho": N * lam / mu,
        "P0": p0,
        "L": L,
        "Lq": lq,
        "lam_ef": lam_ef,
        "W": L / lam_ef,
        "Wq": lq / lam_ef,
        "Pn": pn,
    }


# ---------------------------------------------------------------------------
# M/M/s>1/N – população finita  (slides 20–22, MMsK e MMsN)
# ---------------------------------------------------------------------------
def mmsn(lam: float, mu: float, s: int, N: int) -> dict:
    _positivo(**{"λ": lam, "μ": mu})
    _inteiro_positivo(s=s, N=N)
    s, N = int(s), int(N)
    if s == 1:
        return mm1n(lam, mu, N)
    r = lam / mu
    f = math.factorial

    def termo(n):
        if n < s:
            return f(N) / (f(N - n) * f(n)) * r**n
        return f(N) / (f(N - n) * f(s) * s ** (n - s)) * r**n

    termos = [termo(n) for n in range(N + 1)]
    p0 = 1 / sum(termos)
    pn = [t * p0 for t in termos]
    L = sum(n * pn[n] for n in range(1, N + 1))
    lq = L - r * (N - L)
    lam_ef = lam * (N - L)
    return {
        "modelo": f"M/M/{s}/N={N}",
        "lam": lam, "mu": mu, "s": s, "N": N,
        "rho": N * lam / (s * mu),
        "P0": p0,
        "L": L,
        "Lq": lq,
        "lam_ef": lam_ef,
        "W": L / lam_ef,
        "Wq": lq / lam_ef,
        "Pn": pn,
    }


# ---------------------------------------------------------------------------
# M/G/1 – Pollaczek-Khintchine  (slides 3–5, MG1)
# ---------------------------------------------------------------------------
def mg1(lam: float, mu: float, sigma: float) -> dict:
    """sigma = desvio-padrão do tempo de atendimento (σ² = variância)."""
    _positivo(**{"λ": lam, "μ": mu})
    if sigma is None or sigma < 0:
        raise ErroModelo("σ deve ser maior ou igual a zero.")
    rho = lam / mu
    if rho >= 1:
        raise ErroModelo("Sistema instável: é necessário λ < μ.")
    lq = (lam**2 * sigma**2 + rho**2) / (2 * (1 - rho))
    wq = lq / lam
    return {
        "modelo": "M/G/1",
        "lam": lam, "mu": mu, "s": 1, "sigma": sigma,
        "rho": rho,
        "P0": 1 - rho,
        "Lq": lq,
        "L": rho + lq,
        "Wq": wq,
        "W": wq + 1 / mu,
    }


# ---------------------------------------------------------------------------
# Modelos com prioridades  (slides 8–20, MG1 e com prioridades)
# ---------------------------------------------------------------------------
def _checar_classes(lams, mu, s):
    if not lams:
        raise ErroModelo("Informe pelo menos uma classe.")
    for i, l in enumerate(lams, 1):
        if l <= 0:
            raise ErroModelo(f"λ{i} deve ser maior que zero.")
    _positivo(**{"μ": mu})
    _inteiro_positivo(s=s)
    if sum(lams) >= s * mu:
        raise ErroModelo("Sistema instável: é necessário Σλi < s·μ.")


def prioridade_sem_interrupcao(lams: list[float], mu: float, s: int) -> dict:
    """
    Slide 11:
      W_k = 1 / [ A · (1 - Σ_{i<k} λi / sμ) · (1 - Σ_{i≤k} λi / sμ) ] + 1/μ
      A   = s! · (sμ - λ)/r^s · Σ_{j=0}^{s-1} r^j/j!  + sμ ,  r = λ/μ,  λ = Σ λi
      Wq_k = W_k - 1/μ ;  L_k = λ_k W_k ;  Lq_k = L_k - λ_k/μ
    """
    _checar_classes(lams, mu, s)
    s = int(s)
    lam = sum(lams)
    r = lam / mu
    A = (math.factorial(s) * (s * mu - lam) / r**s
         * sum(r**j / math.factorial(j) for j in range(s)) + s * mu)
    classes = []
    acum_ant = 0.0
    for k, lk in enumerate(lams, 1):
        acum = acum_ant + lk
        W = 1 / (A * (1 - acum_ant / (s * mu)) * (1 - acum / (s * mu))) + 1 / mu
        L = lk * W
        classes.append({
            "classe": k, "lam": lk,
            "W": W, "Wq": W - 1 / mu,
            "L": L, "Lq": L - lk / mu,
        })
        acum_ant = acum
    return {
        "modelo": f"Prioridade sem interrupção (s={s})",
        "s": s, "mu": mu, "lam": lam, "A": A,
        "classes": classes,
        "fcfs": mms(lam, mu, s) if s > 1 else mm1(lam, mu),
    }


def _w_mms(lam, mu, s):
    return mm1(lam, mu)["W"] if s == 1 else mms(lam, mu, s)["W"]


def prioridade_com_interrupcao(lams: list[float], mu: float, s: int) -> dict:
    """
    s = 1 (slides 10 e 15):
      W_k = (1/μ) / [ (1 - Σ_{i<k} λi / sμ) · (1 - Σ_{i≤k} λi / sμ) ]
    s > 1 (slides 16–17): W_1 = W do M/M/s com λ1; para k ≥ 2 usa-se que o
      tempo médio das classes 1..k é o W do M/M/s com λ = λ1+…+λk:
      W̄_{1..k} = Σ_{i≤k} (λi/Λk) W_i   ->   W_k = [Λk·W̄_{1..k} - Λ_{k-1}·W̄_{1..k-1}] / λk
    Como nos slides 15–17:
      Wq_k = W_k - 1/μ ;  L_k = (λ1+…+λk)·W_k ;  Lq_k = L_k - (λ1+…+λk)/μ
    """
    _checar_classes(lams, mu, s)
    s = int(s)
    classes = []
    acum_ant = 0.0
    wbar_ant = 0.0
    for k, lk in enumerate(lams, 1):
        acum = acum_ant + lk
        if s == 1:
            W = (1 / mu) / ((1 - acum_ant / (s * mu)) * (1 - acum / (s * mu)))
        else:
            wbar = _w_mms(acum, mu, s)
            W = (acum * wbar - acum_ant * wbar_ant) / lk
            wbar_ant = wbar
        L = acum * W
        classes.append({
            "classe": k, "lam": lk, "lam_acum": acum,
            "W": W, "Wq": W - 1 / mu,
            "L": L, "Lq": L - acum / mu,
        })
        acum_ant = acum
    lam = sum(lams)
    return {
        "modelo": f"Prioridade com interrupção (s={s})",
        "s": s, "mu": mu, "lam": lam,
        "classes": classes,
        "fcfs": mms(lam, mu, s) if s > 1 else mm1(lam, mu),
    }


def prioridade_geral_sem_interrupcao(lams: list[float], mus: list[float],
                                     variancias: list[float]) -> dict:
    """
    Slides 18–19 (1 servidor, tempos de atendimento gerais por classe):
      E(Wq_k) = Σ_{i=1}^{r} λi (V(Si) + E(Si)²) / [ 2 (1 - Σ_{i<k} ρi)(1 - Σ_{i≤k} ρi) ]
      E(W_k) = E(S_k) + E(Wq_k) ;  L_k = λ_k W_k ;  Lq_k = L_k - λ_k/μ_k
    """
    if not (len(lams) == len(mus) == len(variancias)) or not lams:
        raise ErroModelo("Informe λ, μ e variância para todas as classes.")
    for i, (l, m, v) in enumerate(zip(lams, mus, variancias), 1):
        if l <= 0 or m <= 0:
            raise ErroModelo(f"λ{i} e μ{i} devem ser maiores que zero.")
        if v < 0:
            raise ErroModelo(f"V(S{i}) deve ser maior ou igual a zero.")
    rhos = [l / m for l, m in zip(lams, mus)]
    if sum(rhos) >= 1:
        raise ErroModelo("Sistema instável: é necessário Σρi < 1.")
    numerador = sum(l * (v + (1 / m) ** 2) for l, m, v in zip(lams, mus, variancias))
    classes = []
    acum_ant = 0.0
    for k, (lk, mk, rk) in enumerate(zip(lams, mus, rhos), 1):
        acum = acum_ant + rk
        wq = numerador / (2 * (1 - acum_ant) * (1 - acum))
        W = 1 / mk + wq
        L = lk * W
        classes.append({
            "classe": k, "lam": lk, "mu": mk, "rho": rk,
            "W": W, "Wq": wq, "L": L, "Lq": L - lk / mk,
        })
        acum_ant = acum
    return {
        "modelo": "Prioridade sem interrupção – tempos gerais (M/G/1)",
        "s": 1, "lam": sum(lams), "rho": sum(rhos),
        "classes": classes,
    }
