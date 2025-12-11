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
    
    st.markdown("## 🔐 Acesso Restrito - Robô Tridente V.33")
    password = st.text_input("Digite a senha de acesso:", type="password")
    if st.button("Entrar"):
        if password == SENHA_ACESSO:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ Senha incorreta.")
    return False

# ==============================================================================
# ⚙️ CONFIGURAÇÃO E LÓGICA V.31
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
# 🎨 INTERFACE VISUAL PRO (CSS)
# ==============================================================================
def main():
    if not check_password(): return

    st.set_page_config(page_title="Tridente V.33 Pro", page_icon="🔱", layout="wide")
    
    # CSS AVANÇADO PARA CARDS PROFISSIONAIS
    st.markdown("""
    <style>
    /* Estilo Geral */
    .main-header { font-size: 32px; font-weight: 800; color: #ffffff; text-align: center; margin-bottom: 20px; }
    .sub-header { font-size: 20px; font-weight: 600; color: #a0a0a0; margin-top: 30px; margin-bottom: 15px; border-left: 4px solid #f63366; padding-left: 10px; }
    
    /* Card de Venda (Vermelho Neon) */
    .card-sell {
        background: linear-gradient(135deg, #2b0e0e 0%, #4a1212 100%);
        border: 1px solid #ff4b4b;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(255, 75, 75, 0.1);
        transition: transform 0.2s;
    }
    .card-sell:hover { transform: translateY(-2px); box-shadow: 0 6px 12px rgba(255, 75, 75, 0.2); }
    .sell-title { color: #ff4b4b; font-size: 18px; font-weight: bold; margin: 0; display: flex; align-items: center; gap: 8px; }
    .sell-price { font-size: 24px; color: #fff; font-weight: 700; margin: 10px 0; }
    .sell-reason { color: #ffadad; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }

    /* Card de Compra (Verde Profissional) */
    .card-buy {
        background-color: #0e1117;
        border: 1px solid #2e7d32;
        border-radius: 15px;
        overflow: hidden;
        margin-bottom: 20px;
    }
    .buy-header {
        background: linear-gradient(90deg, #1b3a20 0%, #2e7d32 100%);
        padding: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .buy-ticker { font-size: 22px; font-weight: 900; color: #fff; margin: 0; }
    .buy-tag { background: rgba(0,0,0,0.3); color: #81c784; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    
    .buy-body { padding: 20px; }
    .invest-label { font-size: 13px; color: #888; text-transform: uppercase; }
    .invest-value { font-size: 32px; font-weight: 800; color: #4caf50; margin: 0 0 15px 0; }
    
    /* Caixa de Instrução (Boleta) */
    .boleta-box {
        background-color: #1a1c24;
        border-radius: 8px;
        padding: 15px;
        border-left: 4px solid #4caf50;
    }
    .boleta-title { color: #fff; font-size: 14px; font-weight: bold; margin-bottom: 10px; display: flex; align-items: center; gap: 5px; }
    .boleta-item { color: #ccc; font-size: 13px; margin-bottom: 4px; display: flex; justify-content: space-between; }
    .boleta-val { color: #fff; font-weight: bold; }
    .divider { border-top: 1px solid #333; margin: 8px 0; }

    </style>
    """, unsafe_allow_html=True)

    # HEADER
    st.markdown("<div class='main-header'>🔱 TRIDENTE V.33 PRO</div>", unsafe_allow_html=True)

    # SIDEBAR
    with st.sidebar:
        st.header("💰 Carteira")
        capital = st.number_input("Patrimônio Total (R$)", min_value=0.0, value=2000.0, step=100.0)
        if st.button("🔄 Atualizar"):
            st.cache_data.clear()
            st.rerun()

    # DATA
    with st.spinner('📡 Processando dados...'):
        df = get_data_and_calculate()
    
    if df.empty:
        st.error("Erro de conexão. Tente novamente.")
        return

    vendas = df[df['Acao'] == 'VENDA']
    compras_ataque = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == 'ATAQUE')].sort_values('Score', ascending=False)
    compras_defesa = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == 'DEFESA')].sort_values('Score', ascending=False)

    carteira_final = []
    carteira_final.extend(compras_ataque.head(3).to_dict('records'))
    vagas = 3 - len(carteira_final)
    if vagas > 0: carteira_final.extend(compras_defesa.head(vagas).to_dict('records'))

    # --- SESSÃO 1: VENDAS ---
    st.markdown("<div class='sub-header'>1. ATENÇÃO: VENDAS NECESSÁRIAS</div>", unsafe_allow_html=True)
    
    if not vendas.empty:
        cols = st.columns(3)
        for idx, row in enumerate(vendas.to_dict('records')):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class='card-sell'>
                    <p class='sell-title'>❌ VENDER {row['Ticker']}</p>
                    <p class='sell-price'>R$ {row['Preco']:.2f}</p>
                    <p class='sell-reason'>{row['Status']}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.success("✅ Nenhuma venda necessária. Sua carteira está limpa.")

    # --- SESSÃO 2: COMPRAS ---
    st.markdown("<div class='sub-header'>2. NOVAS COMPRAS (ALOCAÇÃO EQUAL WEIGHT)</div>", unsafe_allow_html=True)
    
    if not carteira_final:
        st.warning(f"⚠️ Mercado sem oportunidades. Fique 100% no Caixa ({ATIVO_CAIXA}).")
    else:
        peso = 1.0 / len(carteira_final)
        cols = st.columns(len(carteira_final))
        
        for i, ativo in enumerate(carteira_final):
            with cols[i]:
                alocacao = capital * peso
                qtd_total = int(alocacao / ativo['Preco'])
                
                # Cálculo Lotes
                qtd_padrao = (qtd_total // 100) * 100
                qtd_frac = qtd_total % 100
                ticker = ativo['Ticker'].replace('.SA', '')
                
                # HTML do Card
                instrucao_html = ""
                
                if qtd_padrao > 0:
                    instrucao_html += f"""
                    <div class='boleta-item'><span>Código:</span> <span class='boleta-val'>{ticker}</span></div>
                    <div class='boleta-item'><span>Qtd:</span> <span class='boleta-val'>{qtd_padrao}</span></div>
                    """
                
                if qtd_frac > 0:
                    if qtd_padrao > 0: instrucao_html += "<div class='divider'></div>"
                    instrucao_html += f"""
                    <div class='boleta-item'><span>Código:</span> <span class='boleta-val'>{ticker}F</span></div>
                    <div class='boleta-item'><span>Qtd:</span> <span class='boleta-val'>{qtd_frac}</span></div>
                    """
                
                st.markdown(f"""
                <div class='card-buy'>
                    <div class='buy-header'>
                        <p class='buy-ticker'>{ativo['Ticker']}</p>
                        <span class='buy-tag'>{ativo['Tipo']}</span>
                    </div>
                    <div class='buy-body'>
                        <p class='invest-label'>Valor a Investir</p>
                        <p class='invest-value'>R$ {alocacao:,.2f}</p>
                        
                        <div class='boleta-box'>
                            <p class='boleta-title'>📝 Ordem de Compra</p>
                            {instrucao_html}
                            <div class='divider'></div>
                            <div class='boleta-item'><span>Preço:</span> <span class='boleta-val'>A Mercado</span></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # --- SESSÃO 3: ESPIÃO ---
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🔍 Ver Tabela Técnica Completa"):
        st.dataframe(df.style.map(lambda x: 'color:#ff4b4b' if 'VENDA' in str(x) else ('color:#4caf50' if 'COMPRA' in str(x) else 'color:#aaa'), subset=['Acao']))

if __name__ == "__main__":
    main()
