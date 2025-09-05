import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import io
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

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
custo_servicos = servicos_operacionais * dias   # ✅ corrigido
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

# ==============================
# FUNÇÕES AUXILIARES PDF
# ==============================
def carregar_logo_path():
    candidatos = ["logo.png", "logo.jpg", "logo.jpeg", "logo.PNG", "logo.JPG", "logo.png.png"]
    for nome in candidatos:
        if os.path.isfile(nome):
            return nome
    for p in glob.glob("logo*"):
        if os.path.isfile(p):
            return p
    return None

LOGO_PATH = carregar_logo_path()

def add_header(canvas, doc):
    canvas.saveState()
    blue = colors.HexColor("#003366")
    margin_x = 1*cm

    has_logo = bool(LOGO_PATH)
    logo_w, logo_h = 80, 70

    if has_logo:
        canvas.drawImage(LOGO_PATH, margin_x, A4[1] - logo_h - 0.5*cm,
                         width=logo_w, height=logo_h, preserveAspectRatio=True, mask="auto")
        title_x = margin_x + logo_w + 1*cm
        title_y = A4[1] - (logo_h/2 + 1*cm)
        y_linha_cabecalho = A4[1] - (logo_h + 1.2*cm)
    else:
        title_x = margin_x
        title_y = A4[1] - 2*cm
        y_linha_cabecalho = A4[1] - 3*cm

    canvas.setFont("Helvetica-Bold", 14)
    canvas.setFillColor(blue)
    canvas.drawString(title_x, title_y, "Relatório de Viabilidade Econômica")

    canvas.setStrokeColor(blue)
    canvas.setLineWidth(1)
    canvas.line(margin_x, y_linha_cabecalho, A4[0] - margin_x, y_linha_cabecalho)

    # Rodapé
    canvas.setFont("Helvetica", 9)
    rodape_y = 2*cm
    canvas.setFillColor(blue)
    canvas.drawCentredString(A4[0]/2, rodape_y + 20, "Rural Nutrição Animal Ltda")
    canvas.drawCentredString(A4[0]/2, rodape_y + 10, "Rod. BR 163 km 38,5 Eldorado-MS")
    canvas.drawCentredString(A4[0]/2, rodape_y, "Fone: (67) 3473-1214 | (67) 99212-5955")
    canvas.line(margin_x, rodape_y + 30, A4[0] - margin_x, rodape_y + 30)

    canvas.restoreState()

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="SectionTitle", fontSize=12, textColor=colors.HexColor("#003366"), spaceBefore=8, spaceAfter=10))
styles.add(ParagraphStyle(name="TableText", fontSize=9, leading=11))

# ==============================
# RELATÓRIO EM 2 PÁGINAS
# ==============================
def gerar_pdf_duas_paginas():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=1.5*cm, rightMargin=1.5*cm,
        topMargin=4.0*cm, bottomMargin=3.0*cm
    )
    elementos = []

    # Página 1
    elementos.append(Paragraph("Resumo Executivo", styles["SectionTitle"]))
    resumo = [
        ["Receita ($)", f"{receita:,.2f}"],
        ["Custo Total ($)", f"{custo_total:,.2f}"],
        ["Lucro ($)", f"{lucro:,.2f}"],
        ["ROI (%)", f"{retorno_sobre_investimento:.2f}%"],
    ]
    tabela_resumo = Table(resumo, colWidths=[200, 200])
    tabela_resumo.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.5,colors.black),
        ("FONTSIZE", (0,0), (-1,-1), 9)
    ]))
    elementos.append(tabela_resumo)
    elementos.append(Spacer(1, 14))

    elementos.append(Paragraph("Indicadores Zootécnicos", styles["SectionTitle"]))
    ind = [
        ["Peso inicial (kg)", f"{peso_inicial:.2f}"],
        ["Peso final (kg)", f"{peso_final:.2f}"],
        ["Dias de trato", f"{dias}"],
        ["Ganho de peso diário (kg/dia)", f"{ganho_dia:.2f}"],
        ["Carcaça final (kg)", f"{carcaca_final:.2f}"],
        ["Carcaça/dia (kg)", f"{carcaca_dia:.2f}"],
    ]
    tabela1 = Table(ind, colWidths=[200, 200])
    tabela1.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.5,colors.black),
        ("FONTSIZE", (0,0), (-1,-1), 9)
    ]))
    elementos.append(tabela1)
    elementos.append(Spacer(1, 14))

    elementos.append(Paragraph("Custos Detalhados", styles["SectionTitle"]))
    custos = [
        ["Valor de compra ($/kg de peso vivo)", f"{preco_compra_kg:.2f}"],
        ["Valor de venda ($/kg de carcaça)", f"{preco_venda_kg:.2f}"],
        ["Custo do animal ($)", f"{valor_compra:,.2f}"],
        ["Custo nutricional ($)", f"{custo_nutricional:,.2f}"],
        ["Serviços operacionais ($)", f"{custo_servicos:,.2f}"],
        ["Custos extras ($)", f"{custos_extras:,.2f}"],
        ["Juros ($)", f"{juros:,.2f}"],
        ["Total de despesas ($)", f"{despesas_totais:,.2f}"],
        ["Custo total ($)", f"{custo_total:,.2f}"],
    ]
    tabela2 = Table(custos, colWidths=[200, 200])
    tabela2.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.5,colors.black),
        ("FONTSIZE", (0,0), (-1,-1), 9)
    ]))
    elementos.append(tabela2)
    elementos.append(Spacer(1, 14))

    elementos.append(Paragraph("Resultado Econômico", styles["SectionTitle"]))
    resultado = [
        ["Receita ($)", f"{receita:,.2f}"],
        ["Lucro líquido ($)", f"{lucro:,.2f}"],
        ["Margem de lucro (%)", f"{margem_lucro:.2f}%"],
        ["Retorno sobre investimento (%)", f"{retorno_sobre_investimento:.2f}%"],
        ["Retorno mensal sobre investimento (%)", f"{retorno_mensal_sobre_investimento:.2f}%"],
        ["Retorno sobre custo total (%)", f"{retorno_sobre_custo_total:.2f}%"],
        ["Retorno mensal sobre custo total (%)", f"{retorno_mensal_sobre_custo_total:.2f}%"],
    ]
    tabela3 = Table(resultado, colWidths=[200, 200])
    tabela3.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.5,colors.black),
        ("FONTSIZE", (0,0), (-1,-1), 9)
    ]))
    elementos.append(tabela3)

    # Página 2 - Gráfico
    elementos.append(PageBreak())
    elementos.append(Paragraph("Análise de Sensibilidade", styles["SectionTitle"]))
    elementos.append(Spacer(1, 10))

    precos = np.linspace(20, 21.25, 23)
    lucros_precos = [(carcaca_final * p) - custo_total for p in precos]

    plt.figure(figsize=(6.5,4.5))
    plt.plot(precos, lucros_precos, marker="o")
    plt.axhline(0, color="red", linestyle="--")
    plt.xlabel("Preço de Venda ($/kg)", fontsize=10, labelpad=8)
    plt.ylabel("Lucro ($)", fontsize=10, labelpad=8)
    plt.title("Lucro em função do preço de venda", fontsize=11, pad=15)
    plt.tight_layout()
    plt.savefig("grafico_preco.png", dpi=150)
    plt.close()

    elementos.append(Image("grafico_preco.png", width=450, height=280))

    doc.build(elementos, onFirstPage=add_header, onLaterPages=add_header)
    buffer.seek(0)
    return buffer

# ==============================
# BOTÃO DE EXPORTAÇÃO
# ==============================
st.markdown("---")
if st.button("📥 Exportar Relatório (2 páginas)"):
    pdf_final = gerar_pdf_duas_paginas()
    st.download_button(
        label="⬇️ Baixar PDF",
        data=pdf_final,
        file_name="relatorio_viabilidade.pdf",
        mime="application/pdf",
    )
