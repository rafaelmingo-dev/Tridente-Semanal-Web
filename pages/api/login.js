// ==============================================================================
// 🔱 ROBÔ TRIDENTE V.32 | API DE LOGIN COM SUPABASE
// ==============================================================================

const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_KEY;

export default async function handler(req, res) {
  // Apenas POST permitido
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, error: 'Método não permitido' });
  }

  const { email, senha } = req.body;

  if (!email || !senha) {
    return res.status(400).json({ success: false, error: 'Email e senha são obrigatórios' });
  }

  try {
    // Busca usuário no Supabase
    const response = await fetch(
      `${SUPABASE_URL}/rest/v1/users?email=eq.${encodeURIComponent(email.toLowerCase().trim())}&select=*`,
      {
        headers: {
          'apikey': SUPABASE_KEY,
          'Authorization': `Bearer ${SUPABASE_KEY}`
        }
      }
    );

    if (!response.ok) {
      return res.status(500).json({ success: false, error: 'Erro ao conectar com banco de dados' });
    }

    const users = await response.json();

    // Verifica se encontrou usuário
    if (!users || users.length === 0) {
      return res.status(401).json({ success: false, error: 'Email não encontrado' });
    }

    const user = users[0];

    // Verifica senha
    if (user.senha !== senha) {
      return res.status(401).json({ success: false, error: 'Senha incorreta' });
    }

    // Verifica se usuário está ativo
    if (!user.ativo) {
      return res.status(401).json({ success: false, error: 'Usuário desativado' });
    }

    // Login bem sucedido
    return res.status(200).json({
      success: true,
      user: {
        id: user.id,
        nome: user.nome,
        email: user.email,
        plano: user.plano
      }
    });

  } catch (error) {
    console.error('Erro no login:', error);
    return res.status(500).json({ success: false, error: 'Erro interno do servidor' });
  }
}
