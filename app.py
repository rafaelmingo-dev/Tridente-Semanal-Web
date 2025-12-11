import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==============================================================================
# 🔐 CONFIGURAÇÃO DE SEGURANÇA (LOGIN)
# ==============================================================================
SENHA_ACESSO = "tridente2025" 

def check_password():
    """Retorna True se o usuário estiver logado."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    st.markdown("## 🔐 Acesso Restrito - Robô Tridente V.35")
    password = st.text_input("Digite a senha de acesso:", type="password")
    
    if st.button("Entrar"):
        if password == SENHA_ACESSO:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ Senha incorreta.")
    return False

# ==============================================================================
# ⚙️ LÓGICA DO ROBÔ (MATEMÁTICA V.31 - GOLDEN STANDARD - MESTRE)
# ==============================================================================
# A LÓGICA PERMANECE INTACTA. NÃO ALTERAR.

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
            
            # Indicadores (Lógica Exata V.31)
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
# 🎨 INTERFACE VISUAL (CSS CORRIGIDO)
# ==============================================================================
def main():
    if not check_password(): return

    st.set_page_config(page_title="Robô Tridente V.35", page_icon="🔱", layout="wide")
    
    # CSS Corrigido e Otimizado
    st.markdown("""
    <style>
    .main-header { font-size: 30px; font-weight: 800; color: #fff; text-align: center; margin-bottom: 5px; }
    .sub-header { font-size: 14px; color: #888; text-align: center; margin-bottom: 20px; }
    
    /* CARD VENDA */
    .card-sell {
        background: linear-gradient(135deg, #3a0000 0%, #1a0000 100%);
        border: 1px solid #ff4444; border-radius: 10px; padding: 15px; margin-bottom: 10px; color: white;
    }
    .sell-title { color: #ff6666; font-size: 18px; font-weight: bold; margin: 0; }
    .sell-info { font-size: 12px; color: #ccc; margin-top: 5px; }

    /* CARD COMPRA */
    .card-buy {
        background-color: #0e1117; border: 1px solid #2e7d32; border-radius: 12px; overflow: hidden; margin-bottom: 20px;
    }
    .buy-header {
        background: #1b5e20; padding: 10px 15px; display: flex; justify-content: space-between; align-items: center;
    }
    .buy-ticker { font-size: 20px; font-weight: 900; color: #fff; margin: 0; }
    .buy-tag { background: #000; color: #4caf50; padding: 2px 8px; border-radius: 6px; font-size: 10px; font-weight: bold; }
    
    .buy-body { padding: 15px; }
    .invest-val { font-size: 24px; font-weight: bold; color: #4caf50; }
    .invest-lbl { font-size: 11px; color: #aaa; text-transform: uppercase; }
    
    /* BOX DA BOLETA */
    .boleta-box {
        background-color: #161b22; border-radius: 8px; padding: 10px; margin-top: 15px; border-left: 3px solid #4caf50;
    }
    .boleta-row { display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 13px; color: #ddd; border-bottom: 1px dashed #333; padding-bottom: 2px;}
    .boleta-row:last-child { border: none; }
    .boleta-val { font-weight: bold; color: #fff; font-family: monospace; }
    
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-header'>🔱 ROBÔ TRIDENTE V.35</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Painel de Execução Profissional</div>", unsafe_allow_html=True)

    # SIDEBAR
    with st.sidebar:
        st.header("💰 Carteira")
        capital = st.number_input("Patrimônio Total (R$)", min_value=0.0, value=2000.0, step=100.0)
        if st.button("🔄 Atualizar"):
            st.cache_data.clear()
            st.rerun()
        st.markdown("---")
        st.info("Estratégia Equal Weight (33%).")

    with st.spinner('📡 Processando...'):
        df = get_data_and_calculate()

    if df.empty:
        st.error("Erro de conexão.")
        return

    vendas = df[df['Acao'] == 'VENDA']
    compras_ataque = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == '⚔️ ATAQUE')].sort_values('Score', ascending=False)
    compras_defesa = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == '🛡️ DEFESA')].sort_values('Score', ascending=False)

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
                <div class='card-sell'>
                    <div class='sell-title'>❌ {row['Ticker']}</div>
                    <div class='sell-info'>Motivo: {row['Status']}</div>
                    <div class='sell-info'>Ref: R$ {row['Preco']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.success("Nenhuma venda necessária.")

    # 2. COMPRAS
    st.markdown("---")
    st.markdown("### 2️⃣ NOVAS COMPRAS")
    
    if not carteira_final:
        st.error(f"Mercado Perigoso. Fique 100% no CAIXA ({ATIVO_CAIXA}).")
    else:
        peso = 1.0 / len(carteira_final)
        cols = st.columns(len(carteira_final))
        
        for i, ativo in enumerate(carteira_final):
            with cols[i]:
                alocacao = capital * peso
                qtd_total = int(alocacao / ativo['Preco'])
                
                # Cálculos
                qtd_padrao = (qtd_total // 100) * 100
                qtd_frac = qtd_total % 100
                ticker = ativo['Ticker'].replace('.SA', '')
                
                # Construção HTML limpa
                html_boleta = ""
                
                if qtd_padrao > 0:
                    html_boleta += f"""
                    <div style='margin-bottom:10px;'>
                        <div style='color:#888; font-size:11px; text-transform:uppercase;'>Opção 1: Lote Padrão</div>
                        <div class='boleta-row'><span>Código:</span> <span class='boleta-val'>{ticker}</span></div>
                        <div class='boleta-row'><span>Qtd:</span> <span class='boleta-val'>{qtd_padrao}</span></div>
                    </div>
                    """
                
                if qtd_frac > 0:
                    label = "Opção 2: Sobra" if qtd_padrao > 0 else "Opção Única"
                    html_boleta += f"""
                    <div>
                        <div style='color:#888; font-size:11px; text-transform:uppercase;'>{label}</div>
                        <div class='boleta-row'><span>Código:</span> <span class='boleta-val'>{ticker}F</span></div>
                        <div class='boleta-row'><span>Qtd:</span> <span class='boleta-val'>{qtd_frac}</span></div>
                    </div>
                    """

                st.markdown(f"""
                <div class='card-buy'>
                    <div class='buy-header'>
                        <div class='buy-ticker'>{ativo['Ticker']}</div>
                        <div class='buy-tag'>{ativo['Tipo']}</div>
                    </div>
                    <div class='buy-body'>
                        <div class='invest-lbl'>Investir</div>
                        <div class='invest-val'>R$ {alocacao:,.0f}</div>
                        
                        <div class='boleta-box'>
                            <div style='color:#4caf50; font-weight:bold; font-size:12px; margin-bottom:5px;'>📝 NA CORRETORA</div>
                            {html_boleta}
                            <div style='border-top:1px solid #333; margin-top:5px; padding-top:5px; text-align:center; font-size:12px; color:#aaa;'>
                                Ordem a Mercado
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # 3. TABELA
    st.markdown("---")
    with st.expander("🔍 Ver Detalhes Técnicos (Espião)"):
        st.dataframe(df.style.map(lambda x: 'color:#ff4b4b' if 'VENDA' in str(x) else ('color:#4caf50' if 'COMPRA' in str(x) else 'color:#aaa'), subset=['Acao']))

if __name__ == "__main__":
    main()
