import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
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
# ⚙️ LÓGICA DO ROBÔ (MATEMÁTICA V.31 - GOLDEN STANDARD)
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
    dias = (5 * 365)
    start = (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d')
    
    resultados = []
    
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
            
            # LÓGICA V.31 RIGOROSA
            if dist < 0: 
                acao = "VENDA"; status = f"ABAIXO DA MÉDIA (MM{P['MM']})"
            elif vol > P['VOL_LIMIT']: 
                acao = "VENDA"; status = f"RISCO ALTO (Vol {vol:.2f})"
            elif rsi_val > P['RSI_MAX']: 
                acao = "NEUTRO"; status = f"RSI ESTICADO ({rsi_val:.0f})"
            elif dist > P['DIST_MAX']: 
                acao = "NEUTRO"; status = f"PREÇO ESTICADO (+{dist:.1%})"
            elif t in ATAQUE and roc <= 0:
                acao = "NEUTRO"; status = "SEM FORÇA (ROC < 0)"
            
            resultados.append({
                'Ticker': t, 'Tipo': tipo, 'Preco': atual, 'Score': score,
                'Acao': acao, 'Status': status, 'ROC': roc, 'RSI': rsi_val
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
    
    # CSS Customizado para deixar mais bonito e legível
    st.markdown("""
    <style>
    .big-font { font-size:24px !important; font-weight: bold; }
    .step-box { background-color: #0e1117; padding: 20px; border-radius: 10px; border-left: 5px solid #ffbd45; margin-bottom: 20px; }
    .sell-box { background-color: #2b1111; padding: 15px; border-radius: 5px; border: 1px solid #ff4b4b; margin-bottom: 10px; }
    .buy-box { background-color: #112b16; padding: 20px; border-radius: 10px; border: 1px solid #2e7d32; margin-bottom: 20px; }
    .metric-label { font-size: 14px; color: #aaa; }
    .metric-value { font-size: 28px; font-weight: bold; color: #fff; }
    </style>
    """, unsafe_allow_html=True)

    st.title("🔱 Robô Tridente V.32 | Painel de Execução")
    st.markdown("Guia passo a passo para investidores iniciantes.")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("💰 Configuração de Capital")
        st.write("Insira o valor TOTAL que você tem hoje (Saldo na corretora + Valor das ações atuais).")
        capital = st.number_input("Patrimônio Total (R$)", min_value=0.0, value=2000.0, step=100.0)
        
        if st.button("🔄 Atualizar Diagnóstico"):
            st.cache_data.clear()
            st.rerun()
            
        st.info("💡 **Dica:** Rode este robô sempre na primeira semana do mês.")

    # Processamento
    with st.spinner('📡 O Robô está analisando os gráficos SEMANAIS...'):
        df = get_data_and_calculate()

    if df.empty:
        st.error("Erro ao conectar com a bolsa. Tente novamente em alguns minutos.")
        return

    # Separação
    vendas = df[df['Acao'] == 'VENDA']
    compras_ataque = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == '⚔️ ATAQUE')].sort_values('Score', ascending=False)
    compras_defesa = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == '🛡️ DEFESA')].sort_values('Score', ascending=False)

    carteira_final = []
    carteira_final.extend(compras_ataque.head(3).to_dict('records'))
    vagas = 3 - len(carteira_final)
    if vagas > 0:
        carteira_final.extend(compras_defesa.head(vagas).to_dict('records'))

    # ==========================================================================
    # 1️⃣ PASSO 1: VENDAS
    # ==========================================================================
    st.markdown("<div class='step-box'><span class='big-font'>1️⃣ PASSO 1: FAZER CAIXA (VENDER)</span></div>", unsafe_allow_html=True)
    
    if not vendas.empty:
        st.warning("⚠️ **ATENÇÃO:** O sistema detectou ativos que perderam a tendência. Se você tiver algum destes na carteira, **VENDA TUDO HOJE**.")
        
        cols = st.columns(3)
        for idx, row in enumerate(vendas.to_dict('records')):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class='sell-box'>
                    <h3 style='color: #ff4b4b; margin:0;'>❌ VENDER {row['Ticker']}</h3>
                    <p style='margin:0;'><b>Preço Ref:</b> R$ {row['Preco']:.2f}</p>
                    <p style='font-size:12px; margin:0;'>Motivo: {row['Status']}</p>
                </div>
                """, unsafe_allow_html=True)
        st.caption("ℹ️ Use o dinheiro dessas vendas para realizar as compras do Passo 2.")
    else:
        st.success("✅ **Nenhuma venda necessária.** Seus ativos atuais continuam fortes e seguros.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================================
    # 2️⃣ PASSO 2: COMPRAS
    # ==========================================================================
    st.markdown("<div class='step-box'><span class='big-font'>2️⃣ PASSO 2: COMPRAR NOVOS ATIVOS</span></div>", unsafe_allow_html=True)
    st.write(f"Vamos distribuir seu patrimônio de **R$ {capital:,.2f}** igualmente entre as 3 melhores oportunidades.")

    if not carteira_final:
        st.error("🛑 **MERCADO PERIGOSO!**")
        st.write("O robô não encontrou 3 ativos seguros hoje. A melhor proteção é ficar líquido.")
        st.info(f"👉 **AÇÃO RECOMENDADA:** Deixe 100% do seu dinheiro no **{ATIVO_CAIXA}** ou Tesouro Selic até o próximo mês.")
    else:
        peso = 1.0 / len(carteira_final)
        
        # Display em Colunas para facilitar leitura
        cols = st.columns(len(carteira_final))
        
        for i, ativo in enumerate(carteira_final):
            with cols[i]:
                alocacao = capital * peso
                qtd_total = int(alocacao / ativo['Preco'])
                
                # Cálculo de Lotes
                lotes_padrao = qtd_total // 100
                qtd_padrao = lotes_padrao * 100
                qtd_frac = qtd_total % 100
                ticker_limpo = ativo['Ticker'].replace('.SA', '')
                
                # Card de Compra
                st.markdown(f"""
                <div class='buy-box'>
                    <div style='text-align: center;'>
                        <h4 style='margin:0; color: #aaa;'>RANK #{i+1}</h4>
                        <h2 style='margin:0; color: #4caf50;'>{ativo['Ticker']}</h2>
                        <span style='background-color: #333; padding: 2px 8px; border-radius: 4px; font-size: 12px;'>{ativo['Tipo']}</span>
                    </div>
                    <hr style='border-color: #2e7d32;'>
                    <p style='text-align: center; font-size: 20px; font-weight: bold;'>Investir: R$ {alocacao:,.2f}</p>
                    <p style='text-align: center; font-size: 14px;'>Preço Atual: R$ {ativo['Preco']:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Instruções da Boleta (Igual ao terminal)
                st.markdown("##### 📝 **Na sua Corretora:**")
                
                tem_compra = False
                
                # Instrução 1: Lote Padrão
                if qtd_padrao > 0:
                    tem_compra = True
                    st.markdown(f"""
                    **Opção 1 (Lote Padrão):**
                    1. Digite o código: `{ticker_limpo}`
                    2. Quantidade: **{qtd_padrao}**
                    3. Preço: **A Mercado**
                    4. ✅ **COMPRAR**
                    """)
                
                # Instrução 2: Fracionário
                if qtd_frac > 0:
                    tem_compra = True
                    titulo = "Opção 2 (Complemento):" if qtd_padrao > 0 else "Opção Única (Fracionário):"
                    st.markdown(f"""
                    **{titulo}**
                    1. Digite o código: `{ticker_limpo}F`
                    2. Quantidade: **{qtd_frac}**
                    3. Preço: **A Mercado**
                    4. ✅ **COMPRAR**
                    """)
                
                if not tem_compra:
                    st.warning("⚠️ Saldo insuficiente para 1 ação.")
                
                st.caption(f"Motivo: {ativo['Status']}")

    # --- TELA 3: TABELA TÉCNICA (EXPANSÍVEL) ---
    st.markdown("<br><hr>", unsafe_allow_html=True)
    with st.expander("🔍 Espião: Ver Tabela Técnica de Todos os Ativos"):
        st.dataframe(
            df[['Ticker', 'Acao', 'Preco', 'Score', 'ROC', 'RSI', 'Status']].style.map(
                lambda x: 'color: #ff4b4b' if 'VENDA' in str(x) else ('color: #4caf50' if 'COMPRA' in str(x) else 'color: #ffbd45'), 
                subset=['Acao']
            ), 
            use_container_width=True
        )

if __name__ == "__main__":
    main()
