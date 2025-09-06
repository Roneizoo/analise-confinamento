import streamlit as st

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================
st.set_page_config(page_title="Simulador Econômico Animal", layout="wide")
st.markdown(
    "<h1 style='text-align: center;'> Análise Econômica do Confinamento de Bovinos </h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ==============================
# ENTRADAS
# ==============================
st.sidebar.header("Parâmetros de Entrada")

peso_inicial = st.sidebar.number_input("Peso inicial (kg)", value=350.0, min_value=0.0, step=1.0, format="%.2f")
ganho_dia = st.sidebar.number_input("Ganho de peso/dia (kg)", value=1.40, min_value=0.0, step=0.05, format="%.2f")
dias = st.sidebar.number_input("Período de trato (dias)", value=110, min_value=1, step=1)

rendimento_ini = st.sidebar.number_input("Rendimento inicial (%)", value=50.0, min_value=0.0, max_value=100.0, step=0.1, format="%.2f") / 100
rendimento_fim = st.sidebar.number_input("Rendimento final (%)", value=56.0, min_value=0.0, max_value=100.0, step=0.1, format="%.2f") / 100

preco_compra_kg = st.sidebar.number_input("Valor de compra ($/kg de peso vivo)", value=11.30, min_value=0.0, step=0.01, format="%.2f")
preco_venda_kg = st.sidebar.number_input("Valor de venda ($/kg de carcaça)", value=21.40, min_value=0.0, step=0.01, format="%.2f")
diaria = st.sidebar.number_input("Custo Nutricional ($/dia)", value=14.50, min_value=0.0, step=0.1, format="%.2f")
servicos_operacionais = st.sidebar.number_input("Serviços operacionais ($/animal/dia)", value=1.0, min_value=0.0, step=0.10, format="%.2f")
custos_extras = st.sidebar.number_input("Custos extras ($/animal)", value=0.0, min_value=0.0, step=0.10, format="%.2f")
juros_mes = st.sidebar.number_input("Juros sobre custo do animal (% ao mês)", value=0.50, min_value=0.0, step=0.05, format="%.2f") / 100

# ==============================
# CÁLCULOS
# ==============================
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

# ==============================
# SAÍDAS EM COLUNAS
# ==============================
col1, col2, col3 = st.columns([1.2, 1.2, 1.2])

with col1:
    st.subheader("⚖️ Indicadores Zootécnicos")
    st.write(f"⚖️ Peso inicial: **{peso_inicial:.2f} kg**")
    st.write(f"⚖️ Peso final: **{peso_final:.2f} kg**")
    st.write(f"📆 Dias de trato: **{dias}**")
    st.write(f"➕ Ganho de peso vivo: **{ganho_peso:.2f} kg**")
    st.write(f"📈 Ganho de peso diário: **{ganho_dia:.2f} kg/dia**")
    st.write(f"🥩 Carcaça final: **{carcaca_final:.2f} kg**")
    st.write(f"🍖 Rendimento de carcaça (%): **{rendimento_fim * 100:.2f}%**")
    st.write(f"⚡ Carcaça produzida/dia: **{carcaca_dia:.2f} kg/dia**")

with col2:
    st.subheader("💰 Custos Detalhados")
    st.write(f"🐄 Custo do animal: **${valor_compra:,.2f}**")
    st.write(f"🥣 Custo nutricional: **${custo_nutricional:,.2f}**")
    st.write(f"👨‍🌾 Serviços operacionais: **${custo_servicos:,.2f}**")
    st.write(f"📦 Custos extras: **${custos_extras:,.2f}**")
    st.write(f"📌 **Despesas totais: ${despesas_totais:,.2f}**")
    st.write(f"🏦 Juros: **${juros:,.2f}**")
    st.write(f"🟠 **Custo total: ${custo_total:,.2f}**")

with col3:
    st.subheader("📊 Resultado Econômico")
    st.write(f"💵 Receita de venda: **${receita:,.2f}**")
    st.write(f"🪙 Lucro líquido: **${lucro:,.2f}**")
    st.write(f"📈 Margem de lucro: **{margem_lucro:.2f}%**")
    st.write(f"📊 Retorno sobre investimento: **{retorno_sobre_investimento:.2f}%**")
    st.write(f"📆 Retorno mensal sobre investimento: **{retorno_mensal_sobre_investimento:.2f}%/mês**")
    st.write(f"📊 Retorno sobre custo total: **{retorno_sobre_custo_total:.2f}%**")
    st.write(f"📆 Retorno mensal sobre custo total: **{retorno_mensal_sobre_custo_total:.2f}%/mês**")
