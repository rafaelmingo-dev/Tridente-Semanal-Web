"use client";
import { useState } from 'react';
import Head from 'next/head';

// ==============================================================================
// 🔱 TRIDENTE V.32 | PAINEL DE EXECUÇÃO PROFISSIONAL
// ==============================================================================

const CONFIG = {
  ativoCaixa: 'B5P211.SA',
};

// Função para calcular a primeira segunda-feira útil do próximo mês
const calcularProximaAnalise = () => {
  const hoje = new Date();
  let ano = hoje.getFullYear();
  let mes = hoje.getMonth() + 1;
  
  if (mes > 11) {
    mes = 0;
    ano++;
  }
  
  let data = new Date(ano, mes, 1);
  
  while (data.getDay() !== 1) {
    data.setDate(data.getDate() + 1);
  }
  
  const opcoes = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' };
  return data.toLocaleDateString('pt-BR', opcoes);
};

export default function Home() {
  // Estados de autenticação
  const [logado, setLogado] = useState(false);
  const [usuario, setUsuario] = useState(null);
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [erroLogin, setErroLogin] = useState('');
  const [carregandoLogin, setCarregandoLogin] = useState(false);
  
  // Estado da tela de disclaimer
  const [aceitouTermos, setAceitouTermos] = useState(false);
  const [checkboxMarcado, setCheckboxMarcado] = useState(false);
  
  // Estados da análise
  const [capital, setCapital] = useState('');
  const [capitalNum, setCapitalNum] = useState(0);
  const [dados, setDados] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analiseFeita, setAnaliseFeita] = useState(false);
  const [erro, setErro] = useState('');

  // LOGIN COM SUPABASE
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
    setAceitouTermos(false);
    setCheckboxMarcado(false);
    setAnaliseFeita(false);
    setCapital('');
    setCapitalNum(0);
    setDados(null);
  };

  const formatCurrency = (v) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(v);

  const handleCapitalChange = (e) => {
    let v = e.target.value.replace(/\D/g, '');
    if (v) { 
      const n = parseInt(v) / 100; 
      setCapitalNum(n); 
      setCapital(formatCurrency(n)); 
    } else { 
      setCapital(''); 
      setCapitalNum(0); 
    }
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
  // TELA 1: LOGIN
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
  // TELA 2: DISCLAIMER E APRESENTAÇÃO
  // ============================================================================
  if (!aceitouTermos) {
    return (
      <><Head><title>Tridente V.32</title><meta name="viewport" content="width=device-width, initial-scale=1" /></Head>
      <div style={{ minHeight: '100vh', background: `radial-gradient(ellipse at top, #0d1a2d 0%, ${cores.fundo} 50%, #050508 100%)`, padding: '20px', fontFamily: "'Segoe UI', sans-serif", color: cores.texto }}>
        <div style={{ maxWidth: '700px', margin: '0 auto' }}>
          
          {/* HEADER */}
          <div style={{ textAlign: 'center', marginBottom: '28px' }}>
            <div style={{ fontSize: '56px', filter: 'drop-shadow(0 0 25px rgba(0, 212, 255, 0.5))' }}>🔱</div>
            <div style={{ fontSize: '30px', fontWeight: '800', color: cores.azul, letterSpacing: '6px' }}>TRIDENTE</div>
            <div style={{ fontSize: '16px', color: cores.texto, marginTop: '12px' }}>Bem-vindo, <strong style={{ color: cores.azul }}>{usuario?.nome}</strong>!</div>
          </div>

          {/* O QUE É O TRIDENTE */}
          <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 15, 0.95))', border: `1px solid ${cores.borda}`, borderRadius: '16px', padding: '24px', marginBottom: '20px' }}>
            <div style={{ fontSize: '18px', fontWeight: '700', color: cores.azul, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span>📊</span> O QUE É O TRIDENTE?
            </div>
            <div style={{ lineHeight: '1.8', fontSize: '15px', color: cores.texto }}>
              O Tridente é um <strong>painel de apoio à decisão</strong> desenvolvido para investidores que desejam construir patrimônio no longo prazo através da renda variável brasileira.
              <br/><br/>
              Criado para quem busca uma abordagem <strong>sistemática, disciplinada e de baixa manutenção</strong>, o painel analisa o mercado e identifica oportunidades com base em critérios técnicos objetivos.
              <br/><br/>
              A metodologia foi desenvolvida para investidores que não têm tempo ou conhecimento técnico avançado, mas desejam participar do mercado de ações de forma <strong>organizada e consistente</strong>.
            </div>
          </div>

          {/* O QUE VOCÊ PODE ESPERAR */}
          <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 15, 0.95))', border: `1px solid ${cores.borda}`, borderRadius: '16px', padding: '24px', marginBottom: '20px' }}>
            <div style={{ fontSize: '18px', fontWeight: '700', color: cores.verde, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span>🎯</span> O QUE VOCÊ PODE ESPERAR?
            </div>
            <div style={{ lineHeight: '1.8', fontSize: '15px', color: cores.texto }}>
              <div style={{ marginBottom: '12px' }}>✅ <strong>Análises mensais simples e objetivas</strong> — O painel faz o trabalho técnico e entrega instruções claras.</div>
              <div style={{ marginBottom: '12px' }}>✅ <strong>Busca por retornos acima da taxa Selic no longo prazo</strong> — O objetivo é superar a renda fixa tradicional ao longo dos anos.</div>
              <div style={{ marginBottom: '12px' }}>✅ <strong>Diversificação entre diferentes setores</strong> — Exposição a múltiplos segmentos da economia brasileira.</div>
              <div style={{ marginBottom: '12px' }}>✅ <strong>Gestão de risco com critérios de saída</strong> — O painel identifica quando é hora de encerrar uma posição.</div>
              <div style={{ marginBottom: '12px' }}>✅ <strong>Instruções passo a passo</strong> — Você saberá exatamente o que fazer na sua corretora.</div>
              <div>✅ <strong>Tempo de dedicação: ~15 minutos por mês</strong> — Ideal para quem tem uma rotina ocupada.</div>
            </div>
          </div>

          {/* O QUE O TRIDENTE NÃO É */}
          <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 15, 0.95))', border: `1px solid rgba(255, 204, 0, 0.3)`, borderRadius: '16px', padding: '24px', marginBottom: '20px' }}>
            <div style={{ fontSize: '18px', fontWeight: '700', color: cores.amarelo, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span>⚠️</span> O QUE O TRIDENTE NÃO É
            </div>
            <div style={{ lineHeight: '1.8', fontSize: '15px', color: cores.texto }}>
              <div style={{ marginBottom: '12px' }}>❌ <strong>Não é garantia de lucro ou rentabilidade</strong> — Todo investimento em renda variável envolve riscos.</div>
              <div style={{ marginBottom: '12px' }}>❌ <strong>Não é recomendação personalizada</strong> — O painel não considera sua situação financeira individual.</div>
              <div style={{ marginBottom: '12px' }}>❌ <strong>Não substitui sua própria análise</strong> — A decisão final é sempre sua.</div>
              <div style={{ marginBottom: '12px' }}>❌ <strong>Não é adequado para ganhos rápidos</strong> — A estratégia é focada no longo prazo.</div>
              <div style={{ padding: '14px', background: 'rgba(255, 51, 102, 0.1)', borderRadius: '10px', marginTop: '16px', color: cores.vermelho }}>
                <strong>⚠️ RISCO:</strong> O mercado de renda variável pode resultar em perdas. Você pode perder parte ou todo o capital investido. Resultados passados não garantem resultados futuros.
              </div>
            </div>
          </div>

          {/* DISCLAIMER CVM */}
          <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 15, 0.95))', border: `1px solid ${cores.roxo}`, borderRadius: '16px', padding: '24px', marginBottom: '20px' }}>
            <div style={{ fontSize: '18px', fontWeight: '700', color: cores.roxo, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span>⚖️</span> AVISO LEGAL
            </div>
            <div style={{ lineHeight: '1.8', fontSize: '14px', color: cores.textoSecundario }}>
              Este painel é uma <strong style={{ color: cores.texto }}>ferramenta educacional independente</strong> que serve como auxílio na formação de investidores iniciantes que buscam ampliar seu conhecimento em renda variável de forma simples e didática.
              <br/><br/>
              Em conformidade com a regulamentação da <strong style={{ color: cores.texto }}>CVM (Comissão de Valores Mobiliários)</strong>, este painel <strong style={{ color: cores.vermelho }}>não constitui indicação, sugestão ou recomendação de compra ou venda</strong> de ativos financeiros.
              <br/><br/>
              As informações apresentadas têm caráter exclusivamente <strong style={{ color: cores.texto }}>informativo e educacional</strong>. Toda e qualquer decisão de investimento é de <strong style={{ color: cores.texto }}>responsabilidade exclusiva do usuário</strong>.
              <br/><br/>
              Antes de investir, considere seus objetivos, situação financeira e consulte um profissional qualificado se necessário.
            </div>
          </div>

          {/* CHECKBOX E BOTÃO */}
          <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 15, 0.95))', border: `1px solid ${cores.borda}`, borderRadius: '16px', padding: '24px' }}>
            <label style={{ display: 'flex', alignItems: 'flex-start', gap: '12px', cursor: 'pointer', marginBottom: '20px' }}>
              <input 
                type="checkbox" 
                checked={checkboxMarcado} 
                onChange={(e) => setCheckboxMarcado(e.target.checked)}
                style={{ width: '22px', height: '22px', marginTop: '2px', accentColor: cores.azul, cursor: 'pointer' }}
              />
              <span style={{ fontSize: '14px', lineHeight: '1.6', color: cores.texto }}>
                Li, compreendi e concordo com os termos acima. Entendo que este painel é uma ferramenta educacional e que toda decisão de investimento é de minha exclusiva responsabilidade.
              </span>
            </label>
            
            <button 
              onClick={() => setAceitouTermos(true)} 
              disabled={!checkboxMarcado}
              style={{ 
                width: '100%', 
                padding: '18px', 
                fontSize: '16px', 
                fontWeight: '700', 
                background: checkboxMarcado ? `linear-gradient(135deg, ${cores.azul} 0%, #0080ff 100%)` : '#2a2a3a', 
                border: 'none', 
                borderRadius: '12px', 
                color: '#fff', 
                cursor: checkboxMarcado ? 'pointer' : 'not-allowed' 
              }}
            >
              🔱 ACESSAR PAINEL DE EXECUÇÃO
            </button>
          </div>

          {/* BOTÃO SAIR */}
          <button onClick={fazerLogout} style={{ width: '100%', marginTop: '16px', padding: '14px', background: 'transparent', border: `1px solid ${cores.borda}`, borderRadius: '12px', color: cores.textoSecundario, cursor: 'pointer', fontSize: '14px' }}>
            🚪 Sair
          </button>
        </div>
      </div></>
    );
  }

  // ============================================================================
  // TELA 3: PAINEL PRINCIPAL
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
          
          {/* INSTRUÇÕES DE USO */}
          <div style={{ background: `linear-gradient(90deg, ${cores.azul}22, transparent)`, borderLeft: `4px solid ${cores.azul}`, padding: '16px', marginBottom: '24px', borderRadius: '0 12px 12px 0' }}>
            <div style={{ fontSize: '18px', fontWeight: '700', color: cores.azul, marginBottom: '16px' }}>📝 COMO USAR O PAINEL</div>
            <div style={{ lineHeight: '2', color: cores.texto, fontSize: '15px' }}>
              <strong style={{ color: cores.verde }}>OPÇÃO 1 — Novo Aporte:</strong><br/>
              Digite o valor que deseja investir. O painel calculará a distribuição entre os ativos selecionados.
              <br/><br/>
              <strong style={{ color: cores.ciano }}>OPÇÃO 2 — Apenas Revisar Posições:</strong><br/>
              Digite <strong>R$ 0,00</strong> ou deixe em branco. O painel mostrará quais posições manter, encerrar ou abrir, sem calcular valores.
            </div>
          </div>

          {/* CHECKLIST */}
          <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: `1px solid ${cores.borda}`, borderRadius: '12px', padding: '16px', marginBottom: '24px' }}>
            <div style={{ fontSize: '14px', fontWeight: '600', color: cores.textoSecundario, marginBottom: '12px' }}>📋 ANTES DE COMEÇAR:</div>
            <div style={{ lineHeight: '1.8', color: cores.texto, fontSize: '14px' }}>
              1. Abra o app da sua corretora.<br/>
              2. Verifique seu <strong>SALDO LIVRE</strong> disponível.<br/>
              3. Se já possui posições do Tridente, some o valor atual delas.
            </div>
          </div>

          <div style={{ marginBottom: '12px', color: cores.texto, fontSize: '16px' }}>
            👉 Digite o valor do aporte <span style={{ color: cores.textoSecundario }}>(ou R$ 0 para apenas revisar)</span>:
          </div>
          <input 
            type="text" 
            value={capital} 
            onChange={handleCapitalChange} 
            placeholder="R$ 0,00" 
            style={{ width: '100%', padding: '18px', fontSize: '26px', textAlign: 'center', fontWeight: '700', fontFamily: 'monospace', background: 'rgba(0, 212, 255, 0.05)', border: `2px solid ${cores.azul}`, borderRadius: '14px', color: cores.azul, marginBottom: '20px', boxSizing: 'border-box', outline: 'none' }} 
          />
          {erro && <div style={{ background: 'rgba(255, 51, 102, 0.15)', border: '1px solid rgba(255, 51, 102, 0.4)', borderRadius: '10px', padding: '14px', marginBottom: '20px', color: cores.vermelho, textAlign: 'center' }}>❌ {erro}</div>}
          <button 
            onClick={executarAnalise} 
            disabled={loading} 
            style={{ width: '100%', padding: '18px', fontSize: '16px', fontWeight: '700', background: !loading ? `linear-gradient(135deg, ${cores.azul} 0%, #0080ff 100%)` : '#2a2a3a', border: 'none', borderRadius: '12px', color: '#fff', cursor: !loading ? 'pointer' : 'not-allowed' }}
          >
            {loading ? '📡 Analisando 26 ativos...' : '🔱 EXECUTAR ANÁLISE'}
          </button>
        </div>
      )}

      {/* RESULTADO DA ANÁLISE */}
      {analiseFeita && dados && (
        <>
          {/* TÍTULO */}
          <div style={{ background: `linear-gradient(135deg, ${cores.azul}22, ${cores.roxo}11)`, border: `2px solid ${cores.azul}`, borderRadius: '14px', padding: '24px', marginBottom: '24px', textAlign: 'center' }}>
            <div style={{ fontSize: '22px', fontWeight: '800', color: cores.azul, letterSpacing: '1px' }}>📘 PAINEL DE EXECUÇÃO</div>
            <div style={{ fontSize: '14px', color: cores.textoSecundario, marginTop: '8px' }}>
              {dados.timestamp} • {dados.config?.totalAtivos || 26} ativos analisados
              {dados.fromCache && <span style={{ marginLeft: '10px', color: cores.verde }}>⚡ Cache</span>}
            </div>
          </div>

          {/* SEÇÃO 1: POSIÇÕES PARA ENCERRAR */}
          <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 15, 0.95))', border: `1px solid ${cores.borda}`, borderRadius: '16px', padding: '24px', marginBottom: '24px' }}>
            <div style={{ fontSize: '20px', fontWeight: '700', color: cores.vermelho, marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ background: cores.vermelho, color: '#fff', padding: '4px 12px', borderRadius: '6px', fontSize: '14px' }}>1</span>
              POSIÇÕES PARA ENCERRAR
            </div>

            {dados.vendas && dados.vendas.length > 0 ? (
              <>
                <div style={{ color: cores.textoSecundario, marginBottom: '16px', fontSize: '14px' }}>
                  Se você possui algum destes ativos, encerre a posição utilizando uma ordem de saída a mercado.
                </div>
                
                {/* GRID DE CARDS */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))', gap: '12px', marginBottom: '16px' }}>
                  {dados.vendas.map((v, i) => (
                    <div key={i} style={{ background: 'rgba(255, 51, 102, 0.1)', border: '1px solid rgba(255, 51, 102, 0.4)', borderRadius: '12px', padding: '16px', textAlign: 'center' }}>
                      <div style={{ fontSize: '24px', marginBottom: '8px' }}>🔴</div>
                      <div style={{ color: cores.vermelho, fontWeight: '700', fontSize: '18px' }}>{v.Ticker.replace('.SA', '')}</div>
                    </div>
                  ))}
                </div>

                <div style={{ background: 'rgba(0, 255, 136, 0.1)', borderRadius: '10px', padding: '14px', color: cores.verde, fontSize: '14px' }}>
                  💵 O capital liberado pode ser utilizado nas novas posições.
                </div>
              </>
            ) : (
              <div style={{ background: 'rgba(0, 255, 136, 0.1)', border: '1px solid rgba(0, 255, 136, 0.3)', borderRadius: '12px', padding: '20px' }}>
                <div style={{ display: 'flex', alignItems: 'center' }}>
                  <span style={{ fontSize: '24px', marginRight: '12px' }}>✅</span>
                  <span style={{ color: cores.verde, fontSize: '16px' }}>Nenhuma posição para encerrar. Seus ativos atuais continuam válidos.</span>
                </div>
              </div>
            )}
          </div>

          {/* SEÇÃO 2: NOVAS POSIÇÕES */}
          <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 15, 0.95))', border: `1px solid ${cores.borda}`, borderRadius: '16px', padding: '24px', marginBottom: '24px' }}>
            <div style={{ fontSize: '20px', fontWeight: '700', color: cores.verde, marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ background: cores.verde, color: '#000', padding: '4px 12px', borderRadius: '6px', fontSize: '14px' }}>2</span>
              NOVAS POSIÇÕES
            </div>

            {capitalNum > 0 && (
              <div style={{ color: cores.textoSecundario, marginBottom: '20px', fontSize: '14px' }}>
                Distribuindo <strong style={{ color: cores.azul }}>{formatCurrency(capitalNum)}</strong> igualmente nos ativos selecionados.
              </div>
            )}

            {capitalNum === 0 && (
              <div style={{ background: 'rgba(0, 212, 255, 0.1)', border: '1px solid rgba(0, 212, 255, 0.3)', borderRadius: '10px', padding: '14px', marginBottom: '20px', color: cores.azul, fontSize: '14px' }}>
                ℹ️ <strong>Modo Revisão:</strong> Exibindo ativos selecionados sem cálculo de valores. Para ver a distribuição, faça uma nova análise informando o valor do aporte.
              </div>
            )}

            {dados.carteiraFinal && dados.carteiraFinal.length > 0 ? (
              <>
                {/* GRID DE CARDS */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '16px' }}>
                  {dados.carteiraFinal.map((ativo, i) => {
                    const peso = 1.0 / dados.carteiraFinal.length;
                    const alocacao = capitalNum * peso;
                    const qtdTotal = capitalNum > 0 ? Math.floor(alocacao / ativo.Preco) : 0;
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
                        {/* HEADER */}
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                            <span style={{ fontSize: '24px' }}>🏆</span>
                            <span style={{ color: corCard, fontWeight: '800', fontSize: '20px' }}>{tickerLimpo}</span>
                          </div>
                          <span style={{ background: corCard, color: '#000', padding: '4px 10px', borderRadius: '6px', fontSize: '11px', fontWeight: '700' }}>{rankLabel}</span>
                        </div>

                        {/* VALOR E PREÇO */}
                        <div style={{ background: 'rgba(0,0,0,0.2)', borderRadius: '10px', padding: '14px' }}>
                          {capitalNum > 0 ? (
                            <>
                              <div style={{ fontSize: '28px', fontWeight: '800', color: cores.verde, marginBottom: '4px' }}>{formatCurrency(alocacao)}</div>
                              <div style={{ fontSize: '13px', color: cores.textoSecundario }}>{isAtaque ? '⚔️ ATAQUE' : '🛡️ DEFESA'} • Preço: R$ {ativo.Preco.toFixed(2)}</div>
                            </>
                          ) : (
                            <div style={{ fontSize: '13px', color: cores.textoSecundario }}>{isAtaque ? '⚔️ ATAQUE' : '🛡️ DEFESA'} • Preço: R$ {ativo.Preco.toFixed(2)}</div>
                          )}
                        </div>

                        {/* DADOS PARA EXECUÇÃO */}
                        {capitalNum > 0 && qtdTotal > 0 && (
                          <div style={{ background: 'rgba(0, 255, 136, 0.1)', border: '1px solid rgba(0, 255, 136, 0.3)', borderRadius: '10px', padding: '14px' }}>
                            <div style={{ color: cores.verde, fontWeight: '600', fontSize: '12px', marginBottom: '10px' }}>📝 DADOS PARA EXECUÇÃO</div>
                            <div style={{ fontSize: '14px', lineHeight: '1.8' }}>
                              {qtdPadrao > 0 && (
                                <div style={{ marginBottom: '8px' }}>
                                  Entrada: <strong style={{ color: cores.azul }}>{qtdPadrao}</strong> x <strong>{tickerLimpo}</strong>
                                  <span style={{ color: cores.textoSecundario, fontSize: '12px' }}> (LOTE)</span>
                                </div>
                              )}
                              {qtdFrac > 0 && (
                                <div>
                                  Entrada: <strong style={{ color: cores.azul }}>{qtdFrac}</strong> x <strong>{tickerLimpo}F</strong>
                                  <span style={{ color: cores.textoSecundario, fontSize: '12px' }}> (FRAC)</span>
                                </div>
                              )}
                            </div>
                          </div>
                        )}

                        {capitalNum > 0 && qtdTotal === 0 && (
                          <div style={{ color: cores.amarelo, fontSize: '13px', padding: '10px', background: 'rgba(255, 204, 0, 0.1)', borderRadius: '8px' }}>
                            ⚠️ Valor insuficiente para este ativo
                          </div>
                        )}

                        {/* CRITÉRIO */}
                        <div style={{ fontSize: '12px', color: cores.roxo }}>
                          Critério: <strong>{ativo.Status}</strong>
                        </div>
                      </div>
                    );
                  })}
                </div>

                {/* AVISO SE NÃO COMPLETOU 3 */}
                {dados.carteiraFinal.length < 3 && (
                  <div style={{ background: 'rgba(255, 204, 0, 0.1)', border: '1px solid rgba(255, 204, 0, 0.3)', borderRadius: '12px', padding: '20px', marginTop: '16px' }}>
                    <div style={{ color: cores.amarelo, fontWeight: '600', marginBottom: '8px' }}>⚠️ Momento de cautela no mercado.</div>
                    <div style={{ color: cores.texto, fontSize: '14px' }}>
                      Não foram identificados 3 ativos que atendam aos critérios. O capital restante pode ser mantido em <strong>{CONFIG.ativoCaixa.replace('.SA', '')}</strong> ou Tesouro Selic.
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div style={{ background: 'rgba(255, 51, 102, 0.1)', border: '2px solid rgba(255, 51, 102, 0.4)', borderRadius: '14px', textAlign: 'center', padding: '40px' }}>
                <div style={{ fontSize: '56px', marginBottom: '16px' }}>🛑</div>
                <div style={{ fontSize: '22px', fontWeight: '800', color: cores.vermelho, marginBottom: '12px' }}>MOMENTO DE CAUTELA</div>
                <div style={{ color: cores.texto, fontSize: '16px', marginBottom: '16px', lineHeight: '1.8' }}>Nenhum ativo atende aos critérios de seleção no momento.</div>
                <div style={{ background: 'rgba(255, 215, 0, 0.15)', borderRadius: '10px', padding: '16px', color: cores.dourado, fontWeight: '600' }}>
                  👉 Mantenha o capital em <strong>{CONFIG.ativoCaixa.replace('.SA', '')}</strong> ou Tesouro Selic.
                </div>
              </div>
            )}
          </div>

          {/* FINALIZAÇÃO */}
          <div style={{ textAlign: 'center', background: 'linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(0, 200, 100, 0.05) 100%)', border: '2px solid rgba(0, 255, 136, 0.3)', borderRadius: '16px', padding: '40px 24px', marginBottom: '24px' }}>
            <div style={{ fontSize: '56px', marginBottom: '16px' }}>🚀</div>
            <div style={{ fontSize: '22px', fontWeight: '800', color: cores.verde, marginBottom: '12px' }}>ANÁLISE CONCLUÍDA</div>
            <div style={{ color: cores.texto, fontSize: '16px', marginBottom: '20px' }}>Aguarde a próxima janela de execução.</div>
            
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
        ⚖️ Ferramenta educacional • Não constitui recomendação de investimento
      </div>
    </div></>
  );
}
