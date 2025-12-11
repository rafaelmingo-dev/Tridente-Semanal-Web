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
    
    st.markdown("## 🔐 TRIDENTE - Acesso Restrito")
    password = st.text_input("Senha:", type="password")
    if st.button("Entrar"):
        if password == SENHA_ACESSO:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("Senha Incorreta")
    return False

# ==============================================================================
# ⚙️ LÓGICA V.31 (MATEMÁTICA PURA) - INALTERADA
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
            tipo = "⚔️ ATAQUE" if t in ATAQUE else "🛡️ DEFESA"
            
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
# 🎨 UI V.47 (TERMINAL VISUAL + ALTO CONTRASTE)
# ==============================================================================
def main():
    if not check_password(): return

    st.set_page_config(page_title="Robô Tridente V.47", page_icon="🔱", layout="wide")
    
    # CSS para Styling
    st.markdown("""
    <style>
    .stApp { background-color: #0b0c10; color: #fff; }
    h1, h2, h3, h4 { color: #fff !important; }
    
    /* CABEÇALHO CENTRALIZADO */
    .header-box { text-align: center; margin-bottom: 25px; }
    .header-title { font-size: 36px; font-weight: 900; color: #fff; margin:0; }
    
    /* CARD GERAL */
    .card-base {
        background-color: #12141c; border: 1px solid #333; border-radius: 12px; padding: 15px; margin-bottom: 20px;
    }
    .card-title { font-size: 20px; font-weight: bold; color: #00ff88; margin-bottom: 10px; }
    
    /* VALORES DETALHADOS */
    .detail-row { display: flex; justify-content: space-between; margin-bottom: 8px; }
    .detail-key { color: #888; font-size: 14px; }
    .detail-val { color: #fff; font-weight: bold; font-size: 14px; }
    
    /* BOLETA TERMINAL STYLE */
    .boleta-term {
        background-color: #000; border: 1px solid #333; border-radius: 6px; padding: 10px; margin-top: 10px;
        font-family: 'Courier New', monospace; color: #fff;
    }
    .boleta-tit { color: #58a6ff; font-weight: bold; font-size: 13px; margin-bottom: 5px; }
    .boleta-code { color: #00ff88; font-weight: bold; }
    .boleta-quant { color: #ffad57; font-weight: bold; }
    .boleta-market { color: #58a6ff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

    # CABEÇALHO
    st.markdown("<div class='header-box'><div class='header-title'>🔱 TRIDENTE V.47</div></div>", unsafe_allow_html=True)

    # SIDEBAR
    with st.sidebar:
        st.header("💰 Carteira")
        capital = st.number_input("Patrimônio (R$)", min_value=0.0, value=2000.0, step=100.0)
        if st.button("🔄 Rodar"):
            st.cache_data.clear()
            st.rerun()
        st.info("Estratégia Equal Weight (33%).")

    with st.spinner('📡 Analisando...'):
        df = get_data_and_calculate()

    if df.empty:
        st.error("Erro Conexão B3.")
        return

    vendas = df[df['Acao'] == 'VENDA']
    ataque = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == 'ATAQUE')].sort_values('Score', ascending=False)
    defesa = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == 'DEFESA')].sort_values('Score', ascending=False)

    final = []
    final.extend(ataque.head(3).to_dict('records'))
    vagas = 3 - len(final)
    if vagas > 0: final.extend(defesa.head(vagas).to_dict('records'))

    # ==========================================================================
    # 1. VENDAS (PASSO A PASSO)
    # ==========================================================================
    st.markdown("## 1️⃣ FAZER CAIXA (VENDER)")
    if not vendas.empty:
        st.warning("⚠️ Venda estes ativos para liberar caixa.")
        
        cols = st.columns(3)
        for idx, row in enumerate(vendas.to_dict('records')):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class='card-base' style='border-color:#ff4444;'>
                    <div class='sell-tit'>❌ {row['Ticker']}</div>
                    <div class='sell-sub'>Motivo: {row['Status']}</div>
                    <div class='sell-sub'>Preço Ref: R$ {row['Preco']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.success("✅ Nenhuma venda necessária.")

    st.markdown("---")

    # ==========================================================================
    # 2. COMPRAS (VISUAL PERFEITO + PASSO A PASSO)
    # ==========================================================================
    st.subheader("2️⃣ NOVAS COMPRAS")
    
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
                
                # Montagem do Bloco de Instrução Terminal-Like
                boleta_content = ""
                
                if padrao > 0:
                    boleta_content += f"<p class='boleta-row'><span class='boleta-key'>1. Lote Padrão:</span><span class='boleta-val'>{padrao} x {cod}</span></p>"
                
                if frac > 0:
                    lbl = "Opção 2 (Sobra):" if padrao > 0 else "Opção Única:"
                    boleta_content += f"<p class='boleta-row'><span class='boleta-key'>{lbl}:</span><span class='boleta-val'>{frac} x {cod}F</span></p>"

                # CARD DE COMPRA
                st.markdown(f"""
                <div class="card-buy">
                    <div class="buy-head">
                        <span class="buy-ticker">{ativo['Ticker']}</span>
                        <span class="buy-badge">RANK #{i+1}</span>
                    </div>
                    <div class="buy-content">
                        <div class="money-row">
                            <div>
                                <div class="val-lbl">INVESTIR</div>
                                <div class="val-big">R$ {alo:,.0f}</div>
                            </div>
                            <div style="text-align:right">
                                <div class="val-lbl">PREÇO REF</div>
                                <div class="val-prc">R$ {ativo['Preco']:.2f}</div>
                            </div>
                        </div>
                        
                        <div class="boleta-box">
                            <div class="boleta-tit">📝 INSTRUÇÕES DE BOLETA:</div>
                            {boleta_content}
                            <hr style="border-color:#333;">
                            <p style="text-align:center; margin:0; color:#00ff88; font-weight:bold;">COMPRAR A MERCADO</p>
                        </div>
                        <p style="text-align:center; font-size:12px; color:#888; margin-top:8px;">Motivo: {ativo['Status']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # 3. TABELA
    st.markdown("---")
    with st.expander("🔍 Espião (Tabela Completa)"):
        st.dataframe(df.style.map(lambda x: 'color:#ff4444' if 'VENDA' in str(x) else ('color:#00ff88' if 'COMPRA' in str(x) else 'color:#aaa'), subset=['Acao']))

if __name__ == "__main__":
    main()
