/* Página de carrito completo */
(function () {
  "use strict";
  const wrap = document.getElementById("cartPage");
  if (!wrap) return;
  const fmt = window.LemFmt;
  const Cart = window.LemCart;
  const esc = (s) =>
    String(s).replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
    );

  function render() {
    const lines = Cart.detailed();
    if (!lines.length) {
      wrap.innerHTML = `<div class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
        <h3>Tu carrito está vacío</h3>
        <p>Descubrí nuestra selección de mates, bombillas y termos.</p>
        <a class="btn btn--primary" href="catalogo.html" style="margin-top:20px">Ir al catálogo</a>
      </div>`;
      return;
    }
    wrap.innerHTML = `
      <div class="cart-table">
        ${lines
          .map(
            (l) => `<div class="cart-table__row" data-id="${l.id}">
          <a class="cart-table__img" href="producto.html?id=${l.id}"><img src="${
              l.images[0].thumb
            }" alt="${esc(l.name)}" loading="lazy"></a>
          <div style="grid-area:info">
            <a href="producto.html?id=${l.id}"><b style="font-family:var(--font-display);font-size:1.05rem">${esc(
              l.name
            )}</b></a>
            <div style="color:var(--muted);font-size:.86rem;margin:2px 0 8px">${esc(
              l.category
            )} · ${fmt(l.price)}</div>
            <div class="cart-line__qty">
              <button class="js-dec" data-id="${l.id}" aria-label="Restar">–</button>
              <span>${l.qty}</span>
              <button class="js-inc" data-id="${l.id}" aria-label="Sumar">+</button>
            </div>
          </div>
          <div class="cart-line__sub" style="grid-area:end;font-family:var(--font-display);font-size:1.15rem">${fmt(
            l.lineTotal
          )}</div>
          <button class="cart-line__rm js-rm" data-id="${l.id}" style="grid-area:end;align-self:end">Quitar</button>
        </div>`
          )
          .join("")}
      </div>
      <aside class="summary">
        <h3>Resumen</h3>
        <div class="summary__row"><span>Subtotal (${Cart.count()} art.)</span><span>${fmt(
      Cart.subtotal()
    )}</span></div>
        <div class="summary__row"><span>Envío</span><span>A calcular</span></div>
        <div class="summary__row total"><span>Total</span><span>${fmt(
          Cart.subtotal()
        )}</span></div>
        <a class="btn btn--primary btn--block" href="checkout.html">Finalizar compra</a>
        <a class="btn btn--wa btn--block" id="cartWa" target="_blank" rel="noopener">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.4 1.3 4.9L2 22l5.3-1.4c1.4.8 3 1.2 4.7 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2z"/></svg>
          Pedir por WhatsApp
        </a>
        <button class="btn btn--ghost btn--block js-clear">Vaciar carrito</button>
        <a class="link-arrow" href="catalogo.html" style="justify-content:center;margin-top:6px">
          Seguir comprando
        </a>
      </aside>`;
    const wa = document.getElementById("cartWa");
    if (wa) wa.href = window.LemWA.cart();
  }

  wrap.addEventListener("click", (e) => {
    if (e.target.closest(".js-clear")) {
      Cart.clear();
      window.LemToast("Carrito vaciado", false);
    }
  });
  document.addEventListener("cart:change", render);
  render();
})();
