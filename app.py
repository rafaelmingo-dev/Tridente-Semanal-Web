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
    
    st.markdown("## 🔐 Robô Tridente V.45")
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
# 🎨 UI V.45 (TERMINAL-LIKE SIMULATION)
# ==============================================================================
def main():
    if not check_password(): return

    st.set_page_config(page_title="Robô Tridente V.45", page_icon="🔱", layout="wide")
    
    # CSS PARA CONTRASTE
    st.markdown("""
    <style>
    .stApp { background-color: #000000; } /* Fundo Preto Puro */
    h1, h2, h3, h4 { color: #00ff88 !important; } /* Texto principal Verde Neon */
    
    /* Bloco de Terminal/Instrução */
    .terminal-box {
        background-color: #111; /* Cinza bem escuro para fundo do terminal */
        border: 1px solid #333;
        border-radius: 8px;
        padding: 15px;
        margin-top: 15px;
        font-family: 'Courier New', monospace;
        color: #ddd; /* Texto cinza claro */
    }
    .terminal-line { margin-bottom: 5px; line-height: 1.5; }
    .terminal-accent { color: #00ff88; font-weight: bold; } /* Destaque Verde Neon */
    .terminal-error { color: #ff4444; font-weight: bold; } /* Destaque Vermelho */
    </style>
    """, unsafe_allow_html=True)

    st.title("🔱 ROBÔ TRIDENTE V.45")
    st.markdown("### Painel de Execução Profissional")
    st.divider()

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

    # CONSTRUÇÃO DO GUIA EM TEXTO FORMATADO (SIMULAÇÃO DO TERMINAL)
    guia_html = ""
    
    # === PASSO 1: VENDAS ===
    guia_html += "<h4>1️⃣ PASSO 1: FAZER CAIXA (VENDER)</h4>"
    if not vendas.empty:
        guia_html += "<p>Verifique sua carteira atual. Se você tiver algum destes ativos, <span class='terminal-error'>VENDA TUDO</span>.</p>"
        guia_html += "<p style='margin-left: 20px;'>"
        for row in vendas.to_dict('records'):
            guia_html += f"❌ <span class='terminal-error'>{row['Ticker']}</span> &rarr; Motivo: {row['Status']}<br>"
        guia_html += "💵 O dinheiro dessas vendas será usado no Passo 2.</p>"
    else:
        guia_html += "<p>✅ Nenhuma venda necessária. Seus ativos atuais continuam bons.</p>"
    
    guia_html += "<hr style='border-color:#333;'>"
    
    # === PASSO 2: COMPRAS ===
    guia_html += f"<h4>2️⃣ PASSO 2: COMPRAR NOVOS ATIVOS</h4>"
    guia_html += f"<p>Vamos distribuir seus <span class='terminal-accent'>R$ {capital:,.2f}</span> igualmente nos {len(final) if final else 0} melhores ativos.</p>"

    if not final:
        guia_html += f"<p style='color:red'>🛑 PARE TUDO. Mercado perigoso. 👉 AÇÃO: Deixe 100% no {ATIVO_CAIXA}.</p>"
    else:
        peso = 1.0 / len(final)
        
        for i, ativo in enumerate(final):
            alo = capital * peso
            qtd = int(alo / ativo['Preco'])
            padrao = (qtd // 100) * 100
            frac = qtd % 100
            cod = ativo['Ticker'].replace('.SA', '')
            
            guia_html += f"<br>"
            guia_html += f"<p style='font-size:16px; font-weight:bold; color:white;'>🏆 RANK #{i+1}: {ativo['Ticker']} ({ativo['Tipo']})</p>"
            guia_html += f"<p style='margin-left: 20px;'>"
            guia_html += f"💰 Valor para investir: <span class='terminal-accent'>R$ {alo:,.2f}</span><br>"
            guia_html += f"📊 Preço Atual: R$ {ativo['Preco']:.2f}<br>"
            guia_html += f"📝 **COMO PREENCHER A ORDEM (BOLETA):**<br>"
            
            # --- DETALHE DA BOLETA (Recria o visual do terminal) ---
            if padrao > 0:
                guia_html += f"&nbsp;&nbsp;&nbsp;&nbsp;[1] Código: <span class='terminal-accent'>{cod}</span> (Lote Padrão)<br>"
                guia_html += f"&nbsp;&nbsp;&nbsp;&nbsp;Quantidade: <span class='terminal-accent'>{padrao}</span><br>"
            
            if frac > 0:
                prefixo = "[2]" if padrao > 0 else "[1]"
                guia_html += f"&nbsp;&nbsp;&nbsp;&nbsp;{prefixo} Código: <span class='terminal-accent'>{cod}F</span> (Fracionário)<br>"
                guia_html += f"&nbsp;&nbsp;&nbsp;&nbsp;Quantidade: <span class='terminal-accent'>{frac}</span><br>"
            
            guia_html += f"&nbsp;&nbsp;&nbsp;&nbsp;Preço: A Mercado &rarr; **CLIQUE EM COMPRAR**<br>"
            guia_html += f"&nbsp;&nbsp;&nbsp;&nbsp;(Motivo: {ativo['Status']})</p>"
            
        # === NOTA FINAL ===
        sobra_vagas = 3 - len(final)
        if sobra_vagas > 0:
            val_sobra = capital * (sobra_vagas/3)
            guia_html += f"<br><p>⚠️ **NOTA:** {sobra_vagas} vaga(s) não preenchida(s)."
            guia_html += f" 👉 Aloque R$ <span class='terminal-accent'>{val_sobra:,.2f}</span> no Caixa ({ATIVO_CAIXA}).</p>"

    # === RODAPÉ ===
    guia_html += "<hr style='border-color:#333;'>"
    guia_html += "<p style='text-align:center'>🚀 OPERAÇÃO CONCLUÍDA. FECHE O APP E SÓ VOLTE MÊS QUE VEM!</p>"
    
    # RENDERIZAÇÃO FINAL NA TELA
    st.markdown(f"<div class='terminal-box'>{guia_html}</div>", unsafe_allow_html=True)
    
    # 3. TABELA
    st.markdown("---")
    with st.expander("🔍 Ver Tabela Técnica Completa"):
        st.dataframe(df.style.map(lambda x: 'color:#ff4444' if 'VENDA' in str(x) else ('color:#00ff88' if 'COMPRA' in str(x) else 'color:#aaa'), subset=['Acao']))

if __name__ == "__main__":
    main()
