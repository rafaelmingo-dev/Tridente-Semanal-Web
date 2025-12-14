// ==============================================================================
// 🔱 TRIDENTE V.32 | WEBHOOK - MERCADO PAGO
// ==============================================================================

const MERCADOPAGO_ACCESS_TOKEN = process.env.MERCADOPAGO_ACCESS_TOKEN;
const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_KEY;

export default async function handler(req, res) {
  // Mercado Pago envia GET para verificar e POST para notificações
  if (req.method === 'GET') {
    return res.status(200).json({ status: 'ok' });
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Método não permitido' });
  }

  try {
    const { type, data } = req.body;

    console.log('Webhook recebido:', { type, data });

    // Só processar pagamentos
    if (type !== 'payment') {
      return res.status(200).json({ received: true, processed: false, reason: 'not a payment' });
    }

    const paymentId = data?.id;

    if (!paymentId) {
      return res.status(200).json({ received: true, processed: false, reason: 'no payment id' });
    }

    // Buscar detalhes do pagamento no Mercado Pago
    const paymentResponse = await fetch(`https://api.mercadopago.com/v1/payments/${paymentId}`, {
      headers: {
        'Authorization': `Bearer ${MERCADOPAGO_ACCESS_TOKEN}`
      }
    });

    if (!paymentResponse.ok) {
      console.error('Erro ao buscar pagamento:', await paymentResponse.text());
      return res.status(200).json({ received: true, processed: false, reason: 'payment not found' });
    }

    const payment = await paymentResponse.json();

    console.log('Pagamento:', {
      id: payment.id,
      status: payment.status,
      external_reference: payment.external_reference
    });

    // Só processar pagamentos aprovados
    if (payment.status !== 'approved') {
      return res.status(200).json({ 
        received: true, 
        processed: false, 
        reason: `payment status: ${payment.status}` 
      });
    }

    // Extrair dados do external_reference
    let referenceData;
    try {
      referenceData = JSON.parse(payment.external_reference);
    } catch (e) {
      console.error('Erro ao parsear external_reference:', e);
      return res.status(200).json({ received: true, processed: false, reason: 'invalid reference' });
    }

    const { userId, plano, email } = referenceData;

    if (!userId) {
      console.error('userId não encontrado no external_reference');
      return res.status(200).json({ received: true, processed: false, reason: 'no userId' });
    }

    // Calcular data de expiração do plano
    const agora = new Date();
    let dataExpiracao;
    
    if (plano === 'anual') {
      dataExpiracao = new Date(agora.setFullYear(agora.getFullYear() + 1));
    } else {
      dataExpiracao = new Date(agora.setMonth(agora.getMonth() + 1));
    }

    // Atualizar usuário no Supabase para PREMIUM
    const updateResponse = await fetch(
      `${SUPABASE_URL}/rest/v1/users?id=eq.${userId}`,
      {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'apikey': SUPABASE_KEY,
          'Authorization': `Bearer ${SUPABASE_KEY}`
        },
        body: JSON.stringify({
          plano: 'premium',
          plano_expira_em: dataExpiracao.toISOString(),
          pagamento_id: paymentId,
          updated_at: new Date().toISOString()
        })
      }
    );

    if (!updateResponse.ok) {
      console.error('Erro ao atualizar usuário:', await updateResponse.text());
      return res.status(200).json({ received: true, processed: false, reason: 'db update failed' });
    }

    console.log(`✅ Usuário ${userId} atualizado para PREMIUM até ${dataExpiracao.toISOString()}`);

    return res.status(200).json({ 
      received: true, 
      processed: true,
      userId,
      plano: 'premium',
      expira: dataExpiracao.toISOString()
    });

  } catch (error) {
    console.error('Erro no webhook:', error);
    // Sempre retornar 200 para o Mercado Pago não reenviar
    return res.status(200).json({ received: true, processed: false, error: error.message });
  }
}
