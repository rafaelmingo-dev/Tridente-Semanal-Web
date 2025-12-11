import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==============================================================================
# 🔐 SEGURANÇA (LOGIN)
# ==============================================================================
SENHA_ACESSO = "tridente2025"

def check_password():
    """Retorna True se o usuário estiver logado."""
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

# ==============================================================================
# ⚙️ LÓGICA V.31 (MATEMÁTICA PURA) - INTACTA
# ==============================================================================
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

# ==============================================================================
# 📡 DOWNLOAD + CÁLCULOS TÉCNICOS V.31
# ==============================================================================
@st.cache_data(ttl=3600)
def get_data_and_calculate():
    dias = (5 * 365)
    start = (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d')
    try:
        data = yf.download(TICKERS, start=start, interval='1wk', progress=False,
                           group_by='ticker', auto_adjust=True)
    except:
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
                safe_vol = max(vol, 0.01)
                score = roc / safe_vol
            else:
                safe_vol = max(vol, 0.01)
                score = 1 / safe_vol

            # REGRAS V.31
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

        except:
            continue

    return pd.DataFrame(resultados)

# ==============================================================================
# 🎨 INTERFACE VISUAL — GUIA OPERACIONAL
# ==============================================================================
def main():

    if not check_password():
        return

    st.set_page_config(page_title="Robô Tridente V.42", page_icon="🔱", layout="wide")

    with st.sidebar:
        st.header("💰 Sua Carteira")
        capital = st.number_input("Patrimônio Total (R$)", min_value=0.0,
                                  value=2000.0, step=100.0)
        if st.button("🔄 Rodar Análise"):
            st.cache_data.clear()
            st.rerun()

    with st.spinner("📡 Conectando à Bolsa (B3)..."):
        df = get_data_and_calculate()

    if df.empty:
        st.error("Erro ao baixar dados. Tente novamente.")
        return

    # ================================
    # SEPARAÇÃO — (LÓGICA INALTERADA)
    # ================================
    vendas = df[df['Acao'] == 'VENDA'].sort_values("Ticker")
    compras_ataque = df[(df['Acao'] == 'COMPRA') &
                        (df['Tipo'] == '⚔️ ATAQUE')].sort_values('Score', ascending=False)
    compras_defesa = df[(df['Acao'] == 'COMPRA') &
                        (df['Tipo'] == '🛡️ DEFESA')].sort_values('Score', ascending=False)

    carteira_final = []
    carteira_final.extend(compras_ataque.head(3).to_dict("records"))
    vagas = 3 - len(carteira_final)
    if vagas > 0:
        carteira_final.extend(compras_defesa.head(vagas).to_dict("records"))

    hoje = datetime.now().strftime("%d/%m/%Y")

    # ================================
    # GUIA OPERACIONAL — VISUAL NOVO
    # ================================
    st.markdown(f"# 📘 GUIA DE OPERAÇÃO PARA INICIANTES | {hoje}")
    st.markdown("---")

    # =====================================
    # 1️⃣ PASSO 1 — FAZER CAIXA (VENDAS)
    # =====================================
    st.markdown("### 1️⃣ PASSO 1: FAZER CAIXA (VENDER)")

    if vendas.empty:
        st.success("Nenhum ativo precisa ser vendido hoje! ✔️")
    else:
        st.write("Verifique sua carteira. Se possuir algum destes ativos, **venda tudo hoje**:")

        for idx, row in vendas.iterrows():
            st.markdown(f"**❌ {row['Ticker']}** — Motivo: **{row['Status']}**")

        st.info("💵 O dinheiro destas vendas será usado no Passo 2.")

    st.markdown("---")

    # =====================================
    # 2️⃣ PASSO 2 — COMPRAR ATIVOS
    # =====================================
    st.markdown("### 2️⃣ PASSO 2: COMPRAR NOVOS ATIVOS")

    if not carteira_final:
        st.error(f"Mercado ruim. Fique 100% no CAIXA ({ATIVO_CAIXA}).")
    else:
        peso = 1 / len(carteira_final)

        for i, ativo in enumerate(carteira_final, start=1):
            alo = capital * peso
            preco = ativo["Preco"]
            qtd_total = int(alo / preco)
            cod = ativo["Ticker"].replace(".SA", "")

            st.markdown("---")
            st.markdown(f"## 🏆 RANK #{i}: {ativo['Ticker']} ({ativo['Tipo']})")

            st.markdown(f"""
            **💰 Valor para investir:** R$ {alo:,.2f}  
            **📊 Preço Atual:** R$ {preco:.2f}  
            """)

            st.markdown("### 📝 COMO PREENCHER A ORDEM (BOLETA):")
            st.markdown(f"""
            - Digite o código: **{cod}F**  
            - Quantidade: **{qtd_total}**  
            - Preço: **A Mercado**  
            - 👉 Clique em **COMPRAR**
            """)

            st.caption(f"Motivo da escolha: **{ativo['Status']}**")

    st.markdown("---")

    # =====================================
    # 3️⃣ DETALHES TÉCNICOS (ESPIÃO)
    # =====================================
    with st.expander("🔍 Ver Detalhes Técnicos (Tabela Completa)"):
        st.dataframe(
            df.style.map(
                lambda x: ("color:#ff4b4b" if "VENDA" in str(x)
                           else ("color:#4caf50" if "COMPRA" in str(x)
                                 else "color:#aaa")),
                subset=['Acao']
            ),
            use_container_width=True
        )


if __name__ == "__main__":
    main()
