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

    st.markdown("## 🔐 Acesso Restrito - Robô Tridente V.34")
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
# Lógica 100% preservada do backtest validado.

ATIVO_CAIXA = 'B5P211.SA'

CATALOGO = {
    # --- DEFESA (SEGURANÇA MÁXIMA) ---
    'IVVB11.SA': {'MM': 40, 'RSI_MAX': 70, 'DIST_MAX': 0.20, 'VOL_LIMIT': 0.4},
    'GOLD11.SA': {'MM': 16, 'RSI_MAX': 70, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.4},
    'B5P211.SA': {'MM': 4 , 'RSI_MAX': 75, 'DIST_MAX': 0.10, 'VOL_LIMIT': 0.4},

    # --- ATAQUE (RETORNO vs RISCO) ---
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
            
            # 1. Indicadores (Lógica Exata V.31)
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

            # 2. Score
            if t in ATAQUE:
                safe_vol = vol if vol > 0.01 else 0.01
                score = roc / safe_vol
            else:
                safe_vol = vol if vol > 0.01 else 0.01
                score = 1 / safe_vol

            # 3. Julgamento (Filtros Rigorosos V.31)
            acao = "COMPRA"
            status = f"SCORE {score:.2f}"
            tipo = "⚔️ ATAQUE" if t in ATAQUE else "🛡️ DEFESA"
            
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
# 🎨 INTERFACE VISUAL (CSS + LAYOUT PROFISSIONAL)
# ==============================================================================
def main():
    if not check_password(): return

    st.set_page_config(page_title="Robô Tridente V.34", page_icon="🔱", layout="wide")
    
    # CSS: Cards Neon para Venda e Cards Verdes para Compra
    st.markdown("""
    <style>
    .main-header { font-size: 34px; font-weight: 800; color: #fff; text-align: center; margin-bottom: 5px; }
    .sub-header { font-size: 16px; color: #888; text-align: center; margin-bottom: 30px; }
    
    /* CARD VENDA (Alerta) */
    .card-sell {
        background: linear-gradient(135deg, #2b0e0e 0%, #3a0000 100%);
        border: 1px solid #ff4444; border-radius: 12px; padding: 15px; margin-bottom: 15px; color: white;
    }
    .sell-title { color: #ff6666; font-size: 20px; font-weight: 900; margin-bottom: 5px; }
    .sell-reason { font-size: 12px; background: rgba(255,0,0,0.2); padding: 3px 8px; border-radius: 4px; display: inline-block; }

    /* CARD COMPRA (Layout Profissional) */
    .card-buy {
        background-color: #0e1117; border: 1px solid #2e7d32; border-radius: 16px; overflow: hidden; margin-bottom: 25px;
    }
    .buy-header {
        background: linear-gradient(90deg, #0d3a15 0%, #1b5e20 100%); padding: 15px 20px;
        display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #2e7d32;
    }
    .buy-ticker { font-size: 24px; font-weight: 900; color: #fff; margin: 0; }
    .buy-tag { background: #000; color: #4caf50; padding: 4px 10px; border-radius: 10px; font-size: 11px; font-weight: bold; }
    
    .buy-body { padding: 20px; }
    .financial-row { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 20px; }
    .money-val { font-size: 28px; font-weight: 800; color: #4caf50; line-height: 1; }
    .money-lbl { font-size: 12px; color: #aaa; text-transform: uppercase; }
    
    /* A BOLETA (A Parte Mais Importante) */
    .boleta-container { background-color: #161b22; border-radius: 10px; padding: 15px; border-left: 4px solid #4caf50; }
    .boleta-header { color: #fff; font-size: 14px; font-weight: bold; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }
    
    .boleta-row { display: flex; justify-content: space-between; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px dashed #333; }
    .boleta-row:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
    
    .boleta-label { font-size: 13px; color: #888; }
    .boleta-value { font-size: 15px; color: #fff; font-weight: 700; font-family: monospace; }
    .boleta-btn { text-align: center; margin-top: 15px; background: #238636; color: white; padding: 8px; border-radius: 6px; font-size: 14px; font-weight: bold; }
    
    .alert-box { background: #2b210e; border: 1px solid #e6b800; padding: 15px; border-radius: 8px; color: #e6b800; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

    # HEADER
    st.markdown("<div class='main-header'>🔱 ROBÔ TRIDENTE V.34</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Painel de Execução Profissional | Equal Weight Strategy</div>", unsafe_allow_html=True)

    # SIDEBAR
    with st.sidebar:
        st.header("💰 Seu Capital")
        st.caption("Atualize este valor todo mês.")
        capital = st.number_input("Patrimônio Total (R$)", min_value=0.0, value=2000.0, step=100.0)
        
        if st.button("🔄 Rodar Análise"):
            st.cache_data.clear()
            st.rerun()
        st.markdown("---")
        st.info("💡 **Dica:** A estratégia V.31 usa alocação igualitária (33%) para proteger seu patrimônio contra quedas bruscas.")

    # PROCESSAMENTO
    with st.spinner('📡 Conectando à B3 e calculando indicadores...'):
        df = get_data_and_calculate()

    if df.empty:
        st.error("❌ Falha na conexão. Tente novamente mais tarde.")
        return

    # SEPARAÇÃO
    vendas = df[df['Acao'] == 'VENDA']
    compras_ataque = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == '⚔️ ATAQUE')].sort_values('Score', ascending=False)
    compras_defesa = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == '🛡️ DEFESA')].sort_values('Score', ascending=False)

    carteira_final = []
    carteira_final.extend(compras_ataque.head(3).to_dict('records'))
    vagas = 3 - len(carteira_final)
    if vagas > 0: carteira_final.extend(compras_defesa.head(vagas).to_dict('records'))

    # ==========================================================================
    # 1. ALERTAS DE VENDA
    # ==========================================================================
    if not vendas.empty:
        st.markdown("### 1️⃣ ALERTAS DE VENDA (FAZER CAIXA)")
        st.write("Verifique sua carteira. Se você tem algum destes ativos, venda hoje.")
        cols = st.columns(3)
        for idx, row in enumerate(vendas.to_dict('records')):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class='card-sell'>
                    <div style='float:right; font-size:20px;'>❌</div>
                    <div class='sell-title'>{row['Ticker']}</div>
                    <div style='margin-bottom:8px'>Ref: <b>R$ {row['Preco']:.2f}</b></div>
                    <div class='sell-reason'>{row['Status']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.success("✅ Nenhuma venda necessária hoje.")

    # ==========================================================================
    # 2. NOVAS COMPRAS (COM CÁLCULO DE BOLETA)
    # ==========================================================================
    st.markdown("---")
    st.markdown("### 2️⃣ NOVAS COMPRAS (PASSO A PASSO)")
    
    if not carteira_final:
        st.markdown(f"""
        <div class='alert-box'>
            🛑 MERCADO PERIGOSO<br>
            Nenhuma oportunidade segura encontrada.<br>
            Fique 100% no CAIXA ({ATIVO_CAIXA}) até o próximo mês.
        </div>
        """, unsafe_allow_html=True)
    else:
        peso = 1.0 / len(carteira_final)
        
        # Grid Responsivo
        cols = st.columns(len(carteira_final))
        
        for i, ativo in enumerate(carteira_final):
            with cols[i]:
                # CÁLCULOS MATEMÁTICOS DETALHADOS
                alocacao = capital * peso
                qtd_total = int(alocacao / ativo['Preco'])
                
                # Divisão Lote Padrão vs Fracionário
                lotes_padrao = qtd_total // 100
                qtd_padrao = lotes_padrao * 100
                qtd_frac = qtd_total % 100
                ticker_limpo = ativo['Ticker'].replace('.SA', '')
                
                # Construção do HTML da Boleta (A parte "Mágica")
                html_instrucoes = ""
                
                if qtd_padrao > 0:
                    html_instrucoes += f"""
                    <div class='boleta-row'>
                        <span class='boleta-label'>Opção 1 (Lote):</span>
                        <span class='boleta-value'>Comprar {qtd_padrao} de {ticker_limpo}</span>
                    </div>
                    """
                
                if qtd_frac > 0:
                    label = "Opção 2 (Resto):" if qtd_padrao > 0 else "Opção Única:"
                    html_instrucoes += f"""
                    <div class='boleta-row'>
                        <span class='boleta-label'>{label}</span>
                        <span class='boleta-value'>Comprar {qtd_frac} de {ticker_limpo}F</span>
                    </div>
                    """
                
                # Renderiza o Card Completo
                st.markdown(f"""
                <div class='card-buy'>
                    <div class='buy-header'>
                        <div>
                            <div style='font-size:12px; color:#a5d6a7; font-weight:bold;'>RANK #{i+1}</div>
                            <div class='buy-ticker'>{ativo['Ticker']}</div>
                        </div>
                        <div class='buy-tag'>{ativo['Tipo']}</div>
                    </div>
                    
                    <div class='buy-body'>
                        <div class='financial-row'>
                            <div>
                                <div class='money-lbl'>Valor a Investir</div>
                                <div class='money-val'>R$ {alocacao:,.0f}</div>
                            </div>
                            <div style='text-align:right'>
                                <div class='money-lbl'>Preço Ref</div>
                                <div style='color:white; font-weight:bold;'>R$ {ativo['Preco']:.2f}</div>
                            </div>
                        </div>
                        
                        <div class='boleta-container'>
                            <div class='boleta-header'>📝 NA SUA CORRETORA:</div>
                            {html_instrucoes}
                            <div class='boleta-row' style='margin-top:10px; border-top:1px solid #333; paddingTop:10px;'>
                                <span class='boleta-label'>Preço da Ordem:</span>
                                <span class='boleta-value' style='color:#4caf50'>A Mercado</span>
                            </div>
                        </div>
                        
                        <div style='text-align:center; margin-top:15px; font-size:11px; color:#666;'>
                            Motivo: {ativo['Status']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ==========================================================================
    # 3. TABELA ESPIÃO
    # ==========================================================================
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🔍 Ver Análise Técnica Completa (Tabela)"):
        st.dataframe(
            df[['Ticker', 'Acao', 'Preco', 'Score', 'ROC', 'RSI', 'Status']].style.map(
                lambda x: 'color: #ff4b4b' if 'VENDA' in str(x) else ('color: #4caf50' if 'COMPRA' in str(x) else 'color: #ffbd45'), 
                subset=['Acao']
            ), 
            use_container_width=True
        )

if __name__ == "__main__":
    main()
