import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Simulador Econômico Animal", layout="wide")
st.markdown("<h1 style='text-align: center;'>Análise Econômica do Confinamento de Bovinos</h1>", unsafe_allow_html=True)
st.markdown("---")

# Entradas
st.sidebar.header("Parâmetros de Entrada")

peso_inicial = st.sidebar.number_input("Peso inicial (kg)", value=350.0)
ganho_dia = st.sidebar.number_input("Ganho de peso/dia (kg)", value=1.40)
dias = st.sidebar.number_input("Período de trato (dias)", value=110)

rendimento_ini = st.sidebar.number_input("Rendimento inicial (%)", value=50.0) / 100
rendimento_fim = st.sidebar.number_input("Rendimento final (%)", value=56.0) / 100

preco_compra_kg = st.sidebar.number_input("Valor de compra ($/kg)", value=11.30)
preco_venda_kg = st.sidebar.number_input("Valor de venda ($/kg carcaça)", value=21.40)
diaria = st.sidebar.number_input("Custo Nutricional ($/dia)", value=14.50)
servicos_operacionais = st.sidebar.number_input("Serviços operacionais ($/dia)", value=1.0)
custos_extras = st.sidebar.number_input("Custos extras ($)", value=0.0)
juros_mes = st.sidebar.number_input("Juros (% ao mês)", value=0.50) / 100

# Cálculos
peso_final = peso_inicial + ganho_dia * dias
carcaca_final = peso_final * rendimento_fim
ganho_peso = peso_final - peso_inicial
ganho_carcaca = carcaca_final - (peso_inicial * rendimento_ini)
carcaca_dia = ganho_carcaca / dias

valor_compra = peso_inicial * preco_compra_kg
custo_nutricional = diaria * dias
custo_servicos = servicos_operacionais * dias
despesas_totais = custo_nutricional + custo_servicos + custos_extras
juros = valor_compra * juros_mes * (dias / 30)
custo_total = valor_compra + despesas_totais + juros

receita = carcaca_final * preco_venda_kg
lucro = receita - custo_total
margem_lucro = (lucro / receita * 100) if receita > 0 else 0
retorno_sobre_investimento = (lucro / valor_compra * 100) if valor_compra > 0 else 0
retorno_mensal_sobre_investimento = (retorno_sobre_investimento / dias) * 30 if dias > 0 else 0
retorno_sobre_custo_total = (lucro / custo_total * 100) if custo_total > 0 else 0
retorno_mensal_sobre_custo_total = (retorno_sobre_custo_total / dias) * 30 if dias > 0 else 0

# Métricas
st.markdown("### 📊 Indicadores Econômicos")
col1, col2, col3 = st.columns(3)
col1.metric("Lucro líquido", f"${lucro:,.2f}")
col2.metric("ROI", f"{retorno_sobre_investimento:.2f}%")
col3.metric("Margem de lucro", f"{margem_lucro:.2f}%")

col4, col5, col6 = st.columns(3)
col4.metric("Retorno mensal ROI", f"{retorno_mensal_sobre_investimento:.2f}%/mês")
col5.metric("Retorno sobre custo", f"{retorno_sobre_custo_total:.2f}%")
col6.metric("Retorno mensal custo", f"{retorno_mensal_sobre_custo_total:.2f}%/mês")

# Gráfico de sensibilidade
st.markdown("### 📈 Lucro em função do preço de venda")
precos = np.linspace(preco_venda_kg * 0.9, preco_venda_kg * 1.1, 20)
lucros_precos = [(carcaca_final * p) - custo_total for p in precos]

fig, ax = plt.subplots()
ax.plot(precos, lucros_precos, marker="o", color="green")
ax.axhline(0, color="red", linestyle="--")
ax.set_xlabel("Preço de Venda ($/kg)")
ax.set_ylabel("Lucro ($)")
ax.set_title("Lucro vs. Preço de Venda")
st.pyplot(fig)

# Tabela de custos
st.markdown("### 💰 Tabela de Custos Detalhados")
df_custos = pd.DataFrame({
    "Descrição": [
        "Custo do animal",
        "Custo nutricional",
        "Serviços operacionais",
        "Custos extras",
        "Juros",
        "Despesas totais",
        "Custo total"
    ],
    "Valor ($)": [
        valor_compra,
        custo_nutricional,
        custo_servicos,
        custos_extras,
        juros,
        despesas_totais,
        custo_total
    ]
})
st.dataframe(df_custos.style.format({"Valor ($)": "{:,.2f}"}))

# Indicadores zootécnicos
st.markdown("### ⚖️ Indicadores Zootécnicos")
colz1, colz2, colz3 = st.columns(3)
colz1.write(f"Peso inicial: **{peso_inicial:.2f} kg**")
colz1.write(f"Peso final: **{peso_final:.2f} kg**")
colz1.write(f"Ganho de peso: **{ganho_peso:.2f} kg**")

colz2.write(f"Dias de trato: **{dias}**")
colz2.write(f"Ganho diário: **{ganho_dia:.2f} kg/dia**")
colz2.write(f"Carcaça final: **{carcaca_final:.2f} kg**")

colz3.write(f"Rendimento carcaça: **{rendimento_fim * 100:.2f}%**")
colz3.write(f"Carcaça/dia: **{carcaca_dia:.2f} kg/dia**")
