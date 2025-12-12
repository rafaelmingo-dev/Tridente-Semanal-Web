"use client";
import { useState } from 'react';
import Head from 'next/head';

const CONFIG = { ativo_seguranca: 'B5P211.SA', peso_ouro: 0.50, peso_prata: 0.35, peso_bronze: 0.15 };
const USUARIOS = { 'demo@tridente.com': { senha: 'demo123', nome: 'Usuário Demo' }, 'rafael@tridente.com': { senha: '123456', nome: 'Rafael' }, 'admin@tridente.com': { senha: 'admin123', nome: 'Admin' } };

export default function Home() {
  const [logado, setLogado] = useState(false);
  const [nomeUsuario, setNomeUsuario] = useState('');
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [erroLogin, setErroLogin] = useState('');
  const [carregandoLogin, setCarregandoLogin] = useState(false);
  const [capital, setCapital] = useState('');
  const [capitalNum, setCapitalNum] = useState(0);
  const [carteira, setCarteira] = useState([]);
  const [loading, setLoading] = useState(false);
  const [analiseFeita, setAnaliseFeita] = useState(false);
  const [erro, setErro] = useState('');
  const [timestamp, setTimestamp] = useState('');

  const fazerLogin = async () => {
    setErroLogin(''); setCarregandoLogin(true);
    await new Promise(r => setTimeout(r, 800));
    const user = USUARIOS[email.toLowerCase().trim()];
    if (user && user.senha === senha) { setNomeUsuario(user.nome); setLogado(true); }
    else { setErroLogin('Email ou senha incorretos'); }
    setCarregandoLogin(false);
  };

  const fazerLogout = () => { setLogado(false); setNomeUsuario(''); setEmail(''); setSenha(''); setAnaliseFeita(false); setCapital(''); setCapitalNum(0); setCarteira([]); };
  const formatCurrency = (v) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(v);
  const handleCapitalChange = (e) => { let v = e.target.value.replace(/\D/g, ''); if (v) { const n = parseInt(v) / 100; setCapitalNum(n); setCapital(formatCurrency(n)); } else { setCapital(''); setCapitalNum(0); } };

  const executarAnalise = async () => {
    setLoading(true); setErro('');
    try {
      const response = await fetch('/api/dados');
      const resultado = await response.json();
      if (resultado.success) { setCarteira(resultado.data); setTimestamp(resultado.timestamp); setAnaliseFeita(true); }
      else { setErro('Erro: ' + resultado.error); }
    } catch (e) { setErro('Erro de conexão.'); }
    setLoading(false);
  };

  const vendas = carteira.filter(a => a.Acao === 'VENDA');
  const compras = carteira.filter(a => a.Acao === 'COMPRA');
  let top3_tickers = [], top3_dados = [];
  if (compras.length >= 3) { top3_dados = compras.slice(0, 3); top3_tickers = top3_dados.map(c => c.Ticker); }
  else if (compras.length > 0) { top3_dados = compras; top3_tickers = compras.map(c => c.Ticker); }

  let pesos = [], nomes = [];
  if (top3_tickers.length === 3) { pesos = [0.50, 0.35, 0.15]; nomes = ["🥇 OURO (50%)", "🥈 PRATA (35%)", "🥉 BRONZE (15%)"]; }
  else if (top3_tickers.length === 2) { pesos = [0.60, 0.40]; nomes = ["🥇 OURO (60%)", "🥈 PRATA (40%)"]; }
  else if (top3_tickers.length === 1) { pesos = [1.0]; nomes = ["🥇 OURO (100%)"]; }

  let sobraTotal = 0;
  const planosCompra = top3_dados.map((ativo, i) => { const p_alvo = pesos[i] * capitalNum; const qtd = Math.floor(p_alvo / ativo.Preco); sobraTotal += p_alvo - (qtd * ativo.Preco); return { tickerClean: ativo.Ticker.replace('.SA', ''), nome: nomes[i], p_alvo, cotacao: ativo.Preco, qtd }; });

  const cores = { fundo: '#0a0a0f', borda: '#1e3a5f', azul: '#00d4ff', verde: '#00ff88', vermelho: '#ff3366', amarelo: '#ffcc00', laranja: '#ff8800', texto: '#e0e0e0', textoSecundario: '#8892a0', dourado: '#ffd700', prata: '#c0c0c0', bronze: '#cd7f32', roxo: '#a855f7' };

  if (!logado) {
    return (
      <><Head><title>Robô Tridente V.20.3</title><meta name="viewport" content="width=device-width, initial-scale=1" /></Head>
      <div style={{ minHeight: '100vh', background: `radial-gradient(ellipse at top, #0d1a2d 0%, ${cores.fundo} 50%, #050508 100%)`, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px', fontFamily: "'Segoe UI', sans-serif" }}>
        <div style={{ width: '100%', maxWidth: '400px' }}>
          <div style={{ textAlign: 'center', marginBottom: '40px' }}><div style={{ fontSize: '72px', marginBottom: '16px', filter: 'drop-shadow(0 0 30px rgba(0, 212, 255, 0.5))' }}>🔱</div><div style={{ fontSize: '28px', fontWeight: '800', color: cores.azul, letterSpacing: '3px' }}>ROBÔ TRIDENTE</div><div style={{ fontSize: '14px', color: cores.textoSecundario, letterSpacing: '4px', marginTop: '8px' }}>V.20.3 • DADOS AO VIVO</div></div>
          <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.95), rgba(10, 10, 15, 0.98))', border: `1px solid ${cores.borda}`, borderRadius: '20px', padding: '40px 32px' }}>
            <div style={{ fontSize: '20px', fontWeight: '600', color: '#fff', marginBottom: '28px', textAlign: 'center' }}>👤 Acesso ao Sistema</div>
            <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} style={{ width: '100%', padding: '16px 20px', fontSize: '15px', background: 'rgba(0,0,0,0.4)', border: `1px solid ${cores.borda}`, borderRadius: '12px', color: cores.texto, marginBottom: '16px', boxSizing: 'border-box', outline: 'none' }} />
            <input type="password" placeholder="Senha" value={senha} onChange={(e) => setSenha(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && fazerLogin()} style={{ width: '100%', padding: '16px 20px', fontSize: '15px', background: 'rgba(0,0,0,0.4)', border: `1px solid ${cores.borda}`, borderRadius: '12px', color: cores.texto, marginBottom: '20px', boxSizing: 'border-box', outline: 'none' }} />
            {erroLogin && <div style={{ background: 'rgba(255, 51, 102, 0.15)', border: '1px solid rgba(255, 51, 102, 0.4)', borderRadius: '10px', padding: '14px', marginBottom: '20px', color: cores.vermelho, fontSize: '14px', textAlign: 'center' }}>❌ {erroLogin}</div>}
            <button onClick={fazerLogin} disabled={carregandoLogin || !email || !senha} style={{ width: '100%', padding: '16px', fontSize: '16px', fontWeight: '700', background: carregandoLogin ? cores.textoSecundario : `linear-gradient(135deg, ${cores.azul} 0%, #0080ff 100%)`, border: 'none', borderRadius: '12px', color: '#fff', cursor: carregandoLogin ? 'wait' : 'pointer' }}>{carregandoLogin ? '⏳ Autenticando...' : '🔱 ENTRAR'}</button>
            <div style={{ marginTop: '28px', padding: '20px', background: 'rgba(0, 212, 255, 0.08)', border: '1px solid rgba(0, 212, 255, 0.2)', borderRadius: '12px', fontSize: '13px' }}><div style={{ color: cores.azul, fontWeight: '600', marginBottom: '10px' }}>🎮 Conta Demo:</div><div style={{ color: cores.textoSecundario }}>Email: <span style={{ color: cores.texto }}>demo@tridente.com</span></div><div style={{ color: cores.textoSecundario }}>Senha: <span style={{ color: cores.texto }}>demo123</span></div></div>
          </div>
        </div>
      </div></>
    );
  }

  return (
    <><Head><title>Robô Tridente V.20.3</title><meta name="viewport" content="width=device-width, initial-scale=1" /></Head>
    <div style={{ minHeight: '100vh', background: `radial-gradient(ellipse at top, #0d1a2d 0%, ${cores.fundo} 50%, #050508 100%)`, padding: '20px', fontFamily: "'Segoe UI', sans-serif", color: cores.texto }}>
      <div style={{ textAlign: 'center', marginBottom: '28px' }}><div style={{ fontSize: '56px', filter: 'drop-shadow(0 0 25px rgba(0, 212, 255, 0.5))' }}>🔱</div><div style={{ fontSize: '26px', fontWeight: '800', color: cores.azul, letterSpacing: '2px' }}>ROBÔ TRIDENTE V.20.3</div><div style={{ fontSize: '12px', color: cores.verde, letterSpacing: '3px', marginTop: '4px' }}>📡 DADOS AO VIVO</div></div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(0, 212, 255, 0.08)', border: '1px solid rgba(0, 212, 255, 0.2)', borderRadius: '12px', padding: '14px 20px', marginBottom: '24px' }}><div><span style={{ color: cores.verde, fontSize: '10px' }}>●</span><span style={{ marginLeft: '10px', fontSize: '14px' }}>Operador: <strong style={{ color: cores.azul }}>{nomeUsuario}</strong></span></div><button onClick={fazerLogout} style={{ background: 'rgba(255, 51, 102, 0.15)', border: '1px solid rgba(255, 51, 102, 0.4)', borderRadius: '8px', padding: '10px 18px', color: cores.vermelho, cursor: 'pointer', fontSize: '12px', fontWeight: '600' }}>🚪 Sair</button></div>

      {!analiseFeita && (
        <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 15, 0.95))', border: `1px solid ${cores.borda}`, borderRadius: '16px', padding: '28px', marginBottom: '24px' }}>
          <div style={{ color: cores.azul, fontWeight: '700', marginBottom: '20px', fontSize: '16px' }}>📝 INSTRUÇÃO INICIAL</div>
          <div style={{ lineHeight: '2', marginBottom: '24px', color: cores.texto, paddingLeft: '16px', borderLeft: `3px solid ${cores.borda}` }}>1. Abra o App/Site da sua corretora.<br/>2. Veja quanto dinheiro você tem no total.</div>
          <div style={{ marginBottom: '12px', color: cores.texto }}>👉 Digite esse valor total (R$):</div>
          <input type="text" value={capital} onChange={handleCapitalChange} placeholder="R$ 0,00" style={{ width: '100%', padding: '18px', fontSize: '26px', textAlign: 'center', fontWeight: '700', fontFamily: 'monospace', background: 'rgba(0, 212, 255, 0.05)', border: `2px solid ${cores.azul}`, borderRadius: '14px', color: cores.azul, marginBottom: '20px', boxSizing: 'border-box', outline: 'none' }} />
          {erro && <div style={{ background: 'rgba(255, 51, 102, 0.15)', border: '1px solid rgba(255, 51, 102, 0.4)', borderRadius: '10px', padding: '14px', marginBottom: '20px', color: cores.vermelho, textAlign: 'center' }}>❌ {erro}</div>}
          <button onClick={executarAnalise} disabled={capitalNum <= 0 || loading} style={{ width: '100%', padding: '18px', fontSize: '16px', fontWeight: '700', background: capitalNum > 0 && !loading ? `linear-gradient(135deg, ${cores.azul} 0%, #0080ff 100%)` : '#2a2a3a', border: 'none', borderRadius: '12px', color: '#fff', cursor: capitalNum > 0 && !loading ? 'pointer' : 'not-allowed' }}>{loading ? '📡 Buscando dados ao vivo...' : '🔱 EXECUTAR ANÁLISE'}</button>
        </div>
      )}

      {analiseFeita && (<>
        <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 15, 0.95))', border: `1px solid ${cores.borda}`, borderRadius: '16px', padding: '24px', marginBottom: '24px', overflowX: 'auto' }}>
          <div style={{ color: cores.azul, fontWeight: '700', marginBottom: '20px', fontSize: '16px', display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: '10px' }}><span>📊 MONITOR TRIDENTE</span><span style={{ color: cores.verde, fontSize: '12px' }}>🟢 {timestamp}</span></div>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '11px', fontFamily: 'monospace' }}>
            <thead><tr style={{ borderBottom: `2px solid ${cores.borda}` }}><th style={{ padding: '10px 4px', textAlign: 'left', color: cores.textoSecundario }}>#</th><th style={{ padding: '10px 4px', textAlign: 'left', color: cores.textoSecundario }}>ATIVO</th><th style={{ padding: '10px 4px', textAlign: 'right', color: cores.textoSecundario }}>FORÇA</th><th style={{ padding: '10px 4px', textAlign: 'center', color: cores.textoSecundario }}>RSI</th><th style={{ padding: '10px 4px', textAlign: 'center', color: cores.textoSecundario }}>SINAL</th><th style={{ padding: '10px 4px', textAlign: 'right', color: cores.textoSecundario }}>PREÇO</th></tr></thead>
            <tbody>{carteira.map((row, i) => { let sinal = '⚪', corSinal = cores.textoSecundario, bgRow = 'transparent'; if (top3_tickers.includes(row.Ticker)) { const idx = top3_tickers.indexOf(row.Ticker); if (idx === 0) { sinal = '🥇 OURO'; corSinal = cores.dourado; bgRow = 'rgba(255, 215, 0, 0.08)'; } else if (idx === 1) { sinal = '🥈 PRATA'; corSinal = cores.prata; bgRow = 'rgba(192, 192, 192, 0.08)'; } else { sinal = '🥉 BRONZE'; corSinal = cores.bronze; bgRow = 'rgba(205, 127, 50, 0.08)'; } } else if (row.Acao === 'COMPRA') { sinal = '🟢 Banco'; corSinal = cores.verde; } else if (row.Acao === 'VENDA') { sinal = '🔴 VENDA'; corSinal = cores.vermelho; } else { sinal = '🟡 Aguarde'; corSinal = cores.amarelo; } return (<tr key={i} style={{ background: bgRow, borderBottom: `1px solid ${cores.borda}` }}><td style={{ padding: '10px 4px', fontWeight: '600' }}>#{i + 1}</td><td style={{ padding: '10px 4px', fontWeight: '700' }}>{row.Ticker.replace('.SA', '')}</td><td style={{ padding: '10px 4px', textAlign: 'right', color: row.ROC > 0 ? cores.verde : cores.vermelho, fontWeight: '600' }}>{row.ROC > 0 ? '+' : ''}{row.ROC.toFixed(1)}%</td><td style={{ padding: '10px 4px', textAlign: 'center' }}>{Math.round(row.RSI)}</td><td style={{ padding: '10px 4px', textAlign: 'center', color: corSinal, fontWeight: '600', fontSize: '10px' }}>{sinal}</td><td style={{ padding: '10px 4px', textAlign: 'right' }}>R$ {row.Preco.toFixed(2)}</td></tr>); })}</tbody>
          </table>
        </div>

        <div style={{ background: 'linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 128, 255, 0.05) 100%)', border: `2px solid ${cores.azul}`, borderRadius: '14px', padding: '24px', marginBottom: '24px', textAlign: 'center' }}><div style={{ fontSize: '20px', fontWeight: '800', color: cores.azul }}>📘 MANUAL DE EXECUÇÃO</div></div>

        <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 15, 0.95))', border: `1px solid ${cores.borda}`, borderRadius: '16px', padding: '24px', marginBottom: '24px' }}>
          <div style={{ color: cores.laranja, fontWeight: '700', marginBottom: '16px', fontSize: '16px' }}>1️⃣ FASE 1: LIMPEZA (VENDAS)</div>
          {vendas.length > 0 ? (<><div style={{ background: 'rgba(255, 136, 0, 0.1)', border: '1px solid rgba(255, 136, 0, 0.3)', borderRadius: '12px', padding: '20px', marginBottom: '16px' }}><div style={{ color: cores.laranja, fontWeight: '600', marginBottom: '12px' }}>⚠️ LISTA DE VENDAS:</div>{vendas.map((a, i) => <div key={i} style={{ color: cores.vermelho, padding: '8px 0', paddingLeft: '16px' }}>🔴 <strong>{a.Ticker.replace('.SA', '')}</strong> ({a.Status})</div>)}</div></>) : (<div style={{ background: 'rgba(0, 255, 136, 0.1)', border: '1px solid rgba(0, 255, 136, 0.3)', borderRadius: '12px', padding: '20px', color: cores.verde }}>✅ Nenhuma venda necessária.</div>)}
        </div>

        <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 15, 0.95))', border: `1px solid ${cores.borda}`, borderRadius: '16px', padding: '24px', marginBottom: '24px' }}>
          <div style={{ color: cores.verde, fontWeight: '700', marginBottom: '16px', fontSize: '16px' }}>2️⃣ FASE 2: COMPRAS</div>
          {top3_tickers.length > 0 ? (<>{planosCompra.map((plano, i) => { let corBorda = cores.dourado, bgCard = 'rgba(255, 215, 0, 0.08)'; if (i === 1) { corBorda = cores.prata; bgCard = 'rgba(192, 192, 192, 0.08)'; } if (i === 2) { corBorda = cores.bronze; bgCard = 'rgba(205, 127, 50, 0.08)'; } return (<div key={i} style={{ background: bgCard, border: `2px solid ${corBorda}`, borderRadius: '14px', padding: '20px', marginBottom: '16px' }}><div style={{ fontSize: '16px', fontWeight: '700', color: corBorda, marginBottom: '16px' }}>{plano.nome}: [{plano.tickerClean}]</div><div style={{ marginBottom: '16px', fontFamily: 'monospace' }}><div>💰 Valor: <strong style={{ color: cores.verde }}>{formatCurrency(plano.p_alvo)}</strong></div><div>📦 Qtd: <strong style={{ color: cores.azul }}>{plano.qtd} ações</strong></div></div><div style={{ background: 'rgba(0, 212, 255, 0.05)', border: '1px solid rgba(0, 212, 255, 0.2)', borderRadius: '10px', padding: '16px' }}><div style={{ color: cores.azul, fontWeight: '600', marginBottom: '10px' }}>👩‍💻 HOME BROKER:</div><div style={{ lineHeight: '2', fontSize: '14px' }}>1. Código: <strong>{plano.tickerClean}</strong> ou <strong>{plano.tickerClean}F</strong><br/>2. <strong>COMPRAR</strong> → Qtd: <strong>{plano.qtd}</strong> → <strong>A MERCADO</strong></div></div></div>); })}{sobraTotal > 50 && (<div style={{ background: 'rgba(0, 255, 136, 0.1)', border: '1px solid rgba(0, 255, 136, 0.3)', borderRadius: '12px', padding: '16px' }}><div style={{ color: cores.verde, fontWeight: '600' }}>💰 SOBRA: {formatCurrency(sobraTotal)}</div></div>)}</>) : (<div style={{ background: 'rgba(255, 51, 102, 0.1)', border: '1px solid rgba(255, 51, 102, 0.3)', borderRadius: '14px', textAlign: 'center', padding: '40px' }}><div style={{ fontSize: '48px', marginBottom: '16px' }}>🛑</div><div style={{ fontSize: '20px', fontWeight: '700', color: cores.vermelho }}>MODO DEFESA</div><div style={{ color: cores.dourado, marginTop: '12px' }}>👉 Coloque tudo no B5P211</div></div>)}
        </div>

        <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 15, 0.95))', border: `1px solid ${cores.borda}`, borderRadius: '16px', padding: '24px', marginBottom: '24px' }}>
          <div style={{ color: cores.roxo, fontWeight: '700', marginBottom: '16px', fontSize: '16px' }}>3️⃣ FASE 3: CHECKOUT</div>
          <div style={{ lineHeight: '2.5' }}>{['Vendeu o que estava vermelho?', 'Comprou Ouro, Prata e Bronze?', 'Sobrou pouco dinheiro? (Normal)'].map((t, i) => (<label key={i} style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}><input type="checkbox" style={{ width: '20px', height: '20px', marginRight: '14px', accentColor: cores.verde }} />{t}</label>))}</div>
        </div>

        <div style={{ textAlign: 'center', background: 'linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(0, 200, 100, 0.05) 100%)', border: '2px solid rgba(0, 255, 136, 0.3)', borderRadius: '16px', padding: '40px 24px', marginBottom: '24px' }}><div style={{ fontSize: '56px', marginBottom: '16px' }}>🚀</div><div style={{ fontSize: '22px', fontWeight: '800', color: cores.verde }}>TUDO PRONTO</div><div style={{ color: cores.texto, fontSize: '15px', marginTop: '12px' }}>FECHE O HOME BROKER E SÓ VOLTE NA PRÓXIMA SEGUNDA.</div></div>

        <button onClick={() => { setAnaliseFeita(false); setCapital(''); setCapitalNum(0); setCarteira([]); }} style={{ width: '100%', padding: '16px', background: 'rgba(255, 255, 255, 0.05)', border: `1px solid ${cores.borda}`, borderRadius: '12px', color: cores.texto, cursor: 'pointer', fontSize: '15px', fontWeight: '600' }}>🔄 Nova Análise</button>
      </>)}

      <div style={{ textAlign: 'center', padding: '24px', fontSize: '11px', color: '#3a3a4a', marginTop: '20px' }}>⚖️ Ferramenta educacional (CVM 598/2018)</div>
    </div></>
  );
}
