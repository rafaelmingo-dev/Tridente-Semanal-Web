// ==============================================================================
// 🔱 TRIDENTE V.32 | API COM SUPABASE
// ==============================================================================

const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_KEY;

// --- CONFIGURAÇÃO ---
const ATIVO_CAIXA = 'B5P211.SA';

// --- CATÁLOGO OTIMIZADO V.32 (26 ATIVOS) ---
const CATALOGO = {
  'IVVB11.SA': { MM: 40, RSI_MAX: 70, DIST_MAX: 0.20, VOL_LIMIT: 0.4 },
  'GOLD11.SA': { MM: 16, RSI_MAX: 70, DIST_MAX: 0.10, VOL_LIMIT: 0.4 },
  'B5P211.SA': { MM: 4,  RSI_MAX: 75, DIST_MAX: 0.10, VOL_LIMIT: 0.4 },
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

// --- FUNÇÃO: Calcular RSI ---
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

// --- FUNÇÃO: julgar_ativo() ---
const julgarAtivo = (d) => {
  const P = d.Params;
  const isAtaque = ATAQUE.includes(d.Ticker);

  if (d.Dist < 0) return { acao: "VENDA", status: `ABAIXO DA MÉDIA (MM${P.MM})` };
  if (d.Vol > P.VOL_LIMIT) return { acao: "VENDA", status: `RISCO ALTO (Vol ${d.Vol.toFixed(2)})` };
  if (d.RSI > P.RSI_MAX) return { acao: "NEUTRO", status: `RSI ESTICADO (${Math.round(d.RSI)})` };
  if (d.Dist > P.DIST_MAX) return { acao: "NEUTRO", status: `PREÇO ESTICADO (+${(d.Dist * 100).toFixed(1)}%)` };

  if (isAtaque) {
    if (d.ROC > 0) return { acao: "COMPRA", status: `SCORE ${d.Score.toFixed(2)}` };
    else return { acao: "NEUTRO", status: "SEM FORÇA (ROC Negativo)" };
  }
  return { acao: "COMPRA", status: `DEFESA (Vol ${d.Vol.toFixed(2)})` };
};

// --- FUNÇÃO: Salvar no Supabase ---
async function salvarResultado(resultado) {
  try {
    const hoje = new Date().toISOString().split('T')[0];
    
    const response = await fetch(`${SUPABASE_URL}/rest/v1/results`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'apikey': SUPABASE_KEY,
        'Authorization': `Bearer ${SUPABASE_KEY}`,
        'Prefer': 'return=minimal'
      },
      body: JSON.stringify({
        data_analise: hoje,
        carteira_final: resultado.carteiraFinal,
        vendas: resultado.vendas,
        candidatos_ataque: resultado.candidatosAtaque,
        candidatos_defesa: resultado.candidatosDefesa,
        todos_ativos: resultado.data
      })
    });
    
    return response.ok;
  } catch (e) {
    console.log('Erro ao salvar:', e);
    return false;
  }
}

// --- FUNÇÃO: Buscar último resultado do Supabase ---
async function buscarUltimoResultado() {
  try {
    const response = await fetch(
      `${SUPABASE_URL}/rest/v1/results?order=data_analise.desc&limit=1`,
      {
        headers: {
          'apikey': SUPABASE_KEY,
          'Authorization': `Bearer ${SUPABASE_KEY}`
        }
      }
    );
    
    if (response.ok) {
      const data = await response.json();
      if (data && data.length > 0) {
        return data[0];
      }
    }
    return null;
  } catch (e) {
    console.log('Erro ao buscar:', e);
    return null;
  }
}

// --- HANDLER PRINCIPAL ---
export default async function handler(req, res) {
  const { forceRefresh } = req.query;

  try {
    // Se não forçar refresh, tenta buscar do cache (Supabase)
    if (forceRefresh !== 'true') {
      const cached = await buscarUltimoResultado();
      if (cached) {
        const hoje = new Date().toISOString().split('T')[0];
        // Se o cache é de hoje, usa ele
        if (cached.data_analise === hoje) {
          return res.status(200).json({
            success: true,
            data: cached.todos_ativos,
            carteiraFinal: cached.carteira_final,
            vendas: cached.vendas,
            candidatosAtaque: cached.candidatos_ataque,
            candidatosDefesa: cached.candidatos_defesa,
            timestamp: cached.timestamp_calculo,
            fromCache: true,
            config: { ativoCaixa: ATIVO_CAIXA, totalAtivos: TICKERS.length }
          });
        }
      }
    }

    // Se não tem cache ou forçou refresh, calcula do zero
    const candidatosAtaque = [];
    const candidatosDefesa = [];
    const vendas = [];
    const todosAtivos = [];

    for (const ticker of TICKERS) {
      try {
        const params = CATALOGO[ticker];
        const isAtaque = ATAQUE.includes(ticker);
        const url = `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?interval=1wk&range=5y`;
        
        const response = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0' } });
        const data = await response.json();
        
        if (data.chart?.result?.[0]) {
          const result = data.chart.result[0];
          const closes = result.indicators.quote[0].close.filter(c => c !== null);
          
          if (closes.length >= 52 && closes.length > params.MM) {
            const preco = closes[closes.length - 1];
            const smaSlice = closes.slice(-params.MM);
            const sma = smaSlice.reduce((a, b) => a + b, 0) / params.MM;
            const dist = (preco / sma) - 1;
            
            const returns = [];
            for (let i = 1; i < closes.length; i++) {
              returns.push((closes[i] - closes[i-1]) / closes[i-1]);
            }
            const vol = Math.sqrt(returns.reduce((a, b) => a + b * b, 0) / returns.length) * Math.sqrt(52);
            
            let roc = 0;
            if (closes.length > 12) {
              const preco12 = closes[closes.length - 13];
              roc = ((preco / preco12) - 1) * 100;
            }
            
            const rsi = calcularRSI(closes);
            const safeVol = vol > 0.01 ? vol : 0.01;
            const score = isAtaque ? roc / safeVol : 1 / safeVol;

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

            if (acao === 'VENDA') vendas.push(dadosAtivo);
            else if (acao === 'COMPRA') {
              if (isAtaque) candidatosAtaque.push(dadosAtivo);
              else candidatosDefesa.push(dadosAtivo);
            }
          }
        }
      } catch (e) {
        console.log(`Erro em ${ticker}:`, e.message);
      }
    }

    candidatosAtaque.sort((a, b) => b.Score - a.Score);
    candidatosDefesa.sort((a, b) => b.Score - a.Score);

    const carteiraFinal = [];
    carteiraFinal.push(...candidatosAtaque.slice(0, 3));
    const vagas = 3 - carteiraFinal.length;
    if (vagas > 0) carteiraFinal.push(...candidatosDefesa.slice(0, vagas));

    todosAtivos.sort((a, b) => b.Score - a.Score);

    // TIMESTAMP NO HORÁRIO DE BRASÍLIA
    const timestamp = new Date().toLocaleString('pt-BR', {
      timeZone: 'America/Sao_Paulo',
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });

    const resultado = {
      success: true,
      data: todosAtivos,
      carteiraFinal,
      vendas,
      candidatosAtaque,
      candidatosDefesa,
      timestamp,
      fromCache: false,
      config: { ativoCaixa: ATIVO_CAIXA, totalAtivos: TICKERS.length, defesa: DEFESA, ataque: ATAQUE }
    };

    // Salva no Supabase para cache
    await salvarResultado(resultado);

    res.status(200).json(resultado);

  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
}
