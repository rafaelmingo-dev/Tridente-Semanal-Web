// ==============================================================================
// 🔱 TRIDENTE V.32 | API DE CHECKOUT - MERCADO PAGO
// ==============================================================================

const MERCADOPAGO_ACCESS_TOKEN = process.env.MERCADOPAGO_ACCESS_TOKEN;
const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_KEY;

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, error: 'Método não permitido' });
  }

  const { userId, userEmail, userName, plano } = req.body;

  if (!userId || !userEmail || !plano) {
    return res.status(400).json({ success: false, error: 'Dados incompletos' });
  }

  // Definir preços
  const precos = {
    mensal: {
      title: 'Tridente PREMIUM - Mensal',
      unit_price: 19.90,
      description: 'Acesso completo ao painel Tridente por 1 mês'
    },
    anual: {
      title: 'Tridente PREMIUM - Anual',
      unit_price: 179.90,
      description: 'Acesso completo ao painel Tridente por 1 ano (economia de 25%)'
    }
  };

  const planoSelecionado = precos[plano];

  if (!planoSelecionado) {
    return res.status(400).json({ success: false, error: 'Plano inválido' });
  }

  try {
    // Criar preferência de pagamento no Mercado Pago
    const preference = {
      items: [
        {
          id: `tridente-${plano}`,
          title: planoSelecionado.title,
          description: planoSelecionado.description,
          quantity: 1,
          currency_id: 'BRL',
          unit_price: planoSelecionado.unit_price
        }
      ],
      payer: {
        email: userEmail,
        name: userName || 'Usuário'
      },
      external_reference: JSON.stringify({
        userId: userId,
        plano: plano,
        email: userEmail
      }),
      back_urls: {
        success: 'https://tridente-semanal-web-wg7t.vercel.app/?pagamento=sucesso',
        failure: 'https://tridente-semanal-web-wg7t.vercel.app/?pagamento=falha',
        pending: 'https://tridente-semanal-web-wg7t.vercel.app/?pagamento=pendente'
      },
      auto_return: 'approved',
      notification_url: 'https://tridente-semanal-web-wg7t.vercel.app/api/webhook',
      statement_descriptor: 'TRIDENTE',
      expires: true,
      expiration_date_from: new Date().toISOString(),
      expiration_date_to: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // 24 horas
    };

    const response = await fetch('https://api.mercadopago.com/checkout/preferences', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${MERCADOPAGO_ACCESS_TOKEN}`
      },
      body: JSON.stringify(preference)
    });

    if (!response.ok) {
      const errorData = await response.text();
      console.error('Erro Mercado Pago:', errorData);
      return res.status(500).json({ success: false, error: 'Erro ao criar pagamento' });
    }

    const data = await response.json();

    return res.status(200).json({
      success: true,
      checkoutUrl: data.init_point,
      preferenceId: data.id
    });

  } catch (error) {
    console.error('Erro no checkout:', error);
    return res.status(500).json({ success: false, error: 'Erro interno do servidor' });
  }
}
