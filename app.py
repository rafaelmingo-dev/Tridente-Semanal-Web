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
    
    st.markdown("## 🔐 Robô Tridente V.39")
    password = st.text_input("Senha:", type="password")
    if st.button("Entrar"):
        if password == SENHA_ACESSO:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("Senha Incorreta")
    return False

# ==============================================================================
# ⚙️ LÓGICA V.31 (MATEMÁTICA PURA - BACKTEST GOLDEN STANDARD)
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
# 🎨 INTERFACE VISUAL NATIVA (SEM ERROS DE HTML)
# ==============================================================================
def main():
    if not check_password(): return

    st.set_page_config(page_title="Robô Tridente V.39", page_icon="🔱", layout="wide")
    
    # CSS APENAS PARA CORES GERAIS
    st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1 { color: #ffffff; text-align: center; }
    h3 { color: #aaaaaa; text-align: center; font-size: 16px; font-weight: normal; }
    div[data-testid="stMetricValue"] { font-size: 24px; color: #4caf50; }
    </style>
    """, unsafe_allow_html=True)

    st.title("🔱 ROBÔ TRIDENTE V.39")
    st.markdown("### Painel de Execução Profissional | Equal Weight (33%)")
    st.divider()

    with st.sidebar:
        st.header("💰 Carteira")
        capital = st.number_input("Patrimônio Total (R$)", min_value=0.0, value=2000.0, step=100.0)
        if st.button("🔄 Rodar Análise"):
            st.cache_data.clear()
            st.rerun()
        st.info("Estratégia Equal Weight (33%): Divide o capital igualmente entre os 3 melhores ativos.")

    with st.spinner('📡 Conectando à B3...'):
        df = get_data_and_calculate()

    if df.empty:
        st.error("Erro na conexão de dados.")
        return

    vendas = df[df['Acao'] == 'VENDA']
    ataque = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == 'ATAQUE')].sort_values('Score', ascending=False)
    defesa = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == 'DEFESA')].sort_values('Score', ascending=False)

    final = []
    final.extend(ataque.head(3).to_dict('records'))
    vagas = 3 - len(final)
    if vagas > 0: final.extend(defesa.head(vagas).to_dict('records'))

    # ==========================================================================
    # 1. ÁREA DE VENDAS
    # ==========================================================================
    if not vendas.empty:
        st.subheader("1️⃣ ALERTAS DE VENDA")
        st.warning("Venda estes ativos se você os tiver na carteira.")
        
        # Grid de Vendas
        cols = st.columns(4)
        for idx, row in enumerate(vendas.to_dict('records')):
            with cols[idx % 4]:
                with st.container(border=True):
                    st.markdown(f"**❌ {row['Ticker']}**")
                    st.caption(f"Ref: R$ {row['Preco']:.2f}")
                    st.error(f"{row['Status']}")
    else:
        st.success("✅ Nenhuma venda necessária hoje.")

    st.markdown("---")

    # ==========================================================================
    # 2. ÁREA DE COMPRAS (DETALHADA)
    # ==========================================================================
    st.subheader("2️⃣ NOVAS COMPRAS (PASSO A PASSO)")
    
    if not final:
        st.error(f"Mercado Ruim. Fique 100% no CAIXA ({ATIVO_CAIXA}).")
    else:
        peso = 1.0 / len(final)
        cols = st.columns(len(final))
        
        for i, ativo in enumerate(final):
            with cols[i]:
                # Cálculos
                alo = capital * peso
                qtd = int(alo / ativo['Preco'])
                padrao = (qtd // 100) * 100
                frac = qtd % 100
                cod = ativo['Ticker'].replace('.SA', '')
                
                # CARD NATIVO DO STREAMLIT (IMPOSSÍVEL DE QUEBRAR)
                with st.container(border=True):
                    # Cabeçalho do Card
                    st.markdown(f"### 🏆 Rank #{i+1}")
                    st.markdown(f"## {ativo['Ticker']}")
                    st.caption(f"Tipo: {ativo['Tipo']}")
                    
                    st.divider()
                    
                    # Valores Financeiros
                    col_a, col_b = st.columns(2)
                    col_a.metric("Investir", f"R$ {alo:,.0f}")
                    col_b.metric("Preço", f"R$ {ativo['Preco']:.2f}")
                    
                    st.divider()
                    
                    # INSTRUÇÕES DA BOLETA (Formatado como Código para clareza)
                    st.markdown("##### 📝 Na Corretora:")
                    
                    if padrao > 0:
                        st.text("Opção 1 (Lote Padrão):")
                        st.info(f"Comprar {padrao} de {cod}")
                    
                    if frac > 0:
                        lbl = "Opção 2 (Sobra):" if padrao > 0 else "Opção Única:"
                        st.text(lbl)
                        st.success(f"Comprar {frac} de {cod}F")
                    
                    st.caption(f"Motivo da escolha: {ativo['Status']}")

    # ==========================================================================
    # 3. TABELA
    # ==========================================================================
    st.markdown("---")
    with st.expander("🔍 Ver Detalhes Técnicos (Espião)"):
        st.dataframe(df.style.map(lambda x: 'color:red' if 'VENDA' in str(x) else ('color:green' if 'COMPRA' in str(x) else 'color:orange'), subset=['Acao']))

if __name__ == "__main__":
    main()
