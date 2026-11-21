# Manual da Calculadora de Teoria das Filas (P108)

Este manual explica:

1. [Como abrir a calculadora](#1-como-abrir-a-calculadora)
2. [Como a tela está organizada](#2-como-a-tela-está-organizada)
3. [Como entrar com os dados (e o que ajustar)](#3-como-entrar-com-os-dados-e-o-que-ajustar)
4. [Como resolver um exercício, passo a passo](#4-como-resolver-um-exercício-passo-a-passo)
5. [Os 8 modelos: quando usar, como foi calculado e exemplo resolvido](#5-os-8-modelos)
6. [Armadilhas comuns nos enunciados](#6-armadilhas-comuns-nos-enunciados)
7. [Mensagens de erro](#7-mensagens-de-erro)

Todas as fórmulas são as dos slides do Prof. Paulo Roberto Maia.
Os exemplos deste manual são exercícios das listas e dos slides, e os valores mostrados são os que a calculadora dá (eles batem com os gabaritos).

---

## 1. Como abrir a calculadora

No terminal, dentro da pasta do projeto:

```bash
pip install -r requirements.txt      # só na primeira vez
python -m streamlit run app.py
```

A página abre no navegador em http://localhost:8501.
Para fechar, aperte **Ctrl+C** no terminal.

> Se aparecer "streamlit não é reconhecido", use `python -m streamlit run app.py` (como acima) em vez de `streamlit run app.py`.

---

## 2. Como a tela está organizada

**Barra lateral (esquerda)** – onde ficam os dados de entrada:

| Campo | Para que serve |
|---|---|
| **Modelo de filas** | Escolhe um dos 8 modelos. Os campos abaixo mudam conforme o modelo. |
| **Casas decimais** | Quantas casas aparecem nos resultados (2 a 8). |
| **Unidade de tempo dos resultados** | Unidade em que W e Wq são mostrados, e em que λ e μ são convertidos. |
| **Chegadas (λ)** | Taxa de chegada ou tempo médio entre chegadas, com a unidade. |
| **Atendimento (μ)** | Taxa de atendimento ou tempo médio de atendimento, com a unidade. |
| **s** | Número de servidores (só nos modelos M/M/s, M/M/s/K e M/M/s/N). |
| **K** | Capacidade máxima do sistema (só nos modelos /K). |
| **N** | Tamanho da população (só nos modelos /N). |
| **σ ou σ²** | Desvio-padrão ou variância do atendimento (só no M/G/1). |

**Área principal** – tem duas abas:

- **🧮 Calculadora**: os resultados.
  Logo abaixo do título aparece uma linha com os valores de λ e μ **já convertidos** para a unidade dos resultados. Confira essa linha sempre.
- **📖 Fórmulas**: todas as fórmulas usadas, por modelo.

No modelo **Prioridades**, os dados das classes são digitados na área principal, não na barra lateral.

---

## 3. Como entrar com os dados (e o que ajustar)

### 3.1 λ e μ: taxa ou tempo médio

Para cada um, escolha como o enunciado deu o dado:

| O enunciado diz… | Escolha | Digite |
|---|---|---|
| "chegam 20 clientes por hora" | **taxa λ** | 20, unidade **hora** |
| "chega um cliente a cada 3 minutos" | **tempo médio entre chegadas** | 3, unidade **minuto** |
| "atende 4 clientes por hora" | **taxa μ** | 4, unidade **hora** |
| "o atendimento leva em média 15 minutos" | **tempo médio de atendimento** | 15, unidade **minuto** |

A calculadora faz a conversão sozinha: tempo médio → taxa (taxa = 1 / tempo) e de uma unidade para outra.
λ e μ podem estar em unidades diferentes; não precisa converter na mão.

### 3.2 Unidade de tempo dos resultados

Escolha a unidade em que **a pergunta** quer a resposta.
Ex.: se a pergunta é "quantos minutos o cliente espera?", escolha **minuto**.

Isso também vale para os valores de **t** em P(W > t) e P(Wq > t): o t é digitado nessa mesma unidade.

> Mudar a unidade **não muda** L, Lq, P0 nem as probabilidades. Só muda W, Wq, as taxas e os tempos.

### 3.3 Outros parâmetros

- **s**: número de atendentes, caixas, pistas, técnicos etc.
- **K**: capacidade **total** do sistema = quem está sendo atendido + quem está na fila.
  Ex.: "1 em atendimento e 3 lugares de espera" → K = 4.
- **N**: número total de clientes que podem chegar (máquinas, robôs, aviões da frota).
  Em população finita, **λ é a taxa de cada cliente** (ex.: cada máquina quebra 1 vez a cada 200 h → λ = 1/200 por hora).
- **σ (M/G/1)**: desvio-padrão do tempo de atendimento, na unidade que você escolher ao lado.
  Se o enunciado der a variância, troque para **variância σ²**.
  Atendimento exponencial → σ = 1/μ. Atendimento constante → σ = 0.

### 3.4 Ferramentas extras na aba Calculadora

| Ferramenta | Modelos | Como usar |
|---|---|---|
| **P(n = …), P(n > …), P(n ≤ …)** | M/M/1, M/M/s | Digite n no campo "n (clientes no sistema)". |
| **P(W > t) e P(Wq > t)** | M/M/1, M/M/s | Digite o t de cada uma (na unidade dos resultados). |
| **Poisson** | M/M/1, M/M/s | Abra "Distribuição de Poisson" e digite x. Dá P(x chegadas) e P(x atendimentos) em **1 unidade de tempo**. |
| **Tabela de Pn** | todos menos M/G/1 e Prioridades | Mostra Pn, P(N ≤ n) e P(N > n) para cada n, com gráfico. Nos modelos M/M/1 e M/M/s, o controle deslizante escolhe até que n a tabela vai. |
| **λ efetiva e P_K** | M/M/1/K, M/M/s/K | Aparecem nos cartões. Logo abaixo aparecem os clientes bloqueados por unidade de tempo (λ·P_K). |
| **Clientes em operação, servidores ocupados** | M/M/1/N, M/M/s/N | Aparecem abaixo dos cartões. |
| **Custo** | M/M/1/N, M/M/s/N | Abra "💲 Custo (opcional)". |
| **Comparação M/M/1 × M/D/1** | M/G/1 | Tabela automática. |
| **Conferência (Lei de Little)** | todos menos Prioridades | Abra "✅ Conferência" para ver que L = λ·W e Lq = λ·Wq. |

---

## 4. Como resolver um exercício, passo a passo

1. **Identifique o modelo** respondendo a estas perguntas:

   ```
   As chegadas e o atendimento são exponenciais (Poisson)?
   ├─ O atendimento NÃO é exponencial (constante, ou só tem média e desvio) → M/G/1
   └─ Sim:
      Os clientes têm prioridades/classes diferentes? → Prioridades
      A população de clientes é pequena e conhecida (N máquinas, N robôs)? → M/M/1/N ou M/M/s/N
      O sistema tem limite de lugares (quem chega cheio vai embora)? → M/M/1/K ou M/M/s/K
      Nenhum dos casos acima → M/M/1 ou M/M/s
   Quantos atendentes? 1 → modelo "1"; mais de 1 → modelo "s"
   ```

2. **Retire os dados do enunciado**: λ, μ (ou os tempos médios) e as unidades; s, K, N ou σ, se houver.
3. **Escolha a unidade dos resultados** igual à unidade em que a pergunta quer a resposta.
4. **Digite os dados** e confira a linha "λ = … e μ = … por …" logo abaixo do título.
5. **Leia os resultados**:

   | Pergunta do enunciado | Onde está |
   |---|---|
   | Taxa de ocupação / utilização | ρ |
   | Probabilidade do sistema vazio / ocioso | P0 |
   | Número médio no sistema | L |
   | Número médio na fila | Lq |
   | Tempo médio no sistema | W |
   | Tempo médio na fila | Wq |
   | Probabilidade de ter exatamente n | P(n = …) ou tabela de Pn |
   | Probabilidade de ter mais de r | P(n > r) |
   | Probabilidade de ter no máximo r | P(n ≤ r) |
   | Probabilidade de ficar mais de t no sistema | P(W > t) |
   | Probabilidade de esperar mais de t na fila | P(Wq > t) |
   | Probabilidade de esperar no máximo t | 1 − P(Wq > t) |
   | Probabilidade de o sistema estar cheio / de perder um cliente | P_K |
   | Clientes perdidos por unidade de tempo | λ·P_K (caixa azul) |

6. **Comparar alternativas** (ex.: "vale a pena contratar mais um atendente?"): calcule cada alternativa e anote os resultados. Basta trocar s, μ ou o modelo na barra lateral.

---

## 5. Os 8 modelos

Notação usada em todo o manual:
λ = taxa de chegada, μ = taxa de atendimento de cada servidor, s = servidores, r = λ/μ.

### 5.1 M/M/1

**Quando usar:** 1 servidor, chegadas Poisson, atendimento exponencial, fila sem limite e população infinita.
**Precisa:** λ < μ.

**Como foi calculado:**

```
ρ = λ/μ            P0 = 1 − ρ          Pn = (1 − ρ)·ρⁿ        P(n > r) = ρ^(r+1)
L = λ/(μ − λ)      Lq = λ²/(μ(μ − λ))  W = 1/(μ − λ)          Wq = λ/(μ(μ − λ))
P(W > t)  = e^(−μ(1−ρ)t)
P(Wq > t) = ρ·e^(−μ(1−ρ)t)
Poisson: P(X = x) = e^(−λ)·λˣ / x!
```

**Exemplo (Lista M/M/s, ex. 13):** chegam 20 clientes por hora e o atendimento leva em média 2 minutos. As respostas são pedidas em minutos.

| Campo | Valor |
|---|---|
| Modelo | M/M/1 |
| Unidade de tempo dos resultados | minuto |
| Chegadas | taxa λ = 20, unidade hora |
| Atendimento | tempo médio de atendimento = 2, unidade minuto |
| t para P(Wq > t) | 5 |
| t para P(W > t) | 7 |

Resultado: L = 2; Lq = 1,3333; W = 6 min; Wq = 4 min; P(Wq > 5) = 0,2897; P(W > 7) = 0,3114.

**Outro exemplo (Lista M/M/s, ex. 5):** λ = 3 e μ = 4 por hora →
L = 3; Lq = 2,25; W = 1 h; Wq = 0,75 h; ρ = 0,75; P(n = 6) = 0,0445; P(W > 2) = 0,1353; P(Wq > 1,5) = 0,1673.

---

### 5.2 M/M/s (s > 1)

**Quando usar:** como o M/M/1, mas com **s servidores** atendendo **uma fila única**.
**Precisa:** λ < s·μ.

**Como foi calculado:**

```
ρ = λ/(sμ)
P0 = 1 / [ Σ_{n=0}^{s−1} rⁿ/n!  +  rˢ/s! · 1/(1 − ρ) ]
Pn = rⁿ/n! · P0                (n ≤ s)
Pn = rⁿ/(s!·s^(n−s)) · P0       (n ≥ s)
Lq = P0·rˢ·ρ / (s!·(1 − ρ)²)    Wq = Lq/λ    L = Lq + λ/μ    W = Wq + 1/μ
P(n > r) = 1 − Σ_{n=0}^{r} Pn
P(W > t)  = e^(−μt)·[ 1 + P0·rˢ/(s!(1−ρ)) · (1 − e^(−μt(s−1−r))) / (s−1−r) ]
P(Wq > t) = [1 − P(Wq = 0)]·e^(−sμ(1−ρ)t),   P(Wq = 0) = Σ_{n=0}^{s−1} Pn
```

Quando s − 1 − r = 0, a fração de P(W > t) vira 0/0. Nesse caso a calculadora usa o limite, que é μt.

**Exemplo (slide – banco):** λ = 0,6 e μ = 0,5 por minuto, s = 3. Resultados em minutos; n = 5; t = 3 para P(W > t); t = 2 para P(Wq > t).

Resultado: ρ = 0,4; P0 = 0,2941; L = 1,2941; Lq = 0,0941; W = 2,1569 min; Wq = 0,1569 min;
P(n > 5) = 0,0090; P(W > 3) = 0,2506; P(Wq > 2) = 0,0233.

**Exemplo de comparação (Lista M/M/s, ex. 7 – hospital):** λ = 2 e μ = 3 por hora.
Com **M/M/1**: L = 2. Com **M/M/s, s = 2**: L = 0,75; Lq = 0,0833; P0 = 0,5; W = 0,375 h; Wq = 0,0417 h.

---

### 5.3 M/M/1/K

**Quando usar:** 1 servidor e **no máximo K clientes no sistema**. Quem chega com o sistema cheio vai embora (é bloqueado).
**Não precisa** de λ < μ: a fila nunca cresce sem limite.

**Como foi calculado:**

```
ρ = λ/μ
P0 = (1 − ρ)/(1 − ρ^(K+1))        Pn = P0·ρⁿ   (n = 0 … K)
L  = ρ/(1 − ρ) − (K+1)·ρ^(K+1)/(1 − ρ^(K+1))
Lq = L − (1 − P0)
λ̄ = λ·(1 − P_K)      (λ efetiva: só quem consegue entrar)
W  = L/λ̄             Wq = Lq/λ̄
```

Se ρ = 1, as fórmulas viram 0/0. Nesse caso a calculadora usa o limite: P0 = 1/(K+1) e L = K/2.

**Exemplo (slide):** λ = 3 e μ = 4 por hora, K = 5 →
P0 = 0,3041; L = 1,7009; Lq = 1,0050; P4 = 0,0962; W = 0,6111 h; Wq = 0,3611 h.

**Exemplo (Lista M/M/s/K, ex. 3):** pista de pouso, 1 avião pousando + 3 esperando (K = 4). Chega 1 avião a cada 4 min e o pouso leva 3 min. Resultados em minutos:
Lq = 0,7721; Wq = 3,4457 min; P4 = 0,1037 (probabilidade de o avião ser desviado).

---

### 5.4 M/M/s/K

**Quando usar:** s servidores e **no máximo K clientes no sistema** (K ≥ s).

**Como foi calculado:**

```
r = λ/μ        ρ = λ/(sμ)
P0 = 1 / [ Σ_{n=0}^{s} rⁿ/n!  +  rˢ/s! · Σ_{n=s+1}^{K} ρ^(n−s) ]
Pn = rⁿ/n! · P0             (n ≤ s)
Pn = rⁿ/(s!·s^(n−s)) · P0    (s < n ≤ K)
Lq = P0·rˢ·ρ/(s!(1−ρ)²) · [1 − ρ^(K−s) − (K−s)·ρ^(K−s)·(1−ρ)]
L  = Σ_{n=0}^{s−1} n·Pn + Lq + s·(1 − Σ_{n=0}^{s−1} Pn)
λ̄ = λ·(1 − P_K)      W = L/λ̄      Wq = Lq/λ̄
```

Se ρ = 1, a fórmula de Lq vira 0/0. Nesse caso a calculadora soma direto: Lq = Σ (n − s)·Pn.
Com s = 1, a calculadora usa automaticamente as fórmulas do M/M/1/K.

**Exemplo (slide – inspeção de carros):** chega 1 carro por minuto e cada inspeção leva 6 min. São 3 boxes e cabem 7 carros no total.

| Campo | Valor |
|---|---|
| Modelo | M/M/s/K |
| Unidade de tempo dos resultados | minuto |
| Chegadas | taxa λ = 1, unidade minuto |
| Atendimento | tempo médio de atendimento = 6, unidade minuto |
| s | 3 |
| K | 7 |

Resultado: P0 = 0,00088; L = 6,0631; Lq = 3,0920; W = 12,2442 min; Wq = 6,2442 min.
Para ver os **carros perdidos por hora**, troque a unidade dos resultados para **hora**: a caixa azul mostra 30,29.

---

### 5.5 M/M/1/N (população finita)

**Quando usar:** 1 servidor (técnico, mecânico) atende uma população **pequena e conhecida** de N clientes (máquinas, robôs).
Um cliente que está no sistema (quebrado) não pode chegar de novo. Por isso a taxa de chegada total cai quando há gente no sistema.

**λ é a taxa de cada cliente** (ex.: cada máquina quebra, em média, a cada 200 h → λ = 1/200 por hora).

**Como foi calculado:**

```
r = λ/μ
P0 = 1 / Σ_{n=0}^{N} N!/(N−n)! · rⁿ       Pn = N!/(N−n)! · rⁿ · P0
L  = N − (μ/λ)·(1 − P0)
Lq = N − ((λ + μ)/λ)·(1 − P0)
λ̄ = λ·(N − L)       W = L/λ̄       Wq = Lq/λ̄
ρ (como no slide) = N·λ/μ
```

Outros valores mostrados:

- **Clientes em operação** = N − L.
- **Fração de cada cliente em operação** = (N − L)/N.
- **Servidores ocupados** = L − Lq. Com s = 1, isso é igual a 1 − P0.

**Exemplo (Lista M/M/s/N, ex. 1):** 10 máquinas; cada uma quebra em média a cada 200 h; o conserto leva em média 10 h.

| Campo | Valor |
|---|---|
| Modelo | M/M/1/N |
| Unidade de tempo dos resultados | hora |
| Chegadas | tempo médio entre chegadas = 200, unidade hora |
| Atendimento | tempo médio de atendimento = 10, unidade hora |
| N | 10 |

Resultado: P0 = 0,5380; L = 0,7593; Lq = 0,2972; W = 16,4330 h; Wq = 6,4330 h.

**Custo** (mesmo exercício): R$ 30/h por máquina parada, R$ 10/h pelo técnico quando ocupado, 8 h por dia.
Em "💲 Custo", preencha 30, 10, "só quando ocupado" e período 8 → **R$ 219,19 por dia**.
A conta é (L·30 + (L − Lq)·10)·8.

---

### 5.6 M/M/s/N (população finita)

**Quando usar:** como o M/M/1/N, mas com **s servidores**.

**Como foi calculado:**

```
r = λ/μ
Pn = N!/((N−n)!·n!) · rⁿ · P0              (n < s)
Pn = N!/((N−n)!·s!·s^(n−s)) · rⁿ · P0       (s ≤ n ≤ N)
P0 = 1 / soma dos termos acima (sem o P0)
L  = Σ_{n=1}^{N} n·Pn
Lq = L − (λ/μ)·(N − L)
λ̄ = λ·(N − L)       W = L/λ̄       Wq = Lq/λ̄
ρ (como no slide) = N·λ/(s·μ)
```

Com s = 1, a calculadora usa automaticamente as fórmulas do M/M/1/N.

**Exemplo (Lista M/M/s/N, ex. 6):** λ = 1/100 e μ = 1/10 por hora (digite os tempos médios 100 h e 10 h), s = 2, N = 4 →
P0 = 0,6820; L = 0,3677; Lq = 0,0045; W = 10,1239 h; Wq = 0,1239 h.

**Exemplo (slide – robôs):** λ = 1/30, μ = 1/3, N = 5.
Com s = 1: robôs em operação = 4,360 e W = 4,4. Com s = 2: robôs em operação = 4,535 e W = 3,075.

---

### 5.7 M/G/1

**Quando usar:** 1 servidor, chegadas Poisson, mas o atendimento tem **qualquer distribuição**. Basta conhecer a média (1/μ) e o desvio-padrão σ.
**Precisa:** λ < μ.

**Como foi calculado (fórmula de Pollaczek-Khintchine):**

```
ρ = λ/μ        P0 = 1 − ρ
Lq = (λ²·σ² + ρ²) / (2·(1 − ρ))
L  = ρ + Lq     Wq = Lq/λ     W = Wq + 1/μ
```

A calculadora também mostra uma tabela comparando o seu caso com:

- **atendimento exponencial** (σ = 1/μ), que dá o mesmo que o M/M/1;
- **atendimento constante** (σ = 0, M/D/1), que dá metade do Lq do M/M/1.

**Exemplo (Lista M/G/1, ex. 2 – caminhões):** chegam 3 caminhões por hora e a descarga leva **sempre** 15 min (constante).

| Campo | Valor |
|---|---|
| Modelo | M/G/1 |
| Unidade de tempo dos resultados | hora |
| Chegadas | taxa λ = 3, unidade hora |
| Atendimento | tempo médio de atendimento = 15, unidade minuto |
| σ | 0 |

Resultado: ρ = 0,75; Lq = 1,125; L = 1,875; Wq = 0,375 h; W = 0,625 h.

**Exemplo (Lista M/G/1, ex. 1):** λ = 0,2 e μ = 0,25, variando σ:

| σ | Lq | L | Wq | W |
|---|---|---|---|---|
| 4 | 3,2 | 4,0 | 16,0 | 20,0 |
| 3 | 2,5 | 3,3 | 12,5 | 16,5 |
| 2 | 2,0 | 2,8 | 10,0 | 14,0 |
| 1 | 1,7 | 2,5 | 8,5 | 12,5 |
| 0 | 1,6 | 2,4 | 8,0 | 12,0 |

---

### 5.8 Prioridades

**Quando usar:** os clientes são divididos em **classes**, e a classe 1 tem a maior prioridade.
Neste modelo os dados são digitados **na área principal**:

| Campo | O que colocar |
|---|---|
| **Disciplina** | "Sem interrupção", "Com interrupção" ou "Sem interrupção – tempos gerais". |
| **Número de classes** | Quantas classes de prioridade existem. |
| **Unidade das taxas informadas** | A unidade "por …" das taxas digitadas (λ de cada classe e μ). |
| **μ** | Taxa de atendimento de **cada servidor** (igual para todas as classes). |
| **s** | Número de servidores. |
| **λ1, λ2, …** | Taxa de chegada de cada classe (λ1 = maior prioridade). |

Os resultados (W e Wq) saem na unidade escolhida na barra lateral.
Abaixo da tabela aparece a comparação com a fila **sem prioridade** (FCFS).

**Sem interrupção ou com interrupção?**

- **Sem interrupção (não preemptiva):** um cliente que já começou a ser atendido termina o atendimento, mesmo que chegue alguém mais prioritário.
- **Com interrupção (preemptiva):** quando chega um cliente mais prioritário, o atendimento atual é interrompido e o cliente de menor prioridade volta para a fila.

**Como foi calculado – sem interrupção (slide 11):**

```
λ = λ1 + λ2 + … (total)     r = λ/μ
A = s!·(sμ − λ)/rˢ · Σ_{j=0}^{s−1} rʲ/j!  +  sμ
B_k = 1 − (λ1 + … + λk)/(sμ)        (B_0 = 1)
W_k  = 1/(A·B_{k−1}·B_k) + 1/μ
Wq_k = W_k − 1/μ       L_k = λk·W_k       Lq_k = L_k − λk/μ
```

**Como foi calculado – com interrupção:**

```
s = 1:   W_k = (1/μ) / (B_{k−1}·B_k)
s > 1:   as classes 1..k juntas se comportam como um M/M/s com λ = λ1+…+λk.
         Chamando de W̄(1..k) o W desse M/M/s e Λk = λ1+…+λk:
         W_k = [Λk·W̄(1..k) − Λ(k−1)·W̄(1..k−1)] / λk
Wq_k = W_k − 1/μ
L_k  = (λ1+…+λk)·W_k          ← como nos slides 15–17
Lq_k = L_k − (λ1+…+λk)/μ
```

> **Atenção:** pela Lei de Little, o número médio de clientes da classe k seria λk·W_k, que é a conta usada no caso sem interrupção.
> A calculadora segue os slides; confirme com o professor qual usar. W e Wq não são afetados.

**Como foi calculado – sem interrupção, tempos gerais (slides 18–19, 1 servidor):**
cada classe tem seu próprio μk e sua variância V(Sk).

```
E(Sk) = 1/μk       ρk = λk/μk
Wq_k = Σ_i λi·(V(Si) + E(Si)²) / [ 2·(1 − ρ1 − … − ρ(k−1))·(1 − ρ1 − … − ρk) ]
W_k  = 1/μk + Wq_k     L_k = λk·W_k     Lq_k = L_k − λk/μk
```

**Exemplo (slides – 3 classes):** λ1 = 0,2, λ2 = 0,6, λ3 = 1,2 e μ = 3.

| Caso | W1 | W2 | W3 |
|---|---|---|---|
| Sem interrupção, s = 1 | 0,5714 | 0,6580 | 1,2424 |
| Sem interrupção, s = 2 | 0,3621 | 0,3665 | 0,3814 |
| Com interrupção, s = 1 | 0,3571 | 0,4870 | 1,3636 |
| Com interrupção, s = 2 | 0,3337 | 0,3413 | 0,3988 |

**Exemplo (slide – tempos gerais):** escolha a disciplina "Sem interrupção – tempos gerais", 2 classes, unidade **hora**:
λ1 = 10, μ1 = 20, V(S1) = 0,00055556 (= 1/1800 h²);
λ2 = 5, μ2 = 15, V(S2) = 0,00055556.
Resultado em horas: Wq1 = 0,0556; Wq2 = 0,3333; W1 = 0,1056; W2 = 0,4000.

> A variância deve estar na **unidade das taxas ao quadrado**. Ex.: se as taxas são por hora, a variância vai em h². Para converter de min² para h², divida por 3600.

---

## 6. Armadilhas comuns nos enunciados

| Enunciado | Como interpretar |
|---|---|
| "no máximo r **no sistema**" | P(n ≤ r) |
| "no máximo r **na fila**" | P(n ≤ r + s), porque s estão sendo atendidos |
| "mais de r na fila" | P(n > r + s) |
| "esperar no máximo t" | 1 − P(Wq > t) |
| "ficar no sistema mais de t" | P(W > t) |
| "1 em atendimento + 3 esperando" | K = 4 (K conta todos) |
| "percentual de tempo ocioso" | P0 |
| "percentual de tempo ocupado" | 1 − P0 (com 1 servidor); com s servidores, use "ocupação de cada servidor" (M/M/s/N) ou ρ |
| "taxa de clientes perdidos" | λ·P_K (caixa azul nos modelos /K) |
| "cada máquina quebra a cada 200 h" (população finita) | λ = 1/200 por hora, **por máquina** |
| "atendimento constante" | M/G/1 com σ = 0 |
| "atendimento exponencial" no M/G/1 | σ = 1/μ (o mesmo valor do tempo médio) |
| Dados dados em minutos, pergunta em horas | Digite em minutos e escolha **hora** na unidade dos resultados |

Algumas respostas dos gabaritos usam interpretações diferentes das acima. Essas divergências estão listadas no [README](README.md#divergências-encontradas-nos-gabaritos).

---

## 7. Mensagens de erro

| Mensagem | O que fazer |
|---|---|
| "Sistema instável: é necessário λ < μ" (ou λ < s·μ) | A fila cresceria sem parar. Confira se λ e μ não estão trocados ou em unidades erradas. Senão, aumente s ou μ. Nos modelos /K e /N essa condição não existe. |
| "… deve ser maior que zero" | Algum campo ficou com 0. Preencha λ e μ. |
| "A capacidade K deve ser maior ou igual ao número de servidores s" | K conta quem está sendo atendido, então K ≥ s. |
| "Não foi possível calcular com esses valores" | Algum número ficou grande demais (ex.: N muito alto). Confira os dados. |
