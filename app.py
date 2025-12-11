# Robô Tridente V.42 — Script completo (visual premium + lógica intacta)
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# -------------------------
# 🔐 SENHA (LOGIN)
# -------------------------
SENHA_ACESSO = "tridente2025"

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    st.markdown("## 🔐 Robô Tridente V.42 - Acesso Restrito")
    password = st.text_input("Digite a senha:", type="password")
    if st.button("Entrar"):
        if password == SENHA_ACESSO:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("Senha incorreta.")
    return False

# -------------------------
# CATALOGO E CONSTANTES (LÓGICA INALTERADA)
# -------------------------
ATIVO_CAIXA = 'B5P211.SA'

CATALOGO = {
    'IVVB11.SA': {'MM': 40, 'RSI_MAX': 70, 'DIST_MAX': 0.20, 'VOL_LIMIT': 0.4},
    'GOLD11.SA': {'MM': 16, 'RSI_MAX': 70, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.4},
    'B5P211.SA': {'MM': 4 , 'RSI_MAX': 75, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.4},
    'HASH11.SA': {'MM': 6 , 'RSI_MAX': 75, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.6},
    'PRIO3.SA':  {'MM': 52, 'RSI_MAX': 70, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.8},
    'BPAC11.SA': {'MM': 16, 'RSI_MAX': 75, 'DIST_MAX': 0.30, 'VOL_LIMIT': 0.4},
    'KEPL3.SA':  {'MM': 4 , 'RSI_MAX': 70, 'DIST_MAX': 0.15, 'VOL_LIMIT': 0.8},
    'PETR4.SA':  {'MM': 40, 'RSI_MAX': 70, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.6},
    'ELET3.SA':  {'MM': 6 , 'RSI_MAX': 70, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.6},
    'CYRE3.SA':  {'MM': 13, 'RSI_MAX': 70, 'DIST_MAX': 0.15, 'VOL_LIMIT': 0.4},
    'CPLE6.SA':  {'MM': 52, 'RSI_MAX': 70, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.4},
    'BBDC4.SA':  {'MM': 6 , 'RSI_MAX': 70, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.4},
    'CMIG4.SA':  {'MM': 52, 'RSI_MAX': 70, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.6},
    'ITUB4.SA':  {'MM': 4 , 'RSI_MAX': 70, 'DIST_MAX': 0.15, 'VOL_LIMIT': 0.4},
    'BBAS3.SA':  {'MM': 6 , 'RSI_MAX': 70, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.6},
    'B3SA3.SA':  {'MM': 10, 'RSI_MAX': 70, 'DIST_MAX': 0.15, 'VOL_LIMIT': 0.4},
    'WEGE3.SA':  {'MM': 20, 'RSI_MAX': 80, 'DIST_MAX': 0.15, 'VOL_LIMIT': 0.4},
    'VALE3.SA':  {'MM': 8 , 'RSI_MAX': 75, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.4},
    'USIM5.SA':  {'MM': 40, 'RSI_MAX': 70, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.4},
    'EZTC3.SA':  {'MM': 40, 'RSI_MAX': 70, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.4},
    'VBBR3.SA':  {'MM': 52, 'RSI_MAX': 70, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.4},
    'SMAL11.SA': {'MM': 13, 'RSI_MAX': 70, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.4},
    'MGLU3.SA':  {'MM': 4 , 'RSI_MAX': 70, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.4},
    'LREN3.SA':  {'MM': 8 , 'RSI_MAX': 80, 'DIST_MAX': 0.20, 'VOL_LIMIT': 0.4},
    'CSAN3.SA':  {'MM': 40, 'RSI_MAX': 70, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.4},
    'HAPV3.SA':  {'MM': 26, 'RSI_MAX': 70, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.4},
}

TICKERS = list(CATALOGO.keys())
DEFESA = ['IVVB11.SA', 'GOLD11.SA', 'B5P211.SA']
ATAQUE = [t for t in TICKERS if t not in DEFESA]

# -------------------------
# DOWNLOAD + CÁLCULOS (CACHEADO)
# -------------------------
@st.cache_data(ttl=3600)
def get_data_and_calculate():
    dias = (5 * 365)
    start = (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d')
    try:
        data = yf.download(TICKERS, start=start, interval='1wk', progress=False,
                           group_by='ticker', auto_adjust=True)
    except Exception:
        return pd.DataFrame()

    resultados = []
    for t in TICKERS:
        try:
            df = data[t].dropna()
            if len(df) < 52:
                continue

            close = df['Close']
            P = CATALOGO[t]

            atual = float(close.iloc[-1])
            sma = close.rolling(P['MM']).mean().iloc[-1]
            dist = (atual / sma) - 1
            vol = close.pct_change().std() * np.sqrt(52)
            roc = ((atual / float(close.iloc[-12])) - 1) * 100

            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            rsi_val = rsi.iloc[-1]

            if t in ATAQUE:
                safe_vol = vol if vol > 0.01 else 0.01
                score = roc / safe_vol
            else:
                safe_vol = vol if vol > 0.01 else 0.01
                score = 1 / safe_vol

            acao = "COMPRA"
            status = f"SCORE {score:.2f}"
            tipo = "⚔️ ATAQUE" if t in ATAQUE else "🛡️ DEFESA"

            if dist < 0:
                acao = "VENDA"
                status = f"ABAIXO DA MÉDIA (MM{P['MM']})"
            elif vol > P['VOL_LIMIT']:
                acao = "VENDA"
                status = f"RISCO ALTO (Vol {vol:.2f})"
            elif rsi_val > P['RSI_MAX']:
                acao = "NEUTRO"
                status = f"RSI ESTICADO ({rsi_val:.0f})"
            elif dist > P['DIST_MAX']:
                acao = "NEUTRO"
                status = f"PREÇO ESTICADO (+{dist:.1%})"
            elif t in ATAQUE and roc <= 0:
                acao = "NEUTRO"
                status = "SEM FORÇA (ROC < 0)"

            resultados.append({
                'Ticker': t,
                'Tipo': tipo,
                'Preco': atual,
                'Score': score,
                'Acao': acao,
                'Status': status
            })
        except Exception:
            continue
    return pd.DataFrame(resultados)

# -------------------------
# CSS / STYLING (visual premium)
# -------------------------
st.markdown("""
<style>
:root{
  --bg:#0b1020;
  --card:#0f1724;
  --accent:#0ea5a4;
  --muted:#94a3b8;
  --glass: rgba(255,255,255,0.03);
  --white:#e6eef8;
}
body { background: #081028; color: var(--white); }
.stApp { background: linear-gradient(180deg,#07102a 0%, #02111a 100%); }

/* Sidebar */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg,#071024,#08172b);
  color: var(--white);
  padding: 18px;
  border-right: 1px solid rgba(255,255,255,0.03);
}

/* Header */
.header-box {
  background: linear-gradient(90deg, rgba(14,165,164,0.12), rgba(59,130,246,0.08));
  border-radius: 14px;
  padding: 14px;
  margin-bottom: 12px;
  border: 1px solid rgba(255,255,255,0.04);
}
.header-title { font-size: 22px; font-weight:800; color: var(--white); }
.header-sub { color: var(--muted); margin-top:4px; }

/* Cards */
.card {
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border-radius: 12px;
  padding: 14px;
  margin-bottom: 12px;
  border: 1px solid rgba(255,255,255,0.04);
  box-shadow: 0 8px 30px rgba(2,6,23,0.55);
}
.card .title { font-weight:700; font-size:16px; color:var(--white); margin-bottom:8px; }

/* Small metrics */
.metric { font-size:18px; font-weight:700; color:var(--white); }
.subtle { color:var(--muted); font-size:13px; }

/* Monospace ASCII block */
.ascii {
  background: linear-gradient(180deg,#07122a,#03111a);
  padding:14px;
  border-radius:10px;
  font-family: "Courier New", Courier, monospace;
  color:#dbeafe;
  border:1px solid rgba(255,255,255,0.03);
  white-space: pre-wrap;
  overflow-x:auto;
}

/* Buttons */
.stButton>button {
  background: linear-gradient(90deg,#06b6d4,#3b82f6);
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  font-weight:700;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Função para montar ASCII guia (formatação igual ao original)
# -------------------------
def montar_ascii_guia(capital, df):
    hoje = datetime.now().strftime("%d/%m/%Y")
    top_line = "█" * 100
    total_tickers = len(TICKERS)
    last_ticker = TICKERS[-1] if TICKERS else ""
    checklist = [
        " 📝 CHECKLIST INICIAL:",
        "    1. Abra o app da sua corretora.",
        "    2. Veja quanto você tem de SALDO LIVRE + Valor das Ações do Robô (se já tiver).",
        "    3. Vamos calcular exatamente o que comprar (Lote Padrão vs Fracionário).",
        "",
        f" 👉 Digite seu PATRIMÔNIO TOTAL para a estratégia (R$): {capital:,.0f}",
        "",
        " 📡 O Robô está analisando os gráficos SEMANAIS...",
        f"    Processando {total_tickers}/{total_tickers}: {last_ticker}...",
        " ✅ Análise Completa.",
    ]

    vendas = df[df['Acao'] == 'VENDA'].sort_values("Ticker")
    compras_ataque = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == '⚔️ ATAQUE')].sort_values('Score', ascending=False)
    compras_defesa = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == '🛡️ DEFESA')].sort_values('Score', ascending=False)

    carteira_final = []
    carteira_final.extend(compras_ataque.head(3).to_dict("records"))
    vagas = 3 - len(carteira_final)
    if vagas > 0:
        carteira_final.extend(compras_defesa.head(vagas).to_dict("records"))

    # PASSO 1 lines
    vendas_lines = []
    if not vendas.empty:
        for _, row in vendas.iterrows():
            vendas_lines.append(f"      ❌ {row['Ticker']} -> Motivo: {row['Status']}")

    # RANK blocks
    invest_amount = capital / 3 if len(carteira_final) > 0 else 0
    ranks_blocks = []
    for i, ativo in enumerate(carteira_final, start=1):
        preco = ativo['Preco']
        qtd = int(invest_amount / preco) if preco > 0 else 0
        score = ativo.get('Score', 0.0)
        ranks_blocks.append(
            {
                "rank": i,
                "ticker": ativo['Ticker'],
                "tipo": ativo['Tipo'],
                "invest": invest_amount,
                "preco": preco,
                "qtd": qtd,
                "score": score,
                "motivo": ativo['Status']
            }
        )

    # build lines
    lines = []
    lines.append(top_line)
    lines.append(" 🔱 ROBÔ TRIDENTE V.42 | GUIA PASSO A PASSO (INICIANTE)")
    lines.append(top_line)
    lines.append("")
    lines.extend(checklist)
    lines.append("")
    lines.append("=" * 100)
    lines.append(f"📘 GUIA DE OPERAÇÃO PARA INICIANTES | {hoje}")
    lines.append("=" * 100)
    lines.append("")

    # PASSO 1
    lines.append("1️⃣  PASSO 1: FAZER CAIXA (VENDER)")
    lines.append("    Verifique sua carteira atual. Se você tiver algum destes ativos, VENDA TUDO.")
    lines.append("    (Use a opção 'Venda a Mercado' no seu Home Broker)")
    if vendas_lines:
        for vl in vendas_lines:
            lines.append(f"    {vl}")
    else:
        lines.append("    ✅ Nenhuma venda necessária hoje.")
    lines.append("    💵 O dinheiro dessas vendas será usado no Passo 2.")
    lines.append("-" * 100)

    # PASSO 2
    lines.append("2️⃣  PASSO 2: COMPRAR NOVOS ATIVOS")
    lines.append(f"    Vamos distribuir seus R$ {capital:,.2f} igualmente nos 3 melhores ativos.")
    lines.append("")

    if not ranks_blocks:
        lines.append(f"   ❌ Mercado ruim. Fique 100% no CAIXA ({ATIVO_CAIXA})")
    else:
        for b in ranks_blocks:
            lines.append("")
            lines.append("   " + "=" * 59)
            lines.append(f"   🏆 RANK #{b['rank']}: {b['ticker']} ({b['tipo']})")
            lines.append("   " + "=" * 59)
            lines.append(f"      💰 Valor para investir: R$ {b['invest']:,.2f}")
            lines.append(f"      📊 Preço Atual:         R$ {b['preco']:,.2f}")
            lines.append("      📝 COMO PREENCHER A ORDEM (BOLETA):")
            lines.append(f"      [2] Digite o código: {b['ticker'].replace('.SA','')}F (Com o 'F' no final)")
            lines.append(f"          Quantidade:      {b['qtd']}")
            lines.append(f"          Preço:           A Mercado")
            lines.append(f"          👉 CLIQUE EM COMPRAR")
            lines.append(f"      (Motivo da escolha: {b['motivo'] if b['motivo'] else f'SCORE {b['score']:.2f}'})")
            lines.append("")

    lines.append("=" * 100)
    lines.append("🚀 OPERAÇÃO CONCLUÍDA. FECHE O APP E SÓ VOLTE MÊS QUE VEM!")
    lines.append("=" * 100)
    lines.append("[Pressione ENTER para encerrar]")

    return "\n".join(lines), carteira_final

# -------------------------
# APP MAIN
# -------------------------
def main():
    if not check_password():
        return

    st.set_page_config(page_title="Robô Tridente V.42", page_icon="🔱", layout="wide")

    # SIDEBAR
    with st.sidebar:
        st.markdown("<div style='font-weight:800; font-size:18px; color:#e6eef8;'>💰 Sua Carteira</div>", unsafe_allow_html=True)
        capital = st.number_input("Patrimônio Total (R$)", min_value=0.0, value=2000.0, step=100.0)
        if st.button("🔄 Rodar Análise"):
            st.cache_data.clear()
            st.rerun()
        st.markdown("---")
        st.markdown("⚙️ Estratégia Otimizada V.31")
        st.markdown("🔒 Uso interno — Resultado não é recomendação de compra.")

    # DOWNLOAD + PROCESSAMENTO
    with st.spinner('📡 Conectando à Bolsa (B3)...'):
        df = get_data_and_calculate()

    if df.empty:
        st.error("Erro ao baixar dados. Tente novamente.")
        return

    # Monta ascii guia e carteira_final
    banner_text, carteira_final = montar_ascii_guia(capital, df)

    # LAYOUT: duas colunas — esquerda com cards resumo, direita com ASCII guia e detalhes
    col1, col2 = st.columns([1, 2], gap="medium")

    # Coluna esquerda — resumo e cards
    with col1:
        st.markdown("<div class='card'><div class='title'>📈 Resumo Rápido</div>", unsafe_allow_html=True)
        vendas = df[df['Acao'] == 'VENDA']
        n_vendas = len(vendas)
        n_compras = len(df[df['Acao'] == 'COMPRA'])
        st.markdown(f"<div class='metric'>🚨 Vendas: {n_vendas}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='subtle'>Ativos com indicação de venda</div>", unsafe_allow_html=True)
        st.markdown("<hr style='opacity:0.06'/>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric'>🟢 Compras: {n_compras}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='subtle'>Ativos com indicação de compra</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Cards detalhados para top 3
        st.markdown("<div class='card'><div class='title'>🏆 Top Picks</div>", unsafe_allow_html=True)
        top_picks = df[(df['Acao']=='COMPRA')].sort_values('Score', ascending=False).head(3).to_dict("records")
        if not top_picks:
            st.markdown("Nenhuma compra identificada no momento.", unsafe_allow_html=True)
        else:
            for i, p in enumerate(top_picks, start=1):
                preco = p['Preco']
                score = p['Score']
                st.markdown(f"**{i}. {p['Ticker']}** — {p['Tipo']}")
                st.markdown(f"- Preço: R$ {preco:.2f}  •  Score: {score:.2f}")
                st.markdown("<hr style='opacity:0.06'/>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Caixa - ativo de reserva
        st.markdown("<div class='card'><div class='title'>🛡️ Caixa/Defesa</div>", unsafe_allow_html=True)
        st.markdown(f"Ativo de Caixa sugerido: **{ATIVO_CAIXA}**", unsafe_allow_html=True)
        st.markdown("Use em mercados ruins para proteger capital.", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Coluna direita — ASCII guia + ações
    with col2:
        st.markdown("<div class='header-box'><div class='header-title'>🔱 ROBÔ TRIDENTE V.42</div><div class='header-sub'>Guia passo a passo - operacional</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='ascii'>{banner_text}</div>", unsafe_allow_html=True)

        # Mostrar os cards de compra de forma visual bonitinha após o ASCII
        if carteira_final:
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            st.markdown("<div class='card'><div class='title'>📋 Ordens sugeridas (Resumo)</div>", unsafe_allow_html=True)
            cols = st.columns(len(carteira_final))
            for i, ativo in enumerate(carteira_final):
                with cols[i]:
                    invest = capital / len(carteira_final)
                    preco = ativo['Preco']
                    qtd = int(invest / preco) if preco > 0 else 0
                    cod = ativo['Ticker'].replace('.SA','') + 'F'
                    st.markdown(f"**{ativo['Ticker']}**")
                    st.markdown(f"- Tipo: {ativo['Tipo']}")
                    st.markdown(f"- Valor p/ investir: R$ {invest:,.2f}")
                    st.markdown(f"- Preço atual: R$ {preco:.2f}")
                    st.markdown(f"- Quantidade: {qtd}")
                    st.markdown(f"- Código (boleta): **{cod}**")
                    st.button(f"✅ Confirmar {ativo['Ticker']}", key=f"confirm_{i}")
            st.markdown("</div>", unsafe_allow_html=True)

    # Expander com tabela detalhada
    with st.expander("🔍 Ver Detalhes Técnicos (Tabela Completa)"):
        styled = df.style.map(
            lambda x: ("color:#ff4b4b" if "VENDA" in str(x) else ("color:#4caf50" if "COMPRA" in str(x) else "color:#aaa")),
            subset=['Acao']
        )
        st.dataframe(styled, use_container_width=True)

    # Rodapé / Créditos
    st.markdown("""<div style="padding:8px; color:#94a3b8; margin-top:10px">⚙️ Lógica V.31 — cálculos idênticos ao backtest. Visual V.42 — atualizado por você.</div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
