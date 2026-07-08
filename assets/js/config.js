/* ============================================================
   LEMATES — Configuración de la tienda
   ------------------------------------------------------------
   COMPLETÁ ACÁ TUS DATOS REALES DE COBRO.
   Los valores marcados con "REEMPLAZAR" son de ejemplo.
   ============================================================ */
window.LEMATES_CONFIG = {
  // WhatsApp de la tienda (formato internacional sin +, ni espacios)
  whatsapp: "5491154693079",

  // ---------------- COBRO ----------------
  pago: {
    // Mercado Pago: alias/CVU de tu cuenta + imagen del QR "Cobrar con QR"
    mercadopago: {
      titular: "",                            // dejar "" para no mostrarlo
      alias: "lemates",
      cvu: "",                                // dejar "" para no mostrarlo
      // QR opcional. Dejar "" para no mostrarlo. Para usarlo, poné la ruta a la imagen.
      qr: "",
      // Link de pago opcional (Mercado Pago "Link de pago" / preferencia). Dejar "" si no usás.
      link: "",
    },
    // Transferencia bancaria
    transferencia: {
      titular: "REEMPLAZAR — Titular de la cuenta",
      banco: "REEMPLAZAR — Banco",
      tipoCuenta: "Caja de ahorro en pesos",
      cbu: "0000000000000000000000",         // REEMPLAZAR — CBU (22 díg.)
      alias: "REEMPLAZAR.alias.banco",
      cuit: "",                               // opcional
    },
  },

  // ---------------- ENVÍOS ----------------
  envio: {
    // CP de origen desde donde despachás (usado por la API de Correo Argentino)
    origenCP: "1704", // REEMPLAZAR por tu CP real de despacho
    // Si true, el checkout intenta cotizar en vivo con /api/shipping (Correo Argentino).
    // Si la API no está configurada o falla, usa el estimador de abajo automáticamente.
    apiHabilitada: true,
    // Peso estimado por categoría (en gramos) para calcular el envío
    pesosPorCategoria: { Mates: 450, Bombillas: 120, Termos: 650, Materas: 500, default: 400 },
    packagingGramos: 250,
    // Dimensiones de la caja (cm) usadas para cotizar
    caja: { alto: 15, ancho: 20, largo: 30 },

    // Estimador de respaldo por zona (ARS). Son valores APROXIMADOS de referencia;
    // la API de Correo Argentino, si está configurada, los reemplaza por la tarifa real.
    estimadorRespaldo: {
      // precio base hasta 1 kg + adicional por cada kg extra
      zonas: {
        0: { domicilio: 5500,  sucursal: 4500,  extraKg: 1000 }, // CABA / GBA
        1: { domicilio: 7000,  sucursal: 5800,  extraKg: 1200 }, // Centro
        2: { domicilio: 8500,  sucursal: 7000,  extraKg: 1500 }, // NEA / NOA / Cuyo
        3: { domicilio: 10500, sucursal: 8800,  extraKg: 1900 }, // Patagonia
      },
      // provincia (como aparece en el checkout) -> zona
      provinciaZona: {
        "CABA": 0, "Buenos Aires": 0,
        "Córdoba": 1, "Santa Fe": 1, "Entre Ríos": 1, "La Pampa": 1,
        "Mendoza": 2, "San Juan": 2, "San Luis": 2, "Tucumán": 2, "Salta": 2,
        "Jujuy": 2, "Santiago del Estero": 2, "Catamarca": 2, "La Rioja": 2,
        "Corrientes": 2, "Misiones": 2, "Chaco": 2, "Formosa": 2,
        "Neuquén": 3, "Río Negro": 3, "Chubut": 3, "Santa Cruz": 3, "Tierra del Fuego": 3,
      },
    },
  },
};
