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
# 🎨 UI V.48 (TERMINAL PURÍSSIMO)
# ==============================================================================
def formatar_instrucao_boleta(ativo, alocacao, qtd, padrao, frac, cod):
    """Gera o bloco de texto formatado como o terminal original."""
    
    instrucao = f"**🏆 RANK #{i+1}: {ativo['Ticker']} ({ativo['Tipo']})**\n\n"
    instrucao += f"💰 Valor para investir: **R$ {alocacao:,.2f}**\n"
    instrucao += f"📊 Preço Atual: **R$ {ativo['Preco']:.2f}**\n\n"
    instrucao += "📝 **COMO PREENCHER A ORDEM (BOLETA):**\n"

    if padrao > 0:
        instrucao += f"1. Digite o código: **{cod}** (Lote Padrão)\n"
        instrucao += f"   Quantidade: **{padrao}**\n"
        instrucao += f"   Preço: A Mercado\n\n"

    if frac > 0:
        prefixo = "2." if padrao > 0 else "1."
        instrucao += f"{prefixo} Digite o código: **{cod}F** (Fracionário)\n"
        instrucao += f"   Quantidade: **{frac}**\n"
        instrucao += f"   Preço: A Mercado\n\n"
    
    instrucao += f"*(Motivo da escolha: {ativo['Status']})*\n"
    
    return instrucao

def main():
    if not check_password(): return

    st.set_page_config(page_title="Robô Tridente V.48", page_icon="🔱", layout="wide")
    
    # CSS MÍNIMO PARA CORREÇÃO DE FUNDO E TEXTO
    st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    h1, h2, h3, h4 { color: #00ff88 !important; }
    p, span, div, li { color: #f0f0f0; } /* Garante texto claro */
    </style>
    """, unsafe_allow_html=True)

    # CABEÇALHO (O mais fiel ao terminal)
    st.title("🔱 ROBÔ TRIDENTE V.48")
    st.markdown("### Guia de Operação Profissional")
    st.markdown(f"**Data da Análise:** {datetime.now().strftime('%d/%m/%Y')}")
    st.divider()

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
    # 1. VENDAS (PASSO 1)
    # ==========================================================================
    st.markdown("## 1️⃣ PASSO 1: FAZER CAIXA (VENDER)")
    
    if not vendas.empty:
        st.warning("⚠️ Venda estes ativos para liberar caixa.")
        
        cols = st.columns(3)
        for idx, row in enumerate(vendas.to_dict('records')):
            with cols[idx % 3]:
                st.error(f"❌ {row['Ticker']}\n\nMotivo: {row['Status']}\n\nPreço Ref: R$ {row['Preco']:.2f}")
    else:
        st.success("✅ Nenhuma venda necessária.")

    st.markdown("---")

    # ==========================================================================
    # 2. COMPRAS (PASSO 2) - VISUAL FIEL
    # ==========================================================================
    st.subheader("2️⃣ PASSO 2: COMPRAR NOVOS ATIVOS")
    
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
                
                # Monta a instrução formatada
                instrucao_completa = formatar_instrucao_boleta(ativo, alo, qtd, padrao, frac, cod)
                
                # Exibe o card com o texto puro, garantindo a fidelidade do layout
                with st.container(border=True):
                    st.markdown(instrucao_completa)
                    st.button(f"✅ COMPRAR {ativo['Ticker']}", key=f"btn_{i}")
        
        # Nota de Sozinho
        sobra_vagas = 3 - len(final)
        if sobra_vagas > 0:
            val_sobra = capital * (sobra_vagas/3)
            st.info(f"⚠️ NOTA: {sobra_vagas} vaga(s) não preenchida(s). Aloque R$ {val_sobra:,.2f} no Caixa ({ATIVO_CAIXA}).")

    # 3. TABELA
    st.markdown("---")
    with st.expander("🔍 Espião (Tabela Técnica Completa)"):
        st.dataframe(df.style.map(lambda x: 'color:#ff4444' if 'VENDA' in str(x) else ('color:#00ff88' if 'COMPRA' in str(x) else 'color:#aaa'), subset=['Acao']))

if __name__ == "__main__":
    main()
