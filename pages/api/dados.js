// ==============================================================================
// 🔱 ROBÔ TRIDENTE V.32 | API BACKEND - 100% FIEL AO PYTHON
// ==============================================================================

export default async function handler(req, res) {
  
  // --- CONFIGURAÇÃO ---
  const ATIVO_CAIXA = 'B5P211.SA';

  // --- CATÁLOGO OTIMIZADO V.30 (26 ATIVOS) ---
  const CATALOGO = {
    // --- DEFESA (3 ativos) ---
    'IVVB11.SA': { MM: 40, RSI_MAX: 70, DIST_MAX: 0.20, VOL_LIMIT: 0.4 },
    'GOLD11.SA': { MM: 16, RSI_MAX: 70, DIST_MAX: 0.10, VOL_LIMIT: 0.4 },
    'B5P211.SA': { MM: 4,  RSI_MAX: 75, DIST_MAX: 0.10, VOL_LIMIT: 0.4 },
    // --- ATAQUE (23 ativos) ---
    'HASH11.SA': { MM: 6,  RSI_MAX: 75, DIST_MAX: 0.10, VOL_LIMIT: 0.6 },
    'PRIO3.SA':  { MM: 52, RSI_MAX: 70, DIST_MAX: 0.10, VOL_LIMIT: 0.8 },
    'BPAC11.SA': { MM: 16, RSI_MAX: 75, DIST_MAX: 0.30, VOL_LIMIT: 0.4 },
    'KEPL3.SA':  { MM: 4,  RSI_MAX: 70, DIST_MAX: 0.15, VOL_LIMIT: 0.8 },
    'PETR4.SA':  { MM: 40, RSI_MAX: 70, DIST_MAX: 0.10, VOL_LIMIT: 0.6 },
    'ELET3.SA':  { MM: 6,  RSI_MAX: 70, DIST_MAX: 0.10, VOL_LIMIT: 0.6 },
    'CYRE3.SA':  { MM: 13, RSI_MAX: 70, DIST_MAX: 0.15, VOL_LIMIT: 0.4 },
    'CPLE6.SA':  { MM: 52, RSI_MAX: 70, DIST_MAX: 0.10, VOL_LIMIT: 0.4 },
    'BBDC4.SA':  { MM: 6,  RSI_MAX: 70, DIST_MAX: 0.10, VOL_LIMIT: 0.4 },
    'CMIG4.SA':  { MM: 52, RSI_MAX: 70, DIST_MAX: 0.10, VOL_LIMIT: 0.6 },
    'ITUB4.SA':  { MM: 4,  RSI_MAX: 70, DIST_MAX: 0.15, VOL_LIMIT: 0.4 },
    'BBAS3.SA':  { MM: 6,  RSI_MAX: 70, DIST_MAX: 0.10, VOL_LIMIT: 0.6 },
    'B3SA3.SA':  { MM: 10, RSI_MAX: 70, DIST_MAX: 0.15, VOL_LIMIT: 0.4 },
    'WEGE3.SA':  { MM: 20, RSI_MAX: 80, DIST_MAX: 0.15, VOL_LIMIT: 0.4 },
    'VALE3.SA':  { MM: 8,  RSI_MAX: 75, DIST_MAX: 0.10, VOL_LIMIT: 0.4 },
    'USIM5.SA':  { MM: 40, RSI_MAX: 70, DIST_MAX: 0.10, VOL_LIMIT: 0.4 },
    'EZTC3.SA':  { MM: 40, RSI_MAX: 70, DIST_MAX: 0.10, VOL_LIMIT: 0.4 },
    'VBBR3.SA':  { MM: 52, RSI_MAX: 70, DIST_MAX: 0.10, VOL_LIMIT: 0.4 },
    'SMAL11.SA': { MM: 13, RSI_MAX: 70, DIST_MAX: 0.10, VOL_LIMIT: 0.4 },
    'MGLU3.SA':  { MM: 4,  RSI_MAX: 70, DIST_MAX: 0.10, VOL_LIMIT: 0.4 },
    'LREN3.SA':  { MM: 8,  RSI_MAX: 80, DIST_MAX: 0.20, VOL_LIMIT: 0.4 },
    'CSAN3.SA':  { MM: 40, RSI_MAX: 70, DIST_MAX: 0.10, VOL_LIMIT: 0.4 },
    'HAPV3.SA':  { MM: 26, RSI_MAX: 70, DIST_MAX: 0.10, VOL_LIMIT: 0.4 },
  };

  const TICKERS = Object.keys(CATALOGO);
  const DEFESA = ['IVVB11.SA', 'GOLD11.SA', 'B5P211.SA'];
  const ATAQUE = TICKERS.filter(t => !DEFESA.includes(t));

  // --- FUNÇÃO: Calcular RSI (período 14) ---
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

  // --- FUNÇÃO: julgar_ativo() - 6 REGRAS (100% igual ao Python) ---
  const julgarAtivo = (d) => {
    const P = d.Params;
    const isAtaque = ATAQUE.includes(d.Ticker);

    // REGRA 1: Abaixo da média móvel → VENDA
    if (d.Dist < 0) {
      return { acao: "VENDA", status: `ABAIXO DA MÉDIA (MM${P.MM})` };
    }

    // REGRA 2: Volatilidade acima do limite → VENDA
    if (d.Vol > P.VOL_LIMIT) {
      return { acao: "VENDA", status: `RISCO ALTO (Vol ${d.Vol.toFixed(2)})` };
    }

    // REGRA 3: RSI esticado → NEUTRO
    if (d.RSI > P.RSI_MAX) {
      return { acao: "NEUTRO", status: `RSI ESTICADO (${Math.round(d.RSI)})` };
    }

    // REGRA 4: Preço esticado (distância) → NEUTRO
    if (d.Dist > P.DIST_MAX) {
      return { acao: "NEUTRO", status: `PREÇO ESTICADO (+${(d.Dist * 100).toFixed(1)}%)` };
    }

    // REGRA 5: ATAQUE precisa de ROC > 0
    if (isAtaque) {
      if (d.ROC > 0) {
        return { acao: "COMPRA", status: `SCORE ${d.Score.toFixed(2)}` };
      } else {
        return { acao: "NEUTRO", status: "SEM FORÇA (ROC Negativo)" };
      }
    }

    // REGRA 6: DEFESA sempre compra se passou nos filtros
    return { acao: "COMPRA", status: `DEFESA (Vol ${d.Vol.toFixed(2)})` };
  };

  try {
    const candidatosAtaque = [];
    const candidatosDefesa = [];
    const vendas = [];
    const todosAtivos = [];

    for (const ticker of TICKERS) {
      try {
        const params = CATALOGO[ticker];
        const isAtaque = ATAQUE.includes(ticker);

        // Busca dados SEMANAIS (interval=1wk) - range 5y para ter histórico suficiente
        const url = `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?interval=1wk&range=5y`;
        
        const response = await fetch(url, {
          headers: { 'User-Agent': 'Mozilla/5.0' }
        });
        
        const data = await response.json();
        
        if (data.chart?.result?.[0]) {
          const result = data.chart.result[0];
          const closes = result.indicators.quote[0].close.filter(c => c !== null);
          
          // Precisa de pelo menos 52 semanas (1 ano) de dados
          if (closes.length >= 52 && closes.length > params.MM) {
            const preco = closes[closes.length - 1];
            
            // Média Móvel (MM semanas)
            const smaSlice = closes.slice(-params.MM);
            const sma = smaSlice.reduce((a, b) => a + b, 0) / params.MM;
            const dist = (preco / sma) - 1;
            
            // Volatilidade anualizada (semanal: sqrt(52))
            const returns = [];
            for (let i = 1; i < closes.length; i++) {
              returns.push((closes[i] - closes[i-1]) / closes[i-1]);
            }
            const vol = Math.sqrt(returns.reduce((a, b) => a + b * b, 0) / returns.length) * Math.sqrt(52);
            
            // ROC de 12 semanas
            let roc = 0;
            if (closes.length > 12) {
              const preco12 = closes[closes.length - 13];
              roc = ((preco / preco12) - 1) * 100;
            }
            
            // RSI
            const rsi = calcularRSI(closes);

            // SCORE (diferente para ATAQUE vs DEFESA)
            const safeVol = vol > 0.01 ? vol : 0.01;
            let score;
            if (isAtaque) {
              score = roc / safeVol;  // Maior ROC e menor Vol = melhor
            } else {
              score = 1 / safeVol;    // Menor Vol = melhor
            }

            const dadosAtivo = {
              Ticker: ticker,
              Preco: Math.round(preco * 100) / 100,
              ROC: Math.round(roc * 100) / 100,
              Dist: Math.round(dist * 10000) / 10000,
              Vol: Math.round(vol * 10000) / 10000,
              RSI: Math.round(rsi * 10) / 10,
              Score: Math.round(score * 100) / 100,
              Params: params,
              Tipo: isAtaque ? 'ATAQUE' : 'DEFESA'
            };

            const { acao, status } = julgarAtivo(dadosAtivo);
            dadosAtivo.Acao = acao;
            dadosAtivo.Status = status;

            todosAtivos.push(dadosAtivo);

            // Separa por categoria
            if (acao === 'VENDA') {
              vendas.push(dadosAtivo);
            } else if (acao === 'COMPRA') {
              if (isAtaque) {
                candidatosAtaque.push(dadosAtivo);
              } else {
                candidatosDefesa.push(dadosAtivo);
              }
            }
          }
        }
      } catch (e) {
        console.log(`Erro em ${ticker}:`, e.message);
      }
    }

    // Ordena por Score (maior primeiro)
    candidatosAtaque.sort((a, b) => b.Score - a.Score);
    candidatosDefesa.sort((a, b) => b.Score - a.Score);

    // Monta carteira final: até 3 de ATAQUE, completa com DEFESA
    const carteiraFinal = [];
    carteiraFinal.push(...candidatosAtaque.slice(0, 3));
    
    const vagas = 3 - carteiraFinal.length;
    if (vagas > 0) {
      carteiraFinal.push(...candidatosDefesa.slice(0, vagas));
    }

    // Ordena todos os ativos por Score para exibição
    todosAtivos.sort((a, b) => b.Score - a.Score);

    const now = new Date();
    const timestamp = now.toLocaleDateString('pt-BR') + ' ' + now.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });

    res.status(200).json({
      success: true,
      data: todosAtivos,
      carteiraFinal: carteiraFinal,
      vendas: vendas,
      candidatosAtaque: candidatosAtaque,
      candidatosDefesa: candidatosDefesa,
      timestamp: timestamp,
      config: {
        ativoCaixa: ATIVO_CAIXA,
        totalAtivos: TICKERS.length,
        defesa: DEFESA,
        ataque: ATAQUE
      }
    });

  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
}
