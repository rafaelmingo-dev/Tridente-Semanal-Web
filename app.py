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
    
    st.markdown("## 🔐 Acesso Restrito - V.43")
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
# 🎨 UI V.43 (DESIGN ALTO CONTRASTE E LEGIBILIDADE)
# ==============================================================================
def main():
    if not check_password(): return

    st.set_page_config(page_title="Robô Tridente V.43", page_icon="🔱", layout="wide")
    
    # CSS CORRIGIDO PARA VISIBILIDADE
    st.markdown("""
    <style>
    /* FUNDO */
    .stApp { background-color: #0b0c10; }
    
    /* CARD VENDA (VERMELHO VIVO) */
    .card-sell {
        background: #2c0b0b;
        border: 2px solid #ff0000;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .sell-tit { color: #ff4d4d; font-size: 20px; font-weight: 900; }
    .sell-sub { color: #ffffff; font-size: 14px; margin-top: 5px; }
    .sell-bg  { background: #500000; color: #ffcccc; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }

    /* CARD COMPRA (VERDE NEON + CINZA LEGÍVEL) */
    .card-buy {
        background-color: #1c1e26; /* Cinza chumbo claro para contraste */
        border: 2px solid #00ff88; /* Borda Verde Neon */
        border-radius: 15px;
        overflow: hidden;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,255,136,0.15);
    }
    .buy-head {
        background: linear-gradient(90deg, #004d26 0%, #002e16 100%);
        padding: 15px 20px;
        display: flex; justify-content: space-between; align-items: center;
        border-bottom: 1px solid #00ff88;
    }
    .buy-tit { color: #ffffff; font-size: 26px; font-weight: 900; text-shadow: 0 2px 4px rgba(0,0,0,0.5); }
    .buy-rnk { color: #00ff88; font-size: 12px; font-weight: bold; letter-spacing: 1px; border: 1px solid #00ff88; padding: 3px 8px; border-radius: 4px; }
    
    .buy-body { padding: 20px; }
    
    /* VALORES */
    .val-row { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 20px; }
    .val-big { font-size: 32px; font-weight: 800; color: #00ff88; line-height: 1; }
    .val-lbl { font-size: 12px; color: #cccccc; text-transform: uppercase; margin-bottom: 5px; font-weight: bold; }
    .val-prc { font-size: 16px; color: #ffffff; font-weight: bold; text-align: right; }

    /* BOLETA BOX (CONTRASTE MÁXIMO) */
    .boleta {
        background-color: #000000; /* Fundo Preto Puro */
        border: 1px solid #444;
        border-radius: 8px;
        padding: 15px;
    }
    .bol-head { color: #58a6ff; font-size: 12px; font-weight: bold; margin-bottom: 10px; text-transform: uppercase; border-bottom: 1px solid #333; padding-bottom: 5px; }
    
    .bol-row { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 14px; border-bottom: 1px dashed #333; padding-bottom: 4px; }
    .bol-row:last-child { border: none; }
    .bol-k { color: #aaaaaa; } /* Cinza claro */
    .bol-v { color: #ffffff; font-weight: bold; font-family: monospace; font-size: 15px; } /* Branco Puro */
    
    .motivo { text-align: center; margin-top: 15px; font-size: 12px; color: #888; }
    </style>
    """, unsafe_allow_html=True)

    st.title("🔱 ROBÔ TRIDENTE V.43")
    st.markdown("#### Painel Profissional | Alto Contraste")

    with st.sidebar:
        st.header("💰 Carteira")
        capital = st.number_input("Patrimônio Total (R$)", min_value=0.0, value=2000.0, step=100.0)
        if st.button("🔄 Rodar Análise"):
            st.cache_data.clear()
            st.rerun()
        st.info("Estratégia Equal Weight (33%)")

    with st.spinner('📡 Analisando...'):
        df = get_data_and_calculate()

    if df.empty:
        st.error("Erro na conexão.")
        return

    vendas = df[df['Acao'] == 'VENDA']
    ataque = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == 'ATAQUE')].sort_values('Score', ascending=False)
    defesa = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == 'DEFESA')].sort_values('Score', ascending=False)

    final = []
    final.extend(ataque.head(3).to_dict('records'))
    vagas = 3 - len(final)
    if vagas > 0: final.extend(defesa.head(vagas).to_dict('records'))

    # 1. VENDAS
    if not vendas.empty:
        st.subheader("1️⃣ VENDAS NECESSÁRIAS")
        cols = st.columns(3)
        for idx, row in enumerate(vendas.to_dict('records')):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="card-sell">
                    <div class="sell-tit">❌ {row['Ticker']}</div>
                    <div class="sell-sub">Ref: <b>R$ {row['Preco']:.2f}</b></div>
                    <div style="margin-top:8px"><span class="sell-bg">{row['Status']}</span></div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.success("✅ Nenhuma venda necessária.")

    st.markdown("---")

    # 2. COMPRAS
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
                
                # HTML BOLETA
                html_bol = ""
                if padrao > 0:
                    html_bol += f"""
                    <div class="bol-row">
                        <span class="bol-k">Opção 1 (Lote):</span>
                        <span class="bol-v">{padrao} x {cod}</span>
                    </div>
                    """
                if frac > 0:
                    lbl = "Opção 2 (Sobra):" if padrao > 0 else "Opção Única:"
                    html_bol += f"""
                    <div class="bol-row">
                        <span class="bol-k">{lbl}</span>
                        <span class="bol-v">{frac} x {cod}F</span>
                    </div>
                    """

                st.markdown(f"""
                <div class="card-buy">
                    <div class="buy-head">
                        <span class="buy-tit">{ativo['Ticker']}</span>
                        <span class="buy-rnk">RANK #{i+1}</span>
                    </div>
                    <div class="buy-body">
                        <div class="val-row">
                            <div>
                                <div class="val-lbl">Investir</div>
                                <div class="val-big">R$ {alo:,.0f}</div>
                            </div>
                            <div style="text-align:right">
                                <div class="val-lbl">Preço</div>
                                <div class="val-prc">R$ {ativo['Preco']:.2f}</div>
                            </div>
                        </div>
                        
                        <div class="boleta">
                            <div class="bol-head">📝 NA CORRETORA</div>
                            {html_bol}
                            <div class="bol-row" style="margin-top:8px; border-top:1px solid #333; padding-top:5px;">
                                <span class="bol-k">Preço Limite:</span>
                                <span class="bol-v" style="color:#00ff88">A Mercado</span>
                            </div>
                        </div>
                        
                        <div class="motivo">Motivo: {ativo['Status']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("🔍 Espião (Tabela Completa)"):
        st.dataframe(df.style.map(lambda x: 'color:#ff4444' if 'VENDA' in str(x) else ('color:#00ff88' if 'COMPRA' in str(x) else 'color:#888'), subset=['Acao']))

if __name__ == "__main__":
    main()
