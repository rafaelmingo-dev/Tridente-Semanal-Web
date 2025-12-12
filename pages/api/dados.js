export default async function handler(req, res) {
  const CATALOGO = {
    'HASH11.SA': { MM: 30, RSI_MAX: 75, DIST_MAX: 0.25, VOL_IDEAL: 0.8 },
    'KEPL3.SA': { MM: 30, RSI_MAX: 70, DIST_MAX: 0.20, VOL_IDEAL: 0.5 },
    'PETR4.SA': { MM: 250, RSI_MAX: 70, DIST_MAX: 0.20, VOL_IDEAL: 0.8 },
    'BPAC11.SA': { MM: 60, RSI_MAX: 70, DIST_MAX: 0.20, VOL_IDEAL: 0.5 },
    'ELET3.SA': { MM: 30, RSI_MAX: 70, DIST_MAX: 0.20, VOL_IDEAL: 0.8 },
    'VBBR3.SA': { MM: 60, RSI_MAX: 70, DIST_MAX: 0.20, VOL_IDEAL: 0.5 },
    'CPLE6.SA': { MM: 60, RSI_MAX: 70, DIST_MAX: 0.20, VOL_IDEAL: 0.3 },
    'CYRE3.SA': { MM: 40, RSI_MAX: 70, DIST_MAX: 0.20, VOL_IDEAL: 0.5 },
    'CMIG4.SA': { MM: 250, RSI_MAX: 70, DIST_MAX: 0.20, VOL_IDEAL: 0.6 },
    'WEGE3.SA': { MM: 100, RSI_MAX: 70, DIST_MAX: 0.20, VOL_IDEAL: 0.4 },
    'VALE3.SA': { MM: 60, RSI_MAX: 70, DIST_MAX: 0.20, VOL_IDEAL: 0.4 },
    'RADL3.SA': { MM: 40, RSI_MAX: 50, DIST_MAX: 0.20, VOL_IDEAL: 0.5 },
    'IVVB11.SA': { MM: 40, RSI_MAX: 75, DIST_MAX: 0.20, VOL_IDEAL: 0.3 },
    'B5P211.SA': { MM: 150, RSI_MAX: 80, DIST_MAX: 0.10, VOL_IDEAL: 0.1 },
    'GOLD11.SA': { MM: 150, RSI_MAX: 70, DIST_MAX: 0.20, VOL_IDEAL: 0.3 },
  };

  const TICKERS = Object.keys(CATALOGO);

  const calcularRSI = (prices, period = 14) => {
    if (prices.length < period + 1) return 50;
    let gains = 0, losses = 0;
    for (let i = prices.length - period; i < prices.length; i++) {
      const diff = prices[i] - prices[i - 1];
      if (diff > 0) gains += diff;
      else losses -= diff;
    }
    if (losses === 0) return 100;
    const rs = gains / losses;
    return 100 - (100 / (1 + rs));
  };

  const julgarAtivo = (d) => {
    if (d.Dist < 0) return { acao: "VENDA", status: `ABAIXO DA MÉDIA (MM${d.MM})` };
    if (d.Vol > d.VOL_IDEAL) return { acao: "VENDA", status: "RISCO ALTO" };
    if (d.RSI > d.RSI_MAX || d.Dist > d.DIST_MAX) return { acao: "NEUTRO", status: `ESTICADO (RSI ${Math.round(d.RSI)})` };
    if (d.ROC > 0) return { acao: "COMPRA", status: "FORTE" };
    return { acao: "NEUTRO", status: "SEM FORÇA" };
  };

  try {
    const carteira = [];

    for (const ticker of TICKERS) {
      try {
        const params = CATALOGO[ticker];
        const url = `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?interval=1d&range=2y`;
        
        const response = await fetch(url, {
          headers: { 'User-Agent': 'Mozilla/5.0' }
        });
        
        const data = await response.json();
        
        if (data.chart?.result?.[0]) {
          const result = data.chart.result[0];
          const closes = result.indicators.quote[0].close.filter(c => c !== null);
          
          if (closes.length > params.MM && closes.length > 60) {
            const preco = closes[closes.length - 1];
            const sma = closes.slice(-params.MM).reduce((a, b) => a + b, 0) / params.MM;
            const dist = (preco / sma) - 1;
            
            const returns = [];
            for (let i = 1; i < closes.length; i++) {
              returns.push((closes[i] - closes[i-1]) / closes[i-1]);
            }
            const vol = Math.sqrt(returns.reduce((a, b) => a + b * b, 0) / returns.length) * Math.sqrt(252);
            
            const preco60 = closes[closes.length - 61];
            const roc = ((preco / preco60) - 1) * 100;
            
            const rsi = calcularRSI(closes);

            const dadosAtivo = {
              Ticker: ticker,
              Preco: Math.round(preco * 100) / 100,
              ROC: Math.round(roc * 100) / 100,
              Dist: Math.round(dist * 10000) / 10000,
              Vol: Math.round(vol * 10000) / 10000,
              RSI: Math.round(rsi * 10) / 10,
              MM: params.MM,
              RSI_MAX: params.RSI_MAX,
              DIST_MAX: params.DIST_MAX,
              VOL_IDEAL: params.VOL_IDEAL
            };

            const { acao, status } = julgarAtivo(dadosAtivo);
            dadosAtivo.Acao = acao;
            dadosAtivo.Status = status;
            carteira.push(dadosAtivo);
          }
        }
      } catch (e) {
        console.log(`Erro em ${ticker}:`, e.message);
      }
    }

    carteira.sort((a, b) => b.ROC - a.ROC);

    const now = new Date();
    const timestamp = now.toLocaleDateString('pt-BR') + ' ' + now.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });

    res.status(200).json({
      success: true,
      data: carteira,
      timestamp: timestamp
    });

  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
}
