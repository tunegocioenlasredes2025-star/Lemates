/* ============================================================
   LEMATES — Núcleo compartido (carrito, nav, WhatsApp, UI)
   ============================================================ */
(function () {
  "use strict";

  const WA_NUMBER = "5491154693079"; // +54 9 11 5469-3079
  const STORE = "Lemates · Tienda Matera";
  // Base para links absolutos (WhatsApp/SEO). En file:// origin es "null": usamos un fallback.
  const SITE = (location.origin && location.origin.startsWith("http"))
    ? location.origin
    : "https://www.lemates.com.ar";
  const CART_KEY = "lemates_cart_v1";
  const DATA = (window.LEMATES_DATA || { products: [], categories: {} });
  const PRODUCTS = DATA.products;
  const byId = (id) => PRODUCTS.find((p) => p.id === id);

  /* ---------- Utilidades ---------- */
  const fmt = (n) =>
    "$" + Number(n).toLocaleString("es-AR", { maximumFractionDigits: 0 });
  const waLink = (msg) =>
    `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(msg)}`;
  const esc = (s) =>
    String(s).replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
    );

  /* ---------- Carrito (localStorage) ---------- */
  const Cart = {
    items: [],
    load() {
      try {
        this.items = JSON.parse(localStorage.getItem(CART_KEY)) || [];
      } catch (e) {
        this.items = [];
      }
      this.items = this.items.filter((i) => byId(i.id));
    },
    save() {
      localStorage.setItem(CART_KEY, JSON.stringify(this.items));
      this.emit();
    },
    emit() {
      document.dispatchEvent(new CustomEvent("cart:change"));
    },
    add(id, qty = 1) {
      const line = this.items.find((i) => i.id === id);
      if (line) line.qty += qty;
      else this.items.push({ id, qty });
      this.save();
    },
    setQty(id, qty) {
      const line = this.items.find((i) => i.id === id);
      if (!line) return;
      line.qty = Math.max(1, qty);
      this.save();
    },
    remove(id) {
      this.items = this.items.filter((i) => i.id !== id);
      this.save();
    },
    clear() {
      this.items = [];
      this.save();
    },
    detailed() {
      return this.items
        .map((i) => {
          const p = byId(i.id);
          return p ? { ...p, qty: i.qty, lineTotal: p.price * i.qty } : null;
        })
        .filter(Boolean);
    },
    count() {
      return this.items.reduce((s, i) => s + i.qty, 0);
    },
    subtotal() {
      return this.detailed().reduce((s, l) => s + l.lineTotal, 0);
    },
  };
  Cart.load();
  window.LemCart = Cart;

  /* ---------- Toast ---------- */
  let toastWrap;
  function toast(msg, icon = true) {
    if (!toastWrap) {
      toastWrap = document.createElement("div");
      toastWrap.className = "toast-wrap";
      document.body.appendChild(toastWrap);
    }
    const t = document.createElement("div");
    t.className = "toast";
    t.innerHTML =
      (icon
        ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>'
        : "") + `<span>${esc(msg)}</span>`;
    toastWrap.appendChild(t);
    requestAnimationFrame(() => t.classList.add("show"));
    setTimeout(() => {
      t.classList.remove("show");
      setTimeout(() => t.remove(), 400);
    }, 2600);
  }
  window.LemToast = toast;

  /* ---------- Mensajes de WhatsApp ---------- */
  function waProduct(p, qty = 1) {
    const url = SITE + "/producto.html?id=" + p.id;
    return waLink(
      `Hola ${STORE}! Me interesa este producto:\n\n*${p.name}*\n${fmt(
        p.price
      )}${qty > 1 ? ` x ${qty}` : ""}\n${url}\n\n¿Está disponible?`
    );
  }
  function waCart() {
    const lines = Cart.detailed();
    if (!lines.length) return waLink(`Hola ${STORE}! Quiero hacer una consulta.`);
    let msg = `Hola ${STORE}! Quiero hacer este pedido:\n\n`;
    lines.forEach((l, i) => {
      msg += `${i + 1}. *${l.name}*\n   ${l.qty} x ${fmt(l.price)} = ${fmt(
        l.lineTotal
      )}\n`;
    });
    msg += `\n*Total: ${fmt(Cart.subtotal())}*\n\n¿Cómo seguimos con el pago y el envío?`;
    return waLink(msg);
  }
  window.LemWA = { link: waLink, product: waProduct, cart: waCart, number: WA_NUMBER };

  /* ---------- Tarjeta de producto (render) ---------- */
  function productCardHTML(p) {
    const img = p.images[0];
    const tags = [];
    if (p.new) tags.push('<span class="tag tag--new">Nuevo</span>');
    if (p.bestseller) tags.push('<span class="tag tag--best">Más vendido</span>');
    if (!p.new && !p.bestseller && p.featured)
      tags.push('<span class="tag tag--feat">Destacado</span>');
    const href = "producto.html?id=" + p.id;
    return `<article class="product-card reveal">
      <a class="product-card__media" href="${href}" aria-label="${esc(p.name)}">
        <img src="${img.thumb}" alt="${esc(p.name)}" loading="lazy" width="600" height="600">
        ${tags.length ? `<div class="product-card__tags">${tags.join("")}</div>` : ""}
        <div class="product-card__quick">
          <span class="btn btn--gold btn--sm btn--block">Ver producto</span>
        </div>
      </a>
      <div class="product-card__body">
        <span class="product-card__cat">${esc(p.category)}</span>
        <h3 class="product-card__name"><a href="${href}">${esc(p.name)}</a></h3>
        <div class="product-card__foot">
          <span class="price">${fmt(p.price)}</span>
          <button class="add-btn js-add" data-id="${p.id}" aria-label="Agregar ${esc(
      p.name
    )} al carrito" title="Agregar al carrito">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
          </button>
        </div>
      </div>
    </article>`;
  }
  window.LemRenderCard = productCardHTML;

  function renderCards(container, list) {
    container.innerHTML = list.map(productCardHTML).join("");
    observeReveals(container);
  }
  window.LemRenderCards = renderCards;

  /* ---------- Delegación: agregar al carrito ---------- */
  document.addEventListener("click", (e) => {
    const add = e.target.closest(".js-add");
    if (add) {
      e.preventDefault();
      const id = add.dataset.id;
      const qty = parseInt(add.dataset.qty || "1", 10);
      Cart.add(id, qty);
      const p = byId(id);
      toast(`${p ? p.name : "Producto"} agregado`);
      openDrawer();
    }
  });

  /* ---------- Contador del carrito ---------- */
  function updateCartCount() {
    const n = Cart.count();
    document.querySelectorAll(".cart-count").forEach((el) => {
      el.textContent = n;
      el.classList.toggle("show", n > 0);
    });
  }

  /* ---------- Cart drawer ---------- */
  let drawer;
  function buildDrawer() {
    drawer = document.createElement("div");
    drawer.className = "drawer";
    drawer.id = "cartDrawer";
    drawer.innerHTML = `
      <div class="drawer__scrim" data-close></div>
      <aside class="drawer__panel" role="dialog" aria-label="Carrito de compras" aria-modal="true">
        <header class="drawer__head">
          <h3>Tu carrito</h3>
          <button class="icon-btn" data-close aria-label="Cerrar carrito">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg>
          </button>
        </header>
        <div class="drawer__body" id="drawerBody"></div>
        <div class="drawer__foot" id="drawerFoot" hidden>
          <div class="drawer__row"><span>Subtotal</span><span id="drawerSub"></span></div>
          <p style="font-size:.8rem;color:var(--muted);margin:-4px 0 4px">Envío calculado en el checkout.</p>
          <a class="btn btn--primary btn--block" href="checkout.html">Finalizar compra</a>
          <a class="btn btn--wa btn--block" id="drawerWa" target="_blank" rel="noopener">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.1-1.7-.8-1.9-.9-.3-.1-.5-.1-.7.1-.2.3-.7.9-.9 1.1-.2.2-.3.2-.6.1-1.5-.8-2.5-1.4-3.5-3.1-.3-.5.3-.4.8-1.4.1-.2 0-.4 0-.5-.1-.1-.7-1.5-.9-2.1-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.3 5.2 4.6 1.9.8 2.7.9 3.6.8.6-.1 1.7-.7 1.9-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3z"/><path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.4 1.3 4.9L2 22l5.3-1.4c1.4.8 3 1.2 4.7 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18c-1.5 0-3-.4-4.2-1.2l-.3-.2-3.1.8.8-3-.2-.3C4.4 15 4 13.5 4 12c0-4.4 3.6-8 8-8s8 3.6 8 8-3.6 8-8 8z"/></svg>
            Pedir por WhatsApp
          </a>
        </div>
      </aside>`;
    document.body.appendChild(drawer);
    drawer.addEventListener("click", (e) => {
      if (e.target.closest("[data-close]")) closeDrawer();
    });
  }
  function renderDrawer() {
    if (!drawer) return;
    const body = drawer.querySelector("#drawerBody");
    const foot = drawer.querySelector("#drawerFoot");
    const lines = Cart.detailed();
    if (!lines.length) {
      body.innerHTML = `<div class="cart-empty">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
        <p>Tu carrito está vacío.</p>
        <a class="btn btn--gold" href="catalogo.html">Ver catálogo</a>
      </div>`;
      foot.hidden = true;
      return;
    }
    body.innerHTML = lines
      .map(
        (l) => `<div class="cart-line" data-id="${l.id}">
        <a class="cart-line__img" href="producto.html?id=${l.id}"><img src="${
          l.images[0].thumb
        }" alt="${esc(l.name)}" loading="lazy"></a>
        <div>
          <div class="cart-line__name">${esc(l.name)}</div>
          <div class="cart-line__price">${fmt(l.price)}</div>
          <div class="cart-line__qty">
            <button class="js-dec" data-id="${l.id}" aria-label="Restar">–</button>
            <span>${l.qty}</span>
            <button class="js-inc" data-id="${l.id}" aria-label="Sumar">+</button>
          </div>
        </div>
        <div class="cart-line__end">
          <span class="cart-line__sub">${fmt(l.lineTotal)}</span>
          <button class="cart-line__rm js-rm" data-id="${l.id}">Quitar</button>
        </div>
      </div>`
      )
      .join("");
    drawer.querySelector("#drawerSub").textContent = fmt(Cart.subtotal());
    drawer.querySelector("#drawerWa").href = waCart();
    foot.hidden = false;
  }
  function openDrawer() {
    if (!drawer) buildDrawer();
    renderDrawer();
    drawer.classList.add("open");
    document.body.style.overflow = "hidden";
  }
  function closeDrawer() {
    if (drawer) drawer.classList.remove("open");
    document.body.style.overflow = "";
  }
  window.LemDrawer = { open: openDrawer, close: closeDrawer };

  // qty +/- and remove inside drawer
  document.addEventListener("click", (e) => {
    const inc = e.target.closest(".js-inc");
    const dec = e.target.closest(".js-dec");
    const rm = e.target.closest(".js-rm");
    if (inc) {
      const l = Cart.items.find((i) => i.id === inc.dataset.id);
      Cart.setQty(inc.dataset.id, (l ? l.qty : 1) + 1);
    } else if (dec) {
      const l = Cart.items.find((i) => i.id === dec.dataset.id);
      Cart.setQty(dec.dataset.id, (l ? l.qty : 1) - 1);
    } else if (rm) {
      Cart.remove(rm.dataset.id);
    }
  });

  /* ---------- Header interacciones ---------- */
  function initHeader() {
    const header = document.querySelector(".header");
    if (header) {
      const onScroll = () =>
        header.classList.toggle("is-scrolled", window.scrollY > 8);
      onScroll();
      window.addEventListener("scroll", onScroll, { passive: true });
    }
    // Cart openers
    document.querySelectorAll("[data-cart-open]").forEach((b) =>
      b.addEventListener("click", (e) => {
        e.preventDefault();
        openDrawer();
      })
    );
    // Mobile menu
    const mnav = document.querySelector(".mobile-nav");
    const toggle = document.querySelector(".menu-toggle");
    if (mnav && toggle) {
      const open = () => {
        mnav.classList.add("open");
        document.body.style.overflow = "hidden";
      };
      const close = () => {
        mnav.classList.remove("open");
        document.body.style.overflow = "";
      };
      toggle.addEventListener("click", open);
      mnav.addEventListener("click", (e) => {
        if (e.target.closest("[data-mclose]") || e.target.classList.contains("mobile-nav__scrim"))
          close();
      });
    }
    // Esc closes overlays
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        closeDrawer();
        if (mnav) mnav.classList.remove("open");
        document.body.style.overflow = "";
      }
    });
  }

  /* ---------- Scroll to top ---------- */
  function initToTop() {
    const btn = document.querySelector(".to-top");
    if (!btn) return;
    const onScroll = () => btn.classList.toggle("show", window.scrollY > 600);
    window.addEventListener("scroll", onScroll, { passive: true });
    btn.addEventListener("click", () =>
      window.scrollTo({ top: 0, behavior: "smooth" })
    );
  }

  /* ---------- Reveal on scroll ---------- */
  let io;
  function observeReveals(root = document) {
    if (!("IntersectionObserver" in window)) {
      root.querySelectorAll(".reveal").forEach((el) => el.classList.add("in"));
      return;
    }
    if (!io) {
      io = new IntersectionObserver(
        (entries) => {
          entries.forEach((en) => {
            if (en.isIntersecting) {
              en.target.classList.add("in");
              io.unobserve(en.target);
            }
          });
        },
        { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
      );
    }
    root.querySelectorAll(".reveal:not(.in)").forEach((el) => io.observe(el));
  }
  window.LemObserve = observeReveals;

  /* ---------- Loader ---------- */
  function hideLoader() {
    const l = document.querySelector(".page-loader");
    if (l) setTimeout(() => l.classList.add("hide"), 200);
  }

  /* ---------- WhatsApp flotante ---------- */
  function initWaFloat() {
    const wa = document.querySelector(".wa-float");
    if (wa && !wa.href)
      wa.href = waLink(`Hola ${STORE}! Quisiera hacer una consulta.`);
  }

  /* ---------- Init ---------- */
  document.addEventListener("cart:change", () => {
    updateCartCount();
    renderDrawer();
  });

  function init() {
    initHeader();
    initToTop();
    initWaFloat();
    updateCartCount();
    observeReveals();
    hideLoader();
    // mark active nav
    const path = location.pathname.split("/").pop() || "index.html";
    document.querySelectorAll("[data-nav]").forEach((a) => {
      if (a.getAttribute("data-nav") === path) a.classList.add("is-active");
    });
  }
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", init);
  else init();

  window.LemFmt = fmt;
  window.LemProducts = PRODUCTS;
})();
