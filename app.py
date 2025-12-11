import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ==============================================================================
# 🔐 CONFIGURAÇÃO DE SEGURANÇA (LOGIN)
# ==============================================================================
# Defina sua senha aqui
SENHA_ACESSO = "tridente2025" 

def check_password():
    """Retorna True se o usuário estiver logado."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    st.markdown("## 🔐 Acesso Restrito - Robô Tridente V.32")
    password = st.text_input("Digite a senha de acesso:", type="password")
    
    if st.button("Entrar"):
        if password == SENHA_ACESSO:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ Senha incorreta.")
    return False

# ==============================================================================
# ⚙️ LÓGICA DO ROBÔ (MATEMÁTICA V.31)
# ==============================================================================
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

@st.cache_data(ttl=3600) # Cache para não baixar dados toda hora (1h)
def get_data_and_calculate():
    dias = (5 * 365)
    start = (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d')
    
    resultados = []
    
    # Baixa tudo de uma vez para ser mais rápido
    try:
        data = yf.download(TICKERS, start=start, interval='1wk', progress=False, group_by='ticker', auto_adjust=True)
    except:
        return []

    for t in TICKERS:
        try:
            df = data[t].dropna()
            if len(df) < 52: continue
            
            close = df['Close']
            P = CATALOGO[t]
            
            # Indicadores
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

            # Score
            if t in ATAQUE:
                safe_vol = vol if vol > 0.01 else 0.01
                score = roc / safe_vol
            else:
                safe_vol = vol if vol > 0.01 else 0.01
                score = 1 / safe_vol

            # Julgamento
            acao = "COMPRA"
            status = f"SCORE {score:.2f}"
            tipo = "⚔️ ATAQUE" if t in ATAQUE else "🛡️ DEFESA"
            
            cor = "green" # Para gráfico
            
            # Filtros de Venda
            if dist < 0: 
                acao = "VENDA"; status = f"ABAIXO DA MÉDIA (MM{P['MM']})"; cor="red"
            elif vol > P['VOL_LIMIT']: 
                acao = "VENDA"; status = f"RISCO ALTO (Vol {vol:.2f})"; cor="red"
            # Filtros de Neutro
            elif rsi_val > P['RSI_MAX']: 
                acao = "NEUTRO"; status = f"RSI ESTICADO ({rsi_val:.0f})"; cor="yellow"
            elif dist > P['DIST_MAX']: 
                acao = "NEUTRO"; status = f"PREÇO ESTICADO (+{dist:.1%})"; cor="yellow"
            elif t in ATAQUE and roc <= 0:
                acao = "NEUTRO"; status = "SEM FORÇA (ROC < 0)"; cor="yellow"
            
            resultados.append({
                'Ticker': t, 'Tipo': tipo, 'Preco': atual, 'Score': score,
                'Acao': acao, 'Status': status, 'Cor': cor, 'ROC': roc, 'RSI': rsi_val
            })
            
        except Exception as e:
            continue
            
    return pd.DataFrame(resultados)

# ==============================================================================
# 📱 INTERFACE VISUAL (STREAMLIT)
# ==============================================================================
def main():
    if not check_password():
        return

    st.set_page_config(page_title="Robô Tridente V.32", page_icon="🔱", layout="wide")
    
    # Cabeçalho
    st.title("🔱 Robô Tridente V.32 | Painel de Controle")
    st.markdown("---")

    # Sidebar (Entrada de Dados)
    with st.sidebar:
        st.header("💰 Seu Capital")
        capital = st.number_input("Quanto você tem hoje?", min_value=0.0, value=2000.0, step=100.0, format="%.2f")
        st.info("Atualize este valor todo mês antes de operar.")
        
        if st.button("🔄 Atualizar Análise"):
            st.cache_data.clear()
            st.rerun()

    # Processamento
    with st.spinner('📡 O Robô está escaneando o mercado...'):
        df = get_data_and_calculate()

    if df.empty:
        st.error("Erro ao baixar dados. Tente novamente mais tarde.")
        return

    # Separação
    vendas = df[df['Acao'] == 'VENDA']
    compras_ataque = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == '⚔️ ATAQUE')].sort_values('Score', ascending=False)
    compras_defesa = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == '🛡️ DEFESA')].sort_values('Score', ascending=False)

    # Montagem da Carteira
    carteira_final = []
    carteira_final.extend(compras_ataque.head(3).to_dict('records'))
    
    vagas = 3 - len(carteira_final)
    if vagas > 0:
        carteira_final.extend(compras_defesa.head(vagas).to_dict('records'))

    # --- TELA 1: ALERTAS DE VENDA ---
    if not vendas.empty:
        st.error("🔴 **ATENÇÃO: VENDAS NECESSÁRIAS**")
        st.write("Se você tem algum destes ativos, venda hoje para liberar caixa.")
        
        cols = st.columns(len(vendas) if len(vendas) < 4 else 4)
        for idx, row in enumerate(vendas.to_dict('records')):
            with cols[idx % 4]:
                st.metric(label=row['Ticker'], value=f"R$ {row['Preco']:.2f}", delta="VENDER", delta_color="inverse")
                st.caption(f"Motivo: {row['Status']}")
        st.markdown("---")
    else:
        st.success("✅ Nenhuma venda técnica necessária hoje.")

    # --- TELA 2: RECOMENDAÇÃO DE COMPRA ---
    st.subheader("🟢 Nova Alocação Sugerida (Equal Weight)")
    
    if not carteira_final:
        st.warning("⚠️ Mercado perigoso. Fique 100% em Caixa (Tesouro Selic / B5P211).")
    else:
        peso = 1.0 / len(carteira_final)
        cols = st.columns(3)
        
        for i, ativo in enumerate(carteira_final):
            alocacao = capital * peso
            qtd_total = int(alocacao / ativo['Preco'])
            
            # Lógica Fracionária
            qtd_padrao = (qtd_total // 100) * 100
            qtd_frac = qtd_total % 100
            
            with cols[i]:
                st.markdown(f"### 🏆 Rank #{i+1}")
                st.markdown(f"**{ativo['Ticker']}** ({ativo['Tipo']})")
                st.metric(label="Preço Atual", value=f"R$ {ativo['Preco']:.2f}")
                
                st.markdown(f"""
                <div style='background-color: #1c2e1c; padding: 15px; border-radius: 10px; border: 1px solid #2e7d32;'>
                    <h3 style='color: #4caf50; margin:0;'>R$ {alocacao:,.2f}</h3>
                    <p>Total Ações: <b>{qtd_total}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("##### 📝 Na Boleta:")
                if qtd_padrao > 0:
                    st.write(f"• **{ativo['Ticker']}**: {qtd_padrao} ações")
                if qtd_frac > 0:
                    st.write(f"• **{ativo['Ticker']}F**: {qtd_frac} ações")
                
                st.caption(f"Motivo: {ativo['Status']}")

    # --- TELA 3: TABELA GERAL (ESPIÃO) ---
    with st.expander("🔍 Ver Análise Técnica Completa de Todos os Ativos"):
        st.dataframe(df.style.map(lambda x: 'color: red' if 'VENDA' in str(x) else ('color: green' if 'COMPRA' in str(x) else 'color: orange'), subset=['Acao']), use_container_width=True)

if __name__ == "__main__":
    main()
