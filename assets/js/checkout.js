/* Checkout: resumen, envío, pago, validación y pedido por WhatsApp */
(function () {
  "use strict";
  const form = document.getElementById("checkoutForm");
  if (!form) return;
  const fmt = window.LemFmt;
  const Cart = window.LemCart;
  const esc = (s) =>
    String(s).replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
    );

  const SHIPPING = {
    retiro: { label: "Retiro en zona oeste (GBA)", price: 0, note: "Coordinamos punto y horario por WhatsApp" },
    domicilio: { label: "Envío a domicilio (Correo Argentino)", price: 4500, note: "Entrega a domicilio en 3-6 días hábiles" },
    sucursal: { label: "Envío a sucursal (Correo Argentino)", price: 3200, note: "Retiro en sucursal de Correo más cercana" },
  };
  let shipping = "domicilio";
  let payment = "transferencia";

  const orderBox = document.getElementById("orderSummary");
  const emptyBox = document.getElementById("checkoutEmpty");
  const mainCols = document.getElementById("checkoutLayout");

  function totals() {
    const sub = Cart.subtotal();
    const ship = SHIPPING[shipping].price;
    return { sub, ship, total: sub + ship };
  }

  function renderSummary() {
    const lines = Cart.detailed();
    if (!lines.length) {
      if (mainCols) mainCols.hidden = true;
      if (emptyBox) emptyBox.hidden = false;
      return;
    }
    const t = totals();
    orderBox.innerHTML = `
      <h3>Tu pedido</h3>
      <div style="margin:14px 0">
        ${lines
          .map(
            (l) => `<div class="order-line">
          <img src="${l.images[0].thumb}" alt="${esc(l.name)}" loading="lazy">
          <div class="order-line__info"><b>${esc(l.name)}</b><span>${l.qty} x ${fmt(
              l.price
            )}</span></div>
          <div style="font-weight:600">${fmt(l.lineTotal)}</div>
        </div>`
          )
          .join("")}
      </div>
      <div class="summary__row"><span>Subtotal</span><span>${fmt(t.sub)}</span></div>
      <div class="summary__row"><span>Envío</span><span>${
        t.ship === 0 ? "Gratis" : fmt(t.ship)
      }</span></div>
      <div class="summary__row total"><span>Total</span><span>${fmt(t.total)}</span></div>
      <p style="font-size:.82rem;color:var(--muted);margin-top:12px">Al confirmar, se abrirá WhatsApp con el detalle de tu pedido para coordinar el pago y el envío.</p>`;
  }

  // shipping radio cards
  form.querySelectorAll('input[name="shipping"]').forEach((r) =>
    r.addEventListener("change", () => {
      shipping = r.value;
      form.querySelectorAll(".radio-card[data-ship]").forEach((c) =>
        c.classList.toggle("selected", c.dataset.ship === shipping)
      );
      renderSummary();
    })
  );
  form.querySelectorAll('input[name="payment"]').forEach((r) =>
    r.addEventListener("change", () => {
      payment = r.value;
      form.querySelectorAll(".radio-card[data-pay]").forEach((c) =>
        c.classList.toggle("selected", c.dataset.pay === payment)
      );
    })
  );

  // validation
  function validate() {
    let ok = true;
    form.querySelectorAll("[required]").forEach((f) => {
      const field = f.closest(".field");
      const bad =
        !f.value.trim() ||
        (f.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.value));
      if (field) field.classList.toggle("error", bad);
      if (bad) ok = false;
    });
    return ok;
  }
  form.querySelectorAll("[required]").forEach((f) =>
    f.addEventListener("input", () => f.closest(".field")?.classList.remove("error"))
  );

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (!Cart.detailed().length) return;
    if (!validate()) {
      form.querySelector(".field.error")?.scrollIntoView({ behavior: "smooth", block: "center" });
      window.LemToast("Completá los datos requeridos", false);
      return;
    }
    const d = Object.fromEntries(new FormData(form).entries());
    const t = totals();
    const lines = Cart.detailed();
    let msg = `Hola Lemates! Confirmo mi pedido:\n\n`;
    lines.forEach((l, i) => {
      msg += `${i + 1}. *${l.name}* — ${l.qty} x ${fmt(l.price)} = ${fmt(l.lineTotal)}\n`;
    });
    msg += `\n*Subtotal:* ${fmt(t.sub)}\n*Envío (${SHIPPING[shipping].label}):* ${
      t.ship === 0 ? "Gratis" : fmt(t.ship)
    }\n*TOTAL:* ${fmt(t.total)}\n\n`;
    msg += `— DATOS —\n`;
    msg += `Nombre: ${d.nombre} ${d.apellido}\n`;
    msg += `Email: ${d.email}\nTel: ${d.telefono}\n`;
    if (shipping !== "retiro") {
      msg += `Dirección: ${d.direccion}\n${d.localidad}, ${d.provincia} (CP ${d.cp})\n`;
    }
    msg += `Pago: ${payment}\n`;
    if (d.obs && d.obs.trim()) msg += `Obs: ${d.obs}\n`;

    window.open(window.LemWA.link(msg), "_blank");
    window.LemToast("Abriendo WhatsApp para confirmar…");
  });

  // toggle address fields visibility based on shipping
  document.addEventListener("cart:change", renderSummary);
  const addrSection = document.getElementById("addressSection");
  function toggleAddr() {
    if (addrSection) addrSection.style.display = shipping === "retiro" ? "none" : "";
    addrSection?.querySelectorAll("[data-reqable]").forEach((f) => {
      if (shipping === "retiro") f.removeAttribute("required");
      else f.setAttribute("required", "");
    });
  }
  form.querySelectorAll('input[name="shipping"]').forEach((r) =>
    r.addEventListener("change", toggleAddr)
  );

  toggleAddr();
  renderSummary();
})();
