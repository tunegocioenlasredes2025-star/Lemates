# -*- coding: utf-8 -*-
"""Genera las páginas HTML estáticas de Lemates a partir de partials compartidos."""
import os, json, html

ROOT = r"C:/TNR/Lemates"
BASE = "https://www.lemates.com.ar"   # <-- Cambiar por el dominio real al desplegar
WA = "5491154693079"
IG = "https://www.instagram.com/lemates1/"
DATA = json.load(open(os.path.join(ROOT, "assets/js/products-data.json"), encoding="utf-8"))

NAV = [
    ("index.html", "Inicio"),
    ("catalogo.html", "Catálogo"),
    ("nosotros.html", "Nosotros"),
    ("faq.html", "Preguntas"),
    ("contacto.html", "Contacto"),
]

# ---------------- Icons ----------------
I = {
 "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>',
 "cart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>',
 "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
 "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="2" y="2" width="20" height="20" rx="5.5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>',
 "wa": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.4 1.3 4.9L2 22l5.3-1.4c1.4.8 3 1.2 4.7 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18c-1.5 0-3-.4-4.2-1.2l-.3-.2-3.1.8.8-3-.2-.3C4.4 15 4 13.5 4 12c0-4.4 3.6-8 8-8s8 3.6 8 8-3.6 8-8 8zm4.5-6.6c-.3-.1-1.7-.8-1.9-.9-.3-.1-.5-.1-.7.1-.2.3-.7.9-.9 1.1-.2.2-.3.2-.6.1-1.5-.8-2.5-1.4-3.5-3.1-.3-.5.3-.4.8-1.4.1-.2 0-.4 0-.5s-.7-1.6-.9-2.2c-.2-.5-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.3 5.2 4.6 1.9.8 2.7.9 3.6.8.6-.1 1.7-.7 1.9-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3z"/></svg>',
 "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>',
 "chev": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>',
 "up": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m18 15-6-6-6 6"/></svg>',
 "star": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14l-5-4.87 6.91-1.01z"/></svg>',
 "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.94.36 1.87.68 2.75a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.88.32 1.81.55 2.75.68A2 2 0 0 1 22 16.92z"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 "truck": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M1 3h15v13H1z"/><path d="M16 8h4l3 3v5h-7V8z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>',
 "hand": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M18 11V6a2 2 0 0 0-2-2 2 2 0 0 0-2 2M14 10V4a2 2 0 0 0-2-2 2 2 0 0 0-2 2v2M10 10.5V6a2 2 0 0 0-2-2 2 2 0 0 0-2 2v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/></svg>',
 "card": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/></svg>',
 "heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8z"/></svg>',
 "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z"/><path d="M2 21c0-3 1.85-5.36 5.08-6"/></svg>',
 "gift": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="8" width="18" height="4"/><path d="M12 8v13M5 12v9h14v-9M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"/></svg>',
 "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>',
}

def esc(s): return html.escape(str(s), quote=True)

def img_for(cat):
    for p in DATA:
        if p["category"] == cat:
            return p["images"][0]
    return DATA[0]["images"][0]

CAT_INFO = {
 "Mates": ("mates", "Imperiales, torpedos y rancheros en calabaza, algarrobo y alpaca."),
 "Bombillas": ("bombillas", "Bombillas y bombillones de alpaca y bronce, cincelados y con dije."),
 "Termos": ("termos", "Termos de alto rendimiento con pico cebador de precisión."),
 "Materas": ("materas", "Materas de cuero y cuerina para llevar tu equipo a todos lados."),
}

# ---------------- Partials ----------------
def head(title, desc, path, og_type="website", extra_ld=None):
    canonical = f"{BASE}/{path}"
    ld = {
        "@context": "https://schema.org",
        "@type": "Store",
        "name": "Lemates · Tienda Matera",
        "image": f"{BASE}/assets/img/brand/og-image.jpg",
        "description": "Tienda matera artesanal. Mates, bombillas, termos y materas de primera calidad. Envíos a todo el país.",
        "url": BASE,
        "telephone": "+5491154693079",
        "areaServed": "AR",
        "sameAs": [IG],
        "priceRange": "$$",
    }
    ld_blocks = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    if extra_ld:
        ld_blocks += f'<script type="application/ld+json">{json.dumps(extra_ld, ensure_ascii=False)}</script>'
    return f'''<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#d38f44">
<meta name="author" content="Lemates">
<meta name="robots" content="index, follow">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Lemates · Tienda Matera">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/assets/img/brand/og-image.jpg">
<meta property="og:locale" content="es_AR">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{BASE}/assets/img/brand/og-image.jpg">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/brand/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/brand/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Marcellus&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Marcellus&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/styles.css">
{ld_blocks}
</head>
<body>
<div class="page-loader"><img class="loader-mate" src="/assets/img/brand/mate-icon.png" alt="Cargando"></div>'''

def brand(footer=False):
    cls = "brand footer__brand" if footer else "brand"
    return f'''<a class="{cls}" href="/index.html" aria-label="Lemates inicio">
  <span class="brand__mark"><img src="/assets/img/brand/mate-icon.png" alt="" width="30" height="30"></span>
  <span class="brand__text"><span class="brand__name">LEMATES</span><span class="brand__sub">Tienda Matera</span></span>
</a>'''

def header(active):
    links = "".join(
        f'<a href="/{h}" data-nav="{h}"{" class=\"is-active\"" if h==active else ""}>{t}</a>'
        for h, t in NAV
    )
    return f'''<header class="header">
  <div class="container header__bar">
    {brand()}
    <nav class="nav" aria-label="Principal">{links}</nav>
    <div class="header__actions">
      <a class="icon-btn" href="/catalogo.html" aria-label="Buscar productos">{I['search']}</a>
      <button class="icon-btn" data-cart-open aria-label="Abrir carrito">{I['cart']}<span class="cart-count">0</span></button>
      <button class="icon-btn menu-toggle" aria-label="Abrir menú">{I['menu']}</button>
    </div>
  </div>
</header>'''

def mobile_nav(active):
    links = "".join(
        f'<a href="/{h}" data-mclose{" class=\"is-active\"" if h==active else ""}>{t}</a>'
        for h, t in NAV
    )
    return f'''<div class="mobile-nav">
  <div class="mobile-nav__scrim"></div>
  <aside class="mobile-nav__panel" role="dialog" aria-label="Menú">
    <div class="mobile-nav__head">{brand()}<button class="icon-btn" data-mclose aria-label="Cerrar menú"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg></button></div>
    <nav class="mobile-nav__links">{links}<a href="/carrito.html" data-mclose>Carrito</a></nav>
    <div class="mobile-nav__foot">
      <a class="btn btn--wa btn--block" href="https://wa.me/{WA}" target="_blank" rel="noopener">{I['wa']} Escribinos por WhatsApp</a>
      <div class="mobile-nav__social">
        <a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{I['ig']}</a>
      </div>
    </div>
  </aside>
</div>'''

def footer():
    shop_links = "".join(f'<a href="/catalogo.html?cat={CAT_INFO[c][0].capitalize()}">{c}</a>' for c in ["Mates","Bombillas","Termos","Materas"])
    return f'''<footer class="footer">
  <div class="container">
    <div class="footer__top">
      <div class="footer__brand">
        {brand(footer=True)}
        <p>Tienda matera artesanal. Seleccionamos cada mate, bombilla y termo para que vivas la tradición con la mejor calidad. Envíos a todo el país.</p>
        <div class="footer__social">
          <a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{I['ig']}</a>
          <a href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="WhatsApp">{I['wa']}</a>
        </div>
      </div>
      <div>
        <h4>Tienda</h4>
        <nav class="footer__links"><a href="/catalogo.html">Catálogo</a>{"".join(f'<a href="/catalogo.html?cat={c}">{c}</a>' for c in ["Mates","Bombillas","Termos","Materas"])}</nav>
      </div>
      <div>
        <h4>Empresa</h4>
        <nav class="footer__links"><a href="/nosotros.html">Nosotros</a><a href="/faq.html">Preguntas frecuentes</a><a href="/contacto.html">Contacto</a><a href="/politicas.html">Políticas</a></nav>
      </div>
      <div>
        <h4>Contacto</h4>
        <ul class="footer__contact">
          <li>{I['wa']}<a href="https://wa.me/{WA}" target="_blank" rel="noopener">+54 9 11 5469-3079</a></li>
          <li>{I['ig']}<a href="{IG}" target="_blank" rel="noopener">@lemates1</a></li>
          <li>{I['pin']}<span>Zona Oeste · GBA, Argentina</span></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© 2026 Lemates · Tienda Matera. Todos los derechos reservados.</span>
      <div class="footer__pay"><span>Transferencia</span><span>Efectivo</span><span>Tarjeta</span></div>
    </div>
  </div>
</footer>'''

def overlays():
    return f'''<a class="wa-float" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="Escribinos por WhatsApp">{I['wa']}</a>
<button class="to-top" aria-label="Volver arriba">{I['up']}</button>'''

def scripts(extra=""):
    s = '<script src="/assets/js/products.js"></script>\n<script src="/assets/js/app.js"></script>'
    if extra:
        s += f'\n<script src="/assets/js/{extra}"></script>'
    return s + "\n</body>\n</html>"

def page(active):
    return header(active) + "\n" + mobile_nav(active)

def to_relative(html_str):
    """Convierte rutas internas absolutas (empiezan con /) en relativas,
    para que el sitio funcione tanto abriendo el archivo (file://) como en un servidor.
    Todas las páginas viven en la raíz, así que basta con quitar el / inicial."""
    # atributos href/src/content que empiezan con "/" (rutas internas)
    for attr in ('href="/', 'src="/', 'content="/'):
        html_str = html_str.replace(attr, attr[:-1])
    return html_str

def write(name, content):
    content = to_relative(content)
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", name)

def breadcrumb(items):
    parts = []
    for i, (label, href) in enumerate(items):
        if href and i < len(items) - 1:
            parts.append(f'<a href="{href}">{esc(label)}</a>')
        else:
            parts.append(f'<span aria-current="page" class="js-crumb-name">{esc(label)}</span>')
    return '<nav class="breadcrumb container" aria-label="Ruta">' + I['chev'].join(parts) + '</nav>'

def crumb_ld(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": lbl,
             "item": (BASE + (href if href else "")) if href else None}
            for i, (lbl, href) in enumerate(items)
        ],
    }

# build individual pages in separate module
import build_pages
build_pages.build(globals())
print("DONE")
