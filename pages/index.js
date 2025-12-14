"use client";
import { useState } from 'react';
import Head from 'next/head';

// ==============================================================================
// 🔱 TRIDENTE V.32 | PAINEL DE EXECUÇÃO PROFISSIONAL - SAAS
// ==============================================================================

const CONFIG = {
  ativoCaixa: 'B5P211.SA',
  precoMensal: 19.90,
  precoAnual: 179.90,
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
  const [telaAtual, setTelaAtual] = useState('login'); // 'login' ou 'cadastro'
  
  // Estados do formulário de login
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [erroLogin, setErroLogin] = useState('');
  const [carregandoLogin, setCarregandoLogin] = useState(false);
  
  // Estados do formulário de cadastro
  const [cadastroNome, setCadastroNome] = useState('');
  const [cadastroEmail, setCadastroEmail] = useState('');
  const [cadastroSenha, setCadastroSenha] = useState('');
  const [cadastroConfirmarSenha, setCadastroConfirmarSenha] = useState('');
  const [erroCadastro, setErroCadastro] = useState('');
  const [sucessoCadastro, setSucessoCadastro] = useState('');
  const [carregandoCadastro, setCarregandoCadastro] = useState(false);
  
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

  // CADASTRO COM SUPABASE
  const fazerCadastro = async () => {
    setErroCadastro('');
    setSucessoCadastro('');
    setCarregandoCadastro(true);
    
    try {
      const response = await fetch('/api/cadastro', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          nome: cadastroNome,
          email: cadastroEmail, 
          senha: cadastroSenha,
          confirmarSenha: cadastroConfirmarSenha
        })
      });
      
      const result = await response.json();
      
      if (result.success) {
        setSucessoCadastro('Conta criada com sucesso! Faça login para continuar.');
        // Limpar formulário
        setCadastroNome('');
        setCadastroEmail('');
        setCadastroSenha('');
        setCadastroConfirmarSenha('');
        // Voltar para login após 2 segundos
        setTimeout(() => {
          setTelaAtual('login');
          setEmail(result.user.email);
          setSucessoCadastro('');
        }, 2000);
      } else {
        setErroCadastro(result.error || 'Erro ao criar conta');
      }
    } catch (e) {
      setErroCadastro('Erro de conexão. Tente novamente.');
    }
    
    setCarregandoCadastro(false);
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

  // Verificar se usuário é premium
  const isPremium = usuario?.plano === 'premium';

  const cores = {
    fundo: '#0a0a0f', borda: '#1e3a5f', azul: '#00d4ff', verde: '#00ff88',
    vermelho: '#ff3366', amarelo: '#ffcc00', laranja: '#ff8800', texto: '#e0e0e0',
    textoSecundario: '#8892a0', dourado: '#ffd700', prata: '#c0c0c0', bronze: '#cd7f32',
    roxo: '#a855f7', ciano: '#06b6d4'
  };

  // ============================================================================
  // TELA 1A: LOGIN
  // ============================================================================
  if (!logado && telaAtual === 'login') {
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
            
            {/* LINK PARA CADASTRO */}
            <div style={{ marginTop: '24px', textAlign: 'center' }}>
              <span style={{ color: cores.textoSecundario, fontSize: '14px' }}>Não tem uma conta? </span>
              <button 
                onClick={() => setTelaAtual('cadastro')} 
                style={{ background: 'none', border: 'none', color: cores.azul, fontSize: '14px', fontWeight: '600', cursor: 'pointer', textDecoration: 'underline' }}
              >
                Criar conta grátis
              </button>
            </div>
            
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
  // TELA 1B: CADASTRO
  // ============================================================================
  if (!logado && telaAtual === 'cadastro') {
    return (
      <><Head><title>Tridente V.32 - Cadastro</title><meta name="viewport" content="width=device-width, initial-scale=1" /></Head>
      <div style={{ minHeight: '100vh', background: `radial-gradient(ellipse at top, #0d1a2d 0%, ${cores.fundo} 50%, #050508 100%)`, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px', fontFamily: "'Segoe UI', sans-serif" }}>
        <div style={{ width: '100%', maxWidth: '400px' }}>
          <div style={{ textAlign: 'center', marginBottom: '40px' }}>
            <div style={{ fontSize: '72px', marginBottom: '16px', filter: 'drop-shadow(0 0 30px rgba(0, 212, 255, 0.5))' }}>🔱</div>
            <div style={{ fontSize: '32px', fontWeight: '800', color: cores.azul, letterSpacing: '6px' }}>TRIDENTE</div>
            <div style={{ fontSize: '14px', color: cores.textoSecundario, letterSpacing: '4px', marginTop: '8px' }}>CRIAR CONTA GRATUITA</div>
          </div>
          <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.95), rgba(10, 10, 15, 0.98))', border: `1px solid ${cores.borda}`, borderRadius: '20px', padding: '40px 32px' }}>
            <div style={{ fontSize: '20px', fontWeight: '600', color: '#fff', marginBottom: '28px', textAlign: 'center' }}>📝 Criar Nova Conta</div>
            
            <input type="text" placeholder="Nome completo" value={cadastroNome} onChange={(e) => setCadastroNome(e.target.value)} style={{ width: '100%', padding: '16px 20px', fontSize: '15px', background: 'rgba(0,0,0,0.4)', border: `1px solid ${cores.borda}`, borderRadius: '12px', color: cores.texto, marginBottom: '16px', boxSizing: 'border-box', outline: 'none' }} />
            
            <input type="email" placeholder="Email" value={cadastroEmail} onChange={(e) => setCadastroEmail(e.target.value)} style={{ width: '100%', padding: '16px 20px', fontSize: '15px', background: 'rgba(0,0,0,0.4)', border: `1px solid ${cores.borda}`, borderRadius: '12px', color: cores.texto, marginBottom: '16px', boxSizing: 'border-box', outline: 'none' }} />
            
            <input type="password" placeholder="Senha (mínimo 6 caracteres)" value={cadastroSenha} onChange={(e) => setCadastroSenha(e.target.value)} style={{ width: '100%', padding: '16px 20px', fontSize: '15px', background: 'rgba(0,0,0,0.4)', border: `1px solid ${cores.borda}`, borderRadius: '12px', color: cores.texto, marginBottom: '16px', boxSizing: 'border-box', outline: 'none' }} />
            
            <input type="password" placeholder="Confirmar senha" value={cadastroConfirmarSenha} onChange={(e) => setCadastroConfirmarSenha(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && fazerCadastro()} style={{ width: '100%', padding: '16px 20px', fontSize: '15px', background: 'rgba(0,0,0,0.4)', border: `1px solid ${cores.borda}`, borderRadius: '12px', color: cores.texto, marginBottom: '20px', boxSizing: 'border-box', outline: 'none' }} />
            
            {erroCadastro && <div style={{ background: 'rgba(255, 51, 102, 0.15)', border: '1px solid rgba(255, 51, 102, 0.4)', borderRadius: '10px', padding: '14px', marginBottom: '20px', color: cores.vermelho, fontSize: '14px', textAlign: 'center' }}>❌ {erroCadastro}</div>}
            
            {sucessoCadastro && <div style={{ background: 'rgba(0, 255, 136, 0.15)', border: '1px solid rgba(0, 255, 136, 0.4)', borderRadius: '10px', padding: '14px', marginBottom: '20px', color: cores.verde, fontSize: '14px', textAlign: 'center' }}>✅ {sucessoCadastro}</div>}
            
            <button onClick={fazerCadastro} disabled={carregandoCadastro || !cadastroNome || !cadastroEmail || !cadastroSenha || !cadastroConfirmarSenha} style={{ width: '100%', padding: '16px', fontSize: '16px', fontWeight: '700', background: carregandoCadastro ? cores.textoSecundario : `linear-gradient(135deg, ${cores.verde} 0%, #00cc66 100%)`, border: 'none', borderRadius: '12px', color: '#000', cursor: carregandoCadastro ? 'wait' : 'pointer' }}>{carregandoCadastro ? '⏳ Criando conta...' : '✅ CRIAR CONTA GRÁTIS'}</button>
            
            {/* LINK PARA LOGIN */}
            <div style={{ marginTop: '24px', textAlign: 'center' }}>
              <span style={{ color: cores.textoSecundario, fontSize: '14px' }}>Já tem uma conta? </span>
              <button 
                onClick={() => { setTelaAtual('login'); setErroCadastro(''); setSucessoCadastro(''); }} 
                style={{ background: 'none', border: 'none', color: cores.azul, fontSize: '14px', fontWeight: '600', cursor: 'pointer', textDecoration: 'underline' }}
              >
                Fazer login
              </button>
            </div>
            
            {/* INFO SOBRE PLANO FREE */}
            <div style={{ marginTop: '28px', padding: '20px', background: 'rgba(0, 255, 136, 0.08)', border: '1px solid rgba(0, 255, 136, 0.2)', borderRadius: '12px', fontSize: '13px' }}>
              <div style={{ color: cores.verde, fontWeight: '600', marginBottom: '10px' }}>🆓 Plano Gratuito inclui:</div>
              <div style={{ color: cores.textoSecundario, lineHeight: '1.8' }}>
                • Acesso ao painel de análise<br/>
                • 1 ativo revelado por análise<br/>
                • Posições para encerrar
              </div>
              <div style={{ marginTop: '12px', color: cores.dourado, fontSize: '12px' }}>
                ⭐ Faça upgrade para PREMIUM e tenha acesso completo!
              </div>
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
            <div style={{ marginTop: '8px' }}>
              <span style={{ padding: '6px 16px', background: isPremium ? 'rgba(255, 215, 0, 0.2)' : 'rgba(255,255,255,0.1)', borderRadius: '20px', fontSize: '12px', color: isPremium ? cores.dourado : cores.textoSecundario, fontWeight: '600' }}>
                {isPremium ? '⭐ PREMIUM' : '🆓 FREE'}
              </span>
            </div>
          </div>

          {/* O QUE É O TRIDENTE - EXPANDIDO */}
          <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 15, 0.95))', border: `1px solid ${cores.borda}`, borderRadius: '16px', padding: '24px', marginBottom: '20px' }}>
            <div style={{ fontSize: '18px', fontWeight: '700', color: cores.azul, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span>📊</span> O QUE É O TRIDENTE?
            </div>
            <div style={{ lineHeight: '1.9', fontSize: '15px', color: cores.texto }}>
              O Tridente é um <strong>painel de apoio à decisão</strong> desenvolvido para investidores que desejam construir patrimônio no longo prazo através da renda variável brasileira.
              <br/><br/>
              
              <strong style={{ color: cores.azul }}>Como funciona?</strong><br/>
              O painel analisa um universo de <strong>26 ativos</strong> cuidadosamente selecionados da bolsa brasileira (B3), incluindo ações de grandes empresas, ETFs e fundos imobiliários. A cada mês, o sistema avalia cada ativo utilizando critérios técnicos objetivos e identifica as melhores oportunidades do momento.
              <br/><br/>
              
              <strong style={{ color: cores.azul }}>O que o painel entrega?</strong><br/>
              Após a análise, você recebe um <strong>guia de execução completo</strong> com instruções passo a passo sobre quais posições manter, quais encerrar e quais novas posições considerar. O painel calcula automaticamente a distribuição do seu capital e fornece os dados exatos para você preencher as ordens na sua corretora.
              <br/><br/>
              
              <strong style={{ color: cores.azul }}>Para quem é indicado?</strong><br/>
              O Tridente foi criado para investidores que buscam uma abordagem <strong>sistemática, disciplinada e de baixa manutenção</strong>. É ideal para quem não tem tempo ou conhecimento técnico avançado, mas deseja participar do mercado de ações de forma organizada e consistente, dedicando apenas alguns minutos por mês.
              <br/><br/>
              
              <strong style={{ color: cores.azul }}>Qual a filosofia do sistema?</strong><br/>
              O Tridente segue uma metodologia baseada em <strong>seguir tendências</strong> e <strong>gerenciar riscos</strong>. O sistema busca identificar ativos em momentos favoráveis e, principalmente, saber a hora certa de sair de posições que não estão mais funcionando. A gestão de risco é tão importante quanto a seleção dos ativos.
            </div>
          </div>

          {/* O QUE VOCÊ PODE ESPERAR */}
          <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 15, 0.95))', border: `1px solid ${cores.borda}`, borderRadius: '16px', padding: '24px', marginBottom: '20px' }}>
            <div style={{ fontSize: '18px', fontWeight: '700', color: cores.verde, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span>🎯</span> O QUE VOCÊ PODE ESPERAR?
            </div>
            <div style={{ lineHeight: '1.8', fontSize: '15px', color: cores.texto }}>
              <div style={{ marginBottom: '12px' }}>✅ <strong>Análises mensais simples e objetivas</strong> — O painel faz o trabalho técnico e entrega instruções claras, sem complicação.</div>
              <div style={{ marginBottom: '12px' }}>✅ <strong>Busca por retornos acima da taxa Selic no longo prazo</strong> — O objetivo é superar a renda fixa tradicional ao longo dos anos, aproveitando o potencial da renda variável.</div>
              <div style={{ marginBottom: '12px' }}>✅ <strong>Diversificação entre diferentes setores</strong> — Exposição a múltiplos segmentos da economia brasileira, reduzindo a dependência de um único setor.</div>
              <div style={{ marginBottom: '12px' }}>✅ <strong>Gestão de risco com critérios de saída definidos</strong> — O painel identifica quando é hora de encerrar uma posição, protegendo seu capital de quedas prolongadas.</div>
              <div style={{ marginBottom: '12px' }}>✅ <strong>Instruções passo a passo detalhadas</strong> — Você saberá exatamente o que fazer na sua corretora, com todos os dados necessários para preencher as ordens.</div>
              <div style={{ marginBottom: '12px' }}>✅ <strong>Tempo de dedicação: ~15 minutos por mês</strong> — Ideal para quem tem uma rotina ocupada e não quer acompanhar o mercado diariamente.</div>
              <div>✅ <strong>Disciplina e consistência</strong> — O sistema remove a emoção das decisões, seguindo regras objetivas independente do humor do mercado.</div>
            </div>
          </div>

          {/* COMO FUNCIONA NA PRÁTICA */}
          <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 15, 0.95))', border: `1px solid ${cores.ciano}`, borderRadius: '16px', padding: '24px', marginBottom: '20px' }}>
            <div style={{ fontSize: '18px', fontWeight: '700', color: cores.ciano, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span>🔄</span> COMO FUNCIONA NA PRÁTICA?
            </div>
            <div style={{ lineHeight: '1.8', fontSize: '15px', color: cores.texto }}>
              <div style={{ marginBottom: '16px', padding: '14px', background: 'rgba(0,0,0,0.2)', borderRadius: '10px', borderLeft: `3px solid ${cores.azul}` }}>
                <strong style={{ color: cores.azul }}>1. Acesse o painel uma vez por mês</strong><br/>
                <span style={{ color: cores.textoSecundario }}>Na primeira segunda-feira útil de cada mês, acesse o Tridente para obter a análise atualizada.</span>
              </div>
              <div style={{ marginBottom: '16px', padding: '14px', background: 'rgba(0,0,0,0.2)', borderRadius: '10px', borderLeft: `3px solid ${cores.verde}` }}>
                <strong style={{ color: cores.verde }}>2. Informe seu capital disponível</strong><br/>
                <span style={{ color: cores.textoSecundario }}>Digite o valor que você tem disponível para investir. O painel calculará a distribuição ideal.</span>
              </div>
              <div style={{ marginBottom: '16px', padding: '14px', background: 'rgba(0,0,0,0.2)', borderRadius: '10px', borderLeft: `3px solid ${cores.amarelo}` }}>
                <strong style={{ color: cores.amarelo }}>3. Receba as instruções detalhadas</strong><br/>
                <span style={{ color: cores.textoSecundario }}>O painel mostrará quais posições encerrar e quais novas posições abrir, com todos os dados para execução.</span>
              </div>
              <div style={{ padding: '14px', background: 'rgba(0,0,0,0.2)', borderRadius: '10px', borderLeft: `3px solid ${cores.roxo}` }}>
                <strong style={{ color: cores.roxo }}>4. Execute as ordens na sua corretora</strong><br/>
                <span style={{ color: cores.textoSecundario }}>Siga o passo a passo e execute as ordens. Depois, é só aguardar até o próximo mês.</span>
              </div>
            </div>
          </div>

          {/* O QUE O TRIDENTE NÃO É */}
          <div style={{ background: 'linear-gradient(145deg, rgba(13, 17, 23, 0.9), rgba(10, 10, 15, 0.95))', border: `1px solid rgba(255, 204, 0, 0.3)`, borderRadius: '16px', padding: '24px', marginBottom: '20px' }}>
            <div style={{ fontSize: '18px', fontWeight: '700', color: cores.amarelo, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span>⚠️</span> O QUE O TRIDENTE NÃO É
            </div>
            <div style={{ lineHeight: '1.8', fontSize: '15px', color: cores.texto }}>
              <div style={{ marginBottom: '12px' }}>❌ <strong>Não é garantia de lucro ou rentabilidade</strong> — Todo investimento em renda variável envolve riscos. Resultados passados não garantem resultados futuros.</div>
              <div style={{ marginBottom: '12px' }}>❌ <strong>Não é recomendação personalizada de investimento</strong> — O painel não considera sua situação financeira individual, seus objetivos ou tolerância a risco.</div>
              <div style={{ marginBottom: '12px' }}>❌ <strong>Não substitui sua própria análise e julgamento</strong> — A decisão final de investir é sempre sua. O painel é uma ferramenta de apoio, não um consultor financeiro.</div>
              <div style={{ marginBottom: '12px' }}>❌ <strong>Não é adequado para quem busca ganhos rápidos</strong> — A metodologia é focada no longo prazo. Se você busca day trade ou ganhos de curto prazo, esta não é a ferramenta adequada.</div>
              <div>❌ <strong>Não é um robô que opera automaticamente</strong> — Você precisará executar as ordens manualmente na sua corretora. O painel fornece as instruções, mas a execução é sua.</div>
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
          <span style={{ marginLeft: '16px', padding: '4px 10px', background: isPremium ? 'rgba(255, 215, 0, 0.2)' : 'rgba(255,255,255,0.1)', borderRadius: '6px', fontSize: '11px', color: isPremium ? cores.dourado : cores.textoSecundario, fontWeight: '600' }}>
            {isPremium ? '⭐ PREMIUM' : '🆓 FREE'}
          </span>
        </div>
        <button onClick={fazerLogout} style={{ background: 'rgba(255, 51, 102, 0.15)', border: '1px solid rgba(255, 51, 102, 0.4)', borderRadius: '8px', padding: '10px 18px', color: cores.vermelho, cursor: 'pointer', fontSize: '12px', fontWeight: '600' }}>🚪 Sair</button>
      </div>

      {/* BANNER UPGRADE - SÓ PARA FREE */}
      {!isPremium && !analiseFeita && (
        <div style={{ background: 'linear-gradient(135deg, rgba(255, 215, 0, 0.15) 0%, rgba(255, 136, 0, 0.1) 100%)', border: '1px solid rgba(255, 215, 0, 0.3)', borderRadius: '12px', padding: '20px', marginBottom: '24px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
            <span style={{ fontSize: '28px' }}>⭐</span>
            <div style={{ flex: 1, minWidth: '200px' }}>
              <div style={{ color: cores.dourado, fontWeight: '700', fontSize: '16px' }}>Faça upgrade para PREMIUM</div>
              <div style={{ color: cores.textoSecundario, fontSize: '13px' }}>Acesso completo a todos os 3 ativos + instruções detalhadas</div>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div style={{ color: cores.verde, fontWeight: '800', fontSize: '20px' }}>R$ {CONFIG.precoMensal.toFixed(2).replace('.', ',')}<span style={{ fontSize: '12px', color: cores.textoSecundario }}>/mês</span></div>
              <div style={{ color: cores.textoSecundario, fontSize: '11px' }}>ou R$ {CONFIG.precoAnual.toFixed(2).replace('.', ',')}/ano</div>
            </div>
          </div>
          <button style={{ width: '100%', padding: '14px', background: `linear-gradient(135deg, ${cores.dourado} 0%, ${cores.laranja} 100%)`, border: 'none', borderRadius: '10px', color: '#000', fontWeight: '700', fontSize: '14px', cursor: 'pointer' }}>
            🚀 FAZER UPGRADE AGORA
          </button>
        </div>
      )}

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
                  Se você possui algum destes ativos, encerre a posição utilizando uma ordem a mercado na sua corretora.
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
                ℹ️ <strong>Modo Revisão:</strong> Exibindo ativos selecionados sem cálculo de valores. Para ver a distribuição e instruções detalhadas, faça uma nova análise informando o valor do aporte.
              </div>
            )}

            {/* AVISO FREE - SÓ VÊ RANK 2 */}
            {!isPremium && dados.carteiraFinal && dados.carteiraFinal.length > 1 && (
              <div style={{ background: 'linear-gradient(135deg, rgba(255, 215, 0, 0.1) 0%, rgba(255, 136, 0, 0.05) 100%)', border: '1px solid rgba(255, 215, 0, 0.3)', borderRadius: '12px', padding: '16px', marginBottom: '20px' }}>
                <div style={{ color: cores.dourado, fontWeight: '600', fontSize: '14px', marginBottom: '8px' }}>🔒 Plano FREE - Acesso Limitado</div>
                <div style={{ color: cores.textoSecundario, fontSize: '13px' }}>
                  Você está vendo apenas 1 dos 3 ativos selecionados. Faça upgrade para PREMIUM e tenha acesso completo.
                </div>
              </div>
            )}

            {dados.carteiraFinal && dados.carteiraFinal.length > 0 ? (
              <>
                {/* CARDS DE NOVAS POSIÇÕES */}
                {dados.carteiraFinal.map((ativo, i) => {
                  // FREE só vê o RANK 2 (índice 1)
                  const deveExibir = isPremium || i === 1;
                  const bloqueado = !isPremium && i !== 1;
                  
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

                  // CARD BLOQUEADO (FREE)
                  if (bloqueado) {
                    return (
                      <div key={i} style={{ background: 'rgba(50, 50, 60, 0.3)', border: `2px dashed ${cores.textoSecundario}`, borderRadius: '14px', padding: '24px', marginBottom: '20px', position: 'relative', overflow: 'hidden' }}>
                        <div style={{ filter: 'blur(8px)', opacity: '0.3' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                              <span style={{ fontSize: '28px' }}>🏆</span>
                              <div>
                                <div style={{ fontWeight: '800', fontSize: '22px' }}>????</div>
                                <div style={{ fontSize: '12px' }}>?????</div>
                              </div>
                            </div>
                            <span style={{ background: corCard, color: '#000', padding: '6px 14px', borderRadius: '8px', fontSize: '12px', fontWeight: '700' }}>{rankLabel}</span>
                          </div>
                        </div>
                        
                        {/* OVERLAY */}
                        <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', textAlign: 'center', width: '80%' }}>
                          <div style={{ fontSize: '40px', marginBottom: '12px' }}>🔒</div>
                          <div style={{ color: cores.dourado, fontWeight: '700', fontSize: '16px', marginBottom: '8px' }}>{rankLabel} - BLOQUEADO</div>
                          <div style={{ color: cores.textoSecundario, fontSize: '13px', marginBottom: '16px' }}>Disponível no plano PREMIUM</div>
                          <button style={{ padding: '10px 20px', background: `linear-gradient(135deg, ${cores.dourado} 0%, ${cores.laranja} 100%)`, border: 'none', borderRadius: '8px', color: '#000', fontWeight: '700', fontSize: '13px', cursor: 'pointer' }}>
                            ⭐ FAZER UPGRADE
                          </button>
                        </div>
                      </div>
                    );
                  }

                  // CARD NORMAL (PREMIUM ou RANK 2 para FREE)
                  return (
                    <div key={i} style={{ background: bgCard, border: `2px solid ${corCard}`, borderRadius: '14px', padding: '24px', marginBottom: '20px' }}>
                      
                      {/* HEADER DO CARD */}
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                          <span style={{ fontSize: '28px' }}>🏆</span>
                          <div>
                            <div style={{ color: corCard, fontWeight: '800', fontSize: '22px' }}>{tickerLimpo}</div>
                            <div style={{ fontSize: '12px', color: cores.textoSecundario }}>{isAtaque ? '⚔️ ATAQUE' : '🛡️ DEFESA'}</div>
                          </div>
                        </div>
                        <span style={{ background: corCard, color: '#000', padding: '6px 14px', borderRadius: '8px', fontSize: '12px', fontWeight: '700' }}>{rankLabel}</span>
                      </div>

                      {/* VALOR E PREÇO */}
                      {capitalNum > 0 && (
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '20px' }}>
                          <div style={{ background: 'rgba(0,0,0,0.2)', borderRadius: '10px', padding: '14px' }}>
                            <div style={{ fontSize: '12px', color: cores.textoSecundario, marginBottom: '4px' }}>💰 Valor a investir</div>
                            <div style={{ fontSize: '24px', fontWeight: '800', color: cores.verde }}>{formatCurrency(alocacao)}</div>
                          </div>
                          <div style={{ background: 'rgba(0,0,0,0.2)', borderRadius: '10px', padding: '14px' }}>
                            <div style={{ fontSize: '12px', color: cores.textoSecundario, marginBottom: '4px' }}>📊 Preço Atual</div>
                            <div style={{ fontSize: '24px', fontWeight: '800', color: cores.azul }}>R$ {ativo.Preco.toFixed(2)}</div>
                          </div>
                        </div>
                      )}

                      {/* MODO REVISÃO - SEM VALORES */}
                      {capitalNum === 0 && (
                        <div style={{ background: 'rgba(0,0,0,0.2)', borderRadius: '10px', padding: '14px', marginBottom: '20px' }}>
                          <div style={{ fontSize: '12px', color: cores.textoSecundario, marginBottom: '4px' }}>📊 Preço Atual</div>
                          <div style={{ fontSize: '24px', fontWeight: '800', color: cores.azul }}>R$ {ativo.Preco.toFixed(2)}</div>
                        </div>
                      )}

                      {/* INSTRUÇÕES DETALHADAS DA BOLETA */}
                      {capitalNum > 0 && qtdTotal > 0 && (
                        <div style={{ background: 'rgba(0, 212, 255, 0.08)', border: '1px solid rgba(0, 212, 255, 0.3)', borderRadius: '12px', padding: '20px' }}>
                          <div style={{ color: cores.azul, fontWeight: '700', fontSize: '16px', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <span>📝</span> COMO PREENCHER A ORDEM (BOLETA):
                          </div>

                          {/* LOTE PADRÃO */}
                          {qtdPadrao > 0 && (
                            <div style={{ background: 'rgba(0,0,0,0.2)', borderRadius: '10px', padding: '16px', marginBottom: qtdFrac > 0 ? '16px' : '0', borderLeft: `3px solid ${cores.verde}` }}>
                              <div style={{ color: cores.verde, fontWeight: '600', marginBottom: '12px' }}>[1] LOTE PADRÃO</div>
                              <div style={{ lineHeight: '2.2', fontSize: '15px' }}>
                                <div>Digite o código: <strong style={{ color: '#fff', background: 'rgba(255,255,255,0.1)', padding: '2px 8px', borderRadius: '4px' }}>{tickerLimpo}</strong></div>
                                <div>Quantidade: <strong style={{ color: cores.azul }}>{qtdPadrao}</strong></div>
                                <div>Preço: <strong style={{ color: cores.amarelo }}>A Mercado</strong> (Melhor oferta)</div>
                                <div style={{ marginTop: '10px', color: cores.verde, fontWeight: '700' }}>👉 EXECUTAR ORDEM</div>
                              </div>
                            </div>
                          )}

                          {/* FRACIONÁRIO */}
                          {qtdFrac > 0 && (
                            <div style={{ background: 'rgba(0,0,0,0.2)', borderRadius: '10px', padding: '16px', borderLeft: `3px solid ${cores.ciano}` }}>
                              <div style={{ color: cores.ciano, fontWeight: '600', marginBottom: '12px' }}>[{qtdPadrao > 0 ? '2' : '1'}] FRACIONÁRIO</div>
                              <div style={{ lineHeight: '2.2', fontSize: '15px' }}>
                                <div>{qtdPadrao > 0 ? 'Também digite' : 'Digite'} o código: <strong style={{ color: '#fff', background: 'rgba(255,255,255,0.1)', padding: '2px 8px', borderRadius: '4px' }}>{tickerLimpo}F</strong> <span style={{ color: cores.textoSecundario }}>(Com o 'F' no final)</span></div>
                                <div>Quantidade: <strong style={{ color: cores.azul }}>{qtdFrac}</strong></div>
                                <div>Preço: <strong style={{ color: cores.amarelo }}>A Mercado</strong></div>
                                <div style={{ marginTop: '10px', color: cores.verde, fontWeight: '700' }}>👉 EXECUTAR ORDEM</div>
                              </div>
                            </div>
                          )}
                        </div>
                      )}

                      {/* VALOR INSUFICIENTE */}
                      {capitalNum > 0 && qtdTotal === 0 && (
                        <div style={{ color: cores.amarelo, fontSize: '14px', padding: '14px', background: 'rgba(255, 204, 0, 0.1)', borderRadius: '10px' }}>
                          ⚠️ Valor insuficiente para abrir posição neste ativo.
                        </div>
                      )}

                      {/* CRITÉRIO DE SELEÇÃO */}
                      <div style={{ marginTop: '16px', padding: '12px', background: 'rgba(168, 85, 247, 0.1)', borderRadius: '8px', color: cores.roxo, fontSize: '13px' }}>
                        Critério de seleção: <strong>{ativo.Status}</strong>
                      </div>
                    </div>
                  );
                })}

                {/* AVISO SE NÃO COMPLETOU 3 */}
                {dados.carteiraFinal.length < 3 && (
                  <div style={{ background: 'rgba(255, 204, 0, 0.1)', border: '1px solid rgba(255, 204, 0, 0.3)', borderRadius: '12px', padding: '20px' }}>
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

          {/* BANNER UPGRADE PÓS-ANÁLISE - SÓ PARA FREE */}
          {!isPremium && (
            <div style={{ background: 'linear-gradient(135deg, rgba(255, 215, 0, 0.15) 0%, rgba(255, 136, 0, 0.1) 100%)', border: '2px solid rgba(255, 215, 0, 0.4)', borderRadius: '16px', padding: '28px', marginBottom: '24px', textAlign: 'center' }}>
              <div style={{ fontSize: '40px', marginBottom: '12px' }}>⭐</div>
              <div style={{ color: cores.dourado, fontWeight: '800', fontSize: '20px', marginBottom: '8px' }}>Desbloqueie o Acesso Completo</div>
              <div style={{ color: cores.texto, fontSize: '15px', marginBottom: '20px', lineHeight: '1.6' }}>
                Tenha acesso aos <strong>3 ativos selecionados</strong>, instruções detalhadas da boleta e muito mais!
              </div>
              <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', flexWrap: 'wrap', marginBottom: '20px' }}>
                <div style={{ background: 'rgba(0,0,0,0.2)', borderRadius: '10px', padding: '16px 24px' }}>
                  <div style={{ color: cores.textoSecundario, fontSize: '12px' }}>MENSAL</div>
                  <div style={{ color: cores.verde, fontWeight: '800', fontSize: '24px' }}>R$ {CONFIG.precoMensal.toFixed(2).replace('.', ',')}</div>
                </div>
                <div style={{ background: 'rgba(255, 215, 0, 0.1)', borderRadius: '10px', padding: '16px 24px', border: '1px solid rgba(255, 215, 0, 0.3)' }}>
                  <div style={{ color: cores.dourado, fontSize: '12px' }}>ANUAL <span style={{ background: cores.verde, color: '#000', padding: '2px 6px', borderRadius: '4px', fontSize: '10px', marginLeft: '6px' }}>-25%</span></div>
                  <div style={{ color: cores.verde, fontWeight: '800', fontSize: '24px' }}>R$ {CONFIG.precoAnual.toFixed(2).replace('.', ',')}</div>
                </div>
              </div>
              <button style={{ padding: '16px 40px', background: `linear-gradient(135deg, ${cores.dourado} 0%, ${cores.laranja} 100%)`, border: 'none', borderRadius: '12px', color: '#000', fontWeight: '700', fontSize: '16px', cursor: 'pointer' }}>
                🚀 FAZER UPGRADE PARA PREMIUM
              </button>
            </div>
          )}

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
