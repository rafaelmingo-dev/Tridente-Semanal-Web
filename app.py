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

    st.markdown("## 🔐 Robô Tridente V.37 - Acesso Restrito")
    password = st.text_input("Digite a senha:", type="password")
    
    if st.button("Entrar"):
        if password == SENHA_ACESSO:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("Senha incorreta.")
    return False

# ==============================================================================
# ⚙️ LÓGICA V.31 (MATEMÁTICA GOLDEN STANDARD) - INTACTA
# ==============================================================================
ATIVO_CAIXA = 'B5P211.SA'

CATALOGO = {
    # --- DEFESA ---
    'IVVB11.SA': {'MM': 40, 'RSI_MAX': 70, 'DIST_MAX': 0.20, 'VOL_LIMIT': 0.4},
    'GOLD11.SA': {'MM': 16, 'RSI_MAX': 70, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.4},
    'B5P211.SA': {'MM': 4 , 'RSI_MAX': 75, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.4},
    # --- ATAQUE ---
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
    """Baixa dados e aplica a lógica V.31 minuciosamente."""
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
# 🎨 INTERFACE VISUAL (CSS OTIMIZADO PARA EVITAR ERROS)
# ==============================================================================
def main():
    if not check_password(): return

    st.set_page_config(page_title="Robô Tridente V.37", page_icon="🔱", layout="wide")
    
    # CSS LIMPO E SEGURO
    st.markdown("""
    <style>
    .main-header { font-size: 32px; font-weight: 800; color: #fff; text-align: center; margin-bottom: 20px; }
    
    /* CARD VENDA */
    .card-sell {
        background-color: #3a0000;
        border: 1px solid #ff4444; border-radius: 10px; padding: 15px; margin-bottom: 15px;
    }
    .sell-text { color: #ff6666; font-size: 18px; font-weight: bold; }
    .sell-sub { color: #fff; font-size: 14px; }

    /* CARD COMPRA */
    .card-buy {
        background-color: #0e1117; 
        border: 1px solid #2e7d32; 
        border-radius: 12px; 
        padding: 0px; 
        overflow: hidden;
        margin-bottom: 20px;
    }
    .buy-head {
        background-color: #1b5e20; padding: 12px; display: flex; justify-content: space-between; align-items: center;
    }
    .buy-title { color: #fff; font-size: 22px; font-weight: 900; margin:0; }
    .buy-badge { background-color: #000; color: #4caf50; padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: bold; }
    
    .buy-content { padding: 15px; }
    .money-val { font-size: 26px; font-weight: 800; color: #4caf50; }
    
    /* BOLETA STYLE */
    .boleta-wrap {
        background-color: #161b22; 
        border-radius: 8px; 
        padding: 12px; 
        margin-top: 15px; 
        border-left: 4px solid #4caf50;
    }
    .bol-line {
        display: flex; justify-content: space-between; margin-bottom: 6px; border-bottom: 1px dashed #333; padding-bottom: 4px;
    }
    .bol-key { color: #888; font-size: 13px; }
    .bol-val { color: #fff; font-weight: bold; font-family: monospace; font-size: 14px; }
    
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-header'>🔱 ROBÔ TRIDENTE V.37</div>", unsafe_allow_html=True)

    # SIDEBAR
    with st.sidebar:
        st.header("💰 Carteira")
        capital = st.number_input("Patrimônio Total (R$)", min_value=0.0, value=2000.0, step=100.0)
        if st.button("🔄 Rodar Análise"):
            st.cache_data.clear()
            st.rerun()
        st.info("Estratégia Equal Weight (33%).")

    # DADOS
    with st.spinner('📡 Analisando...'):
        df = get_data_and_calculate()

    if df.empty:
        st.error("Erro de conexão com B3.")
        return

    # LÓGICA DE ALOCAÇÃO
    vendas = df[df['Acao'] == 'VENDA']
    compras_ataque = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == 'ATAQUE')].sort_values('Score', ascending=False)
    compras_defesa = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == 'DEFESA')].sort_values('Score', ascending=False)

    carteira_final = []
    carteira_final.extend(compras_ataque.head(3).to_dict('records'))
    vagas = 3 - len(carteira_final)
    if vagas > 0: carteira_final.extend(compras_defesa.head(vagas).to_dict('records'))

    # 1. VENDAS
    if not vendas.empty:
        st.markdown("### 1️⃣ ALERTAS DE VENDA")
        cols = st.columns(3)
        for idx, row in enumerate(vendas.to_dict('records')):
            with cols[idx % 3]:
                # HTML SIMPLIFICADO PARA EVITAR ERROS
                st.markdown(f"""
                <div class="card-sell">
                    <div class="sell-text">❌ {row['Ticker']}</div>
                    <div class="sell-sub">Motivo: {row['Status']}</div>
                    <div class="sell-sub">Ref: R$ {row['Preco']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.success("✅ Nenhuma venda necessária.")

    # 2. COMPRAS
    st.markdown("---")
    st.markdown("### 2️⃣ NOVAS COMPRAS (PASSO A PASSO)")
    
    if not carteira_final:
        st.error(f"Mercado Ruim. Fique 100% no CAIXA ({ATIVO_CAIXA}).")
    else:
        peso = 1.0 / len(carteira_final)
        cols = st.columns(len(carteira_final))
        
        for i, ativo in enumerate(carteira_final):
            with cols[i]:
                alocacao = capital * peso
                qtd_total = int(alocacao / ativo['Preco'])
                
                # CÁLCULOS
                qtd_padrao = (qtd_total // 100) * 100
                qtd_frac = qtd_total % 100
                ticker_base = ativo['Ticker'].replace('.SA', '')
                
                # HTML BUILDER (STRING PURA PARA SEGURANÇA)
                html_card = f"""
                <div class="card-buy">
                    <div class="buy-head">
                        <span class="buy-title">{ativo['Ticker']}</span>
                        <span class="buy-badge">{ativo['Tipo']}</span>
                    </div>
                    <div class="buy-content">
                        <div style="font-size:12px; color:#aaa;">VALOR A INVESTIR</div>
                        <div class="money-val">R$ {alocacao:,.0f}</div>
                        
                        <div class="boleta-wrap">
                            <div style="color:#4caf50; font-weight:bold; font-size:12px; margin-bottom:8px;">📝 ORDEM NA CORRETORA</div>
                """
                
                # Adiciona Lote Padrão se existir
                if qtd_padrao > 0:
                    html_card += f"""
                    <div class="bol-line">
                        <span class="bol-key">Opção 1 (Lote):</span>
                        <span class="bol-val">{qtd_padrao} x {ticker_base}</span>
                    </div>
                    """
                
                # Adiciona Fracionário se existir
                if qtd_frac > 0:
                    label = "Opção 2 (Sobra):" if qtd_padrao > 0 else "Opção Única:"
                    html_card += f"""
                    <div class="bol-line">
                        <span class="bol-key">{label}</span>
                        <span class="bol-val">{qtd_frac} x {ticker_base}F</span>
                    </div>
                    """
                
                # Fecha o HTML
                html_card += f"""
                            <div style="margin-top:8px; text-align:center; font-size:11px; color:#666;">
                                Preço: A Mercado | Motivo: {ativo['Status']}
                            </div>
                        </div>
                    </div>
                </div>
                """
                
                st.markdown(html_card, unsafe_allow_html=True)

    # 3. TABELA ESPIÃO
    st.markdown("---")
    with st.expander("🔍 Espião (Tabela Técnica Completa)"):
        st.dataframe(df.style.map(lambda x: 'color:#ff4b4b' if 'VENDA' in str(x) else ('color:#4caf50' if 'COMPRA' in str(x) else 'color:#aaa'), subset=['Acao']))

if __name__ == "__main__":
    main()
