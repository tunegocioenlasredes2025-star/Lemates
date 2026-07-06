# Lemates · Tienda Matera

Tienda online premium (eCommerce) para **Lemates**, marca argentina de mates, bombillas, termos y materas artesanales.

Sitio **multipágina estático** (HTML + CSS + JavaScript vanilla, sin dependencias ni build), optimizado para **mobile-first, SEO y rendimiento**. Listo para desplegar en Vercel.

---

## Estructura

```
Lemates/
├── index.html            Home
├── catalogo.html         Catálogo con buscador, filtros y orden
├── producto.html         Ficha de producto (?id=slug)
├── nosotros.html         Sobre nosotros
├── faq.html              Preguntas frecuentes (con FAQ schema)
├── contacto.html         Contacto (formulario → WhatsApp)
├── carrito.html          Carrito completo
├── checkout.html         Checkout (envío, pago, validación)
├── politicas.html        Envíos, pagos, cambios, privacidad, términos
├── 404.html              Página no encontrada
├── favicon.ico
├── robots.txt / sitemap.xml / site.webmanifest / vercel.json
├── assets/
│   ├── css/styles.css    Sistema de diseño completo
│   ├── js/
│   │   ├── products.js         Datos del catálogo (autogenerado)
│   │   ├── products-data.json  Fuente de datos
│   │   ├── app.js              Núcleo: carrito, drawer, WhatsApp, UI
│   │   ├── catalog.js          Lógica del catálogo
│   │   ├── product.js          Lógica de la ficha de producto
│   │   ├── cart-page.js        Carrito completo
│   │   └── checkout.js         Checkout
│   └── img/
│       ├── brand/        Logo, favicons, OG image, mate icon
│       └── products/     Imágenes optimizadas (WebP)
├── Catalogo/             Imágenes originales (no se publican)
└── scripts/              Generadores (build del sitio y del catálogo)
```

## Características

- **Diseño premium**: paleta terracota de marca, tipografías Marcellus + Plus Jakarta Sans, microanimaciones, glassmorphism sutil.
- **Carrito** con localStorage: drawer lateral + página completa, cantidades, subtotales.
- **WhatsApp**: botón flotante, compra directa, consulta de producto y envío del carrito completo con detalle y total.
- **Checkout** con métodos de envío (Correo Argentino / retiro) y pago (transferencia, efectivo, tarjeta; Mercado Pago preparado), validación y confirmación por WhatsApp.
- **SEO**: meta tags, Open Graph, Twitter Cards, JSON-LD (Store, Product, BreadcrumbList, FAQPage), sitemap, robots, canonical, alt text, lazy loading, imágenes WebP.
- **Mobile-first** y responsive en todos los breakpoints.

## Desarrollo local

Cualquier servidor estático. Por ejemplo:

```bash
python -m http.server 4330
# abrir http://localhost:4330
```

## Regenerar el sitio o el catálogo

Para volver a construir las páginas HTML (tras editar `scripts/build_pages.py`):

```bash
cd scripts && python build_site.py
```

Para reprocesar imágenes y datos desde `Catalogo/` (requiere ImageMagick):

```bash
python scripts/build_catalog.py
```

## Cobro y envíos (IMPORTANTE — configurar)

### 1. Datos de cobro — `assets/js/config.js`
Editá `assets/js/config.js` y reemplazá los valores marcados con `REEMPLAZAR`:
- **Mercado Pago:** `alias`, `cvu`, `titular`. Subí tu QR real en `assets/img/pago/qr-mercadopago.png` (reemplazá el placeholder).
- **Transferencia:** `banco`, `cbu`, `alias`, `titular`.

En el checkout, el cliente elige el método, ve el QR / CVU / CBU y el total exacto, paga, y envía el **comprobante por WhatsApp** con un botón (el pedido queda pre-armado en el mensaje; el cliente adjunta la captura en el chat).

### 2. Envíos — API de Correo Argentino (MiCorreo)
El checkout cotiza el envío **en vivo** con la función serverless `api/shipping.js`. Necesitás una cuenta de la API "MiCorreo/PaqAr" de Correo Argentino y cargar estas variables de entorno en Vercel (**Project → Settings → Environment Variables**), según `.env.example`:

```
CORREO_USER, CORREO_PASSWORD, CORREO_CUSTOMER_ID, CORREO_ORIGIN_CP, CORREO_ENV=prod
```

Mientras no estén cargadas (o si la API falla), el checkout usa automáticamente un **estimador por zona** definido en `config.js` (`envio.estimadorRespaldo`), y confirma el valor final por WhatsApp. Los pesos por categoría y las dimensiones de la caja también se configuran en `config.js`.

## Despliegue en Vercel

1. Subir el repositorio a GitHub (ya hecho).
2. Importar en Vercel: **Framework Preset = Other**, sin build command. Vercel detecta automáticamente la carpeta `api/` como funciones serverless.
3. Cargar las variables de entorno de Correo Argentino (ver arriba).
4. **Antes de publicar**, reemplazar `https://www.lemates.com.ar` por el dominio real en:
   `scripts/build_site.py` (constante `BASE`), `robots.txt`, `sitemap.xml`, y luego regenerar.

## Datos de la marca

- Instagram: [@lemates1](https://www.instagram.com/lemates1/)
- WhatsApp: +54 9 11 5469-3079
- Paleta: `#d38f44` · `#f3e1d8` · `#984c39` · `#b88450`
