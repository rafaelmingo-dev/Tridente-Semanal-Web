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
    
    st.markdown("## 🔐 Robô Tridente V.40")
    password = st.text_input("Senha:", type="password")
    if st.button("Entrar"):
        if password == SENHA_ACESSO:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("Senha Incorreta")
    return False

# ==============================================================================
# ⚙️ LÓGICA V.31 (MATEMÁTICA INTACTA)
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
            
            # --- CÁLCULOS IDÊNTICOS AO BACKTEST V.31 ---
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

            # JULGAMENTO (REGRAS V.31)
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
# 🎨 INTERFACE VISUAL V.40 (PROFISSIONAL + HTML BLINDADO)
# ==============================================================================
def main():
    if not check_password(): return

    st.set_page_config(page_title="Robô Tridente V.40", page_icon="🔱", layout="wide")
    
    # CSS: ESTILO DARK MODERN (Sem quebras)
    st.markdown("""
    <style>
    /* FUNDO E TEXTO */
    .stApp { background-color: #0e1117; }
    h1, h2, h3 { color: #fff !important; }
    
    /* CABEÇALHO */
    .main-header { 
        text-align: center; padding: 20px; 
        background: linear-gradient(90deg, #0e1117 0%, #161b22 100%);
        border-bottom: 1px solid #30363d; margin-bottom: 20px;
    }
    .header-title { font-size: 40px; font-weight: 800; background: -webkit-linear-gradient(#eee, #999); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin:0; }
    .header-sub { font-size: 16px; color: #666; margin-top: 5px; text-transform: uppercase; letter-spacing: 2px; }

    /* CARD DE VENDA (VERMELHO) */
    .sell-card {
        background-color: #2b0e0e; border: 1px solid #8a2be2; /* Borda roxa sutil para diferenciar */
        border: 1px solid #ff4444; border-radius: 8px; padding: 15px; margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .sell-ticker { font-size: 20px; font-weight: bold; color: #ff6666; display: flex; justify-content: space-between; }
    .sell-detail { font-size: 13px; color: #ccc; margin-top: 5px; }
    .sell-tag { background: #5c0000; padding: 2px 6px; border-radius: 4px; font-size: 11px; color: #ffaaaa; }

    /* CARD DE COMPRA (VERDE PROFISSIONAL) */
    .buy-card {
        background-color: #12141c; border: 1px solid #238636; border-radius: 12px; overflow: hidden; margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
    }
    .buy-header {
        background: #181c26; padding: 12px 15px; border-bottom: 1px solid #30363d;
        display: flex; justify-content: space-between; align-items: center;
    }
    .buy-ticker { font-size: 22px; font-weight: 900; color: #fff; margin:0; }
    .buy-type { font-size: 11px; font-weight: bold; color: #2ea043; border: 1px solid #2ea043; padding: 2px 8px; border-radius: 20px; }
    
    .buy-content { padding: 15px; }
    
    /* DINHEIRO */
    .money-section { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 15px; }
    .money-label { font-size: 11px; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; }
    .money-value { font-size: 28px; font-weight: 700; color: #3fb950; line-height: 1; }
    .price-ref { font-size: 14px; color: #c9d1d9; text-align: right; }

    /* BOLETA BOX (O Passo a Passo) */
    .boleta-box {
        background-color: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 12px;
    }
    .boleta-title { font-size: 12px; font-weight: bold; color: #58a6ff; margin-bottom: 8px; text-transform: uppercase; border-bottom: 1px solid #30363d; padding-bottom: 5px; }
    .boleta-row { display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 13px; }
    .boleta-key { color: #8b949e; }
    .boleta-val { color: #f0f6fc; font-family: 'Courier New', monospace; font-weight: bold; }
    
    .status-footer { margin-top: 10px; font-size: 11px; color: #484f58; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

    # LAYOUT PRINCIPAL
    st.markdown("""
    <div class="main-header">
        <p class="header-title">🔱 ROBÔ TRIDENTE V.40</p>
        <p class="header-sub">Painel de Execução Profissional | Equal Weight (33%)</p>
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.header("💰 Sua Carteira")
        st.write("Digite o valor total (Saldo + Ações):")
        capital = st.number_input("R$", min_value=0.0, value=2000.0, step=100.0)
        if st.button("🔄 ATUALIZAR AGORA"):
            st.cache_data.clear()
            st.rerun()
        st.info("Estratégia Otimizada V.31")

    with st.spinner('📡 Conectando aos servidores da B3...'):
        df = get_data_and_calculate()

    if df.empty:
        st.error("Erro na conexão de dados. Tente novamente.")
        return

    # LÓGICA DE ALOCAÇÃO
    vendas = df[df['Acao'] == 'VENDA']
    compras_ataque = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == 'ATAQUE')].sort_values('Score', ascending=False)
    compras_defesa = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == 'DEFESA')].sort_values('Score', ascending=False)

    carteira_final = []
    carteira_final.extend(compras_ataque.head(3).to_dict('records'))
    vagas = 3 - len(carteira_final)
    if vagas > 0: carteira_final.extend(compras_defesa.head(vagas).to_dict('records'))

    # ==========================================================================
    # SEÇÃO 1: VENDAS (DESIGN ALERTA)
    # ==========================================================================
    if not vendas.empty:
        st.markdown("### 1️⃣ VENDAS NECESSÁRIAS")
        st.write("Venda estes ativos para liberar caixa:")
        cols = st.columns(3)
        for idx, row in enumerate(vendas.to_dict('records')):
            with cols[idx % 3]:
                # HTML Montado em Linha Única para evitar bugs
                html_sell = f"""
                <div class="sell-card">
                    <div class="sell-ticker">
                        <span>{row['Ticker']}</span>
                        <span>❌</span>
                    </div>
                    <div class="sell-detail">Preço Atual: <b>R$ {row['Preco']:.2f}</b></div>
                    <div style="margin-top:8px"><span class="sell-tag">{row['Status']}</span></div>
                </div>
                """
                st.markdown(html_sell, unsafe_allow_html=True)
    else:
        st.success("✅ Nenhuma venda necessária hoje.")

    # ==========================================================================
    # SEÇÃO 2: COMPRAS (DESIGN PRO DETALHADO)
    # ==========================================================================
    st.markdown("---")
    st.markdown("### 2️⃣ NOVAS COMPRAS")
    
    if not carteira_final:
        st.warning(f"Mercado sem oportunidades. Fique 100% no CAIXA ({ATIVO_CAIXA}).")
    else:
        peso = 1.0 / len(carteira_final)
        cols = st.columns(len(carteira_final))
        
        for i, ativo in enumerate(carteira_final):
            with cols[i]:
                # CÁLCULOS
                alo = capital * peso
                qtd = int(alo / ativo['Preco'])
                padrao = (qtd // 100) * 100
                frac = qtd % 100
                cod = ativo['Ticker'].replace('.SA', '')
                
                # HTML DINÂMICO (BOLETA)
                html_boleta_rows = ""
                
                if padrao > 0:
                    html_boleta_rows += f"""
                    <div class="boleta-row">
                        <span class="boleta-key">1. Lote Padrão:</span>
                        <span class="boleta-val">Comprar {padrao} x {cod}</span>
                    </div>
                    """
                
                if frac > 0:
                    label = "2. Fracionário:" if padrao > 0 else "1. Fracionário:"
                    html_boleta_rows += f"""
                    <div class="boleta-row">
                        <span class="boleta-key">{label}</span>
                        <span class="boleta-val">Comprar {frac} x {cod}F</span>
                    </div>
                    """
                
                # CARD COMPLETO
                html_card = f"""
                <div class="card-buy">
                    <div class="buy-header">
                        <span class="buy-ticker">{ativo['Ticker']}</span>
                        <span class="buy-type">{ativo['Tipo']}</span>
                    </div>
                    <div class="buy-content">
                        <div class="money-section">
                            <div>
                                <div class="money-label">Valor a Investir</div>
                                <div class="money-value">R$ {alo:,.0f}</div>
                            </div>
                            <div class="price-ref">
                                Preço<br><b>R$ {ativo['Preco']:.2f}</b>
                            </div>
                        </div>
                        <div class="boleta-box">
                            <div class="boleta-title">📝 ORDEM NA CORRETORA</div>
                            {html_boleta_rows}
                            <div class="boleta-row" style="border-top:1px dashed #30363d; margin-top:5px; padding-top:5px;">
                                <span class="boleta-key">Preço Limite:</span>
                                <span class="boleta-val" style="color:#3fb950">A Mercado</span>
                            </div>
                        </div>
                        <div class="status-footer">Motivo: {ativo['Status']}</div>
                    </div>
                </div>
                """
                st.markdown(html_card, unsafe_allow_html=True)

    # ==========================================================================
    # SEÇÃO 3: ESPIÃO
    # ==========================================================================
    st.markdown("---")
    with st.expander("🔍 Ver Análise Técnica de Todos os Ativos"):
        st.dataframe(df.style.map(lambda x: 'color:#ff6666' if 'VENDA' in str(x) else ('color:#3fb950' if 'COMPRA' in str(x) else 'color:#8b949e'), subset=['Acao']))

if __name__ == "__main__":
    main()
