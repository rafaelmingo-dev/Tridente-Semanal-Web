import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==============================================================================
# 🔐 SEGURANÇA
# ==============================================================================
SENHA_ACESSO = "tridente2025" 

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True
    
    st.markdown("## 🔐 Acesso Restrito V.38")
    password = st.text_input("Senha:", type="password")
    if st.button("Entrar"):
        if password == SENHA_ACESSO:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("Senha Incorreta")
    return False

# ==============================================================================
# ⚙️ LÓGICA V.31 (MATEMÁTICA PURA)
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

@st.cache_data(ttl=3600)
def get_data_and_calculate():
    dias = (5 * 365)
    start = (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d')
    try:
        data = yf.download(TICKERS, start=start, interval='1wk', progress=False, group_by='ticker', auto_adjust=True)
    except: return []

    resultados = []
    for t in TICKERS:
        try:
            df = data[t].dropna()
            if len(df) < 52: continue
            
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
            tipo = "ATAQUE" if t in ATAQUE else "DEFESA"
            
            if dist < 0: acao = "VENDA"; status = f"ABAIXO DA MÉDIA (MM{P['MM']})"
            elif vol > P['VOL_LIMIT']: acao = "VENDA"; status = f"RISCO ALTO (Vol {vol:.2f})"
            elif rsi_val > P['RSI_MAX']: acao = "NEUTRO"; status = f"RSI ESTICADO ({rsi_val:.0f})"
            elif dist > P['DIST_MAX']: acao = "NEUTRO"; status = f"PREÇO ESTICADO (+{dist:.1%})"
            elif t in ATAQUE and roc <= 0: acao = "NEUTRO"; status = "SEM FORÇA (ROC < 0)"
            
            resultados.append({
                'Ticker': t, 'Tipo': tipo, 'Preco': atual, 'Score': score,
                'Acao': acao, 'Status': status
            })
        except: continue
    return pd.DataFrame(resultados)

# ==============================================================================
# 🎨 UI
# ==============================================================================
def main():
    if not check_password(): return

    st.set_page_config(page_title="Robô Tridente V.38", page_icon="🔱", layout="wide")
    
    st.markdown("""
    <style>
    .main-header {font-size: 32px; font-weight: 800; color: #fff; text-align: center;}
    .sub-header {font-size: 14px; color: #888; text-align: center; margin-bottom: 20px;}
    
    /* Venda Card */
    .card-sell {
        background: #3a0000; border: 1px solid #ff4444; border-radius: 8px; padding: 15px; margin-bottom: 10px;
    }
    .sell-txt { color: #ff6666; font-size: 18px; font-weight: bold; margin: 0; }
    .sell-det { color: #fff; font-size: 13px; margin: 0; }

    /* Compra Card */
    .card-buy {
        background-color: #0e1117; border: 1px solid #2e7d32; border-radius: 12px; overflow: hidden; margin-bottom: 15px;
    }
    .buy-head {
        background-color: #1b5e20; padding: 10px 15px; display: flex; justify-content: space-between; align-items: center;
    }
    .buy-tit { color: #fff; font-size: 20px; font-weight: 900; margin: 0; }
    .buy-bdg { background: #000; color: #4caf50; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; }
    
    .buy-bod { padding: 15px; }
    .val-big { font-size: 24px; font-weight: 800; color: #4caf50; margin: 0; }
    .val-lbl { font-size: 11px; color: #aaa; text-transform: uppercase; margin: 0; }
    
    /* Boleta Clean */
    .boleta-wrap {
        background-color: #161b22; border-radius: 6px; padding: 10px; margin-top: 10px; border-left: 3px solid #4caf50;
    }
    .bol-row {
        display: flex; justify-content: space-between; border-bottom: 1px dashed #333; padding-bottom: 3px; margin-bottom: 3px;
    }
    .bol-row:last-child { border: none; margin: 0; padding: 0; }
    .bol-k { color: #888; font-size: 12px; }
    .bol-v { color: #fff; font-weight: bold; font-family: monospace; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-header'>🔱 ROBÔ TRIDENTE V.38</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Versão Definitiva</div>", unsafe_allow_html=True)

    with st.sidebar:
        st.header("💰 Carteira")
        capital = st.number_input("Patrimônio (R$)", min_value=0.0, value=2000.0, step=100.0)
        if st.button("🔄 Rodar"):
            st.cache_data.clear()
            st.rerun()
        st.info("Estratégia Equal Weight (33%)")

    with st.spinner('📡 Conectando...'):
        df = get_data_and_calculate()

    if df.empty:
        st.error("Erro na B3.")
        return

    vendas = df[df['Acao'] == 'VENDA']
    ataque = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == 'ATAQUE')].sort_values('Score', ascending=False)
    defesa = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == 'DEFESA')].sort_values('Score', ascending=False)

    final = []
    final.extend(ataque.head(3).to_dict('records'))
    vagas = 3 - len(final)
    if vagas > 0: final.extend(defesa.head(vagas).to_dict('records'))

    # VENDAS
    if not vendas.empty:
        st.markdown("### 1️⃣ VENDER")
        cols = st.columns(3)
        for idx, row in enumerate(vendas.to_dict('records')):
            with cols[idx % 3]:
                # HTML SEM IDENTAÇÃO PARA EVITAR ERRO
                st.markdown(f"<div class='card-sell'><p class='sell-txt'>❌ {row['Ticker']}</p><p class='sell-det'>Motivo: {row['Status']}</p></div>", unsafe_allow_html=True)
    else:
        st.success("Nenhuma venda necessária.")

    # COMPRAS
    st.markdown("---")
    st.markdown("### 2️⃣ COMPRAR")
    
    if not final:
        st.error(f"Fique 100% no CAIXA ({ATIVO_CAIXA}).")
    else:
        peso = 1.0 / len(final)
        cols = st.columns(len(final))
        
        for i, ativo in enumerate(final):
            with cols[i]:
                alo = capital * peso
                qtd = int(alo / ativo['Preco'])
                padrao = (qtd // 100) * 100
                frac = qtd % 100
                cod = ativo['Ticker'].replace('.SA', '')
                
                # HTML MONTOU EM LINHA ÚNICA
                html_items = ""
                if padrao > 0:
                    html_items += f"<div class='bol-row'><span class='bol-k'>Opção 1:</span><span class='bol-v'>{padrao} x {cod}</span></div>"
                if frac > 0:
                    lbl = "Opção 2:" if padrao > 0 else "Única:"
                    html_items += f"<div class='bol-row'><span class='bol-k'>{lbl}</span><span class='bol-v'>{frac} x {cod}F</span></div>"

                html_card = f"""
                <div class='card-buy'>
                    <div class='buy-head'>
                        <span class='buy-tit'>{ativo['Ticker']}</span>
                        <span class='buy-bdg'>{ativo['Tipo']}</span>
                    </div>
                    <div class='buy-bod'>
                        <p class='val-lbl'>INVESTIR</p>
                        <p class='val-big'>R$ {alo:,.0f}</p>
                        <div class='boleta-wrap'>
                            <div style='color:#4caf50;font-weight:bold;font-size:11px;margin-bottom:5px;'>NA CORRETORA</div>
                            {html_items}
                            <div style='margin-top:5px;font-size:10px;color:#666;text-align:center;'>{ativo['Status']}</div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(html_card, unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("🔍 Tabela Completa"):
        st.dataframe(df.style.map(lambda x: 'color:#f44' if 'VENDA' in str(x) else ('color:#4f4' if 'COMPRA' in str(x) else 'color:#aaa'), subset=['Acao']))

if __name__ == "__main__":
    main()
