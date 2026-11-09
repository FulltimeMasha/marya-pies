export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'method_not_allowed' });
  const { name, phone, when, note, items, total } = req.body || {};
  if (!name || !phone || !Array.isArray(items) || !items.length) {
    return res.status(400).json({ error: 'missing_fields' });
  }
  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chat = process.env.TELEGRAM_CHAT_ID;
  if (!token || !chat) return res.status(503).json({ error: 'not_configured' });

  const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const lines = items.map((i) => `• ${esc(i.name)} — ${esc(i.size)} × ${Number(i.qty) || 1} = $${(Number(i.price) || 0) * (Number(i.qty) || 1)}`);
  const text =
    `🥧 <b>Новый заказ — Marya Pies</b>\n\n` +
    lines.join('\n') +
    `\n\n<b>Итого: $${Number(total) || 0}</b>` +
    `\nИмя: ${esc(name)}\nКонтакт: ${esc(phone)}` +
    (when ? `\nКогда: ${esc(when)}` : '') +
    (note ? `\nКомментарий: ${esc(note)}` : '');

  try {
    const r = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: chat, text, parse_mode: 'HTML' }),
    });
    const j = await r.json();
    if (!j.ok) return res.status(502).json({ error: 'telegram_failed' });
    return res.status(200).json({ ok: true });
  } catch (e) {
    return res.status(502).json({ error: 'telegram_failed' });
  }
}
