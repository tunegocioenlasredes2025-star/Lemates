/* ============================================================
   LEMATES — Cálculo de envíos
   Intenta cotizar en vivo con la API de Correo Argentino (/api/shipping);
   si no está disponible, usa el estimador por zona del config.
   ============================================================ */
(function () {
  "use strict";
  const CFG = (window.LEMATES_CONFIG && window.LEMATES_CONFIG.envio) || {};
  const Cart = window.LemCart;

  function cartWeightGrams() {
    const pesos = CFG.pesosPorCategoria || {};
    const pack = CFG.packagingGramos || 200;
    let g = pack;
    (Cart ? Cart.detailed() : []).forEach((l) => {
      const w = pesos[l.category] != null ? pesos[l.category] : (pesos.default || 400);
      g += w * l.qty;
    });
    return Math.max(300, Math.min(25000, Math.round(g)));
  }

  function estimate(provincia) {
    const est = CFG.estimadorRespaldo || { zonas: {}, provinciaZona: {} };
    const zona = est.provinciaZona[provincia];
    if (zona == null) return null; // sin provincia no estimamos
    const z = est.zonas[zona];
    if (!z) return null;
    const kg = cartWeightGrams() / 1000;
    const extra = Math.max(0, Math.ceil(kg - 1)) * (z.extraKg || 0);
    return {
      source: "estimador",
      domicilio: { price: z.domicilio + extra, etaMin: 3, etaMax: 6 },
      sucursal: { price: z.sucursal + extra, etaMin: 3, etaMax: 6 },
    };
  }

  async function quote(cp, provincia) {
    const w = cartWeightGrams();
    const caja = CFG.caja || { alto: 15, ancho: 20, largo: 30 };
    // 1) intentar API en vivo
    if (CFG.apiHabilitada && cp && String(cp).trim().length >= 4) {
      try {
        const r = await fetch("/api/shipping", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            postalCodeDestination: String(cp).trim(),
            weight: w,
            height: caja.alto,
            width: caja.ancho,
            length: caja.largo,
          }),
        });
        if (r.ok) {
          const data = await r.json();
          if (data && data.ok && (data.domicilio || data.sucursal)) {
            return {
              source: data.source || "correo-argentino",
              domicilio: data.domicilio
                ? { price: data.domicilio.price, etaMin: data.domicilio.etaMin, etaMax: data.domicilio.etaMax }
                : null,
              sucursal: data.sucursal
                ? { price: data.sucursal.price, etaMin: data.sucursal.etaMin, etaMax: data.sucursal.etaMax }
                : null,
            };
          }
        }
      } catch (e) {
        /* cae al estimador */
      }
    }
    // 2) respaldo por zona
    return estimate(provincia);
  }

  window.LemShipping = { quote, estimate, cartWeightGrams };
})();
