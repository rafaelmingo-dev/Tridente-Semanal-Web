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
# ATENÇÃO: Esta é a lógica exata validada no backtest de 5 anos.
# Não altere os parâmetros abaixo para manter a consistência estatística.

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
        # Download Otimizado
        data = yf.download(TICKERS, start=start, interval='1wk', progress=False, group_by='ticker', auto_adjust=True)
    except:
        return []

    for t in TICKERS:
        try:
            # Tratamento de dados
            df = data[t].dropna()
            if len(df) < 52: continue
            
            close = df['Close']
            P = CATALOGO[t]
            
            # Cálculo de Indicadores (Fiel ao Backtest V.31)
            atual = float(close.iloc[-1])
            sma = close.rolling(P['MM']).mean().iloc[-1]
            dist = (atual / sma) - 1
            vol = close.pct_change().std() * np.sqrt(52)
            roc = ((atual / float(close.iloc[-12])) - 1) * 100
            
            # RSI Clássico 14
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            rsi_val = rsi.iloc[-1]

            # Score (Eficiência para Ataque, Estabilidade para Defesa)
            if t in ATAQUE:
                safe_vol = vol if vol > 0.01 else 0.01
                score = roc / safe_vol
            else:
                safe_vol = vol if vol > 0.01 else 0.01
                score = 1 / safe_vol

            # Julgamento V.31 (Filtros Rigorosos)
            acao = "COMPRA"
            status = f"SCORE {score:.2f}"
            tipo = "⚔️ ATAQUE" if t in ATAQUE else "🛡️ DEFESA"
            
            # 1. Filtro de Tendência (Média)
            if dist < 0: 
                acao = "VENDA"; status = f"ABAIXO DA MÉDIA (MM{P['MM']})"
            # 2. Filtro de Risco (Volatilidade)
            elif vol > P['VOL_LIMIT']: 
                acao = "VENDA"; status = f"RISCO ALTO (Vol {vol:.2f})"
            # 3. Filtro de Topo (RSI)
            elif rsi_val > P['RSI_MAX']: 
                acao = "NEUTRO"; status = f"RSI ESTICADO ({rsi_val:.0f})"
            # 4. Filtro de Topo (Distância da Média - CRUCIAL V.31)
            elif dist > P['DIST_MAX']: 
                acao = "NEUTRO"; status = f"PREÇO ESTICADO (+{dist:.1%})"
            # 5. Filtro de Momentum (Apenas para Ataque)
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
# 🎨 INTERFACE VISUAL PRO (CSS + LAYOUT)
# ==============================================================================
def main():
    if not check_password():
        return

    st.set_page_config(page_title="Robô Tridente V.34", page_icon="🔱", layout="wide")
    
    # CSS Profissional (Cards Neon, Degradês e Fontes)
    st.markdown("""
    <style>
    /* Tipografia e Estrutura */
    .main-header { font-size: 34px; font-weight: 800; color: #ffffff; text-align: center; margin-bottom: 5px; letter-spacing: -1px; }
    .sub-header { font-size: 16px; color: #888; text-align: center; margin-bottom: 30px; font-weight: 400; }
    
    /* Separadores de Seção */
    .section-title { 
        font-size: 22px; font-weight: 700; color: #fff; 
        margin-top: 40px; margin-bottom: 15px; 
        border-left: 5px solid #f63366; padding-left: 15px; 
        background: linear-gradient(90deg, rgba(246,51,102,0.1) 0%, rgba(0,0,0,0) 100%);
    }

    /* CARD DE VENDA (Alerta Máximo) */
    .card-sell {
        background: linear-gradient(135deg, #2b0e0e 0%, #3a0000 100%);
        border: 1px solid #ff3333;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(255, 50, 50, 0.15);
        color: white;
    }
    .sell-icon { font-size: 24px; float: right; }
    .sell-ticker { font-size: 22px; font-weight: 900; color: #ff6666; margin-bottom: 5px; }
    .sell-reason { font-size: 13px; color: #ffcccc; background: rgba(255,0,0,0.2); padding: 4px 8px; border-radius: 4px; display: inline-block;}

    /* CARD DE COMPRA (Elegante e Didático) */
    .card-buy {
        background-color: #0e1117;
        border: 1px solid #2e7d32;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.1);
        margin-bottom: 25px;
    }
    .buy-header {
        background: linear-gradient(90deg, #0d3a15 0%, #1b5e20 100%);
        padding: 15px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #2e7d32;
    }
    .buy-rank { font-size: 12px; font-weight: bold; color: #a5d6a7; text-transform: uppercase; letter-spacing: 1px; }
    .buy-ticker { font-size: 26px; font-weight: 900; color: #fff; margin: 0; }
    .buy-tag { background: #000; color: #4caf50; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; border: 1px solid #4caf50; }
    
    .buy-body { padding: 20px; }
    .financial-box { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 20px; }
    .invest-label { font-size: 12px; color: #aaa; text-transform: uppercase; margin-bottom: 2px;}
    .invest-value { font-size: 32px; font-weight: 800; color: #4caf50; line-height: 1; }
    .price-value { font-size: 14px; color: #fff; text-align: right; }

    /* A ÁREA DE INSTRUÇÃO DETALHADA (O Pulo do Gato) */
    .instruction-box {
        background-color: #161b22;
        border-radius: 10px;
        padding: 15px;
        border-left: 4px solid #4caf50;
        margin-top: 10px;
    }
    .inst-title { color: #fff; font-size: 14px; font-weight: bold; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }
    .inst-row { display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 14px; color: #ddd; border-bottom: 1px dashed #333; padding-bottom: 4px;}
    .inst-row:last-child { border-bottom: none; }
    .inst-val { font-weight: 700; color: #fff; font-family: monospace; font-size: 15px; }
    .inst-action { text-align: center; margin-top: 10px; background: #238636; color: white; padding: 8px; border-radius: 6px; font-weight: bold; font-size: 14px; }
    
    .divider { height: 1px; background: #30363d; margin: 15px 0; }
    </style>
    """, unsafe_allow_html=True)

    # HEADER PRINCIPAL
    st.markdown("<div class='main-header'>🔱 ROBÔ TRIDENTE V.34</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Painel de Execução Profissional | Equal Weight Strategy</div>", unsafe_allow_html=True)

    # SIDEBAR
    with st.sidebar:
        st.header("💰 Seu Capital")
        st.caption("Atualize este valor mensalmente.")
        capital = st.number_input("Patrimônio Total (R$)", min_value=0.0, value=2000.0, step=100.0)
        
        if st.button("🔄 Rodar Análise"):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.info("💡 **Dica:** A estratégia V.31 usa alocação igualitária (33% em cada ativo) para reduzir o risco de drawdown.")

    # PROCESSAMENTO DE DADOS
    with st.spinner('📡 Conectando à B3 e calculando indicadores V.31...'):
        df = get_data_and_calculate()

    if df.empty:
        st.error("❌ Falha na conexão com dados de mercado. Tente novamente mais tarde.")
        return

    # LÓGICA DE ALOCAÇÃO
    vendas = df[df['Acao'] == 'VENDA']
    compras_ataque = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == '⚔️ ATAQUE')].sort_values('Score', ascending=False)
    compras_defesa = df[(df['Acao'] == 'COMPRA') & (df['Tipo'] == '🛡️ DEFESA')].sort_values('Score', ascending=False)

    carteira_final = []
    carteira_final.extend(compras_ataque.head(3).to_dict('records'))
    vagas = 3 - len(carteira_final)
    if vagas > 0:
        carteira_final.extend(compras_defesa.head(vagas).to_dict('records'))

    # ==========================================================================
    # SEÇÃO 1: VENDAS (RED NEON CARDS)
    # ==========================================================================
    st.markdown("<div class='section-title'>1️⃣ ALERTAS DE VENDA (FAZER CAIXA)</div>", unsafe_allow_html=True)
    
    if not vendas.empty:
        st.markdown("**Verifique sua carteira.** Se você possui algum destes ativos, a recomendação é encerrar a posição.")
        cols = st.columns(3)
        for idx, row in enumerate(vendas.to_dict('records')):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class='card-sell'>
                    <div class='sell-icon'>❌</div>
                    <div class='sell-ticker'>{row['Ticker']}</div>
                    <div style='margin-bottom:10px;'>Preço Ref: <b>R$ {row['Preco']:.2f}</b></div>
                    <div class='sell-reason'>{row['Status']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.success("✅ Nenhuma venda técnica necessária. Sua carteira atual está saudável.")

    # ==========================================================================
    # SEÇÃO 2: COMPRAS (GREEN PRO CARDS COM INSTRUÇÃO DETALHADA)
    # ==========================================================================
    st.markdown("<div class='section-title'>2️⃣ NOVAS COMPRAS (PASSO A PASSO)</div>", unsafe_allow_html=True)
    
    if not carteira_final:
        st.error("🛑 NENHUMA OPORTUNIDADE SEGURA ENCONTRADA.")
        st.write(f"A melhor posição hoje é estar 100% Líquido em **{ATIVO_CAIXA}** ou Tesouro Selic.")
    else:
        peso = 1.0 / len(carteira_final)
        
        # Grid Responsivo
        cols = st.columns(len(carteira_final))
        
        for i, ativo in enumerate(carteira_final):
            with cols[i]:
                # Cálculos Financeiros
                alocacao = capital * peso
                qtd_total = int(alocacao / ativo['Preco'])
                ticker_limpo = ativo['Ticker'].replace('.SA', '')
                
                # Lógica de Lotes
                lotes_padrao = qtd_total // 100
                qtd_padrao = lotes_padrao * 100
                qtd_frac = qtd_total % 100
                
                # Construção do HTML do Card
                html_lote_padrao = ""
                html_lote_frac = ""
                
                if qtd_padrao > 0:
                    html_lote_padrao = f"""
                    <div style='margin-bottom: 10px;'>
                        <div class='inst-row'><span style='color:#888'>Opção 1: Lote Padrão</span></div>
                        <div class='inst-row'><span>Código:</span> <span class='inst-val'>{ticker_limpo}</span></div>
                        <div class='inst-row'><span>Quantidade:</span> <span class='inst-val'>{qtd_padrao}</span></div>
                    </div>
                    """
                
                if qtd_frac > 0:
                    label = "Opção 2: Complemento (Fracionário)" if qtd_padrao > 0 else "Opção Única: Fracionário"
                    divider = "<div class='divider'></div>" if qtd_padrao > 0 else ""
                    html_lote_frac = f"""
                    {divider}
                    <div>
                        <div class='inst-row'><span style='color:#888'>{label}</span></div>
                        <div class='inst-row'><span>Código:</span> <span class='inst-val'>{ticker_limpo}F</span></div>
                        <div class='inst-row'><span>Quantidade:</span> <span class='inst-val'>{qtd_frac}</span></div>
                    </div>
                    """
                
                # Card Completo
                st.markdown(f"""
                <div class='card-buy'>
                    <div class='buy-header'>
                        <div>
                            <div class='buy-rank'>RANK #{i+1}</div>
                            <div class='buy-ticker'>{ativo['Ticker']}</div>
                        </div>
                        <div class='buy-tag'>{ativo['Tipo']}</div>
                    </div>
                    
                    <div class='buy-body'>
                        <div class='financial-box'>
                            <div>
                                <div class='invest-label'>Investir</div>
                                <div class='invest-value'>R$ {alocacao:,.0f}</div>
                            </div>
                            <div class='price-value'>
                                Preço: R$ {ativo['Preco']:.2f}<br>
                                <span style='font-size:10px; color:#aaa'>{ativo['Status']}</span>
                            </div>
                        </div>
                        
                        <div class='instruction-box'>
                            <div class='inst-title'>📝 NA SUA CORRETORA</div>
                            {html_lote_padrao}
                            {html_lote_frac}
                            <div class='inst-action'>👉 ENVIAR ORDEM DE COMPRA</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ==========================================================================
    # SEÇÃO 3: ESPIÃO TÉCNICO
    # ==========================================================================
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🔍 Ver Detalhes Técnicos de Todos os Ativos (Espião)"):
        st.dataframe(
            df[['Ticker', 'Acao', 'Preco', 'Score', 'ROC', 'RSI', 'Status']].style.map(
                lambda x: 'color: #ff4b4b' if 'VENDA' in str(x) else ('color: #4caf50' if 'COMPRA' in str(x) else 'color: #ffbd45'), 
                subset=['Acao']
            ), 
            use_container_width=True
        )

if __name__ == "__main__":
    main()
