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
    
    st.markdown("## 🔐 Acesso Restrito - Robô Tridente")
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
# 🎨 UI V.44 (HTML BLINDADO E CONCATENADO)
# ==============================================================================
def main():
    if not check_password(): return

    st.set_page_config(page_title="Robô Tridente V.44", page_icon="🔱", layout="wide")
    
    # CSS OTIMIZADO
    st.markdown("""
    <style>
    .stApp { background-color: #0b0c10; color: #fff; }
    h1, h2, h3 { color: #fff !important; }
    
    /* CARD VENDA */
    .card-sell {
        background: #2b0e0e; border: 1px solid #ff4444; border-radius: 8px; padding: 15px; margin-bottom: 10px;
    }
    .sell-tit { color: #ff6666; font-size: 18px; font-weight: bold; margin: 0; }
    .sell-sub { color: #fff; font-size: 13px; }

    /* CARD COMPRA */
    .card-buy {
        background-color: #12141c; border: 2px solid #00ff88; border-radius: 12px; margin-bottom: 20px; overflow: hidden;
    }
    .buy-head {
        background: #002e16; padding: 10px 15px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #00ff88;
    }
    .buy-tit { color: #fff; font-size: 22px; font-weight: 900; margin: 0; }
    .buy-bg { background: #000; color: #00ff88; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    
    .buy-body { padding: 15px; }
    .money-row { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 15px; }
    .money-val { font-size: 28px; font-weight: 800; color: #00ff88; line-height: 1; }
    .money-lbl { font-size: 11px; color: #aaa; text-transform: uppercase; }
    .money-prc { font-size: 14px; color: #fff; text-align: right; }

    /* BOLETA TABLE STYLE */
    .boleta-box {
        background-color: #000; border: 1px solid #333; border-radius: 6px; padding: 10px; border-left: 4px solid #00ff88;
    }
    .boleta-tit { color: #58a6ff; font-size: 12px; font-weight: bold; margin-bottom: 5px; border-bottom: 1px solid #333; padding-bottom: 5px; }
    .bol-row { display: flex; justify-content: space-between; margin-bottom: 4px; font-size: 13px; color: #ddd; }
    .bol-val { color: #fff; font-weight: bold; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

    st.title("🔱 ROBÔ TRIDENTE V.44")
    st.markdown("#### Painel Profissional | Equal Weight (33%)")

    with st.sidebar:
        st.header("💰 Carteira")
        capital = st.number_input("Patrimônio (R$)", min_value=0.0, value=2000.0, step=100.0)
        if st.button("🔄 Rodar"):
            st.cache_data.clear()
            st.rerun()
        st.info("Estratégia V.31 Otimizada")

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

    # VENDAS
    if not vendas.empty:
        st.subheader("1️⃣ VENDAS")
        cols = st.columns(3)
        for idx, row in enumerate(vendas.to_dict('records')):
            with cols[idx % 3]:
                # HTML CONCATENADO PARA NAO QUEBRAR
                html = ""
                html += f"<div class='card-sell'>"
                html += f"<div class='sell-tit'>❌ {row['Ticker']}</div>"
                html += f"<div class='sell-sub'>Ref: R$ {row['Preco']:.2f}</div>"
                html += f"<div class='sell-sub' style='color:#ffaaaa'>{row['Status']}</div>"
                html += f"</div>"
                st.markdown(html, unsafe_allow_html=True)
    else:
        st.success("✅ Nenhuma venda necessária.")

    st.markdown("---")

    # COMPRAS
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
                
                # MONTAGEM SEGURA DO HTML (SEM IDENTAÇÃO INTERNA)
                html = ""
                html += f"<div class='card-buy'>"
                html += f"<div class='buy-head'>"
                html += f"<span class='buy-tit'>{ativo['Ticker']}</span>"
                html += f"<span class='buy-bg'>RANK #{i+1}</span>"
                html += f"</div>"
                
                html += f"<div class='buy-body'>"
                html += f"<div class='money-row'>"
                html += f"<div><div class='money-lbl'>INVESTIR</div><div class='money-val'>R$ {alo:,.0f}</div></div>"
                html += f"<div class='money-prc'>Preço<br>R$ {ativo['Preco']:.2f}</div>"
                html += f"</div>"
                
                html += f"<div class='boleta-box'>"
                html += f"<div class='boleta-tit'>📝 NA CORRETORA</div>"
                
                if padrao > 0:
                    html += f"<div class='bol-row'><span>Opção 1 (Lote):</span><span class='bol-val'>Comprar {padrao} x {cod}</span></div>"
                
                if frac > 0:
                    lbl = "Opção 2 (Sobra):" if padrao > 0 else "Opção Única:"
                    html += f"<div class='bol-row'><span>{lbl}</span><span class='bol-val'>Comprar {frac} x {cod}F</span></div>"
                
                html += f"<div style='border-top:1px dashed #333; margin-top:5px; padding-top:5px; text-align:center; font-size:12px; color:#666;'>Ordem a Mercado</div>"
                html += f"</div>" # fecha boleta
                
                html += f"<div style='text-align:center; margin-top:10px; font-size:11px; color:#888;'>Motivo: {ativo['Status']}</div>"
                html += f"</div>" # fecha body
                html += f"</div>" # fecha card

                st.markdown(html, unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("🔍 Espião (Tabela Completa)"):
        st.dataframe(df.style.map(lambda x: 'color:#ff4444' if 'VENDA' in str(x) else ('color:#00ff88' if 'COMPRA' in str(x) else 'color:#888'), subset=['Acao']))

if __name__ == "__main__":
    main()
