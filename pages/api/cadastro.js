// ==============================================================================
// 🔱 TRIDENTE V.32 | API DE CADASTRO COM HASH DE SENHA
// ==============================================================================

import bcrypt from 'bcryptjs';

const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_KEY;

export default async function handler(req, res) {
  // Apenas POST permitido
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, error: 'Método não permitido' });
  }

  const { nome, email, senha, confirmarSenha } = req.body;

  // Validações básicas
  if (!nome || !email || !senha || !confirmarSenha) {
    return res.status(400).json({ success: false, error: 'Todos os campos são obrigatórios' });
  }

  if (nome.trim().length < 2) {
    return res.status(400).json({ success: false, error: 'Nome deve ter pelo menos 2 caracteres' });
  }

  // Validar formato do email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return res.status(400).json({ success: false, error: 'Email inválido' });
  }

  // Validar senha
  if (senha.length < 6) {
    return res.status(400).json({ success: false, error: 'Senha deve ter pelo menos 6 caracteres' });
  }

  if (senha !== confirmarSenha) {
    return res.status(400).json({ success: false, error: 'Senhas não conferem' });
  }

  try {
    const emailNormalizado = email.toLowerCase().trim();

    // Verificar se email já existe
    const checkResponse = await fetch(
      `${SUPABASE_URL}/rest/v1/users?email=eq.${encodeURIComponent(emailNormalizado)}&select=id`,
      {
        headers: {
          'apikey': SUPABASE_KEY,
          'Authorization': `Bearer ${SUPABASE_KEY}`
        }
      }
    );

    if (!checkResponse.ok) {
      return res.status(500).json({ success: false, error: 'Erro ao verificar email' });
    }

    const existingUsers = await checkResponse.json();

    if (existingUsers && existingUsers.length > 0) {
      return res.status(400).json({ success: false, error: 'Este email já está cadastrado' });
    }

    // Hash da senha com bcrypt (10 rounds)
    const senhaHash = await bcrypt.hash(senha, 10);

    // Criar usuário no Supabase
    const createResponse = await fetch(
      `${SUPABASE_URL}/rest/v1/users`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'apikey': SUPABASE_KEY,
          'Authorization': `Bearer ${SUPABASE_KEY}`,
          'Prefer': 'return=representation'
        },
        body: JSON.stringify({
          nome: nome.trim(),
          email: emailNormalizado,
          senha: senhaHash,
          plano: 'free',
          ativo: true,
          created_at: new Date().toISOString()
        })
      }
    );

    if (!createResponse.ok) {
      const errorData = await createResponse.text();
      console.error('Erro ao criar usuário:', errorData);
      return res.status(500).json({ success: false, error: 'Erro ao criar conta' });
    }

    const newUser = await createResponse.json();

    // Cadastro bem sucedido
    return res.status(201).json({
      success: true,
      message: 'Conta criada com sucesso!',
      user: {
        id: newUser[0]?.id,
        nome: newUser[0]?.nome,
        email: newUser[0]?.email,
        plano: newUser[0]?.plano
      }
    });

  } catch (error) {
    console.error('Erro no cadastro:', error);
    return res.status(500).json({ success: false, error: 'Erro interno do servidor' });
  }
}
