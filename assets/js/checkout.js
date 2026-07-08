/* Checkout: cotización de envío en vivo, métodos de pago (MP/transferencia/efectivo),
   modal de pago con QR + CVU y envío del comprobante por WhatsApp. */
(function () {
  "use strict";
  const form = document.getElementById("checkoutForm");
  if (!form) return;
  const fmt = window.LemFmt;
  const Cart = window.LemCart;
  const CFG = window.LEMATES_CONFIG || {};
  const PAGO = CFG.pago || {};
  const esc = (s) =>
    String(s == null ? "" : s).replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
    );

  // Estado de envío calculado (precios reales o estimados)
  let ship = {
    method: "domicilio", // domicilio | sucursal | retiro
    rates: { domicilio: null, sucursal: null }, // {price, etaMin, etaMax} | null
    source: null,
    retiro: { price: 0 },
  };
  let payment = "mercadopago";

  const orderBox = document.getElementById("orderSummary");
  const emptyBox = document.getElementById("checkoutEmpty");
  const mainCols = document.getElementById("checkoutLayout");
  const addrSection = document.getElementById("addressSection");

  function shipPrice() {
    if (ship.method === "retiro") return 0;
    const r = ship.rates[ship.method];
    return r ? r.price : null; // null = aún no calculado
  }
  function totals() {
    const sub = Cart.subtotal();
    const s = shipPrice();
    return { sub, ship: s, total: sub + (s || 0), pending: s === null && ship.method !== "retiro" };
  }

  // ---------- Resumen del pedido ----------
  function renderSummary() {
    const lines = Cart.detailed();
    if (!lines.length) {
      if (mainCols) mainCols.hidden = true;
      if (emptyBox) emptyBox.hidden = false;
      const btn = document.getElementById("confirmBtn");
      if (btn) btn.closest("div").hidden = true;
      return;
    }
    const t = totals();
    const shipLabel =
      ship.method === "retiro"
        ? "Gratis"
        : t.ship == null
        ? '<span style="color:var(--muted)">Ingresá tu CP</span>'
        : fmt(t.ship);
    orderBox.innerHTML = `
      <h3>Tu pedido</h3>
      <div style="margin:14px 0">
        ${lines
          .map(
            (l) => `<div class="order-line">
          <img src="${l.images[0].thumb}" alt="${esc(l.name)}" loading="lazy">
          <div class="order-line__info"><b>${esc(l.name)}</b><span>${l.qty} x ${fmt(l.price)}</span></div>
          <div style="font-weight:600">${fmt(l.lineTotal)}</div>
        </div>`
          )
          .join("")}
      </div>
      <div class="summary__row"><span>Subtotal</span><span>${fmt(t.sub)}</span></div>
      <div class="summary__row"><span>Envío</span><span>${shipLabel}</span></div>
      <div class="summary__row total"><span>Total</span><span>${
        t.pending ? fmt(t.sub) + "<small style='font-size:.6em'> + envío</small>" : fmt(t.total)
      }</span></div>
      ${
        ship.source === "estimador" && ship.method !== "retiro"
          ? '<p style="font-size:.78rem;color:var(--muted);margin-top:10px">Envío estimado. Confirmamos el valor exacto por WhatsApp.</p>'
          : ""
      }`;
  }

  // ---------- Cálculo de envío ----------
  const shipCards = {
    domicilio: form.querySelector('.radio-card[data-ship="domicilio"] .r-price'),
    sucursal: form.querySelector('.radio-card[data-ship="sucursal"] .r-price'),
  };
  function paintShipCards() {
    ["domicilio", "sucursal"].forEach((k) => {
      const el = shipCards[k];
      if (!el) return;
      const r = ship.rates[k];
      el.innerHTML = r ? fmt(r.price) : '<span style="color:var(--muted);font-weight:500">según CP</span>';
    });
  }
  let calcTimer;
  function recalcShipping() {
    const cp = (form.querySelector('[name="cp"]') || {}).value || "";
    const prov = (form.querySelector('[name="provincia"]') || {}).value || "";
    if (!window.LemShipping) return;
    if (ship.method === "retiro") {
      renderSummary();
      return;
    }
    // estado "calculando"
    ["domicilio", "sucursal"].forEach((k) => {
      if (shipCards[k]) shipCards[k].innerHTML = '<span style="color:var(--muted);font-weight:500">calculando…</span>';
    });
    window.LemShipping.quote(cp, prov).then((res) => {
      if (res) {
        ship.rates.domicilio = res.domicilio || null;
        ship.rates.sucursal = res.sucursal || null;
        ship.source = res.source;
      } else {
        ship.rates.domicilio = ship.rates.sucursal = null;
        ship.source = null;
      }
      paintShipCards();
      renderSummary();
    });
  }
  function debouncedRecalc() {
    clearTimeout(calcTimer);
    calcTimer = setTimeout(recalcShipping, 450);
  }

  // ---------- Selección de envío ----------
  form.querySelectorAll('input[name="shipping"]').forEach((r) =>
    r.addEventListener("change", () => {
      ship.method = r.value;
      form.querySelectorAll(".radio-card[data-ship]").forEach((c) =>
        c.classList.toggle("selected", c.dataset.ship === ship.method)
      );
      toggleAddr();
      if (ship.method !== "retiro") recalcShipping();
      renderSummary();
    })
  );

  // ---------- Selección de pago ----------
  form.querySelectorAll('input[name="payment"]').forEach((r) =>
    r.addEventListener("change", () => {
      payment = r.value;
      form.querySelectorAll(".radio-card[data-pay]").forEach((c) =>
        c.classList.toggle("selected", c.dataset.pay === payment)
      );
    })
  );

  // ---------- Dirección visible según envío ----------
  function toggleAddr() {
    if (!addrSection) return;
    const retiro = ship.method === "retiro";
    addrSection.style.display = retiro ? "none" : "";
    addrSection.querySelectorAll("[data-reqable]").forEach((f) => {
      if (retiro) f.removeAttribute("required");
      else f.setAttribute("required", "");
    });
  }

  // recalcular al cambiar CP / provincia
  const cpEl = form.querySelector('[name="cp"]');
  const provEl = form.querySelector('[name="provincia"]');
  if (cpEl) cpEl.addEventListener("input", debouncedRecalc);
  if (provEl) provEl.addEventListener("change", recalcShipping);

  // ---------- Validación ----------
  function validate() {
    let ok = true;
    form.querySelectorAll("[required]").forEach((f) => {
      if (f.offsetParent === null) return; // oculto (ej. dirección en retiro)
      const field = f.closest(".field");
      const bad =
        !f.value.trim() || (f.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.value));
      if (field) field.classList.toggle("error", bad);
      if (bad) ok = false;
    });
    return ok;
  }
  form.querySelectorAll("[required]").forEach((f) =>
    f.addEventListener("input", () => f.closest(".field")?.classList.remove("error"))
  );

  // ---------- Mensaje de pedido para WhatsApp ----------
  const SHIP_LABELS = {
    domicilio: "Envío a domicilio (Correo Argentino)",
    sucursal: "Envío a sucursal (Correo Argentino)",
    retiro: "Retiro en zona oeste (GBA)",
  };
  const PAY_LABELS = {
    mercadopago: "Mercado Pago (QR, CVU o tarjeta)",
    transferencia: "Transferencia bancaria",
    efectivo: "EFECTIVO — abona al recibir/retirar",
  };
  function buildMessage(d, withComprobante) {
    const t = totals();
    const lines = Cart.detailed();
    let msg = withComprobante
      ? "Hola Lemates! Ya realicé el pago de mi pedido y adjunto el comprobante 👇\n\n"
      : "Hola Lemates! Confirmo mi pedido:\n\n";
    lines.forEach((l, i) => {
      msg += `${i + 1}. *${l.name}* — ${l.qty} x ${fmt(l.price)} = ${fmt(l.lineTotal)}\n`;
    });
    msg += `\n*Subtotal:* ${fmt(t.sub)}\n`;
    msg += `*Envío (${SHIP_LABELS[ship.method]}):* ${
      ship.method === "retiro" ? "Gratis" : t.ship == null ? "a confirmar" : fmt(t.ship)
    }\n`;
    msg += `*TOTAL:* ${t.pending ? fmt(t.sub) + " + envío" : fmt(t.total)}\n\n`;
    msg += `— DATOS —\nNombre: ${d.nombre} ${d.apellido}\nEmail: ${d.email}\nTel: ${d.telefono}\n`;
    if (ship.method !== "retiro") {
      msg += `Dirección: ${d.direccion}\n${d.localidad}, ${d.provincia} (CP ${d.cp})\n`;
    }
    msg += `Pago: ${PAY_LABELS[payment]}\n`;
    if (d.obs && d.obs.trim()) msg += `Obs: ${d.obs}\n`;
    return msg;
  }

  // ---------- Modal de pago ----------
  let modal;
  function copyBtn(value, label) {
    return `<button type="button" class="copy-chip" data-copy="${esc(value)}">
      <span>${esc(value)}</span>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
    </button>`;
  }
  function payBlock() {
    const t = totals();
    const totalTxt = t.pending ? fmt(t.sub) + " + envío" : fmt(t.total);
    if (payment === "mercadopago") {
      const mp = PAGO.mercadopago || {};
      return `
        <div class="pay-amount"><span>Total a pagar</span><b>${totalTxt}</b></div>
        <div class="pay-qr">
          <img src="${esc(mp.qr || "")}" alt="QR de Mercado Pago" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
          <div class="pay-qr__ph" style="display:none">Subí tu QR en<br><code>${esc(mp.qr || "assets/img/pago/qr-mercadopago.png")}</code></div>
        </div>
        <p class="pay-hint">Escaneá el QR o transferí al CVU/alias (también podés pagar con <b>tarjeta</b> desde Mercado Pago):</p>
        <div class="pay-data">
          <div><span>Alias</span>${copyBtn(mp.alias || "", "alias")}</div>
          <div><span>CVU</span>${copyBtn(mp.cvu || "", "CVU")}</div>
          ${mp.titular ? `<div><span>Titular</span><span class="pay-static">${esc(mp.titular)}</span></div>` : ""}
        </div>
        ${
          mp.link
            ? `<a class="btn btn--gold btn--block" href="${esc(mp.link)}" target="_blank" rel="noopener" style="margin-top:12px">Pagar con link de Mercado Pago</a>`
            : ""
        }`;
    }
    if (payment === "transferencia") {
      const tr = PAGO.transferencia || {};
      return `
        <div class="pay-amount"><span>Total a transferir</span><b>${totalTxt}</b></div>
        <p class="pay-hint">Transferí a la siguiente cuenta y guardá el comprobante:</p>
        <div class="pay-data">
          ${tr.banco ? `<div><span>Banco</span><span class="pay-static">${esc(tr.banco)}</span></div>` : ""}
          ${tr.tipoCuenta ? `<div><span>Cuenta</span><span class="pay-static">${esc(tr.tipoCuenta)}</span></div>` : ""}
          <div><span>CBU</span>${copyBtn(tr.cbu || "", "CBU")}</div>
          <div><span>Alias</span>${copyBtn(tr.alias || "", "alias")}</div>
          ${tr.titular ? `<div><span>Titular</span><span class="pay-static">${esc(tr.titular)}</span></div>` : ""}
          ${tr.cuit ? `<div><span>CUIT</span>${copyBtn(tr.cuit, "CUIT")}</div>` : ""}
        </div>`;
    }
    // efectivo
    return `
      <div class="pay-amount"><span>Total</span><b>${totalTxt}</b></div>
      <p class="pay-hint">Pagás en efectivo al momento de retirar tu pedido. Coordinamos punto y horario por WhatsApp.</p>`;
  }
  function buildModal() {
    modal = document.createElement("div");
    modal.className = "pay-modal";
    modal.innerHTML = `
      <div class="pay-modal__scrim" data-pclose></div>
      <div class="pay-modal__panel" role="dialog" aria-modal="true" aria-label="Pago del pedido">
        <button class="icon-btn pay-modal__x" data-pclose aria-label="Cerrar">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg>
        </button>
        <span class="eyebrow">Casi listo</span>
        <h3 id="payTitle">Pagá tu pedido</h3>
        <div id="payBody"></div>
        <div class="pay-note" id="payNote"></div>
        <a class="btn btn--wa btn--lg btn--block" id="paySend" target="_blank" rel="noopener"></a>
        <button type="button" class="btn btn--ghost btn--block" data-pclose style="margin-top:10px">Volver</button>
      </div>`;
    document.body.appendChild(modal);
    modal.addEventListener("click", (e) => {
      if (e.target.closest("[data-pclose]")) closeModal();
      const cp = e.target.closest(".copy-chip");
      if (cp) {
        const val = cp.dataset.copy || "";
        navigator.clipboard?.writeText(val).then(
          () => window.LemToast("Copiado: " + val),
          () => window.LemToast("Copiá manualmente: " + val, false)
        );
      }
    });
  }
  function openModal(d) {
    if (!modal) buildModal();
    modal.querySelector("#payTitle").textContent =
      payment === "efectivo" ? "Coordiná tu retiro" : "Pagá tu pedido";
    modal.querySelector("#payBody").innerHTML = payBlock();
    const withComp = payment !== "efectivo";
    modal.querySelector("#payNote").innerHTML = withComp
      ? "Cuando hagas el pago, tocá el botón: se abre WhatsApp con <b>el detalle de tu pedido</b> ya escrito. Ahí <b>adjuntá la captura del comprobante</b> y coordinamos el envío."
      : "Vas a pagar <b>en efectivo</b> al recibir o retirar. Tocá el botón para enviarnos <b>el pedido por WhatsApp</b> y coordinar la entrega.";
    const send = modal.querySelector("#paySend");
    send.innerHTML =
      '<svg viewBox="0 0 24 24" fill="currentColor" style="width:1.2em;height:1.2em"><path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.4 1.3 4.9L2 22l5.3-1.4c1.4.8 3 1.2 4.7 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2z"/></svg>' +
      (withComp ? "Enviar pedido + comprobante" : "Enviar pedido por WhatsApp");
    send.href = window.LemWA.link(buildMessage(d, withComp));
    modal.classList.add("open");
    document.body.style.overflow = "hidden";
  }
  function closeModal() {
    if (modal) modal.classList.remove("open");
    document.body.style.overflow = "";
  }
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeModal();
  });

  // ---------- Submit ----------
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (!Cart.detailed().length) return;
    if (!validate()) {
      form.querySelector(".field.error")?.scrollIntoView({ behavior: "smooth", block: "center" });
      window.LemToast("Completá los datos requeridos", false);
      return;
    }
    const d = Object.fromEntries(new FormData(form).entries());
    openModal(d);
  });

  // ---------- Init ----------
  document.addEventListener("cart:change", () => {
    renderSummary();
    if (ship.method !== "retiro") debouncedRecalc();
  });
  toggleAddr();
  paintShipCards();
  renderSummary();
})();
