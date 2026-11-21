# Projeto P108 – Calculadora de Teoria das Filas

Projeto da disciplina **Otimização II (P108 – Inatel)**.

É uma calculadora com interface web, feita em **Python** com **Streamlit**, que resolve os 8 modelos de filas estudados em aula.
O usuário informa os dados do problema (taxas, tempos, número de servidores, capacidade, população…) e a calculadora mostra as medidas de desempenho da fila.

Todas as fórmulas seguem os slides do Prof. Paulo Roberto Maia, e os resultados foram conferidos com as listas de exercícios da disciplina.

## Modelos

| Modelo | Situação | O que calcula |
|---|---|---|
| **M/M/1** | 1 servidor, fila sem limite | ρ, P0, L, Lq, W, Wq, Pn, P(n>r), P(W>t), P(Wq>t), Poisson |
| **M/M/s** (s>1) | s servidores, fila única | as mesmas medidas do M/M/1 |
| **M/M/1/K** | 1 servidor, no máximo K clientes no sistema | P0, Pn, L, Lq, λ efetiva, W, Wq, P_K e clientes bloqueados |
| **M/M/s/K** | s servidores, no máximo K clientes no sistema | as mesmas medidas do M/M/1/K |
| **M/M/1/N** | 1 servidor, população finita de N clientes | P0, Pn, L, Lq, λ efetiva, W, Wq, clientes em operação e custo |
| **M/M/s/N** | s servidores, população finita de N clientes | as mesmas medidas do M/M/1/N |
| **M/G/1** | 1 servidor, atendimento com qualquer distribuição | Pollaczek-Khintchine, comparado com M/M/1 (exponencial) e M/D/1 (constante) |
| **Prioridades** | clientes divididos em classes | sem interrupção e com interrupção (s ≥ 1), e sem interrupção com tempos gerais por classe |

## Funcionalidades

- λ e μ podem ser digitados como **taxa** ("20 por hora") ou como **tempo médio** ("2 minutos"), cada um na sua unidade. A conversão é automática.
- Os resultados saem na unidade de tempo escolhida (segundo, minuto, hora, dia ou mês).
- Probabilidades: P(n = r), P(n > r), P(n ≤ r), P(W > t), P(Wq > t) e distribuição de Poisson.
- Tabela e gráfico de Pn com probabilidades acumuladas.
- Clientes bloqueados (modelos /K), clientes em operação e custo (modelos /N).
- Comparação com a fila sem prioridade (FCFS) nos modelos de prioridade.
- Conferência dos resultados pela Lei de Little.
- Aba **Fórmulas** com todas as fórmulas usadas.

## Como rodar

Requer Python 3.10 ou mais novo.

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

A página abre em http://localhost:8501.

> No Windows, se `streamlit run app.py` der "não é reconhecido", use `python -m streamlit run app.py`, como acima.

## Como usar

1. Na barra lateral, escolha o **modelo**.
2. Escolha a **unidade de tempo dos resultados** (a unidade em que a pergunta quer a resposta).
3. Informe **λ** e **μ** (como taxa ou tempo médio) e, se o modelo pedir, **s**, **K**, **N** ou **σ**.
4. Leia os resultados na aba **Calculadora**.

O **[MANUAL.md](MANUAL.md)** tem o passo a passo completo: como entrar com os dados, como escolher o modelo pelo enunciado, as fórmulas de cada modelo e exercícios resolvidos.

## Estrutura

```
app.py                    interface (Streamlit)
filas/core.py             fórmulas dos 8 modelos (Python puro, sem dependências)
tests/test_exercicios.py  validação com as listas de exercícios e os exemplos dos slides
MANUAL.md                 manual de uso e exercícios resolvidos
.streamlit/config.toml    configuração do Streamlit
requirements.txt          dependências
```

Os cálculos ficam separados da interface: `filas/core.py` tem uma função por modelo, que recebe λ, μ e os outros parâmetros e devolve P0, L, Lq, W, Wq e as demais medidas.

## Validação

```bash
python -m unittest -v
```

São 46 testes com os gabaritos das quatro listas (M/M/s, M/M/s/K, M/M/s/N, M/G/1 e prioridades) e os exemplos dos slides.
Todos passam.

As fórmulas também foram conferidas de forma independente, recalculando cada modelo pela soma direta das probabilidades Pn.

### Divergências encontradas nos gabaritos

As fórmulas do slide foram mantidas. Os testes documentam estes casos:

1. **Lista M/M/s/K, ex. 4, 5 e 6e (s = 2):** os gabaritos (Lq = 0,0848; L = 0,8212; P = 0,0182; Wq = 0,0288) só batem com **K = 4**.
   Pelos enunciados ("2 pistas + 3 em espera", "máximo de 5 pacientes"), o esperado seria K = 5.
2. **Lista M/M/s, ex. 14c:** o valor 92,7% corresponde a P(n ≤ 5).
   Com 2 pistas, "no máximo 4 aviões esperando" equivale a P(n ≤ 6) = 95,4%.
3. **Lista M/M/s, ex. 8:** o enunciado já informa Wq = 1 min (valor medido).
   O gabarito vem da Lei de Little com esse Wq, não do M/M/2 calculado (que daria L = 2,4).
4. **Lista M/M/s/N, ex. 4c:** o gabarito 0,667 é o ρ = Nλ/μ do slide.
   A fração de tempo ocupado (1 − P0) seria 0,507. O ex. 3c usa 1 − P0.
5. **Lista M/M/s/N, ex. 6d (0,8184) e ex. 5b/5c (custos 478,672 e 270,336):** não foi possível reproduzir esses valores.
   Pela mesma conta do ex. 3d, a fração de operação do ex. 6d dá (N − L)/N = 0,908.
6. **Prioridade com interrupção:** os slides 15–17 calculam L_k = (λ1+…+λk)·W_k, com λ acumulado.
   No modo sem interrupção, o slide usa L_k = λk·W_k, que é o que a Lei de Little dá. O programa segue cada slide como está.
