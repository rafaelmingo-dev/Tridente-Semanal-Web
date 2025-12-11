from http.server import BaseHTTPRequestHandler
import json
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

CONFIG = {
    'ativo_seguranca': 'B5P211.SA',
    'anos_historico': 5,
    'peso_ouro': 0.50,
    'peso_prata': 0.35,
    'peso_bronze': 0.15,
}

CATALOGO = {
    'HASH11.SA': {'MM': 30,  'RSI_MAX': 75, 'DIST_MAX': 0.25, 'VOL_IDEAL': 0.8},
    'KEPL3.SA':  {'MM': 30,  'RSI_MAX': 70, 'DIST_MAX': 0.20, 'VOL_IDEAL': 0.5},
    'PETR4.SA':  {'MM': 250, 'RSI_MAX': 70, 'DIST_MAX': 0.20, 'VOL_IDEAL': 0.8},
    'BPAC11.SA': {'MM': 60,  'RSI_MAX': 70, 'DIST_MAX': 0.20, 'VOL_IDEAL': 0.5},
    'ELET3.SA':  {'MM': 30,  'RSI_MAX': 70, 'DIST_MAX': 0.20, 'VOL_IDEAL': 0.8},
    'VBBR3.SA':  {'MM': 60,  'RSI_MAX': 70, 'DIST_MAX': 0.20, 'VOL_IDEAL': 0.5},
    'CPLE6.SA':  {'MM': 60,  'RSI_MAX': 70, 'DIST_MAX': 0.20, 'VOL_IDEAL': 0.3},
    'CYRE3.SA':  {'MM': 40,  'RSI_MAX': 70, 'DIST_MAX': 0.20, 'VOL_IDEAL': 0.5},
    'CMIG4.SA':  {'MM': 250, 'RSI_MAX': 70, 'DIST_MAX': 0.20, 'VOL_IDEAL': 0.6},
    'WEGE3.SA':  {'MM': 100, 'RSI_MAX': 70, 'DIST_MAX': 0.20, 'VOL_IDEAL': 0.4},
    'VALE3.SA':  {'MM': 60,  'RSI_MAX': 70, 'DIST_MAX': 0.20, 'VOL_IDEAL': 0.4},
    'RADL3.SA':  {'MM': 40,  'RSI_MAX': 50, 'DIST_MAX': 0.20, 'VOL_IDEAL': 0.5},
    'IVVB11.SA': {'MM': 40,  'RSI_MAX': 75, 'DIST_MAX': 0.20, 'VOL_IDEAL': 0.3},
    'B5P211.SA': {'MM': 150, 'RSI_MAX': 80, 'DIST_MAX': 0.10, 'VOL_IDEAL': 0.1},
    'GOLD11.SA': {'MM': 150, 'RSI_MAX': 70, 'DIST_MAX': 0.20, 'VOL_IDEAL': 0.3},
}

TICKERS = list(CATALOGO.keys())

def obter_dados(ticker):
    dias = (CONFIG['anos_historico'] * 365) + 200
    start = (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d')
    try:
        df = yf.download(ticker, start=start, progress=False, auto_adjust=True)
        if df.empty or len(df) < 252:
            return None
        if isinstance(df.columns, pd.MultiIndex):
            try:
                return df.xs(ticker, level=1, axis=1)['Close']
            except:
                return df.iloc[:, 0]
        return df['Close']
    except:
        return None

def calcular_score(ticker, prices):
    if ticker not in CATALOGO:
        return None
    PARAMS = CATALOGO[ticker]
    try:
        prices = pd.to_numeric(prices, errors='coerce').dropna()
        atual = float(prices.iloc[-1])
        sma = prices.rolling(PARAMS['MM']).mean().iloc[-1]
        dist = (atual / sma) - 1
        vol = prices.pct_change().dropna().std() * np.sqrt(252)
        roc = 0.0
        if len(prices) > 60:
            roc = ((atual / float(prices.iloc[-60])) - 1) * 100
        delta = prices.diff(1)
        up = delta.where(delta > 0, 0).rolling(14).mean()
        down = -delta.where(delta < 0, 0).rolling(14).mean()
        if down.iloc[-1] == 0:
            rsi = 100
        else:
            rsi = 100 - (100 / (1 + up.iloc[-1]/down.iloc[-1]))
        return {
            'Ticker': ticker, 'Preco': round(atual, 2), 'ROC': round(roc, 2),
            'Dist': round(dist, 4), 'Vol': round(vol, 4), 'RSI': round(rsi, 1),
            'MM': PARAMS['MM'], 'RSI_MAX': PARAMS['RSI_MAX'],
            'DIST_MAX': PARAMS['DIST_MAX'], 'VOL_IDEAL': PARAMS['VOL_IDEAL']
        }
    except:
        return None

def julgar_ativo(d):
    if d['Dist'] < 0:
        return "VENDA", f"ABAIXO DA MÉDIA (MM{d['MM']})"
    if d['Vol'] > d['VOL_IDEAL']:
        return "VENDA", "RISCO ALTO"
    if d['RSI'] > d['RSI_MAX'] or d['Dist'] > d['DIST_MAX']:
        return "NEUTRO", f"ESTICADO (RSI {d['RSI']:.0f})"
    if d['ROC'] > 0:
        return "COMPRA", "FORTE"
    return "NEUTRO", "SEM FORÇA"

def analisar_mercado():
    carteira = []
    for ticker in TICKERS:
        try:
            prices = obter_dados(ticker)
            if prices is not None:
                dados = calcular_score(ticker, prices)
                if dados:
                    acao, status = julgar_ativo(dados)
                    dados['Acao'] = acao
                    dados['Status'] = status
                    carteira.append(dados)
        except:
            continue
    carteira = sorted(carteira, key=lambda x: x['ROC'], reverse=True)
    return {'success': True, 'data': carteira, 'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M'), 'config': CONFIG}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        try:
            resultado = analisar_mercado()
            self.wfile.write(json.dumps(resultado).encode())
        except Exception as e:
            self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode())
