"""
Validação do núcleo de cálculo com os gabaritos das listas de exercícios
e dos exemplos dos slides. Rodar:  python -m unittest -v
"""
import math
import unittest

from filas import core


class Base(unittest.TestCase):
    def ok(self, valor, esperado, tol=None, rel=0.01):
        """Compara com tolerância relativa (padrão 1%, os gabaritos são arredondados)."""
        if tol is None:
            tol = max(abs(esperado) * rel, 5e-4)
        self.assertAlmostEqual(valor, esperado, delta=tol)


# ---------------------------------------------------------------------------
class TestMM1(Base):
    def test_slide_ex2_barbearia(self):
        r = core.mm1(3, 4)
        self.ok(r["P0"], 0.25)
        self.ok(r["L"], 3)
        self.ok(r["Lq"], 2.25)
        self.ok(r["W"], 1)
        self.ok(r["Wq"], 0.75)

    def test_lista_mms_ex1(self):
        # média da tabela ≈ 12 equip./mês ; ociosidade 0,25 -> μ = 16
        lam = sum(x * f for x, f in [(9, .067), (10, .1), (11, .2), (12, .267),
                                     (13, .2), (14, .1), (15, .067)])
        self.ok(lam, 12, rel=0.002)
        lam, mu = 12, 16
        r = core.mm1(lam, mu)
        self.ok(r["W"], 0.25)
        self.ok(r["P0"], 0.25)
        self.ok(1 - core.mm1_p_maior(lam, mu, 4), 0.7627)  # c)
        self.ok(r["Lq"], 2.25)
        self.ok(r["Wq"], 0.1875)
        self.ok(r["L"], 3)
        self.ok(core.mm1_p_w(lam, mu, 20 / 30), 0.069)     # g) 20 dias
        self.ok(core.mm1_p_wq(lam, mu, 15 / 30), 0.1015)   # h) 15 dias

    def test_lista_mms_ex2(self):
        lam, mu = 12.8, 16  # ρ = 0,8 e Wq = 15 min
        r = core.mm1(lam, mu)
        self.ok(r["Wq"], 0.25)
        self.ok(r["Lq"], 3.2)
        self.ok(r["L"], 4)
        self.ok(r["P0"], 0.2)
        self.ok(core.mm1_p_w(lam, mu, 0.5), 0.2019)
        self.ok(core.mm1_p_wq(lam, mu, 0.25), 0.3595)
        self.ok(core.poisson(10, lam), 0.0898)
        self.ok(core.poisson(12, mu), 0.066)
        self.ok(core.mm1_pn(lam, mu, 10), 0.0215)

    def test_lista_mms_ex3(self):
        # Lq = 3,2 -> ρ = 0,8 ; P(n < 6) = 1 - P(n > 5)
        self.ok(1 - core.mm1_p_maior(0.8, 1, 5), 0.7378)

    def test_lista_mms_ex5(self):
        r = core.mm1(3, 4)
        self.ok(r["Lq"], 2.25)
        self.ok(r["L"], 3)
        self.ok(r["Wq"], 0.75)
        self.ok(r["W"], 1)
        self.ok(core.mm1_pn(3, 4, 6), 0.0445)
        self.ok(r["rho"], 0.75)
        self.ok(core.mm1_p_w(3, 4, 2), 0.1353)
        self.ok(core.mm1_p_wq(3, 4, 1.5), 0.1673)

    def test_lista_mms_ex6(self):
        r = core.mm1(4, 5)
        self.ok(r["Wq"], 0.8)
        self.ok(r["Lq"], 3.2)
        self.ok(r["L"], 4)
        self.ok(r["W"], 1)
        self.ok(core.mm1_p_w(4, 5, 1), 0.3679)
        self.ok(core.mm1_p_wq(4, 5, 0.8), 0.3595)

    def test_lista_mms_ex13(self):
        r = core.mm1(20 / 60, 1 / 2)  # por minuto
        self.ok(r["L"], 2)
        self.ok(r["W"], 6)
        self.ok(r["Wq"], 4)
        self.ok(r["Lq"], 1.333)
        self.ok(core.mm1_p_wq(20 / 60, 1 / 2, 5), 0.2897)
        self.ok(core.mm1_p_w(20 / 60, 1 / 2, 7), 0.3114)
        r = core.mm1(20 / 60, 1 / 1.5)
        self.ok(core.mm1_p_wq(20 / 60, 1 / 1.5, 5), 0.0944)
        self.ok(core.mm1_p_w(20 / 60, 1 / 1.5, 7), 0.0970)

    def test_instavel(self):
        with self.assertRaises(core.ErroModelo):
            core.mm1(5, 5)


# ---------------------------------------------------------------------------
class TestMMs(Base):
    def test_slide_ex2_banco(self):
        lam, mu, s = 0.6, 0.5, 3
        r = core.mms(lam, mu, s)
        self.ok(r["rho"], 0.4)
        self.ok(r["L"], 1.29)
        self.ok(r["Lq"], 0.094, rel=0.02)
        self.ok(r["P0"], 0.294)
        self.ok(core.mms_p_maior(lam, mu, s, 5), 0.0091, rel=0.03)
        self.ok(r["Wq"], 0.157, rel=0.02)
        self.ok(r["W"], 2.16)
        self.ok(core.mms_p_w(lam, mu, s, 3), 0.2506)
        self.ok(core.mms_p_wq(lam, mu, s, 2), 0.0233)

    def test_lista_mms_ex7_hospital(self):
        r1 = core.mm1(2, 3)
        r2 = core.mms(2, 3, 2)
        self.ok(r2["rho"], 1 / 3)
        self.ok(r1["L"], 2)
        self.ok(r2["L"], 0.75)
        self.ok(r2["Lq"], 1 / 12)
        self.ok(r2["P0"], 0.5)
        self.ok(core.mm1_p_maior(2, 3, 2), 0.2962)
        self.ok(core.mms_p_maior(2, 3, 2, 2), 0.0556)
        self.ok(r2["Wq"], 1 / 24)
        self.ok(r2["W"], 3 / 8)
        self.ok(core.mm1_p_wq(2, 3, 0.5), 0.404)
        self.ok(core.mms_p_wq(2, 3, 2, 0.5), 0.023, rel=0.03)
        self.ok(core.mm1_p_w(2, 3, 1), 0.3679)
        self.ok(core.mms_p_w(2, 3, 2, 1), 0.0655)

    def test_lista_mms_ex8_banco(self):
        # O enunciado DÁ Wq = 1 min (medido); o resto sai pelas relações de Little
        lam, mu, wq = 40 / 60, 1 / 2, 1  # por minuto
        W = wq + 1 / mu
        self.ok(lam * W, 2)
        self.ok(lam * wq, 0.667)
        self.ok(W, 3)

    def test_lista_mms_ex9_sac(self):
        self.assertGreater(core.mm1(5, 7)["Wq"] * 60, 5)
        self.assertLessEqual(core.mms(5, 7, 2)["Wq"] * 60, 2)  # resposta: 2 atendentes

    def test_lista_mms_ex14_aeroporto(self):
        self.ok(core.mm1(10, 20)["Lq"], 0.5)
        self.ok(core.mm1(15, 20)["Lq"], 2.25)
        self.ok(1 - core.mm1_p_wq(10, 20, 0.5), 0.9966, rel=0.001)
        self.ok(1 - core.mm1_p_wq(15, 20, 0.5), 0.9384, rel=0.001)
        r = core.mms(25, 20, 2)
        self.ok(r["Lq"], 0.8013)
        self.ok(1 - core.mms_p_wq(25, 20, 2, 0.5), 0.9997, rel=0.001)
        # critério 2: nº na fila ≤ 4  <=> n ≤ 4 + s
        self.ok(1 - core.mm1_p_maior(10, 20, 5), 0.984, rel=0.002)
        self.ok(1 - core.mm1_p_maior(15, 20, 5), 0.822, rel=0.002)
        # gabarito 92,7% = P(n ≤ 5); com 2 pistas "≤ 4 na fila" seria P(n ≤ 6) = 95,4%
        self.ok(1 - core.mms_p_maior(25, 20, 2, 5), 0.927, rel=0.002)

    def test_lista_mms_ex15_banco(self):
        a = core.mms(2, 1, 4)
        self.ok(a["Lq"], 0.1739)
        self.ok(1 - core.mms_p_maior(2, 1, 4, 9), 0.997, rel=0.002)
        self.ok(1 - core.mms_p_wq(2, 1, 4, 5), 0.9999, rel=0.001)
        b = core.mms(3, 1, 4)
        self.ok(b["Lq"], 1.5283)
        self.ok(1 - core.mms_p_maior(3, 1, 4, 9), 0.909, rel=0.002)
        self.ok(1 - core.mms_p_wq(3, 1, 4, 5), 0.9966, rel=0.001)
        c = core.mms(3, 1, 5)
        self.assertLessEqual(c["Lq"], 1)


# ---------------------------------------------------------------------------
class TestMM1K(Base):
    def test_slide_ex2(self):
        r = core.mm1k(3, 4, 5)
        self.ok(r["P0"], 0.3041)
        self.ok(r["L"], 1.7009)
        self.ok(r["Lq"], 1.005)
        self.ok(r["Pn"][4], 0.09623)
        self.ok(r["W"], 0.6111)
        self.ok(r["Wq"], 0.3611)

    def test_lista_mmsk_ex1(self):
        r = core.mm1k(2, 4, 5)
        self.ok(r["P0"], 0.5079)
        self.ok(r["L"], 0.9048)
        self.ok(r["Lq"], 0.4127)
        self.ok(r["Pn"][4], 0.03175)
        self.ok(r["W"], 0.4597)
        self.ok(r["Wq"], 0.2097)

    def test_lista_mmsk_ex2(self):
        r = core.mm1k(1, 60 / 45, 4)
        self.ok(r["L"], 1.4443)
        self.ok(r["PK"], 0.1037)
        self.ok(r["Wq"], 0.8614)

    def test_lista_mmsk_ex3(self):
        r = core.mm1k(1 / 4, 1 / 3, 4)  # 1 pousando + 3 em espera
        self.ok(r["Lq"], 0.7721)
        self.ok(r["Wq"], 3.4457)
        self.ok(r["Pn"][4], 0.1037)

    def test_lista_mmsk_ex6(self):
        r = core.mm1k(3, 4, 4)
        self.ok(r["Lq"], 0.7721)
        self.ok(r["L"], 1.4443)
        self.ok(r["W"], 0.5371)
        self.ok(r["Wq"], 0.2871)
        # e) gabarito 0,0288 corresponde a K = 4 (ver README – divergências)
        self.ok(core.mmsk(3, 4, 2, 4)["Wq"], 0.0288)

    def test_rho_igual_1(self):
        r = core.mm1k(2, 2, 4)
        self.ok(r["P0"], 0.2)
        self.ok(r["L"], 2)


# ---------------------------------------------------------------------------
class TestMMsK(Base):
    def test_slide_ex2_inspecao(self):
        r = core.mmsk(1, 1 / 6, 3, 7)
        self.ok(r["P0"], 0.00088, rel=0.02)
        self.ok(r["L"], 6.0631)
        self.ok(r["Lq"], 3.0920)
        self.ok(r["W"], 12.2442)
        self.ok(r["Wq"], 6.2439)
        self.ok(1 * r["PK"] * 60, 30.29)  # carros/hora perdidos

    # Ex. 4 e 5: os gabaritos batem com K = 4 (o enunciado sugere K = 5).
    def test_lista_mmsk_ex4(self):
        r = core.mmsk(1 / 4, 1 / 3, 2, 4)
        self.ok(r["Lq"], 0.0848)
        self.ok(r["Wq"], 0.3455)
        self.ok(r["PK"], 0.0182)

    def test_lista_mmsk_ex5(self):
        r = core.mmsk(1, 60 / 45, 2, 4)
        self.ok(r["L"], 0.8212)
        self.ok(r["PK"], 0.0182)
        self.ok(r["Wq"], 0.0864)

    def test_bate_com_soma_direta(self):
        r = core.mmsk(1, 1 / 6, 3, 7)
        self.ok(sum(r["Pn"]), 1, tol=1e-9)
        self.ok(r["Lq"], sum((n - 3) * p for n, p in enumerate(r["Pn"]) if n > 3), tol=1e-9)
        self.ok(r["L"], sum(n * p for n, p in enumerate(r["Pn"])), tol=1e-9)


# ---------------------------------------------------------------------------
class TestMM1N(Base):
    def test_slide_ex2_robos(self):
        r = core.mm1n(1 / 30, 1 / 3, 5)
        self.ok(5 - r["L"], 4.360)
        self.ok(r["W"], 4.4)
        self.ok(r["P0"], 0.5640)

    def test_lista_mmsn_ex1(self):
        r = core.mm1n(1 / 200, 1 / 10, 10)
        self.ok(r["P0"], 0.5380)
        self.ok(r["Lq"], 0.2972)
        self.ok(r["L"], 0.7593)
        self.ok(r["Wq"], 6.4330)
        self.ok(r["W"], 16.4330)
        # custo diário: máquinas paradas (L·30) + técnico ocupado ((1-P0)·10), 8 h
        self.ok((r["L"] * 30 + (1 - r["P0"]) * 10) * 8, 219.192)

    def test_lista_mmsn_ex3(self):
        r = core.mm1n(1 / 10, 1 / 8, 2)
        self.ok(r["P0"], 0.2577)
        self.ok(r["L"], 1.072)
        self.ok(r["Lq"], 0.330)
        self.ok(r["W"], 11.556)
        self.ok(r["Wq"], 3.556)
        self.ok(1 - r["P0"], 0.7423)
        self.ok((2 - r["L"]) / 2, 0.464)

    def test_lista_mmsn_ex4(self):
        r = core.mm1n(1 / 9, 1 / 2, 3)
        self.ok(r["L"], 0.7181)
        self.ok(r["W"], 2.832)
        # c) gabarito 0,667 = ρ = Nλ/μ do slide (1 - P0 daria 0,507)
        self.ok(r["rho"], 0.667)
        self.ok(core.mmsn(1 / 9, 1 / 2, 2, 3)["L"], 0.5528)

    def test_lista_mmsn_ex5(self):
        r = core.mm1n(1 / 10, 1 / 2, 4)
        self.ok(4 - r["L"], 3.0082)
        # b) e c) (custos 478,672 e 270,336): não foi possível reproduzir (ver README)


# ---------------------------------------------------------------------------
class TestMMsN(Base):
    def test_slide_ex2_robos(self):
        r = core.mmsn(1 / 30, 1 / 3, 2, 5)
        self.ok(5 - r["L"], 4.535)
        self.ok(r["W"], 3.075)

    def test_lista_mmsn_ex6(self):
        r = core.mmsn(1 / 100, 1 / 10, 2, 4)
        self.ok(r["P0"], 0.6820)
        self.ok(r["L"], 0.3677)
        self.ok(r["Lq"], 0.0045, rel=0.03)
        self.ok(r["W"], 10.1239)
        self.ok(r["Wq"], 0.1239, rel=0.02)
        self.ok(1 - r["P0"], 0.3180)
        # d) gabarito 0,8184 não reproduzido: (N - L)/N = 0,908 (mesma conta do ex. 3d)

    def test_soma_pn(self):
        r = core.mmsn(1 / 30, 1 / 3, 2, 5)
        self.ok(sum(r["Pn"]), 1, tol=1e-9)
        self.ok(r["Lq"], sum((n - 2) * p for n, p in enumerate(r["Pn"]) if n > 2), tol=1e-9)


# ---------------------------------------------------------------------------
class TestMG1(Base):
    def test_lista_mg1_ex1(self):
        esperado = {4: (3.2, 4.0, 16.0, 20.0), 3: (2.5, 3.3, 12.5, 16.5),
                    2: (2.0, 2.8, 10.0, 14.0), 1: (1.7, 2.5, 8.5, 12.5),
                    0: (1.6, 2.4, 8.0, 12.0)}
        for sigma, (lq, L, wq, W) in esperado.items():
            r = core.mg1(0.2, 0.25, sigma)
            self.ok(r["Lq"], lq)
            self.ok(r["L"], L)
            self.ok(r["Wq"], wq)
            self.ok(r["W"], W)
        self.ok(core.mg1(0.2, 0.25, 0)["Lq"] / core.mg1(0.2, 0.25, 4)["Lq"], 0.5)
        # d) μ aumentado de 0,05 com σ = 4 chega perto de Lq = 1,6
        self.ok(core.mg1(0.2, 0.30, 4)["Lq"], 1.6, rel=0.02)

    def test_slide_ex2_marsha(self):
        lam, mu = 25, 3600 / 90  # por hora
        a = core.mg1(lam, mu, 1 / mu)  # exponencial: σ = 1/μ
        self.ok(a["Lq"], 1.042)
        self.ok(a["L"], 1.667)
        self.ok(a["Wq"], 0.042)
        self.ok(a["W"], 0.067)
        b = core.mg1(lam, mu, 0)
        self.ok(b["Lq"], 0.521)
        self.ok(b["L"], 1.146)
        self.ok(b["Lq"] / a["Lq"], 0.5)

    def test_mg1_exponencial_igual_mm1(self):
        self.ok(core.mg1(2, 3, 1 / 3)["L"], core.mm1(2, 3)["L"], tol=1e-12)

    def test_lista_mmc_ex2_caminhoes(self):
        # lista M/G/1 ex. 2: tempo constante de 15 min (σ = 0)
        r = core.mg1(3, 4, 0)
        self.ok(r["Lq"], 1.125)
        self.ok(r["L"], 1.875)
        self.ok(r["Wq"], 0.375)
        self.ok(r["W"], 0.625)
        self.ok(r["rho"], 0.75)


# ---------------------------------------------------------------------------
class TestPrioridades(Base):
    def test_slide_ex1_sem_interrupcao_s1(self):
        r = core.prioridade_sem_interrupcao([0.2, 0.6, 1.2], 3, 1)["classes"]
        self.ok(r[0]["W"], 0.5714)
        self.ok(r[0]["Wq"], 0.23809)
        self.ok(r[0]["L"], 0.11428)
        self.ok(r[0]["Lq"], 0.047619)
        self.ok(r[1]["W"], 0.65800)
        self.ok(r[1]["Lq"], 0.19480)
        self.ok(r[2]["W"], 1.24242)
        self.ok(r[2]["L"], 1.4909)

    def test_slide_ex1_sem_interrupcao_s2(self):
        r = core.prioridade_sem_interrupcao([0.2, 0.6, 1.2], 3, 2)["classes"]
        self.ok(r[0]["W"], 0.36207)
        self.ok(r[0]["Lq"], 0.00574)
        self.ok(r[1]["W"], 0.36649)
        self.ok(r[1]["Wq"], 0.03316)
        self.ok(r[2]["W"], 0.38141)
        self.ok(r[2]["Lq"], 0.05769)

    def test_slide_ex1_com_interrupcao_s1(self):
        r = core.prioridade_com_interrupcao([0.2, 0.6, 1.2], 3, 1)["classes"]
        self.ok(r[0]["W"], 0.3571)
        self.ok(r[0]["Lq"], 0.004753)
        self.ok(r[1]["W"], 0.4870)
        self.ok(r[1]["L"], 0.3896)
        self.ok(r[1]["Lq"], 0.1229)
        self.ok(r[2]["W"], 1.3636)
        self.ok(r[2]["L"], 2.7272)
        self.ok(r[2]["Lq"], 2.0605)

    def test_slide_ex1_com_interrupcao_s2(self):
        r = core.prioridade_com_interrupcao([0.2, 0.6, 1.2], 3, 2)["classes"]
        self.ok(r[0]["W"], 0.33370)
        self.ok(r[0]["Wq"], 0.000367, rel=0.03)
        self.ok(r[1]["W"], 0.34126)
        self.ok(r[1]["Wq"], 0.00793, rel=0.02)
        self.ok(r[1]["L"], 0.27300)
        self.ok(r[2]["W"], 0.39875)
        self.ok(r[2]["L"], 0.79751)
        self.ok(r[2]["Lq"], 0.13084)

    def test_slide_ex2_spt(self):
        r = core.prioridade_geral_sem_interrupcao([10, 5], [20, 15], [1 / 1800, 1 / 1800])
        c = r["classes"]
        self.ok(c[0]["Wq"], 0.0556)
        self.ok(c[1]["Wq"], 0.3333)
        self.ok(c[0]["W"], 0.1056)  # slide arredonda para 0,11
        self.ok(c[1]["W"], 0.40, rel=0.01)

    def test_slide_ex3_delegacia(self):
        c = core.prioridade_sem_interrupcao([10, 20], 7.5, 5)["classes"]
        self.ok(c[0]["Wq"], 0.0201)
        self.ok(c[1]["Wq"], 0.1007)

    def test_lista_prio_ex4_airlines(self):
        r = core.prioridade_sem_interrupcao([2, 10], 20, 1)
        c = r["classes"]
        self.ok(c[0]["Lq"], 0.067, rel=0.02)
        self.ok(c[0]["L"], 0.167)
        self.ok(c[0]["Wq"], 0.033, rel=0.02)
        self.ok(c[0]["W"], 0.083, rel=0.02)
        self.ok(c[1]["L"], 1.333)
        self.ok(c[1]["Wq"], 0.083, rel=0.02)
        self.ok(c[1]["W"], 0.133)
        self.ok(c[0]["Wq"] / c[1]["Wq"], 0.4)
        self.ok(r["fcfs"]["rho"] * 12, 7.2)

    def test_lista_prio_ex5(self):
        a = core.prioridade_sem_interrupcao([2, 3], 6, 1)["classes"]
        self.ok(a[0]["Wq"], 0.208)
        self.ok(a[0]["W"], 0.375)
        self.ok(a[1]["Lq"], 3.75)
        self.ok(a[1]["L"], 4.25)
        self.ok(a[1]["Wq"], 1.25)
        self.ok(a[1]["W"], 1.417)
        b = core.prioridade_sem_interrupcao([2, 3], 3, 2)["classes"]
        self.ok(b[0]["Lq"], 0.379)
        self.ok(b[0]["L"], 1.045)
        self.ok(b[0]["Wq"], 0.189)
        self.ok(b[0]["W"], 0.523)
        self.ok(b[1]["Lq"], 3.409)
        self.ok(b[1]["L"], 4.409)
        self.ok(b[1]["Wq"], 1.136)
        self.ok(b[1]["W"], 1.47)

    def test_lista_prio_ex6(self):
        self.ok(core.mm1(8, 10)["W"], 0.5)
        b = core.prioridade_sem_interrupcao([2, 4, 2], 10, 1)["classes"]
        self.ok(b[0]["W"], 0.2)
        self.ok(b[1]["W"], 0.35)
        self.ok(b[2]["W"], 1.1)
        c = core.prioridade_com_interrupcao([2, 4, 2], 10, 1)["classes"]
        self.ok(c[0]["W"], 0.125)
        self.ok(c[1]["W"], 0.3125)
        self.ok(c[2]["W"], 1.25)

    def test_lista_prio_ex7(self):
        lams = [0.1, 0.4, 1.5]
        esperado = {
            ("com", 1): (0.011, 0.080, 0.867),
            ("com", 2): (0.00009, 0.00289, 0.05493),
            ("sem", 1): (0.230, 0.276, 0.800),
            ("sem", 2): (0.028, 0.031, 0.045),
        }
        for (tipo, s), wqs in esperado.items():
            f = core.prioridade_com_interrupcao if tipo == "com" else core.prioridade_sem_interrupcao
            c = f(lams, 3, s)["classes"]
            for k in range(3):
                with self.subTest(tipo=tipo, s=s, classe=k + 1):
                    self.ok(c[k]["Wq"], wqs[k], rel=0.03)


if __name__ == "__main__":
    unittest.main()
