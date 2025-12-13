"use client";
import { useState } from 'react';
import Head from 'next/head';

// ==============================================================================
// 🔱 TRIDENTE V.32 | LAYOUT PROFISSIONAL COM CARDS
// ==============================================================================

const CONFIG = {
  ativoCaixa: 'B5P211.SA',
};

// Função para calcular a primeira segunda-feira útil do próximo mês
const calcularProximaAnalise = () => {
  const hoje = new Date();
  let ano = hoje.getFullYear();
  let mes = hoje.getMonth() + 1; // Próximo mês
  
  if (mes > 11) {
    mes = 0;
    ano++;
  }
  
  // Primeiro dia do próximo mês
  let data = new Date(ano, mes, 1);
  
  // Encontrar a primeira segunda-feira
  while (data.getDay() !== 1) {
    data.setDate(data.getDate() + 1);
  }
  
  // Formatar a data
  const opcoes = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' };
  return data.toLocaleDateString('pt-BR', opcoes);
};

export default function Home() {
  const [logado, setLogado] = useState(false);
  const [usuario, setUsuario] = useState(null);
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [erroLogin, setErroLogin] = useState('');
  const [carregandoLogin, setCarregandoLogin] = useState(false);
  const [capital, setCapital] = useState('');
  const [capitalNum, setCapitalNum] = useState(0);
  const [dados, setDados] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analiseFeita, setAnaliseFeita] = useState(false);
  const [erro, setErro] = useState('');

  // LOGIN REAL COM SUPABASE
  const fazerLogin = async () => {
    setErroLogin('');
    setCarregandoLogin(true);
    
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, senha })
      });
      
      const result = await response.json();
      
      if (result.success) {
        setUsuario(result.user);
        setLogado(true);
      } else {
        setErroLogin(result.error || 'Email ou senha incorretos');
      }
    } catch (e) {
      setErroLogin('Erro de conexão. Tente novamente.');
    }
    
    setCarregandoLogin(false);
  };

  const fazerLogout = () => {
    setLogado(false);
    setUsuario(null);
    setEmail('');
    setSenha('');
    setAnaliseFeita(false);
    setCapital('');
    setCapitalNum(0);
    setDados(null);
  };

  const formatCurrency = (v) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(v);

  const handleCapitalChange = (e) => {
    let v = e.target.value.replace(/\D/g, '');
    if (v) { const n = parseInt(v) / 100; setCapitalNum(n); setCapital(formatCurrency(n)); }
    else { setCapital(''); setCapitalNum(0); }
  };

  const executarAnalise = async () => {
    setLoading(true);
    setErro('');
    try {
      const response = await fetch('/api/dados');
      const resultado = await response.json();
      if (resultado.success) {
        setDados(resultado);
        setAnaliseFeita(true);
      } else {
        setErro('Erro: ' + resultado.error);
      }
    } catch (e) {
      setErro('Erro de conexão.');
    }
    setLoading(false);
  };

  const cores = {
    fundo: '#0a0a0f', borda: '#1e3a5f', azul: '#00d4ff', verde: '#00ff88',
    vermelho: '#ff3366', amarelo: '#ffcc00', laranja: '#ff8800', texto: '#e0e0e0',
    textoSecundario: '#8892a0', dourado: '#ffd700', prata: '#c0c0c0', bronze: '#cd7f32',
    roxo: '#a855f7', ciano: '#06b6d4'
  };

  // ============================================================================
  // TELA DE LOGIN
  // ============================================================================
  if (!logado) {
    return (
      <><Head><title>Tridente V.32</title><meta name="viewport" content="width=device-width, initial-scale=1" /></Head>
      <div style={{ minHeight: '100vh', background: `radial-gradient(ellipse at top, #0d1a2d 0%, ${cores.fundo} 50%, #050508 100%)`, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px', fontFamily: "'Segoe UI', sans-serif" }}>
        <div style={{ width: '100%', maxWidth: '400px' }}>
          <div style={{ textAlign: 'center', marginBottom: '40px' }}>
            <div style={{ fontSize: '72px', marginBottom: '16px', filter: 'drop-shadow(0 0 30px rgba(0, 212, 255, 0.5))' }}>🔱</div>
            <div style={{ fontSize: '32px', fontWeight: '800', color: cores.azul, letterSpacing: '6px' }}>TRIDENTE</div>
            <div style={{ fontSize: '14px', color: cores.textoSecundario, letterSpacing: '4px', marginTop: '8px' }}>V.32 • PAINEL DE EXECUÇÃO</div>
          </div>
          <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.95), rgba(10, 10, 15, 0.98))', border: `1px solid ${cores.borda}`, borderRadius: '20px', padding: '40px 32px' }}>
            <div style={{ fontSize: '20px', fontWeight: '600', color: '#fff', marginBottom: '28px', textAlign: 'center' }}>👤 Acesso ao Sistema</div>
            <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} style={{ width: '100%', padding: '16px 20px', fontSize: '15px', background: 'rgba(0,0,0,0.4)', border: `1px solid ${cores.borda}`, borderRadius: '12px', color: cores.texto, marginBottom: '16px', boxSizing: 'border-box', outline: 'none' }} />
            <input type="password" placeholder="Senha" value={senha} onChange={(e) => setSenha(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && fazerLogin()} style={{ width: '100%', padding: '16px 20px', fontSize: '15px', background: 'rgba(0,0,0,0.4)', border: `1px solid ${cores.borda}`, borderRadius: '12px', color: cores.texto, marginBottom: '20px', boxSizing: 'border-box', outline: 'none' }} />
            {erroLogin && <div style={{ background: 'rgba(255, 51, 102, 0.15)', border: '1px solid rgba(255, 51, 102, 0.4)', borderRadius: '10px', padding: '14px', marginBottom: '20px', color: cores.vermelho, fontSize: '14px', textAlign: 'center' }}>❌ {erroLogin}</div>}
            <button onClick={fazerLogin} disabled={carregandoLogin || !email || !senha} style={{ width: '100%', padding: '16px', fontSize: '16px', fontWeight: '700', background: carregandoLogin ? cores.textoSecundario : `linear-gradient(135deg, ${cores.azul} 0%, #0080ff 100%)`, border: 'none', borderRadius: '12px', color: '#fff', cursor: carregandoLogin ? 'wait' : 'pointer' }}>{carregandoLogin ? '⏳ Autenticando...' : '🔱 ENTRAR'}</button>
            <div style={{ marginTop: '28px', padding: '20px', background: 'rgba(0, 212, 255, 0.08)', border: '1px solid rgba(0, 212, 255, 0.2)', borderRadius: '12px', fontSize: '13px' }}>
              <div style={{ color: cores.azul, fontWeight: '600', marginBottom: '10px' }}>🎮 Conta Demo:</div>
              <div style={{ color: cores.textoSecundario }}>Email: <span style={{ color: cores.texto }}>demo@tridente.com</span></div>
              <div style={{ color: cores.textoSecundario }}>Senha: <span style={{ color: cores.texto }}>demo123</span></div>
            </div>
          </div>
        </div>
      </div></>
    );
  }

  // ============================================================================
  // APP PRINCIPAL
  // ============================================================================
  return (
    <><Head><title>Tridente V.32</title><meta name="viewport" content="width=device-width, initial-scale=1" /></Head>
    <div style={{ minHeight: '100vh', background: `radial-gradient(ellipse at top, #0d1a2d 0%, ${cores.fundo} 50%, #050508 100%)`, padding: '20px', fontFamily: "'Segoe UI', sans-serif", color: cores.texto }}>

      {/* HEADER */}
      <div style={{ textAlign: 'center', marginBottom: '28px' }}>
        <div style={{ fontSize: '56px', filter: 'drop-shadow(0 0 25px rgba(0, 212, 255, 0.5))' }}>🔱</div>
        <div style={{ fontSize: '30px', fontWeight: '800', color: cores.azul, letterSpacing: '6px' }}>TRIDENTE</div>
        <div style={{ fontSize: '12px', color: cores.textoSecundario, letterSpacing: '3px', marginTop: '4px' }}>V.32 • PAINEL DE EXECUÇÃO PROFISSIONAL</div>
      </div>

      {/* BARRA USUÁRIO */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px', background: 'rgba(0, 212, 255, 0.08)', border: '1px solid rgba(0, 212, 255, 0.2)', borderRadius: '12px', padding: '14px 20px', marginBottom: '24px' }}>
        <div>
          <span style={{ color: cores.verde, fontSize: '10px' }}>●</span>
          <span style={{ marginLeft: '10px', fontSize: '14px' }}>
            Operador: <strong style={{ color: cores.azul }}>{usuario?.nome}</strong>
          </span>
          <span style={{ marginLeft: '16px', padding: '4px 10px', background: usuario?.plano === 'premium' ? 'rgba(255, 215, 0, 0.2)' : 'rgba(255,255,255,0.1)', borderRadius: '6px', fontSize: '11px', color: usuario?.plano === 'premium' ? cores.dourado : cores.textoSecundario }}>
            {usuario?.plano?.toUpperCase() || 'FREE'}
          </span>
        </div>
        <button onClick={fazerLogout} style={{ background: 'rgba(255, 51, 102, 0.15)', border: '1px solid rgba(255, 51, 102, 0.4)', borderRadius: '8px', padding: '10px 18px', color: cores.vermelho, cursor: 'pointer', fontSize: '12px', fontWeight: '600' }}>🚪 Sair</button>
      </div>

      {/* INPUT CAPITAL */}
      {!analiseFeita && (
        <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 15, 0.95))', border: `1px solid ${cores.borda}`, borderRadius: '16px', padding: '28px', marginBottom: '24px' }}>
          <div style={{ background: `linear-gradient(90deg, ${cores.azul}22, transparent)`, borderLeft: `4px solid ${cores.azul}`, padding: '16px', marginBottom: '24px', borderRadius: '0 12px 12px 0' }}>
            <div style={{ fontSize: '18px', fontWeight: '700', color: cores.azul, marginBottom: '12px' }}>📝 CHECKLIST INICIAL</div>
            <div style={{ lineHeight: '2', color: cores.texto, fontSize: '15px' }}>
              1. Abra o app da sua corretora.<br/>
              2. Veja quanto você tem de <strong>SALDO LIVRE</strong> + Valor das Ações do Robô (se já tiver).<br/>
              3. Vamos calcular exatamente o que comprar (Lote Padrão vs Fracionário).
            </div>
          </div>
          <div style={{ marginBottom: '12px', color: cores.texto, fontSize: '16px' }}>👉 Digite seu <strong>PATRIMÔNIO TOTAL</strong> para a estratégia (R$):</div>
          <input type="text" value={capital} onChange={handleCapitalChange} placeholder="R$ 0,00" style={{ width: '100%', padding: '18px', fontSize: '26px', textAlign: 'center', fontWeight: '700', fontFamily: 'monospace', background: 'rgba(0, 212, 255, 0.05)', border: `2px solid ${cores.azul}`, borderRadius: '14px', color: cores.azul, marginBottom: '20px', boxSizing: 'border-box', outline: 'none' }} />
          {erro && <div style={{ background: 'rgba(255, 51, 102, 0.15)', border: '1px solid rgba(255, 51, 102, 0.4)', borderRadius: '10px', padding: '14px', marginBottom: '20px', color: cores.vermelho, textAlign: 'center' }}>❌ {erro}</div>}
          <button onClick={executarAnalise} disabled={capitalNum <= 0 || loading} style={{ width: '100%', padding: '18px', fontSize: '16px', fontWeight: '700', background: capitalNum > 0 && !loading ? `linear-gradient(135deg, ${cores.azul} 0%, #0080ff 100%)` : '#2a2a3a', border: 'none', borderRadius: '12px', color: '#fff', cursor: capitalNum > 0 && !loading ? 'pointer' : 'not-allowed' }}>
            {loading ? '📡 Analisando gráficos SEMANAIS de 26 ativos...' : '🔱 EXECUTAR ANÁLISE'}
          </button>
        </div>
      )}

      {/* RESULTADO */}
      {analiseFeita && dados && (
        <>
          {/* TÍTULO DO GUIA */}
          <div style={{ background: `linear-gradient(135deg, ${cores.azul}22, ${cores.roxo}11)`, border: `2px solid ${cores.azul}`, borderRadius: '14px', padding: '24px', marginBottom: '24px', textAlign: 'center' }}>
            <div style={{ fontSize: '22px', fontWeight: '800', color: cores.azul, letterSpacing: '1px' }}>📘 GUIA DE OPERAÇÃO</div>
            <div style={{ fontSize: '14px', color: cores.textoSecundario, marginTop: '8px' }}>
              {dados.timestamp} • {dados.config?.totalAtivos || 26} ativos analisados
              {dados.fromCache && <span style={{ marginLeft: '10px', color: cores.verde }}>⚡ Cache</span>}
            </div>
          </div>

          {/* PASSO 1: VENDAS - LAYOUT EM CARDS */}
          <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 15, 0.95))', border: `1px solid ${cores.borda}`, borderRadius: '16px', padding: '24px', marginBottom: '24px' }}>
            <div style={{ fontSize: '20px', fontWeight: '700', color: cores.vermelho, marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ background: cores.vermelho, color: '#fff', padding: '4px 12px', borderRadius: '6px', fontSize: '14px' }}>1</span>
              VENDAS NECESSÁRIAS
            </div>

            {dados.vendas && dados.vendas.length > 0 ? (
              <>
                <div style={{ color: cores.textoSecundario, marginBottom: '16px', fontSize: '14px' }}>
                  Se você tiver algum destes ativos na carteira, venda tudo usando "Venda a Mercado".
                </div>
                
                {/* GRID DE CARDS DE VENDAS */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '12px', marginBottom: '16px' }}>
                  {dados.vendas.map((v, i) => (
                    <div key={i} style={{ background: 'rgba(255, 51, 102, 0.1)', border: '1px solid rgba(255, 51, 102, 0.4)', borderRadius: '12px', padding: '16px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <span style={{ fontSize: '18px' }}>❌</span>
                        <span style={{ color: cores.vermelho, fontWeight: '700', fontSize: '18px' }}>{v.Ticker.replace('.SA', '')}</span>
                      </div>
                      <div style={{ color: cores.textoSecundario, fontSize: '12px' }}>{v.Status}</div>
                      <div style={{ color: cores.texto, fontSize: '13px' }}>Preço: <strong>R$ {v.Preco?.toFixed(2)}</strong></div>
                    </div>
                  ))}
                </div>

                <div style={{ background: 'rgba(0, 255, 136, 0.1)', borderRadius: '10px', padding: '14px', color: cores.verde, fontSize: '14px' }}>
                  💵 O dinheiro dessas vendas será usado nas compras abaixo.
                </div>
              </>
            ) : (
              <div style={{ background: 'rgba(0, 255, 136, 0.1)', border: '1px solid rgba(0, 255, 136, 0.3)', borderRadius: '12px', padding: '20px' }}>
                <div style={{ display: 'flex', alignItems: 'center' }}>
                  <span style={{ fontSize: '24px', marginRight: '12px' }}>✅</span>
                  <span style={{ color: cores.verde, fontSize: '16px' }}>Nenhuma venda necessária. Seus ativos atuais continuam bons.</span>
                </div>
              </div>
            )}
          </div>

          {/* PASSO 2: COMPRAS */}
          <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 15, 0.95))', border: `1px solid ${cores.borda}`, borderRadius: '16px', padding: '24px', marginBottom: '24px' }}>
            <div style={{ fontSize: '20px', fontWeight: '700', color: cores.verde, marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ background: cores.verde, color: '#000', padding: '4px 12px', borderRadius: '6px', fontSize: '14px' }}>2</span>
              NOVAS COMPRAS
            </div>

            <div style={{ color: cores.textoSecundario, marginBottom: '20px', fontSize: '14px' }}>
              Distribuindo <strong style={{ color: cores.azul }}>{formatCurrency(capitalNum)}</strong> igualmente nos 3 melhores ativos.
            </div>

            {dados.carteiraFinal && dados.carteiraFinal.length > 0 ? (
              <>
                {/* GRID DE CARDS DE COMPRAS */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '16px' }}>
                  {dados.carteiraFinal.map((ativo, i) => {
                    const peso = 1.0 / dados.carteiraFinal.length;
                    const alocacao = capitalNum * peso;
                    const qtdTotal = Math.floor(alocacao / ativo.Preco);
                    const lotesPadrao = Math.floor(qtdTotal / 100);
                    const qtdPadrao = lotesPadrao * 100;
                    const qtdFrac = qtdTotal % 100;
                    const tickerLimpo = ativo.Ticker.replace('.SA', '');
                    const isAtaque = ativo.Tipo === 'ATAQUE';
                    const corCard = i === 0 ? cores.dourado : i === 1 ? cores.prata : cores.bronze;
                    const bgCard = i === 0 ? 'rgba(255, 215, 0, 0.08)' : i === 1 ? 'rgba(192, 192, 192, 0.08)' : 'rgba(205, 127, 50, 0.08)';
                    const rankLabel = i === 0 ? 'RANK 1' : i === 1 ? 'RANK 2' : 'RANK 3';

                    return (
                      <div key={i} style={{ background: bgCard, border: `2px solid ${corCard}`, borderRadius: '14px', padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
                        {/* HEADER DO CARD */}
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                            <span style={{ fontSize: '24px' }}>🏆</span>
                            <span style={{ color: corCard, fontWeight: '800', fontSize: '20px' }}>{tickerLimpo}</span>
                          </div>
                          <span style={{ background: corCard, color: '#000', padding: '4px 10px', borderRadius: '6px', fontSize: '11px', fontWeight: '700' }}>{rankLabel}</span>
                        </div>

                        {/* VALOR E PREÇO */}
                        <div style={{ background: 'rgba(0,0,0,0.2)', borderRadius: '10px', padding: '14px' }}>
                          <div style={{ fontSize: '28px', fontWeight: '800', color: cores.verde, marginBottom: '4px' }}>{formatCurrency(alocacao)}</div>
                          <div style={{ fontSize: '13px', color: cores.textoSecundario }}>{isAtaque ? '⚔️ ATAQUE' : '🛡️ DEFESA'} • Preço: R$ {ativo.Preco.toFixed(2)}</div>
                        </div>

                        {/* ORDEM NA CORRETORA */}
                        <div style={{ background: 'rgba(0, 255, 136, 0.1)', border: '1px solid rgba(0, 255, 136, 0.3)', borderRadius: '10px', padding: '14px' }}>
                          <div style={{ color: cores.verde, fontWeight: '600', fontSize: '12px', marginBottom: '10px' }}>📝 ORDEM NA CORRETORA</div>
                          
                          {qtdTotal > 0 ? (
                            <div style={{ fontSize: '14px', lineHeight: '1.8' }}>
                              {qtdPadrao > 0 && (
                                <div style={{ marginBottom: '8px' }}>
                                  Comprar <strong style={{ color: cores.azul }}>{qtdPadrao}</strong> x <strong>{tickerLimpo}</strong>
                                  <span style={{ color: cores.textoSecundario, fontSize: '12px' }}> (LOTE)</span>
                                </div>
                              )}
                              {qtdFrac > 0 && (
                                <div>
                                  Comprar <strong style={{ color: cores.azul }}>{qtdFrac}</strong> x <strong>{tickerLimpo}F</strong>
                                  <span style={{ color: cores.textoSecundario, fontSize: '12px' }}> (FRAC)</span>
                                </div>
                              )}
                            </div>
                          ) : (
                            <div style={{ color: cores.amarelo, fontSize: '13px' }}>⚠️ Saldo insuficiente</div>
                          )}
                        </div>

                        {/* MOTIVO */}
                        <div style={{ fontSize: '12px', color: cores.roxo }}>
                          Motivo: <strong>{ativo.Status}</strong> | Preço: A Mercado
                        </div>
                      </div>
                    );
                  })}
                </div>

                {/* AVISO SE NÃO COMPLETOU 3 */}
                {dados.carteiraFinal.length < 3 && (
                  <div style={{ background: 'rgba(255, 204, 0, 0.1)', border: '1px solid rgba(255, 204, 0, 0.3)', borderRadius: '12px', padding: '20px', marginTop: '16px' }}>
                    <div style={{ color: cores.amarelo, fontWeight: '600', marginBottom: '8px' }}>⚠️ Mercado difícil - não encontramos 3 ativos bons.</div>
                    <div style={{ color: cores.texto, fontSize: '14px' }}>
                      👉 O dinheiro restante (<strong>{formatCurrency(capitalNum * ((3 - dados.carteiraFinal.length) / 3))}</strong>) deve ficar no <strong>CAIXA ({CONFIG.ativoCaixa.replace('.SA', '')})</strong> ou Tesouro Selic.
                    </div>
                  </div>
                )}
              </>
            ) : (
              /* MODO DEFESA TOTAL */
              <div style={{ background: 'rgba(255, 51, 102, 0.1)', border: '2px solid rgba(255, 51, 102, 0.4)', borderRadius: '14px', textAlign: 'center', padding: '40px' }}>
                <div style={{ fontSize: '56px', marginBottom: '16px' }}>🛑</div>
                <div style={{ fontSize: '22px', fontWeight: '800', color: cores.vermelho, marginBottom: '12px' }}>MERCADO PERIGOSO</div>
                <div style={{ color: cores.texto, fontSize: '16px', marginBottom: '16px', lineHeight: '1.8' }}>Nenhuma compra segura no momento.</div>
                <div style={{ background: 'rgba(255, 215, 0, 0.15)', borderRadius: '10px', padding: '16px', color: cores.dourado, fontWeight: '600' }}>
                  👉 Deixe 100% no <strong>{CONFIG.ativoCaixa.replace('.SA', '')}</strong> ou Tesouro Selic.
                </div>
              </div>
            )}
          </div>

          {/* FINALIZAÇÃO COM DATA DA PRÓXIMA ANÁLISE */}
          <div style={{ textAlign: 'center', background: 'linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(0, 200, 100, 0.05) 100%)', border: '2px solid rgba(0, 255, 136, 0.3)', borderRadius: '16px', padding: '40px 24px', marginBottom: '24px' }}>
            <div style={{ fontSize: '56px', marginBottom: '16px' }}>🚀</div>
            <div style={{ fontSize: '22px', fontWeight: '800', color: cores.verde, marginBottom: '12px' }}>OPERAÇÃO CONCLUÍDA</div>
            <div style={{ color: cores.texto, fontSize: '16px', marginBottom: '20px' }}>Feche o app e aguarde a próxima janela de execução.</div>
            
            {/* DATA DA PRÓXIMA ANÁLISE */}
            <div style={{ background: 'rgba(0, 212, 255, 0.1)', border: '1px solid rgba(0, 212, 255, 0.3)', borderRadius: '12px', padding: '20px', marginTop: '16px' }}>
              <div style={{ color: cores.azul, fontSize: '14px', marginBottom: '8px' }}>📅 PRÓXIMA ANÁLISE</div>
              <div style={{ color: '#fff', fontSize: '18px', fontWeight: '700', textTransform: 'capitalize' }}>{calcularProximaAnalise()}</div>
            </div>
          </div>

          {/* BOTÃO NOVA ANÁLISE */}
          <button onClick={() => { setAnaliseFeita(false); setCapital(''); setCapitalNum(0); setDados(null); }} style={{ width: '100%', padding: '16px', background: 'rgba(255, 255, 255, 0.05)', border: `1px solid ${cores.borda}`, borderRadius: '12px', color: cores.texto, cursor: 'pointer', fontSize: '15px', fontWeight: '600' }}>
            🔄 Nova Análise
          </button>
        </>
      )}

      {/* FOOTER */}
      <div style={{ textAlign: 'center', padding: '24px', fontSize: '11px', color: '#3a3a4a', marginTop: '20px' }}>
        ⚖️ Ferramenta educacional (CVM 598/2018)
      </div>
    </div></>
  );
}
