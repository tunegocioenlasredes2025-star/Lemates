/* Página de producto: galería, zoom, cantidad, acciones, relacionados, SEO JSON-LD */
(function () {
  "use strict";
  const root = document.getElementById("productRoot");
  if (!root) return;
  const products = window.LemProducts;
  const fmt = window.LemFmt;
  const params = new URLSearchParams(location.search);
  const id = params.get("id");
  const p = products.find((x) => x.id === id);
  const SITE =
    location.origin && location.origin.startsWith("http")
      ? location.origin
      : "https://www.lemates.com.ar";

  const notFound = document.getElementById("productNotFound");
  if (!p) {
    root.hidden = true;
    if (notFound) notFound.hidden = false;
    return;
  }

  const esc = (s) =>
    String(s).replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
    );

  // ----- Meta / título / breadcrumb -----
  document.title = `${p.name} — ${fmt(p.price)} | Lemates`;
  const md = document.querySelector('meta[name="description"]');
  if (md) md.setAttribute("content", p.description.slice(0, 155));
  const canon = document.querySelector('link[rel="canonical"]');
  if (canon) canon.href = SITE + "/producto.html?id=" + p.id;
  document.querySelectorAll(".js-crumb-name").forEach((n) => (n.textContent = p.name));
  const ogt = document.querySelector('meta[property="og:title"]');
  if (ogt) ogt.setAttribute("content", `${p.name} — Lemates`);
  const ogi = document.querySelector('meta[property="og:image"]');
  if (ogi) ogi.setAttribute("content", SITE + "/" + p.images[0].src);

  // ----- Render -----
  const tagsHTML = [
    p.new ? '<span class="tag tag--new">Nuevo</span>' : "",
    p.bestseller ? '<span class="tag tag--best">Más vendido</span>' : "",
  ].join("");

  const thumbs = p.images
    .map(
      (im, i) =>
        `<button class="gallery__thumb${i === 0 ? " active" : ""}" data-i="${i}" aria-label="Imagen ${
          i + 1
        }"><img src="${im.thumb}" alt="${esc(p.name)} ${i + 1}" loading="lazy"></button>`
    )
    .join("");

  const matHTML = (p.materials || []).length
    ? `<div class="materials-row">${p.materials
        .map((m) => `<span class="mat-tag">${esc(m)}</span>`)
        .join("")}</div>`
    : "";

  root.innerHTML = `
    <div class="gallery">
      <div class="gallery__main" id="galMain">
        ${tagsHTML ? `<div class="product-card__tags">${tagsHTML}</div>` : ""}
        <img src="${p.images[0].src}" alt="${esc(p.name)}" id="galImg" width="1000" height="1000">
      </div>
      ${p.images.length > 1 ? `<div class="gallery__thumbs">${thumbs}</div>` : ""}
    </div>
    <div class="product-info">
      <span class="product-card__cat">${esc(p.category)}</span>
      <h1>${esc(p.name)}</h1>
      <div class="price-row">
        <span class="price">${fmt(p.price)}</span>
        <span class="stock-pill"><span class="dot"></span> En stock</span>
      </div>
      ${matHTML}
      <p class="desc">${esc(p.description)}</p>
      <div class="qty-row">
        <div class="qty-stepper">
          <button id="qMinus" aria-label="Restar">–</button>
          <span id="qVal">1</span>
          <button id="qPlus" aria-label="Sumar">+</button>
        </div>
        <span style="font-size:.88rem;color:var(--muted)">Cantidad</span>
      </div>
      <div class="product-actions">
        <button class="btn btn--primary btn--lg btn--block" id="addBtn">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
          Agregar al carrito
        </button>
        <div class="row">
          <a class="btn btn--gold" href="checkout.html" id="buyBtn">Comprar ahora</a>
          <a class="btn btn--wa" id="waBtn" target="_blank" rel="noopener">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.4 1.3 4.9L2 22l5.3-1.4c1.4.8 3 1.2 4.7 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18c-1.5 0-3-.4-4.2-1.2l-.3-.2-3.1.8.8-3-.2-.3C4.4 15 4 13.5 4 12c0-4.4 3.6-8 8-8s8 3.6 8 8-3.6 8-8 8zm4.5-6.6c-.3-.1-1.7-.8-1.9-.9-.3-.1-.5-.1-.7.1-.2.3-.7.9-.9 1.1-.2.2-.3.2-.6.1-1.5-.8-2.5-1.4-3.5-3.1-.3-.5.3-.4.8-1.4.1-.2 0-.4 0-.5s-.7-1.6-.9-2.2c-.2-.5-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.3 5.2 4.6 1.9.8 2.7.9 3.6.8.6-.1 1.7-.7 1.9-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3z"/></svg>
            WhatsApp
          </a>
        </div>
      </div>
      <ul class="product-meta">
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9h18M3 9l2-5h14l2 5M3 9v10a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1V9"/></svg><span>Envíos a todo el país por Correo Argentino y retiro en zona oeste (GBA).</span></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg><span>Producto artesanal seleccionado pieza por pieza.</span></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg><span>Consultá disponibilidad y coordiná tu compra por WhatsApp.</span></li>
      </ul>
    </div>`;

  // ----- Galería -----
  const galImg = document.getElementById("galImg");
  const galMain = document.getElementById("galMain");
  root.querySelectorAll(".gallery__thumb").forEach((btn) =>
    btn.addEventListener("click", () => {
      const i = +btn.dataset.i;
      galImg.src = p.images[i].src;
      root.querySelectorAll(".gallery__thumb").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      galMain.classList.remove("zoomed");
    })
  );
  // zoom on click (desktop) with transform-origin follow
  galMain.addEventListener("click", () => galMain.classList.toggle("zoomed"));
  galMain.addEventListener("mousemove", (e) => {
    if (!galMain.classList.contains("zoomed")) return;
    const r = galMain.getBoundingClientRect();
    galImg.style.transformOrigin = `${((e.clientX - r.left) / r.width) * 100}% ${
      ((e.clientY - r.top) / r.height) * 100
    }%`;
  });

  // ----- Cantidad -----
  let qty = 1;
  const qVal = document.getElementById("qVal");
  document.getElementById("qMinus").addEventListener("click", () => {
    qty = Math.max(1, qty - 1);
    qVal.textContent = qty;
  });
  document.getElementById("qPlus").addEventListener("click", () => {
    qty += 1;
    qVal.textContent = qty;
  });

  // ----- Acciones -----
  const waBtn = document.getElementById("waBtn");
  const syncWa = () => (waBtn.href = window.LemWA.product(p, qty));
  syncWa();
  document.getElementById("qMinus").addEventListener("click", syncWa);
  document.getElementById("qPlus").addEventListener("click", syncWa);
  document.getElementById("addBtn").addEventListener("click", () => {
    window.LemCart.add(p.id, qty);
    window.LemToast(`${p.name} agregado (${qty})`);
    window.LemDrawer.open();
  });
  document.getElementById("buyBtn").addEventListener("click", () => {
    window.LemCart.add(p.id, qty);
  });

  // ----- Relacionados -----
  const relWrap = document.getElementById("relatedGrid");
  if (relWrap) {
    let rel = products.filter((x) => x.id !== p.id && x.category === p.category);
    if (rel.length < 4)
      rel = rel.concat(products.filter((x) => x.id !== p.id && x.category !== p.category));
    window.LemRenderCards(relWrap, rel.slice(0, 4));
  }

  // ----- JSON-LD -----
  const ld = {
    "@context": "https://schema.org/",
    "@type": "Product",
    name: p.name,
    image: p.images.map((im) => SITE + "/" + im.src),
    description: p.description,
    category: p.category,
    brand: { "@type": "Brand", name: "Lemates" },
    offers: {
      "@type": "Offer",
      priceCurrency: "ARS",
      price: p.price,
      availability: "https://schema.org/InStock",
      url: SITE + "/producto.html?id=" + p.id,
      seller: { "@type": "Organization", name: "Lemates · Tienda Matera" },
    },
  };
  const s = document.createElement("script");
  s.type = "application/ld+json";
  s.textContent = JSON.stringify(ld);
  document.head.appendChild(s);
})();
