/* ============================================================
   Cotización de envíos — Correo Argentino API "MiCorreo"
   Función serverless de Vercel (Node).
   ------------------------------------------------------------
   Requiere estas variables de entorno en Vercel:
     CORREO_USER        Usuario de la API MiCorreo
     CORREO_PASSWORD    Contraseña de la API MiCorreo
     CORREO_CUSTOMER_ID Identificador de cliente (customerId)
     CORREO_ORIGIN_CP   CP de origen del despacho (ej: 1704)
     CORREO_ENV         "prod" (por defecto) o "test"
   Si faltan credenciales o la API falla, responde { ok:false }
   con status 200 para que el frontend use su estimador de respaldo.
   ============================================================ */

const BASES = {
  prod: "https://api.correoargentino.com.ar/micorreo/v1",
  test: "https://apitest.correoargentino.com.ar/micorreo/v1",
};

// Cache del token entre invocaciones "calientes" del serverless
let tokenCache = { value: null, expires: 0 };

async function getToken(base, user, password) {
  const now = Date.now();
  if (tokenCache.value && tokenCache.expires > now + 30000) return tokenCache.value;
  const auth = Buffer.from(`${user}:${password}`).toString("base64");
  const res = await fetch(`${base}/token`, {
    method: "POST",
    headers: { Authorization: `Basic ${auth}` },
  });
  if (!res.ok) throw new Error(`token ${res.status}`);
  const data = await res.json();
  const exp = data.expires ? Date.parse(data.expires.replace(" ", "T")) : now + 5 * 60000;
  tokenCache = { value: data.token, expires: isNaN(exp) ? now + 5 * 60000 : exp };
  return data.token;
}

module.exports = async (req, res) => {
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  if (req.method === "OPTIONS") { res.status(204).end(); return; }
  if (req.method !== "POST") {
    res.status(405).json({ ok: false, error: "method_not_allowed" });
    return;
  }

  const { CORREO_USER, CORREO_PASSWORD, CORREO_CUSTOMER_ID, CORREO_ORIGIN_CP, CORREO_ENV } = process.env;
  const base = BASES[CORREO_ENV === "test" ? "test" : "prod"];

  // Parseo del body (Vercel suele parsearlo; contemplamos ambos casos)
  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch { body = {}; } }
  body = body || {};

  // Normaliza cualquier CP argentino al código de 4 dígitos (ej: "B1714FZL" -> "1714")
  const cp4 = (v) => {
    const m = String(v || "").match(/\d{4}/);
    return m ? m[0] : String(v || "").trim();
  };
  const postalCodeDestination = cp4(body.postalCodeDestination || body.cp || "");
  const origin = cp4(body.postalCodeOrigin || CORREO_ORIGIN_CP || "");
  const weight = Math.max(1, Math.min(25000, parseInt(body.weight, 10) || 1000)); // gramos
  const height = Math.max(1, Math.min(150, parseInt(body.height, 10) || 15));
  const width = Math.max(1, Math.min(150, parseInt(body.width, 10) || 20));
  const length = Math.max(1, Math.min(150, parseInt(body.length, 10) || 30));

  if (!postalCodeDestination) {
    res.status(200).json({ ok: false, error: "cp_destino_requerido" });
    return;
  }
  if (!CORREO_USER || !CORREO_PASSWORD || !CORREO_CUSTOMER_ID || !origin) {
    // Credenciales no configuradas aún -> el frontend usa el estimador
    res.status(200).json({ ok: false, error: "api_no_configurada" });
    return;
  }

  try {
    const token = await getToken(base, CORREO_USER, CORREO_PASSWORD);
    const rateRes = await fetch(`${base}/rates`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        customerId: CORREO_CUSTOMER_ID,
        postalCodeOrigin: origin,
        postalCodeDestination,
        dimensions: { weight, height, width, length }, // sin deliveredType -> devuelve D y S
      }),
    });
    if (!rateRes.ok) {
      res.status(200).json({ ok: false, error: `rates_${rateRes.status}` });
      return;
    }
    const data = await rateRes.json();
    const rates = (data.rates || []).map((r) => ({
      type: r.deliveredType,          // "D" domicilio | "S" sucursal
      name: r.productName,
      price: Math.round(Number(r.price)),
      etaMin: r.deliveryTimeMin,
      etaMax: r.deliveryTimeMax,
    }));
    // Precio más barato por tipo de entrega
    const pick = (t) => rates.filter((r) => r.type === t).sort((a, b) => a.price - b.price)[0] || null;
    res.status(200).json({
      ok: true,
      source: "correo-argentino",
      domicilio: pick("D"),
      sucursal: pick("S"),
      rates,
      validTo: data.validTo || null,
    });
  } catch (err) {
    res.status(200).json({ ok: false, error: "api_error", detail: String(err && err.message || err) });
  }
};
