"""
Interface – Teoria das Filas (P108 – Otimização II, Inatel)
Executar:  streamlit run app.py
"""
import math

import pandas as pd
import streamlit as st

from filas import core

st.set_page_config(page_title="Teoria das Filas – P108", page_icon="📐", layout="wide")

MODELOS = [
    "M/M/1",
    "M/M/s (s>1)",
    "M/M/1/K",
    "M/M/s/K",
    "M/M/1/N (população finita)",
    "M/M/s/N (população finita)",
    "M/G/1",
    "Prioridades",
]

# horas equivalentes a cada unidade de tempo (para conversões)
UNIDADES = {"segundo": 1 / 3600, "minuto": 1 / 60, "hora": 1.0, "dia": 24.0, "mês (30 dias)": 720.0}


def taxa_para(valor, unidade_origem, unidade_destino):
    """Converte uma taxa (por unidade_origem) para por unidade_destino."""
    return valor * UNIDADES[unidade_destino] / UNIDADES[unidade_origem]


def tempo_para(valor, unidade_origem, unidade_destino):
    return valor * UNIDADES[unidade_origem] / UNIDADES[unidade_destino]


def fmt(x, casas=4):
    if x is None:
        return "—"
    if isinstance(x, float) and (math.isinf(x) or math.isnan(x)):
        return str(x)
    if x != 0 and abs(x) < 10 ** (-casas):
        return f"{x:.2e}".replace(".", ",")
    return f"{x:.{casas}f}".replace(".", ",")


# ---------------------------------------------------------------------------
# Barra lateral
# ---------------------------------------------------------------------------
st.sidebar.title("⚙️ Configuração")
modelo = st.sidebar.selectbox("Modelo de filas", MODELOS)
casas = st.sidebar.slider("Casas decimais", 2, 8, 4)
un = st.sidebar.selectbox(
    "Unidade de tempo dos resultados", list(UNIDADES), index=2,
    help="λ e μ são convertidos para esta unidade; W e Wq saem nela.",
)


def entrada_taxa(nome, simbolo, padrao, chave, tempo_nome):
    """Lê uma taxa (λ ou μ) como taxa ou como tempo médio, já convertida para `un`."""
    st.sidebar.markdown(f"**{nome}**")
    modo = st.sidebar.radio(
        f"Informar {simbolo} como", [f"taxa {simbolo}", tempo_nome],
        key=f"modo_{chave}", horizontal=True, label_visibility="collapsed",
    )
    c1, c2 = st.sidebar.columns([3, 2])
    unidade = c2.selectbox("unidade", list(UNIDADES), index=2, key=f"un_{chave}")
    if modo.startswith("taxa"):
        v = c1.number_input(f"{simbolo} (por {unidade})", min_value=0.0, value=padrao,
                            format="%.6f", key=f"v_{chave}")
        return taxa_para(v, unidade, un)
    v = c1.number_input(f"{tempo_nome} ({unidade})", min_value=0.0, value=1 / padrao,
                        format="%.6f", key=f"t_{chave}")
    if v == 0:
        return 0.0
    return 1 / tempo_para(v, unidade, un)


def inteiro(nome, padrao, minimo=1, ajuda=None):
    return int(st.sidebar.number_input(nome, min_value=minimo, value=padrao, step=1, help=ajuda))


params = {}
if modelo != "Prioridades":
    params["lam"] = entrada_taxa("Chegadas", "λ", 3.0, "lam", "tempo médio entre chegadas")
    params["mu"] = entrada_taxa("Atendimento", "μ", 4.0, "mu", "tempo médio de atendimento")
    if modelo in ("M/M/s (s>1)", "M/M/s/K", "M/M/s/N (população finita)"):
        params["s"] = inteiro("s – número de servidores", 2)
    if modelo in ("M/M/1/K", "M/M/s/K"):
        params["K"] = inteiro("K – capacidade máxima do sistema (fila + atendimento)", 5)
    if modelo.startswith("M/M/1/N") or modelo.startswith("M/M/s/N"):
        params["N"] = inteiro("N – tamanho da população", 5)
        st.sidebar.caption("Em população finita, λ é a taxa de chegada **de cada cliente** "
                           "(ex.: 1/tempo médio entre quebras de uma máquina).")
    if modelo == "M/G/1":
        st.sidebar.markdown("**Variabilidade do atendimento**")
        tipo_sigma = st.sidebar.radio("Informar", ["desvio-padrão σ", "variância σ²"], horizontal=True)
        c1, c2 = st.sidebar.columns([3, 2])
        un_sigma = c2.selectbox("unidade", list(UNIDADES), index=2, key="un_sigma")
        v = c1.number_input(tipo_sigma, min_value=0.0, value=0.25, format="%.6f")
        sigma = math.sqrt(v) if tipo_sigma.startswith("vari") else v
        params["sigma"] = tempo_para(sigma, un_sigma, un)

# ---------------------------------------------------------------------------
# Cabeçalho
# ---------------------------------------------------------------------------
st.title("📐 Teoria das Filas")
st.caption("P108 – Otimização II · Inatel · fórmulas conforme os slides do Prof. Paulo Roberto Maia")

aba_calc, aba_form = st.tabs(["🧮 Calculadora", "📖 Fórmulas"])


# ---------------------------------------------------------------------------
# Componentes de exibição
# ---------------------------------------------------------------------------
def cartoes(res, extras=()):
    itens = [("ρ (taxa de ocupação)", res.get("rho")), ("P0", res.get("P0")),
             ("L", res["L"]), ("Lq", res["Lq"]),
             (f"W ({un})", res["W"]), (f"Wq ({un})", res["Wq"])]
    itens += list(extras)
    cols = st.columns(len(itens))
    for c, (nome, v) in zip(cols, itens):
        c.metric(nome, fmt(v, casas))


def tabela_pn(pn, rotulo="n"):
    df = pd.DataFrame({rotulo: range(len(pn)), "Pn": pn})
    df["P(N ≤ n)"] = df["Pn"].cumsum()
    df["P(N > n)"] = 1 - df["P(N ≤ n)"]
    c1, c2 = st.columns([2, 3])
    c1.dataframe(df.style.format({"Pn": lambda x: fmt(x, casas), "P(N ≤ n)": lambda x: fmt(x, casas),
                                  "P(N > n)": lambda x: fmt(x, casas)}),
                 hide_index=True, width="stretch")
    c2.bar_chart(df.set_index(rotulo)["Pn"])


def mostrar_erro(e):
    st.error(f"⚠️ {e}")


def ferramentas_infinitas(lam, mu, s):
    """Probabilidades extras para M/M/1 e M/M/s (slides 35–37 e 46–47)."""
    st.subheader("Probabilidades")
    c1, c2, c3 = st.columns(3)
    n = c1.number_input("n (clientes no sistema)", min_value=0, value=2, step=1)
    t_w = c2.number_input(f"t para P(W > t) ({un})", min_value=0.0, value=1.0, format="%.6f")
    t_wq = c3.number_input(f"t para P(Wq > t) ({un})", min_value=0.0, value=1.0, format="%.6f")
    if s == 1:
        pn = core.mm1_pn(lam, mu, n)
        p_maior = core.mm1_p_maior(lam, mu, n)
        p_w = core.mm1_p_w(lam, mu, t_w)
        p_wq = core.mm1_p_wq(lam, mu, t_wq)
    else:
        pn = core.mms_pn(lam, mu, s, n)
        p_maior = core.mms_p_maior(lam, mu, s, n)
        p_w = core.mms_p_w(lam, mu, s, t_w)
        p_wq = core.mms_p_wq(lam, mu, s, t_wq)
    cols = st.columns(5)
    cols[0].metric(f"P(n = {n})", fmt(pn, casas))
    cols[1].metric(f"P(n > {n})", fmt(p_maior, casas))
    cols[2].metric(f"P(n ≤ {n})", fmt(1 - p_maior, casas))
    cols[3].metric(f"P(W > {fmt(t_w, 3)})", fmt(p_w, casas))
    cols[4].metric(f"P(Wq > {fmt(t_wq, 3)})", fmt(p_wq, casas))

    with st.expander("Distribuição de Poisson – P(X = x) = e^(−λ) λ^x / x!"):
        st.caption("Ex.: probabilidade de ocorrerem x chegadas (média λ) ou x atendimentos "
                   f"(média μ) em uma unidade de tempo ({un}).")
        c1, c2 = st.columns(2)
        x = c1.number_input("x", min_value=0, value=10, step=1)
        c2.metric(f"P(x chegadas)  λ={fmt(lam, 3)}", fmt(core.poisson(x, lam), casas))
        c2.metric(f"P(x atendimentos)  μ={fmt(mu, 3)}", fmt(core.poisson(x, mu), casas))

    nmax = st.slider("Tabela Pn até n =", 5, 60, 15)
    pns = [core.mm1_pn(lam, mu, i) if s == 1 else core.mms_pn(lam, mu, s, i) for i in range(nmax + 1)]
    tabela_pn(pns)


def verificacao(res):
    lam_ef = res.get("lam_ef", res["lam"])
    with st.expander("✅ Conferência (Lei de Little)"):
        st.write(f"λ efetiva = {fmt(lam_ef, casas)}")
        st.write(f"L = λ·W → {fmt(lam_ef * res['W'], casas)}  (calculado: {fmt(res['L'], casas)})")
        st.write(f"Lq = λ·Wq → {fmt(lam_ef * res['Wq'], casas)}  (calculado: {fmt(res['Lq'], casas)})")
        if "Pn" in res:
            st.write(f"Σ Pn = {fmt(sum(res['Pn']), casas)}")


# ---------------------------------------------------------------------------
# Calculadora
# ---------------------------------------------------------------------------
with aba_calc:
    st.header(modelo)
    if modelo != "Prioridades":
        info = f"λ = {fmt(params['lam'], casas)} e μ = {fmt(params['mu'], casas)} por {un}"
        for k in ("s", "K", "N"):
            if k in params:
                info += f" · {k} = {params[k]}"
        if "sigma" in params:
            info += f" · σ = {fmt(params['sigma'], casas)} {un} (σ² = {fmt(params['sigma'] ** 2, casas)})"
        st.caption(info)

    try:
        if modelo == "M/M/1":
            res = core.mm1(params["lam"], params["mu"])
            cartoes(res)
            ferramentas_infinitas(params["lam"], params["mu"], 1)
            verificacao(res)

        elif modelo == "M/M/s (s>1)":
            res = core.mms(params["lam"], params["mu"], params["s"])
            cartoes(res)
            ferramentas_infinitas(params["lam"], params["mu"], params["s"])
            verificacao(res)

        elif modelo in ("M/M/1/K", "M/M/s/K"):
            s = 1 if modelo == "M/M/1/K" else params["s"]
            res = core.mmsk(params["lam"], params["mu"], s, params["K"])
            cartoes(res, [("λ efetiva", res["lam_ef"]), (f"P{params['K']} (sistema cheio)", res["PK"])])
            st.info(f"Clientes perdidos (bloqueados) por {un}: λ·P_K = "
                    f"{fmt(params['lam'] * res['PK'], casas)}")
            tabela_pn(res["Pn"])
            verificacao(res)

        elif modelo.startswith("M/M/1/N") or modelo.startswith("M/M/s/N"):
            s = 1 if modelo.startswith("M/M/1/N") else params["s"]
            res = core.mmsn(params["lam"], params["mu"], s, params["N"])
            N = params["N"]
            cartoes(res, [("λ efetiva", res["lam_ef"])])
            c = st.columns(4)
            c[0].metric("Clientes em operação (N − L)", fmt(N - res["L"], casas))
            c[1].metric("Fração de cada cliente em operação", fmt((N - res["L"]) / N, casas))
            c[2].metric("Servidores ocupados (média)", fmt(res["L"] - res["Lq"], casas))
            c[3].metric("Ocupação de cada servidor", fmt((res["L"] - res["Lq"]) / s, casas))
            st.caption("ρ é mostrado como no slide: ρ = Nλ/(sμ). Para s = 1, a fração de tempo "
                       "em que o servidor está ocupado é 1 − P0.")
            with st.expander("💲 Custo (opcional)"):
                c1, c2, c3 = st.columns(3)
                cm = c1.number_input(f"Custo por cliente parado por {un}", min_value=0.0, value=0.0)
                cs = c2.number_input(f"Custo do servidor por {un}", min_value=0.0, value=0.0)
                modo = c3.radio("Servidor cobrado", ["só quando ocupado", "o tempo todo"])
                horas = st.number_input(f"Quantidade de {un}s no período (ex.: 8 h/dia)",
                                        min_value=0.0, value=1.0)
                ocupados = res["L"] - res["Lq"] if modo == "só quando ocupado" else s
                total = (res["L"] * cm + ocupados * cs) * horas
                st.metric("Custo total no período", fmt(total, 2))
                st.caption("Custo = (L·custo por cliente parado + servidores·custo do servidor) × período.")
            tabela_pn(res["Pn"])
            verificacao(res)

        elif modelo == "M/G/1":
            res = core.mg1(params["lam"], params["mu"], params["sigma"])
            cartoes(res)
            st.subheader("Comparação")
            exp = core.mg1(params["lam"], params["mu"], 1 / params["mu"])
            cte = core.mg1(params["lam"], params["mu"], 0)
            df = pd.DataFrame(
                [[f"Informado (σ = {fmt(params['sigma'], casas)})", res["Lq"], res["L"], res["Wq"], res["W"]],
                 ["Exponencial – M/M/1 (σ = 1/μ)", exp["Lq"], exp["L"], exp["Wq"], exp["W"]],
                 ["Constante – M/D/1 (σ = 0)", cte["Lq"], cte["L"], cte["Wq"], cte["W"]]],
                columns=["Caso", "Lq", "L", "Wq", "W"])
            st.dataframe(df.style.format({c: lambda x: fmt(x, casas) for c in ["Lq", "L", "Wq", "W"]}),
                         hide_index=True, width="stretch")
            st.write(f"Razão Lq(informado) / Lq(M/M/1) = **{fmt(res['Lq'] / exp['Lq'], casas)}**")
            verificacao(res)

        elif modelo == "Prioridades":
            tipo = st.radio("Disciplina", ["Sem interrupção", "Com interrupção",
                                           "Sem interrupção – tempos gerais (μ e σ² por classe)"],
                            horizontal=True)
            c1, c2, c3 = st.columns(3)
            k = int(c1.number_input("Número de classes", 1, 10, 3))
            un_in = c2.selectbox("Unidade das taxas informadas (por …)", list(UNIDADES), index=2)
            geral = tipo.startswith("Sem interrupção – tempos")
            if not geral:
                mu_in = c3.number_input("μ – taxa de atendimento de cada servidor", min_value=0.0,
                                        value=3.0, format="%.6f")
                s = int(st.number_input("s – número de servidores", 1, 50, 1))
            padrao = [0.2, 0.6, 1.2, 0.5, 0.3]
            st.markdown("**Classes** (1 = maior prioridade)")
            lams, mus, vs = [], [], []
            for i in range(k):
                cols = st.columns(3)
                lams.append(cols[0].number_input(f"λ{i + 1}", min_value=0.0,
                                                 value=padrao[i] if i < len(padrao) else 0.1,
                                                 format="%.6f", key=f"lam_{i}"))
                if geral:
                    mus.append(cols[1].number_input(f"μ{i + 1}", min_value=0.0, value=20.0,
                                                    format="%.6f", key=f"mu_{i}"))
                    vs.append(cols[2].number_input(f"V(S{i + 1}) = σ² (em {un_in}²)", min_value=0.0,
                                                   value=0.0, format="%.8f", key=f"v_{i}"))
            lams = [taxa_para(v, un_in, un) for v in lams]
            if geral:
                mus = [taxa_para(v, un_in, un) for v in mus]
                vs = [v * (UNIDADES[un_in] / UNIDADES[un]) ** 2 for v in vs]
                res = core.prioridade_geral_sem_interrupcao(lams, mus, vs)
            else:
                mu = taxa_para(mu_in, un_in, un)
                f = core.prioridade_sem_interrupcao if tipo == "Sem interrupção" else core.prioridade_com_interrupcao
                res = f(lams, mu, s)

            df = pd.DataFrame(res["classes"]).rename(columns={
                "classe": "Classe", "lam": "λk", "lam_acum": "λ1+…+λk", "mu": "μk", "rho": "ρk",
                "W": f"W ({un})", "Wq": f"Wq ({un})"})
            num = [c for c in df.columns if c != "Classe"]
            st.dataframe(df.style.format({c: lambda x: fmt(x, casas) for c in num}),
                         hide_index=True, width="stretch")
            st.bar_chart(df.set_index("Classe")[[f"W ({un})", f"Wq ({un})"]], stack=False)
            if tipo == "Com interrupção":
                st.caption("Como nos slides 15–17: L_k = (λ1+…+λk)·W_k e Lq_k = L_k − (λ1+…+λk)/μ.")
            if "fcfs" in res:
                fc = res["fcfs"]
                st.info(f"Sem prioridade (FCFS, {fc['modelo']} com λ = {fmt(fc['lam'], casas)}): "
                        f"W = {fmt(fc['W'], casas)} · Wq = {fmt(fc['Wq'], casas)} · "
                        f"L = {fmt(fc['L'], casas)} · Lq = {fmt(fc['Lq'], casas)} · "
                        f"ocupação ρ = {fmt(fc['rho'], casas)}")
    except core.ErroModelo as e:
        mostrar_erro(e)
    except (ZeroDivisionError, OverflowError) as e:
        mostrar_erro(f"Não foi possível calcular com esses valores ({e}).")


# ---------------------------------------------------------------------------
# Fórmulas
# ---------------------------------------------------------------------------
FORMULAS = {
    "M/M/1": [
        r"\rho=\lambda/\mu,\quad P_0=1-\rho,\quad P_n=(1-\rho)\rho^n,\quad P(n>r)=\rho^{\,r+1}",
        r"L=\frac{\lambda}{\mu-\lambda},\quad L_q=\frac{\lambda^2}{\mu(\mu-\lambda)},\quad "
        r"W=\frac{1}{\mu-\lambda},\quad W_q=\frac{\lambda}{\mu(\mu-\lambda)}",
        r"P(W>t)=e^{-\mu(1-\rho)t},\quad P(W_q>t)=\rho\,e^{-\mu(1-\rho)t}",
    ],
    "M/M/s (s>1)": [
        r"P_0=1\Big/\left[\sum_{n=0}^{s-1}\frac{(\lambda/\mu)^n}{n!}+\frac{(\lambda/\mu)^s}{s!}\cdot\frac{1}{1-\lambda/(s\mu)}\right]",
        r"P_n=\frac{(\lambda/\mu)^n}{n!}P_0\ (n\le s),\qquad P_n=\frac{(\lambda/\mu)^n}{s!\,s^{n-s}}P_0\ (n\ge s)",
        r"L_q=\frac{P_0(\lambda/\mu)^s\rho}{s!(1-\rho)^2},\ W_q=\frac{L_q}{\lambda},\ L=L_q+\frac{\lambda}{\mu},\ W=W_q+\frac1\mu",
        r"P(W>t)=e^{-\mu t}\left[1+\frac{P_0(\lambda/\mu)^s}{s!(1-\rho)}\left(\frac{1-e^{-\mu t(s-1-\lambda/\mu)}}{s-1-\lambda/\mu}\right)\right]",
        r"P(W_q>t)=\left[1-P(W_q=0)\right]e^{-s\mu(1-\rho)t},\quad P(W_q=0)=\sum_{n=0}^{s-1}P_n",
    ],
    "M/M/1/K": [
        r"\rho=\lambda/\mu,\quad P_0=\frac{1-\rho}{1-\rho^{K+1}},\quad P_n=\frac{1-\rho}{1-\rho^{K+1}}\rho^n",
        r"L=\frac{\rho}{1-\rho}-\frac{(K+1)\rho^{K+1}}{1-\rho^{K+1}},\quad L_q=L-(1-P_0)",
        r"\bar\lambda=\lambda(1-P_K),\quad W=L/\bar\lambda,\quad W_q=L_q/\bar\lambda",
    ],
    "M/M/s/K": [
        r"P_0=1\Big/\left[\sum_{n=0}^{s}\frac{(\lambda/\mu)^n}{n!}+\frac{(\lambda/\mu)^s}{s!}\sum_{n=s+1}^{K}\left(\frac{\lambda}{s\mu}\right)^{n-s}\right]",
        r"L_q=\frac{P_0(\lambda/\mu)^s\rho}{s!(1-\rho)^2}\left[1-\rho^{K-s}-(K-s)\rho^{K-s}(1-\rho)\right]",
        r"L=\sum_{n=0}^{s-1}nP_n+L_q+s\left(1-\sum_{n=0}^{s-1}P_n\right),\quad \bar\lambda=\lambda(1-P_K)",
    ],
    "M/M/1/N (população finita)": [
        r"P_0=1\Big/\sum_{n=0}^{N}\frac{N!}{(N-n)!}\left(\frac\lambda\mu\right)^n,\quad P_n=\frac{N!}{(N-n)!}\left(\frac\lambda\mu\right)^nP_0",
        r"L=N-\frac{\mu}{\lambda}(1-P_0),\quad L_q=N-\frac{\lambda+\mu}{\lambda}(1-P_0)",
        r"\bar\lambda=\lambda(N-L),\quad W=L/\bar\lambda,\quad W_q=L_q/\bar\lambda",
    ],
    "M/M/s/N (população finita)": [
        r"P_0=1\Big/\left[\sum_{n=0}^{s-1}\frac{N!}{(N-n)!\,n!}\left(\frac\lambda\mu\right)^n+\sum_{n=s}^{N}\frac{N!}{(N-n)!\,s!\,s^{n-s}}\left(\frac\lambda\mu\right)^n\right]",
        r"L=\sum_{n=1}^{N}nP_n,\quad L_q=L-\frac{\lambda}{\mu}(N-L),\quad \bar\lambda=\lambda(N-L)",
    ],
    "M/G/1": [
        r"P_0=1-\rho,\quad L_q=\frac{\lambda^2\sigma^2+\rho^2}{2(1-\rho)}\ \text{(Pollaczek-Khintchine)}",
        r"L=\rho+L_q,\quad W_q=L_q/\lambda,\quad W=W_q+1/\mu",
    ],
    "Prioridades": [
        r"\textbf{Sem interrupção: } W_k=1\Big/\left[A\left(1-\frac{\sum_{i=1}^{k-1}\lambda_i}{s\mu}\right)\left(1-\frac{\sum_{i=1}^{k}\lambda_i}{s\mu}\right)\right]+\frac1\mu",
        r"A=s!\,\frac{s\mu-\lambda}{r^s}\sum_{j=0}^{s-1}\frac{r^j}{j!}+s\mu,\quad r=\lambda/\mu",
        r"\textbf{Com interrupção (s=1): } W_k=\frac{1/\mu}{\left(1-\frac{\sum_{i<k}\lambda_i}{s\mu}\right)\left(1-\frac{\sum_{i\le k}\lambda_i}{s\mu}\right)}",
        r"\textbf{Com interrupção (s>1): } \bar W_{1..k}=W_{M/M/s}(\lambda_1+\dots+\lambda_k),\ W_k=\frac{\Lambda_k\bar W_{1..k}-\Lambda_{k-1}\bar W_{1..k-1}}{\lambda_k}",
        r"\textbf{Tempos gerais: } E(W_{q_k})=\frac{\sum_i\lambda_i\left(V(S_i)+E(S_i)^2\right)}{2\left(1-\sum_{i<k}\rho_i\right)\left(1-\sum_{i\le k}\rho_i\right)}",
        r"\textbf{Sem interrupção: } W_{q_k}=W_k-\frac1\mu,\quad L_k=\lambda_kW_k,\quad L_{q_k}=L_k-\frac{\lambda_k}{\mu}",
        r"\textbf{Com interrupção (slides 15–17): } W_{q_k}=W_k-\frac1\mu,\quad L_k=(\lambda_1+\dots+\lambda_k)W_k,"
        r"\quad L_{q_k}=L_k-\frac{\lambda_1+\dots+\lambda_k}{\mu}",
    ],
}

SIGLAS = r"""
| Sigla | Nome | Significado |
|---|---|---|
| $\lambda$ | taxa de chegada | quantos clientes chegam por unidade de tempo |
| $\mu$ | taxa de atendimento | quantos clientes **um** servidor atende por unidade de tempo ($1/\mu$ = tempo médio de atendimento) |
| $s$ | número de servidores | quantos atendentes trabalham em paralelo |
| $K$ | capacidade do sistema | número máximo de clientes no sistema (na fila + em atendimento) |
| $N$ | tamanho da população | número total de clientes que podem chegar (população finita) |
| $\rho$ | taxa de ocupação (utilização) | fração do tempo em que os servidores estão ocupados: $\lambda/\mu$ (1 servidor) ou $\lambda/(s\mu)$ |
| $P_0$ | probabilidade de sistema vazio | chance de não haver nenhum cliente (taxa de ociosidade) |
| $P_n$ | probabilidade de $n$ clientes | chance de haver exatamente $n$ clientes no sistema |
| $P_K$ | probabilidade de sistema cheio | chance de o sistema estar lotado; o cliente que chega é bloqueado/perdido |
| $L$ | nº médio no sistema | média de clientes no sistema (na fila + em atendimento) |
| $L_q$ | nº médio na fila | média de clientes esperando na fila |
| $W$ | tempo médio no sistema | tempo total médio de um cliente (espera + atendimento) |
| $W_q$ | tempo médio na fila | tempo médio que um cliente espera até ser atendido |
| $\bar\lambda$ | taxa efetiva de chegada | taxa dos clientes que realmente entram no sistema (modelos /K e /N) |
| $\sigma$ | desvio-padrão do atendimento | variabilidade do tempo de atendimento no M/G/1 ($\sigma^2$ = variância) |
| $P(n>r)$ | — | probabilidade de haver mais de $r$ clientes no sistema |
| $P(W>t)$ | — | probabilidade de o tempo no sistema passar de $t$ |
| $P(W_q>t)$ | — | probabilidade de a espera na fila passar de $t$ |
| $k$ | classe de prioridade | nos modelos de prioridade, $k=1$ é a classe mais prioritária |

**Lei de Little:** $L = \lambda W$ e $L_q = \lambda W_q$ (usando $\bar\lambda$ nos modelos /K e /N).
"""

with aba_form:
    with st.expander("📌 Significado das siglas", expanded=True):
        st.markdown(SIGLAS)
    for nome, linhas in FORMULAS.items():
        with st.expander(nome, expanded=(nome == modelo)):
            for f in linhas:
                st.latex(f)
