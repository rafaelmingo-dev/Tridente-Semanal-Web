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
    
    st.markdown("## 🔐 Robô Tridente V.36")
    password = st.text_input("Senha:", type="password")
    if st.button("Entrar"):
        if password == SENHA_ACESSO:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("Senha incorreta.")
    return False

# ==============================================================================
# ⚙️ LÓGICA V.31 (MATEMÁTICA PURA - NÃO ALTERAR)
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
    # Cálculo V.31 Exato
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
# 🎨 UI PROFISSIONAL (CSS CORRIGIDO)
# ==============================================================================
def main():
    if not check_password(): return

    st.set_page_config(page_title="Robô Tridente V.36", page_icon="🔱", layout="wide")
    
    # CSS BLINDADO (Evita vazar código)
    st.markdown("""
    <style>
    .main-title { font-size: 32px; color: #fff; text-align: center; font-weight: 800; margin-bottom: 10px; }
    .sub-title { font-size: 16px; color: #aaa; text-align: center; margin-bottom: 30px; }
    
    /* CARD VENDA */
    .sell-card {
        background: linear-gradient(135deg, #3a0000 0%, #1a0000 100%);
        border: 1px solid #ff4444; border-radius: 12px; padding: 20px; margin-bottom: 15px;
    }
    .sell-head { color: #ff6666; font-size: 20px; font-weight: bold; }
    .sell-sub { color: #fff; font-size: 14px; margin-top: 5px; }
    .sell-bad { color: #ffaaaa; font-size: 12px; background: rgba(255,0,0,0.2); padding: 2px 6px; border-radius: 4px; }

    /* CARD COMPRA */
    .buy-card {
        background-color: #0e1117; border: 1px solid #2e7d32; border-radius: 15px; overflow: hidden; margin-bottom: 20px;
    }
    .buy-top {
        background: #1b5e20; padding: 15px; display: flex; justify-content: space-between; align-items: center;
    }
    .buy-name { color: #fff; font-size: 22px; font-weight: 900; margin: 0; }
    .buy-type { background: #000; color: #4caf50; padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: bold; }
    
    .buy-content { padding: 20px; }
    .money-row { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 20px; }
    .money-big { color: #4caf50; font-size: 28px; font-weight: 800; line-height: 1; }
    .money-small { color: #aaa; font-size: 12px; text-transform: uppercase; }
    
    /* BOLETA BOX */
    .boleta { background: #161b22; border-radius: 8px; padding: 15px; border-left: 4px solid #4caf50; }
    .bol-row { display: flex; justify-content: space-between; margin-bottom: 8px; border-bottom: 1px dashed #333; padding-bottom: 4px; }
    .bol-row:last-child { border: none; }
    .bol-lbl { color: #888; font-size: 13px; }
    .bol-val { color: #fff; font-weight: bold; font-family: monospace; font-size: 14px; }
    
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-title'>🔱 ROBÔ TRIDENTE V.36</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Sistema de Execução Profissional</div>", unsafe_allow_html=True)

    with st.sidebar:
        st.header("💰 Carteira")
        capital = st.number_input("Patrimônio Total (R$)", min_value=0.0, value=2000.0, step=100.0)
        if st.button("🔄 Rodar Análise"):
            st.cache_data.clear()
            st.rerun()
        st.info("Estratégia Equal Weight (33%).")

    with st.spinner('📡 Analisando...'):
        df = get_data_and_calculate()

    if df.empty:
        st.error("Erro ao baixar dados.")
        return

    vendas = df[df['Acao'] == 'VENDA']
    compras_ataque = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == 'ATAQUE')].sort_values('Score', ascending=False)
    compras_defesa = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == 'DEFESA')].sort_values('Score', ascending=False)

    carteira_final = []
    carteira_final.extend(compras_ataque.head(3).to_dict('records'))
    vagas = 3 - len(carteira_final)
    if vagas > 0: carteira_final.extend(compras_defesa.head(vagas).to_dict('records'))

    # 1. VENDAS
    st.markdown("### 1️⃣ ALERTAS DE VENDA")
    if not vendas.empty:
        cols = st.columns(3)
        for idx, row in enumerate(vendas.to_dict('records')):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class='sell-card'>
                    <div class='sell-head'>❌ {row['Ticker']}</div>
                    <div class='sell-sub'>Ref: R$ {row['Preco']:.2f}</div>
                    <div class='sell-bad'>{row['Status']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.success("Nenhuma venda necessária.")

    # 2. COMPRAS
    st.markdown("---")
    st.markdown("### 2️⃣ NOVAS COMPRAS")
    
    if not carteira_final:
        st.error(f"Mercado Ruim. Fique 100% no CAIXA ({ATIVO_CAIXA}).")
    else:
        peso = 1.0 / len(carteira_final)
        cols = st.columns(len(carteira_final))
        
        for i, ativo in enumerate(carteira_final):
            with cols[i]:
                alocacao = capital * peso
                qtd_total = int(alocacao / ativo['Preco'])
                
                # Cálculos
                lotes = qtd_total // 100
                padrao = lotes * 100
                frac = qtd_total % 100
                cod = ativo['Ticker'].replace('.SA', '')
                
                # Montagem HTML Limpa
                html_boleta = ""
                
                if padrao > 0:
                    html_boleta += f"""
                    <div class='bol-row'>
                        <span class='bol-lbl'>Opção 1 (Lote):</span>
                        <span class='bol-val'>{padrao} x {cod}</span>
                    </div>
                    """
                
                if frac > 0:
                    lbl = "Opção 2 (Resto):" if padrao > 0 else "Opção Única:"
                    html_boleta += f"""
                    <div class='bol-row'>
                        <span class='bol-lbl'>{lbl}</span>
                        <span class='bol-val'>{frac} x {cod}F</span>
                    </div>
                    """

                st.markdown(f"""
                <div class='buy-card'>
                    <div class='buy-top'>
                        <div class='buy-name'>{ativo['Ticker']}</div>
                        <div class='buy-type'>{ativo['Tipo']}</div>
                    </div>
                    <div class='buy-content'>
                        <div class='money-row'>
                            <div>
                                <div class='money-small'>Investir</div>
                                <div class='money-big'>R$ {alocacao:,.0f}</div>
                            </div>
                            <div style='text-align:right'>
                                <div class='money-small'>Preço</div>
                                <div style='color:white; font-weight:bold'>R$ {ativo['Preco']:.2f}</div>
                            </div>
                        </div>
                        
                        <div class='boleta'>
                            <div style='color:#4caf50; font-weight:bold; font-size:12px; margin-bottom:10px;'>📝 ORDEM NA CORRETORA</div>
                            {html_boleta}
                            <div style='margin-top:10px; text-align:center; font-size:11px; color:#666;'>
                                Motivo: {ativo['Status']}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("🔍 Espião (Tabela Técnica)"):
        st.dataframe(df.style.map(lambda x: 'color:#ff4b4b' if 'VENDA' in str(x) else ('color:#4caf50' if 'COMPRA' in str(x) else 'color:#aaa'), subset=['Acao']))

if __name__ == "__main__":
    main()
