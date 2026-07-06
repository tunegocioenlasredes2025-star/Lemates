# -*- coding: utf-8 -*-
"""Cuerpos de cada página. build(g) recibe los helpers de build_site."""

def build(g):
    head=g["head"]; page=g["page"]; footer=g["footer"]; overlays=g["overlays"]
    scripts=g["scripts"]; write=g["write"]; I=g["I"]; DATA=g["DATA"]; esc=g["esc"]
    img_for=g["img_for"]; breadcrumb=g["breadcrumb"]; crumb_ld=g["crumb_ld"]
    BASE=g["BASE"]; WA=g["WA"]; IG=g["IG"]; CAT_INFO=g["CAT_INFO"]

    def sec_head(eyebrow, title, sub="", center=False, tag="h2"):
        c = " center" if center else ""
        p = f"<p class='lead'>{sub}</p>" if sub else ""
        return f'''<div class="section-head{c} reveal"><span class="eyebrow">{eyebrow}</span><{tag}>{title}</{tag}>{p}</div>'''

    featured = [p for p in DATA if p["featured"]][:8]
    if len(featured) < 8:
        featured += [p for p in DATA if p not in featured][:8-len(featured)]
    news = [p for p in DATA if p["new"]][:4] or DATA[:4]
    ig_imgs = [p["images"][0]["thumb"] for p in DATA[:6]]

    # ============================================================ HOME
    hero_img = "assets/img/products/imperial-calabaza-repujado-virola-y-base-de-alpaca-y-pelotas-de-bronce.webp"
    cats_html = ""
    for c in ["Mates","Bombillas","Termos","Materas"]:
        im = img_for(c); slug, dsc = CAT_INFO[c]
        cats_html += f'''<a class="cat-card reveal" href="/catalogo.html?cat={c}">
      <img src="/{im['thumb']}" alt="{c}" loading="lazy">
      <div><div class="cat-card__name">{c}</div><div class="cat-card__meta">Ver colección {I['arrow']}</div></div>
    </a>'''

    benefits = [
        (I['truck'], "Envíos a todo el país", "Despachamos por Correo Argentino y coordinamos retiro en zona oeste."),
        (I['hand'], "Selección artesanal", "Elegimos pieza por pieza mates, bombillas y termos de calidad real."),
        (I['chat'], "Atención directa", "Te asesoramos por WhatsApp antes, durante y después de tu compra."),
        (I['shield'], "Compra segura", "Transferencia, efectivo o tarjeta. Coordinás todo con una persona real."),
    ]
    ben_html = "".join(f'''<div class="benefit reveal" data-delay="{i%4}"><div class="benefit__ic">{ic}</div><h3>{t}</h3><p>{d}</p></div>''' for i,(ic,t,d) in enumerate(benefits))

    steps = [
        ("Elegí tu equipo","Explorá el catálogo y sumá tus favoritos al carrito."),
        ("Confirmá el pedido","Finalizá la compra o escribinos directo por WhatsApp."),
        ("Coordinamos el pago","Transferencia, efectivo o tarjeta, como te quede cómodo."),
        ("Recibí tu mate","Envío a todo el país o retiro en zona oeste del GBA."),
    ]
    steps_html = "".join(f'''<div class="step reveal" data-delay="{i%4}"><div class="step__n">0{i+1}</div><h3>{t}</h3><p>{d}</p></div>''' for i,(t,d) in enumerate(steps))

    testis = [
        ("Excelente calidad y atención. El mate llegó impecable y curado, listo para usar. Volveré a comprar sin dudas.","Carolina G.","Compra verificada"),
        ("Me asesoraron por WhatsApp para elegir la bombilla ideal. Muy buena onda y producto de primera.","Martín R.","Cliente frecuente"),
        ("El termo mantiene la temperatura como ninguno. Se nota que eligen bien lo que venden.","Lucía P.","Compra verificada"),
    ]
    testi_html = "".join(f'''<figure class="testi reveal" data-delay="{i%3}">
      <div class="testi__stars">{I['star']*5}</div>
      <blockquote><p>“{q}”</p></blockquote>
      <figcaption class="testi__who"><span class="testi__av">{n[0]}</span><span><b>{n}</b><span>{r}</span></span></figcaption>
    </figure>''' for i,(q,n,r) in enumerate(testis))

    ig_html = "".join(f'''<a class="ig-item reveal" href="{IG}" target="_blank" rel="noopener" aria-label="Ver en Instagram"><img src="/{im}" alt="Publicación de Lemates en Instagram" loading="lazy"></a>''' for im in ig_imgs)

    feat_cards = "".join(g["__card"](p) if "__card" in g else "" for p in [])  # placeholder

    body = f'''{page("index.html")}
<main id="main">
  <!-- HERO -->
  <section class="hero">
    <div class="container hero__inner">
      <div class="hero__content reveal">
        <span class="eyebrow">Tradición matera argentina</span>
        <h1>El mate perfecto <em>existe</em>. Y te está esperando.</h1>
        <p class="lead">Mates, bombillas, termos y materas seleccionados a mano. Piezas artesanales de calidad real para disfrutar cada mateada como se merece.</p>
        <div class="hero__cta">
          <a class="btn btn--primary btn--lg" href="/catalogo.html">Ver catálogo {I['arrow']}</a>
          <a class="btn btn--outline btn--lg" href="https://wa.me/{WA}" target="_blank" rel="noopener">Asesorate por WhatsApp</a>
        </div>
        <ul class="hero__trust">
          <li>{I['check']} Envíos a todo el país</li>
          <li>{I['check']} Atención personalizada</li>
          <li>{I['check']} Productos artesanales</li>
        </ul>
      </div>
      <div class="hero__media reveal" data-delay="1">
        <div class="hero__glow"></div>
        <div class="hero__card"><img src="/{hero_img}" alt="Mate imperial de calabaza repujado con virola de alpaca" width="600" height="750" fetchpriority="high"></div>
        <div class="hero__badge hero__badge--tl"><span class="n">+20</span><span class="l">modelos<br>disponibles</span></div>
        <div class="hero__badge hero__badge--br"><span style="color:var(--primary)">{I['star']}</span><span><b style="font-family:var(--font-display);font-size:1.1rem">Calidad</b><br><span class="l">artesanal garantizada</span></span></div>
      </div>
    </div>
  </section>

  <!-- STRIP -->
  <div class="strip"><div class="container"><div class="strip__row">
    <span>{I['truck']} Envíos a todo el país</span>
    <span>{I['hand']} Selección artesanal</span>
    <span>{I['wa']} Compra por WhatsApp</span>
    <span>{I['card']} Transferencia · Efectivo · Tarjeta</span>
  </div></div></div>

  <!-- CATEGORÍAS -->
  <section class="section">
    <div class="container">
      {sec_head("Explorá por categoría","Todo para tu mateada","Desde imperiales de calabaza hasta termos de alto rendimiento.", center=True)}
      <div class="grid cat-grid">{cats_html}</div>
    </div>
  </section>

  <!-- DESTACADOS -->
  <section class="section" style="background:var(--cream-2)">
    <div class="container">
      <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:20px;flex-wrap:wrap">
        {sec_head("Selección Lemates","Productos destacados")}
        <a class="link-arrow reveal" href="/catalogo.html" style="margin-bottom:8px">Ver todo el catálogo {I['arrow']}</a>
      </div>
      <div class="grid card-grid" id="featuredGrid"></div>
    </div>
  </section>

  <!-- BENEFICIOS -->
  <section class="section">
    <div class="container">
      {sec_head("Por qué elegirnos","Una tienda matera de verdad","No somos un marketplace. Somos una marca que cuida cada detalle.", center=True)}
      <div class="grid benefits">{ben_html}</div>
    </div>
  </section>

  <!-- PROCESO -->
  <section class="section" style="background:var(--cream-2)">
    <div class="container">
      {sec_head("Simple y sin vueltas","Cómo comprar en Lemates", center=True)}
      <div class="grid steps">{steps_html}</div>
    </div>
  </section>

  <!-- NUEVOS -->
  <section class="section">
    <div class="container">
      <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:20px;flex-wrap:wrap">
        {sec_head("Recién llegados","Novedades")}
        <a class="link-arrow reveal" href="/catalogo.html?sort=new" style="margin-bottom:8px">Ver novedades {I['arrow']}</a>
      </div>
      <div class="grid card-grid" id="newGrid"></div>
    </div>
  </section>

  <!-- TESTIMONIOS -->
  <section class="section" style="background:var(--cream-2)">
    <div class="container">
      {sec_head("Lo que dicen","Materos que ya nos eligieron", center=True)}
      <div class="grid testi-grid">{testi_html}</div>
    </div>
  </section>

  <!-- CTA -->
  <section class="section--tight"><div class="container">
    <div class="cta-band reveal">
      <span class="eyebrow" style="color:#f3e1d8;justify-content:center">Empezá hoy</span>
      <h2>Tu próxima mateada arranca acá</h2>
      <p>Elegí tu equipo ideal y recibilo en tu casa. Y si tenés dudas, escribinos: te ayudamos a elegir.</p>
      <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap">
        <a class="btn btn--gold btn--lg" href="/catalogo.html">Ver catálogo</a>
        <a class="btn btn--outline btn--lg" href="https://wa.me/{WA}" target="_blank" rel="noopener">{I['wa']} WhatsApp</a>
      </div>
    </div>
  </div></section>

  <!-- INSTAGRAM -->
  <section class="section">
    <div class="container">
      {sec_head("@lemates1","Seguinos en Instagram","Sumate a la comunidad matera y enterate de todas las novedades.", center=True)}
      <div class="grid ig-grid">{ig_html}</div>
      <div class="text-center" style="margin-top:30px"><a class="btn btn--outline" href="{IG}" target="_blank" rel="noopener">{I['ig']} Seguir a @lemates1</a></div>
    </div>
  </section>

  <!-- NEWSLETTER -->
  <section class="section--tight"><div class="container">
    <div class="newsletter reveal">
      <div><span class="eyebrow">Novedades</span><h2 style="margin-top:12px">Sumate al club matero</h2><p class="lead" style="margin-top:8px">Ofertas, lanzamientos y tips para tu mate. Sin spam.</p></div>
      <form onsubmit="event.preventDefault();this.reset();window.LemToast('¡Gracias por suscribirte!')">
        <input type="email" placeholder="Tu email" required aria-label="Email">
        <button class="btn btn--primary" type="submit">Suscribirme</button>
      </form>
    </div>
  </div></section>
</main>
{footer()}
{overlays()}
<script>
document.addEventListener('DOMContentLoaded',function(){{
  var f=document.getElementById('featuredGrid');
  if(f) window.LemRenderCards(f, window.LemProducts.filter(p=>p.featured).slice(0,8).length?window.LemProducts.filter(p=>p.featured).slice(0,8):window.LemProducts.slice(0,8));
  var n=document.getElementById('newGrid');
  if(n){{var nv=window.LemProducts.filter(p=>p.new).slice(0,4);window.LemRenderCards(n, nv.length?nv:window.LemProducts.slice(-4));}}
}});
</script>
{scripts()}'''
    write("index.html", head(
        "Lemates · Tienda Matera | Mates, bombillas y termos artesanales",
        "Tienda matera artesanal. Mates de calabaza y algarrobo, bombillas de alpaca, termos y materas. Envíos a todo el país. Comprá por la web o WhatsApp.",
        "index.html") + body)

    # ============================================================ CATÁLOGO
    chips = '<button class="chip" data-cat="all">Todos</button>' + "".join(
        f'<button class="chip" data-cat="{c}">{c}</button>' for c in ["Mates","Bombillas","Termos","Materas"])
    cl = [("Inicio","/index.html"),("Catálogo",None)]
    body = f'''{page("catalogo.html")}
{breadcrumb(cl)}
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Catálogo completo</span>
    <h1>Todo para el mate perfecto</h1>
    <p class="lead">Explorá nuestra selección de mates, bombillas, termos y materas. Filtrá, buscá y encontrá tu próximo compañero de mateadas.</p>
  </div>
</section>
<main id="main" class="section" style="padding-top:clamp(28px,4vw,48px)">
  <div class="container catalog-layout">
    <div class="catalog-toolbar">
      <div class="search-box">{I['search']}<input type="search" id="search" placeholder="Buscar productos, materiales…" aria-label="Buscar"></div>
      <div class="chips">{chips}</div>
      <div class="toolbar-group">
        <div class="select-wrap">
          <select id="sort" aria-label="Ordenar por">
            <option value="featured">Destacados</option>
            <option value="best">Más vendidos</option>
            <option value="new">Más nuevos</option>
            <option value="price-asc">Precio: menor a mayor</option>
            <option value="price-desc">Precio: mayor a menor</option>
          </select>
        </div>
      </div>
    </div>
    <div class="catalog-meta"><span id="resultCount"></span><button class="link-arrow" id="clearFilters" style="font-size:.85rem">Limpiar filtros</button></div>
    <div class="grid card-grid" id="catalogGrid"></div>
    <div class="empty-state" id="catalogEmpty" hidden>
      {I['search']}
      <h3>No encontramos productos</h3>
      <p>Probá con otra búsqueda o quitá los filtros.</p>
    </div>
  </div>
</main>
{footer()}
{overlays()}
{scripts("catalog.js")}'''
    write("catalogo.html", head(
        "Catálogo | Lemates · Tienda Matera",
        "Catálogo completo de Lemates: mates, bombillas, termos y materas artesanales. Filtrá por categoría, precio y más. Envíos a todo el país.",
        "catalogo.html", extra_ld=crumb_ld(cl)) + body)

    # ============================================================ PRODUCTO
    pl = [("Inicio","/index.html"),("Catálogo","/catalogo.html"),("Producto",None)]
    body = f'''{page("catalogo.html")}
{breadcrumb(pl)}
<main id="main" class="section" style="padding-top:clamp(20px,3vw,36px)">
  <div class="container">
    <div class="product-view" id="productRoot"></div>
    <div id="productNotFound" hidden>
      <div class="empty-state">
        {I['search']}
        <h3>Producto no encontrado</h3>
        <p>El producto que buscás no está disponible.</p>
        <a class="btn btn--primary" href="/catalogo.html" style="margin-top:20px">Volver al catálogo</a>
      </div>
    </div>
  </div>
</main>
<section class="section" style="background:var(--cream-2)" id="relatedSection">
  <div class="container">
    <div class="section-head"><span class="eyebrow">También te puede gustar</span><h2>Productos relacionados</h2></div>
    <div class="grid card-grid" id="relatedGrid"></div>
  </div>
</section>
{footer()}
{overlays()}
{scripts("product.js")}'''
    write("producto.html", head(
        "Producto | Lemates · Tienda Matera",
        "Descubrí este producto artesanal de Lemates. Mates, bombillas y termos de primera calidad con envíos a todo el país.",
        "producto.html", og_type="product", extra_ld=crumb_ld(pl)) + body)

    # ============================================================ NOSOTROS
    ab_img = "assets/img/products/matera-de-cuero.webp"
    values = [
        (I['leaf'],"Tradición","Honramos la cultura matera argentina en cada pieza que elegimos."),
        (I['hand'],"Artesanía","Priorizamos el trabajo hecho a mano y los materiales nobles."),
        (I['heart'],"Cercanía","Atención humana y directa. Detrás de Lemates hay personas, no un formulario."),
    ]
    val_html = "".join(f'''<div class="value reveal" data-delay="{i%3}"><div class="value__ic">{ic}</div><h3>{t}</h3><p>{d}</p></div>''' for i,(ic,t,d) in enumerate(values))
    stats = [("+20","Modelos en catálogo"),("100%","Selección artesanal"),("24h","Respuesta por WhatsApp"),("País","Envíos a toda Argentina")]
    stat_html = "".join(f'''<div class="reveal" data-delay="{i%4}"><div class="stat__n">{n}</div><div class="stat__l">{l}</div></div>''' for i,(n,l) in enumerate(stats))
    al = [("Inicio","/index.html"),("Nosotros",None)]
    body = f'''{page("nosotros.html")}
{breadcrumb(al)}
<main id="main">
  <section class="section">
    <div class="container about-hero">
      <div class="reveal">
        <span class="eyebrow">Nuestra historia</span>
        <h1 style="margin:16px 0 20px">Nacimos por amor al mate</h1>
        <p class="lead" style="margin-bottom:16px">Lemates es una tienda matera pensada para quienes viven el mate como un ritual. Cada día compartimos ese momento y queríamos que el equipo estuviera a la altura.</p>
        <p style="color:var(--ink-soft);margin-bottom:16px">Seleccionamos mates de calabaza y algarrobo, bombillas de alpaca y bronce, termos de alto rendimiento y materas resistentes. No vendemos por vender: elegimos piezas que nosotros mismos usaríamos, con materiales nobles y terminaciones prolijas.</p>
        <p style="color:var(--ink-soft)">Somos una marca cercana. Te asesoramos por WhatsApp, coordinamos el pago que te quede cómodo y despachamos a todo el país. Así de simple, así de matero.</p>
        <div style="margin-top:28px;display:flex;gap:14px;flex-wrap:wrap">
          <a class="btn btn--primary" href="/catalogo.html">Ver catálogo</a>
          <a class="btn btn--outline" href="/contacto.html">Contactanos</a>
        </div>
      </div>
      <div class="about-hero__img reveal" data-delay="1"><img src="/{ab_img}" alt="Matera de cuero artesanal de Lemates" width="600" height="750" loading="lazy"></div>
    </div>
  </section>
  <section class="section" style="background:var(--cream-2)">
    <div class="container">
      <div class="section-head center reveal"><span class="eyebrow">Lo que nos mueve</span><h2>Nuestros valores</h2></div>
      <div class="grid values-grid">{val_html}</div>
    </div>
  </section>
  <section class="section"><div class="container"><div class="grid stats">{stat_html}</div></div></section>
  <section class="section--tight"><div class="container">
    <div class="cta-band reveal">
      <span class="eyebrow" style="color:#f3e1d8;justify-content:center">Sumate</span>
      <h2>Viví el mate como se merece</h2>
      <p>Descubrí nuestra selección y encontrá tu equipo ideal.</p>
      <a class="btn btn--gold btn--lg" href="/catalogo.html">Explorar productos</a>
    </div>
  </div></section>
</main>
{footer()}
{overlays()}
{scripts()}'''
    write("nosotros.html", head(
        "Sobre nosotros | Lemates · Tienda Matera",
        "Conocé Lemates, la tienda matera artesanal nacida por amor al mate. Selección de piezas nobles, atención cercana y envíos a todo el país.",
        "nosotros.html", extra_ld=crumb_ld(al)) + body)

    # ============================================================ FAQ
    faqs = [
        ("¿Hacen envíos a todo el país?","Sí. Despachamos a toda la Argentina a través de Correo Argentino (a domicilio o a sucursal). También podés coordinar el retiro sin cargo en la zona oeste del Gran Buenos Aires."),
        ("¿Cuánto tarda el envío?","Una vez confirmado el pago, despachamos dentro de las 24-48 hs hábiles. El tiempo de entrega de Correo Argentino suele ser de 3 a 6 días hábiles según la localidad."),
        ("¿Qué medios de pago aceptan?","Pagás con Mercado Pago (escaneando el QR o transfiriendo al CVU), con transferencia bancaria (CBU/alias), o en efectivo si retirás en zona oeste. Al confirmar el pedido te mostramos los datos y el total exacto; después nos enviás el comprobante por WhatsApp."),
        ("¿Puedo comprar directamente por WhatsApp?","¡Claro! Podés armar tu carrito en la web y enviarlo por WhatsApp con un clic, o escribirnos directamente para que te asesoremos y coordinemos todo."),
        ("¿Los mates vienen curados?","Los mates de calabaza requieren un curado inicial. Te enviamos las indicaciones y estamos para ayudarte por WhatsApp en todo el proceso para que tu mate dure muchos años."),
        ("¿Los productos son artesanales?","Sí. Seleccionamos piezas artesanales con materiales nobles como calabaza, algarrobo, alpaca, bronce y cuero. Por su naturaleza, cada pieza puede tener pequeñas variaciones que la hacen única."),
        ("¿Puedo cambiar o devolver un producto?","Sí. Tenés hasta 10 días corridos desde la recepción para solicitar un cambio o devolución, siempre que el producto esté sin uso y en su estado original. Escribinos y te guiamos."),
        ("¿Hacen ventas por mayor o regalos empresariales?","Sí, trabajamos pedidos por cantidad y regalos personalizados. Escribinos por WhatsApp contándonos qué necesitás y armamos una propuesta a medida."),
    ]
    faq_html = "".join(f'''<div class="faq-item reveal">
      <button class="faq-q" aria-expanded="false">{q}<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg></button>
      <div class="faq-a"><div class="faq-a__inner">{a}</div></div>
    </div>''' for q,a in faqs)
    faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    fl = [("Inicio","/index.html"),("Preguntas frecuentes",None)]
    body = f'''{page("faq.html")}
{breadcrumb(fl)}
<section class="page-hero"><div class="container">
  <span class="eyebrow">Ayuda</span><h1>Preguntas frecuentes</h1>
  <p class="lead">Resolvé tus dudas sobre envíos, pagos y productos. Si te queda algo, escribinos por WhatsApp.</p>
</div></section>
<main id="main" class="section">
  <div class="container">
    <div class="faq-list">{faq_html}</div>
    <div class="text-center reveal" style="margin-top:44px">
      <p style="color:var(--ink-soft);margin-bottom:16px">¿No encontraste lo que buscabas?</p>
      <a class="btn btn--wa" href="https://wa.me/{WA}" target="_blank" rel="noopener">{I['wa']} Escribinos por WhatsApp</a>
    </div>
  </div>
</main>
{footer()}
{overlays()}
<script>
document.addEventListener('click',function(e){{
  var q=e.target.closest('.faq-q'); if(!q)return;
  var item=q.closest('.faq-item'); var a=item.querySelector('.faq-a');
  var open=item.classList.toggle('open'); q.setAttribute('aria-expanded',open);
  a.style.maxHeight = open ? a.scrollHeight+'px' : '0';
}});
</script>
{scripts()}'''
    write("faq.html", head(
        "Preguntas frecuentes | Lemates · Tienda Matera",
        "Envíos, pagos, cambios y cuidado del mate. Respondemos las preguntas más frecuentes de Lemates · Tienda Matera.",
        "faq.html", extra_ld=faq_ld) + body)

    # ============================================================ CONTACTO
    cards = [
        (I['wa'],"WhatsApp","Respondemos al toque","+54 9 11 5469-3079",f"https://wa.me/{WA}"),
        (I['ig'],"Instagram","Seguinos y escribinos","@lemates1",IG),
        (I['pin'],"Zona de retiro","Coordinamos punto y horario","Zona Oeste · GBA",None),
        (I['clock'],"Horarios","Atención por WhatsApp","Lun a Sáb · 9 a 20 h",None),
    ]
    card_html = ""
    for ic,t,s,v,href in cards:
        val = f'<a href="{href}" target="_blank" rel="noopener">{v}</a>' if href else f'<p>{v}</p>'
        card_html += f'''<div class="contact-card reveal"><div class="contact-card__ic">{ic}</div><div><h4>{t}</h4><p style="font-size:.82rem;color:var(--muted)">{s}</p>{val}</div></div>'''
    col = [("Inicio","/index.html"),("Contacto",None)]
    body = f'''{page("contacto.html")}
{breadcrumb(col)}
<section class="page-hero"><div class="container">
  <span class="eyebrow">Hablemos</span><h1>Contacto</h1>
  <p class="lead">Estamos para ayudarte a elegir tu mate ideal. Escribinos por el canal que prefieras.</p>
</div></section>
<main id="main" class="section">
  <div class="container contact-layout">
    <div class="contact-info">{card_html}</div>
    <div class="form-card reveal" data-delay="1">
      <h3 style="letter-spacing:.2px">Envianos un mensaje</h3>
      <p style="padding-left:0">Completá el formulario y te respondemos por WhatsApp a la brevedad.</p>
      <form id="contactForm">
        <div class="form-grid">
          <div class="field"><label>Nombre <span class="req">*</span></label><input name="nombre" required><div class="field__err">Ingresá tu nombre</div></div>
          <div class="field"><label>Teléfono <span class="req">*</span></label><input name="telefono" required><div class="field__err">Ingresá tu teléfono</div></div>
          <div class="field full"><label>Email</label><input type="email" name="email" placeholder="opcional"></div>
          <div class="field full"><label>Mensaje <span class="req">*</span></label><textarea name="mensaje" required placeholder="Contanos qué estás buscando…"></textarea><div class="field__err">Escribí tu mensaje</div></div>
        </div>
        <button class="btn btn--primary btn--lg btn--block" type="submit" style="margin-top:18px">{I['wa']} Enviar por WhatsApp</button>
      </form>
    </div>
  </div>
</main>
{footer()}
{overlays()}
<script>
document.getElementById('contactForm').addEventListener('submit',function(e){{
  e.preventDefault(); var ok=true;
  this.querySelectorAll('[required]').forEach(function(f){{var bad=!f.value.trim();f.closest('.field').classList.toggle('error',bad);if(bad)ok=false;}});
  if(!ok){{window.LemToast('Completá los campos requeridos',false);return;}}
  var d=Object.fromEntries(new FormData(this).entries());
  var msg='Hola Lemates! Soy '+d.nombre+'.\\n'+d.mensaje+(d.email?'\\n\\nEmail: '+d.email:'')+'\\nTel: '+d.telefono;
  window.open('https://wa.me/{WA}?text='+encodeURIComponent(msg),'_blank');
  window.LemToast('Abriendo WhatsApp…');
}});
document.querySelectorAll('#contactForm [required]').forEach(function(f){{f.addEventListener('input',function(){{f.closest('.field').classList.remove('error');}});}});
</script>
{scripts()}'''
    write("contacto.html", head(
        "Contacto | Lemates · Tienda Matera",
        "Contactá a Lemates por WhatsApp o Instagram. Te asesoramos para elegir tu mate, bombilla o termo ideal. Envíos a todo el país.",
        "contacto.html", extra_ld=crumb_ld(col)) + body)

    # ============================================================ CARRITO
    kl = [("Inicio","/index.html"),("Carrito",None)]
    body = f'''{page("carrito.html")}
{breadcrumb(kl)}
<section class="page-hero" style="padding-block:clamp(24px,4vw,40px)"><div class="container">
  <span class="eyebrow">Tu selección</span><h1>Carrito de compras</h1>
</div></section>
<main id="main" class="section" style="padding-top:clamp(24px,4vw,44px)">
  <div class="container">
    <div class="cart-page" id="cartPage"></div>
  </div>
</main>
{footer()}
{overlays()}
{scripts("cart-page.js")}'''
    write("carrito.html", head(
        "Carrito | Lemates · Tienda Matera",
        "Revisá tu carrito de compras en Lemates. Modificá cantidades y finalizá tu pedido por la web o WhatsApp.",
        "carrito.html") + body)

    # ============================================================ CHECKOUT
    provincias = ["Buenos Aires","CABA","Catamarca","Chaco","Chubut","Córdoba","Corrientes","Entre Ríos","Formosa","Jujuy","La Pampa","La Rioja","Mendoza","Misiones","Neuquén","Río Negro","Salta","San Juan","San Luis","Santa Cruz","Santa Fe","Santiago del Estero","Tierra del Fuego","Tucumán"]
    prov_opts = '<option value="" disabled selected>Elegí tu provincia</option>' + "".join(f'<option>{p}</option>' for p in provincias)
    ship_cards = f'''
      <label class="radio-card selected" data-ship="domicilio"><input type="radio" name="shipping" value="domicilio" checked><span><b>Envío a domicilio</b><span>Correo Argentino · 2-6 días hábiles</span></span><span class="r-price"><span style="color:var(--muted);font-weight:500">según CP</span></span></label>
      <label class="radio-card" data-ship="sucursal"><input type="radio" name="shipping" value="sucursal"><span><b>Envío a sucursal</b><span>Retirás en la sucursal de Correo más cercana</span></span><span class="r-price"><span style="color:var(--muted);font-weight:500">según CP</span></span></label>
      <label class="radio-card" data-ship="retiro"><input type="radio" name="shipping" value="retiro"><span><b>Retiro en zona oeste (GBA)</b><span>Coordinamos punto y horario por WhatsApp</span></span><span class="r-price">Gratis</span></label>'''
    pay_cards = f'''
      <label class="radio-card selected" data-pay="mercadopago"><input type="radio" name="payment" value="mercadopago" checked><span><b>Mercado Pago</b><span>Escaneá el QR o transferí al CVU. Enviás el comprobante.</span></span></label>
      <label class="radio-card" data-pay="transferencia"><input type="radio" name="payment" value="transferencia"><span><b>Transferencia bancaria</b><span>CBU / alias. Enviás el comprobante por WhatsApp.</span></span></label>
      <label class="radio-card" data-pay="efectivo"><input type="radio" name="payment" value="efectivo"><span><b>Efectivo</b><span>Pagás al retirar en zona oeste (GBA).</span></span></label>'''
    body = f'''{page("catalogo.html")}
{breadcrumb([("Inicio","/index.html"),("Carrito","/carrito.html"),("Checkout",None)])}
<section class="page-hero" style="padding-block:clamp(24px,4vw,40px)"><div class="container">
  <span class="eyebrow">Último paso</span><h1>Finalizar compra</h1>
</div></section>
<main id="main" class="section" style="padding-top:clamp(24px,4vw,44px)">
  <div class="container">
    <div id="checkoutEmpty" hidden>
      <div class="empty-state">
        {I['cart']}
        <h3>Tu carrito está vacío</h3>
        <p>Sumá productos antes de finalizar la compra.</p>
        <a class="btn btn--primary" href="/catalogo.html" style="margin-top:20px">Ir al catálogo</a>
      </div>
    </div>
    <form class="checkout-layout" id="checkoutForm" novalidate hidden="false">
      <div id="checkoutLayout">
        <div class="form-card">
          <h3><span class="num">1</span> Tus datos</h3>
          <p>¿Quién recibe el pedido?</p>
          <div class="form-grid">
            <div class="field"><label>Nombre <span class="req">*</span></label><input name="nombre" required><div class="field__err">Requerido</div></div>
            <div class="field"><label>Apellido <span class="req">*</span></label><input name="apellido" required><div class="field__err">Requerido</div></div>
            <div class="field"><label>Email <span class="req">*</span></label><input type="email" name="email" required><div class="field__err">Email inválido</div></div>
            <div class="field"><label>Teléfono <span class="req">*</span></label><input name="telefono" required><div class="field__err">Requerido</div></div>
          </div>
        </div>
        <div class="form-card">
          <h3><span class="num">2</span> Método de envío</h3>
          <p>Elegí cómo querés recibir tu pedido.</p>
          <div class="radio-cards">{ship_cards}</div>
        </div>
        <div class="form-card" id="addressSection">
          <h3><span class="num">3</span> Dirección de envío</h3>
          <p>¿A dónde lo enviamos?</p>
          <div class="form-grid">
            <div class="field full"><label>Dirección <span class="req">*</span></label><input name="direccion" data-reqable required placeholder="Calle, número, piso/depto"><div class="field__err">Requerido</div></div>
            <div class="field"><label>Provincia <span class="req">*</span></label><select name="provincia" data-reqable required>{prov_opts}</select><div class="field__err">Requerido</div></div>
            <div class="field"><label>Localidad <span class="req">*</span></label><input name="localidad" data-reqable required><div class="field__err">Requerido</div></div>
            <div class="field"><label>Código Postal <span class="req">*</span></label><input name="cp" data-reqable required><div class="field__err">Requerido</div></div>
            <div class="field full"><label>Observaciones</label><textarea name="obs" placeholder="Entre calles, referencias, horario de entrega… (opcional)"></textarea></div>
          </div>
        </div>
        <div class="form-card">
          <h3><span class="num">4</span> Método de pago</h3>
          <p>Elegí cómo pagar. En el siguiente paso te mostramos los datos.</p>
          <div class="radio-cards">{pay_cards}</div>
        </div>
      </div>
      <aside class="summary" id="orderSummary"></aside>
      <div style="grid-column:1/-1;margin-top:4px">
        <button class="btn btn--primary btn--lg btn--block" id="confirmBtn" type="submit" form="checkoutForm">Continuar al pago {I['arrow']}</button>
        <p style="text-align:center;font-size:.82rem;color:var(--muted);margin-top:12px">Pagás con Mercado Pago o transferencia y nos enviás el comprobante por WhatsApp. Coordinamos el envío al recibirlo.</p>
      </div>
    </form>
  </div>
</main>
{footer()}
{overlays()}
{scripts(["shipping.js", "checkout.js"])}'''
    write("checkout.html", head(
        "Checkout | Lemates · Tienda Matera",
        "Finalizá tu compra en Lemates. Elegí envío y medio de pago, y confirmá tu pedido por WhatsApp de forma simple y segura.",
        "checkout.html") + body)

    # ============================================================ POLÍTICAS
    legal_nav = "".join(f'<a class="chip" href="#{i}">{t}</a>' for i,t in [("envios","Envíos"),("pagos","Pagos"),("cambios","Cambios y devoluciones"),("privacidad","Privacidad"),("terminos","Términos")])
    body = f'''{page("catalogo.html")}
{breadcrumb([("Inicio","/index.html"),("Políticas",None)])}
<section class="page-hero"><div class="container">
  <span class="eyebrow">Información legal</span><h1>Políticas de la tienda</h1>
  <p class="lead">Todo lo que necesitás saber sobre envíos, pagos, cambios y el uso de nuestro sitio.</p>
</div></section>
<main id="main" class="section">
  <div class="container legal">
    <div class="legal__nav">{legal_nav}</div>
    <h2 id="envios">Política de envíos</h2>
    <p>Realizamos envíos a todo el territorio de la República Argentina a través de Correo Argentino, en sus modalidades a domicilio y a sucursal. También ofrecemos retiro sin cargo coordinando punto y horario en la zona oeste del Gran Buenos Aires.</p>
    <ul>
      <li>Los pedidos se despachan dentro de las 24 a 48 horas hábiles posteriores a la acreditación del pago.</li>
      <li>Los plazos de entrega estimados son de 2 a 6 días hábiles según la localidad de destino.</li>
      <li>El costo de envío se calcula automáticamente en el checkout según tu código postal, la modalidad elegida (domicilio o sucursal) y el peso del pedido.</li>
      <li>Una vez despachado, te compartimos el número de seguimiento por WhatsApp.</li>
    </ul>
    <h2 id="pagos">Medios de pago</h2>
    <p>Podés pagar de forma simple y segura con cualquiera de estas opciones:</p>
    <ul>
      <li><b>Mercado Pago:</b> escaneás el QR desde la app o transferís al CVU/alias, y nos enviás el comprobante por WhatsApp.</li>
      <li><b>Transferencia bancaria:</b> transferís al CBU/alias que se muestra en el checkout y nos enviás el comprobante por WhatsApp.</li>
      <li><b>Efectivo:</b> disponible para retiros en zona oeste del GBA; pagás al retirar.</li>
    </ul>
    <p>En todos los casos, al confirmar el pedido te mostramos los datos de pago y el total exacto. Coordinamos el envío apenas recibimos tu comprobante.</p>
    <h2 id="cambios">Cambios y devoluciones</h2>
    <p>Tu satisfacción es nuestra prioridad. Podés solicitar el cambio o la devolución de un producto dentro de los 10 días corridos desde su recepción, conforme a la normativa de defensa del consumidor.</p>
    <h3>Condiciones</h3>
    <ul>
      <li>El producto debe estar sin uso y en su estado y empaque original.</li>
      <li>Los mates de calabaza no curados pueden devolverse; una vez curados o utilizados, no admiten devolución por razones de higiene.</li>
      <li>Los costos de envío de la devolución corren por cuenta del comprador, salvo error o falla atribuible a Lemates.</li>
    </ul>
    <p>Para iniciar un cambio o devolución, escribinos por WhatsApp y te guiamos en todo el proceso.</p>
    <h2 id="privacidad">Política de privacidad</h2>
    <p>En Lemates respetamos tu privacidad. Los datos que nos brindás (nombre, contacto y dirección) se utilizan exclusivamente para procesar y despachar tu pedido, y para comunicarnos con vos respecto de la compra.</p>
    <ul>
      <li>No compartimos ni vendemos tus datos a terceros.</li>
      <li>No almacenamos datos de tarjetas ni credenciales de pago en este sitio.</li>
      <li>Podés solicitar la baja o modificación de tus datos escribiéndonos por WhatsApp.</li>
    </ul>
    <h2 id="terminos">Términos y condiciones</h2>
    <p>Al realizar una compra en Lemates aceptás estos términos. Los precios están expresados en pesos argentinos e incluyen impuestos, y pueden modificarse sin previo aviso. Las imágenes son ilustrativas; al tratarse de productos artesanales, cada pieza puede presentar pequeñas variaciones que la hacen única.</p>
    <p>Lemates se reserva el derecho de actualizar estas políticas. La versión vigente es la publicada en este sitio.</p>
    <p style="margin-top:30px;font-size:.86rem;color:var(--muted)">Última actualización: julio de 2026. Ante cualquier duda, escribinos por WhatsApp al +54 9 11 5469-3079.</p>
  </div>
</main>
{footer()}
{overlays()}
{scripts()}'''
    write("politicas.html", head(
        "Políticas | Lemates · Tienda Matera",
        "Políticas de envíos, pagos, cambios y privacidad de Lemates · Tienda Matera. Comprá con confianza y atención personalizada.",
        "politicas.html") + body)

    # ============================================================ 404
    body = f'''{page("index.html")}
<main id="main" class="notfound">
  <div class="container">
    <div class="notfound__big">404</div>
    <h1>Se nos escapó el mate</h1>
    <p>La página que buscás no existe o fue movida. Volvé al inicio o explorá nuestro catálogo.</p>
    <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap">
      <a class="btn btn--primary" href="/index.html">Volver al inicio</a>
      <a class="btn btn--outline" href="/catalogo.html">Ver catálogo</a>
    </div>
  </div>
</main>
{footer()}
{overlays()}
{scripts()}'''
    write("404.html", head(
        "Página no encontrada | Lemates",
        "La página que buscás no existe. Volvé al inicio o explorá el catálogo de Lemates · Tienda Matera.",
        "404.html") + body)
