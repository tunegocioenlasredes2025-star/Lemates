# -*- coding: utf-8 -*-
"""Procesa las imágenes originales de Catalogo/ y genera:
   - assets/img/products/*.webp  (imagen 1000px + thumb 600px, optimizadas)
   - assets/js/products-data.json
   - assets/js/products.js
Requiere ImageMagick (comando `magick`).
"""
import os, re, subprocess, json, unicodedata, collections

ROOT = r"C:/TNR/Lemates"
SRC = os.path.join(ROOT, "Catalogo/Catalogo")
OUT = os.path.join(ROOT, "assets/img/products")
KNOWN_EXT = {'.jpg', '.jpeg', '.png', '.webp'}
os.makedirs(OUT, exist_ok=True)

def slugify(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

def parse_price(fn):
    m = re.search(r'\$?\s*([0-9]{1,3}(?:[.,][0-9]{3})+)', fn)
    if m:
        return int(m.group(1).replace('.', '').replace(',', ''))
    m = re.search(r'\$\s*([0-9]+)', fn)
    return int(m.group(1)) if m else None

def titlecase(name):
    small = {'de', 'y', 'con', 'del', 'la', 'el', 'al', 'a'}
    return ' '.join((w.lower() if i > 0 and w.lower() in small else (w[:1].upper() + w[1:] if w else w))
                    for i, w in enumerate(name.split()))

def categorize(name):
    n = name.lower()
    if n.startswith('bombill'):
        return 'Bombillas'
    if 'termo' in n:
        return 'Termos'
    if 'matera' in n:
        return 'Materas'
    return 'Mates'

MAT = {
    'alpaca': 'alpaca', 'bronce': 'bronce', 'calabaza': 'calabaza natural', 'algarrobo': 'madera de algarrobo',
    'acero': 'acero inoxidable', 'cuero': 'cuero genuino', 'cuerina': 'cuerina premium',
    'repujado': 'repujado artesanal', 'cincelad': 'cincelado a mano', 'laqueado': 'terminación laqueada',
    'virola': 'virola de alpaca', 'grabado': 'grabado',
}

def materials(name):
    n = name.lower(); found = []
    for k, v in MAT.items():
        if k in n and v not in found:
            found.append(v)
    return found

def description(name, cat):
    mats = materials(name)
    matstr = (' Confeccionado en ' + ', '.join(mats) + '.') if mats else ''
    if cat == 'Bombillas':
        base = f"{name}. Bombilla artesanal pensada para durar toda la vida, con pico filtrante que garantiza un mate limpio y parejo."
    elif cat == 'Termos':
        base = f"{name}. Termo de alto rendimiento que mantiene la temperatura ideal durante horas, con pico cebador de precisión."
    elif cat == 'Materas':
        base = f"{name}. Matera resistente y elegante para llevar tu equipo a todos lados, con espacio para mate, termo y yerba."
    else:
        base = f"{name}. Mate curado y listo para usar, con terminaciones prolijas que resaltan la tradición matera argentina."
    return base + matstr


MATERAS_DIR = os.path.join(ROOT, "Materas")
MATERAS = [
    {"id": "matera-de-cuero", "name": "Matera de Cuero", "price": 37000,
     "materials": ["cuero genuino"],
     "files": ["Matera de Cuero.jfif", "Matera de cuero negra.jfif",
               "Matera de Cuero Bordo.jfif", "matera de cuero 2.jfif"]},
    {"id": "matera-de-cuerina", "name": "Matera de Cuerina", "price": 16000,
     "materials": ["cuerina premium"],
     "files": ["matera de cuerina.jfif", "matera de cuerina 2.jfif"]},
]

def build_materas():
    """Procesa la carpeta Materas/ (varias imágenes por producto, deslizables)."""
    out = []
    for p in MATERAS:
        imgs = []
        for i, f in enumerate(p["files"]):
            src = os.path.join(MATERAS_DIR, f)
            if not os.path.isfile(src):
                continue
            suf = "" if i == 0 else f"-{i+1}"
            main_f = f'{p["id"]}{suf}.webp'; thumb_f = f'{p["id"]}{suf}-thumb.webp'
            subprocess.run(f'magick "{src}" -auto-orient -resize "1000x1000>" -strip -quality 82 "{OUT}/{main_f}"', shell=True, check=True)
            subprocess.run(f'magick "{src}" -auto-orient -resize "600x600>" -strip -quality 80 "{OUT}/{thumb_f}"', shell=True, check=True)
            imgs.append({"src": f"assets/img/products/{main_f}", "thumb": f"assets/img/products/{thumb_f}"})
        out.append({
            "id": p["id"], "name": p["name"], "price": p["price"], "category": "Materas",
            "images": imgs,
            "description": f'{p["name"]}. Matera resistente y elegante para llevar tu equipo a todos lados, '
                           f'con espacio para mate, termo y yerba. Ideal para la mateada al aire libre.',
            "short": "En " + ", ".join(p["materials"]) + ".",
            "materials": p["materials"], "stock": True,
            "featured": p["id"] == "matera-de-cuero",
            "bestseller": p["price"] in (16000, 22000, 23000, 30000, 32000),
            "new": True,
        })
    return out


def main():
    records = []
    for fn in sorted(os.listdir(SRC)):
        path = os.path.join(SRC, fn)
        if not os.path.isfile(path):
            continue
        if re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}', fn):  # archivos sin nombre (UUID duplicados)
            continue
        price = parse_price(fn)
        if price is None:
            print("SKIP (sin precio):", fn); continue
        root, ext = os.path.splitext(fn)
        name = root if ext.lower() in KNOWN_EXT else fn
        name = re.sub(r'\$?\s*[0-9]{1,3}(?:[.,][0-9]{3})+.*$', '', name)
        name = re.sub(r'\(\d+\)', '', name)
        name = name.replace('_', '"').replace('”', '"').replace('“', '"')
        name = re.sub(r'\s+', ' ', name).strip(' -"')
        view = 0
        mv = re.search(r'\s(\d)$', name)
        if mv:
            view = int(mv.group(1)); name = name[:mv.start()].strip()
        records.append({'file': fn, 'path': path, 'price': price, 'name': name, 'view': view})

    groups = {}; order = []
    norm = lambda n: re.sub(r'[^a-z0-9]', '', n.lower())
    for r in records:
        key = (norm(r['name']), r['price'])
        if key not in groups:
            groups[key] = []; order.append(key)
        groups[key].append(r)

    products = []
    for key in order:
        grp = sorted(groups[key], key=lambda r: r['view'])
        base = grp[0]
        disp = titlecase(base['name']); slug = slugify(base['name'])
        cat = categorize(base['name'])
        imgs = []
        for i, r in enumerate(grp):
            suf = '' if i == 0 else f'-{i+1}'
            main_f = f"{slug}{suf}.webp"; thumb_f = f"{slug}{suf}-thumb.webp"
            subprocess.run(f'magick "{r["path"]}" -auto-orient -resize "1000x1000>" -strip -quality 80 "{OUT}/{main_f}"', shell=True, check=True)
            subprocess.run(f'magick "{r["path"]}" -auto-orient -resize "600x600>" -strip -quality 78 "{OUT}/{thumb_f}"', shell=True, check=True)
            imgs.append({'src': f"assets/img/products/{main_f}", 'thumb': f"assets/img/products/{thumb_f}"})
        products.append({
            'id': slug, 'name': disp, 'price': base['price'], 'category': cat,
            'images': imgs, 'description': description(disp, cat),
            'short': ('En ' + ', '.join(materials(disp)[:3]) + '.') if materials(disp) else 'Pieza artesanal de tienda matera.',
            'materials': materials(disp), 'stock': True,
            'featured': False, 'bestseller': False, 'new': False,
        })

    by_cat = collections.defaultdict(list)
    for p in products:
        by_cat[p['category']].append(p)
    for ps in by_cat.values():
        for p in sorted(ps, key=lambda p: -len(p['images']))[:2]:
            p['featured'] = True
    for p in products:
        if p['price'] in (22000, 23000, 30000, 32000):
            p['bestseller'] = True
    for p in products[-6:]:
        p['new'] = True

    # Materas curadas (carpeta Materas/, sin precio en el nombre): reemplazan las de la categoría
    products = [p for p in products if p['category'] != 'Materas'] + build_materas()

    json.dump(products, open(os.path.join(ROOT, "assets/js/products-data.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    CATMETA = {
        'Mates': {'slug': 'mates', 'desc': 'Imperiales, torpedos, camioneros y rancheros.'},
        'Bombillas': {'slug': 'bombillas', 'desc': 'Bombillas y bombillones de alpaca y bronce.'},
        'Termos': {'slug': 'termos', 'desc': 'Termos de alto rendimiento con pico cebador.'},
        'Materas': {'slug': 'materas', 'desc': 'Materas de cuero y cuerina.'},
    }
    js = "// Auto-generado desde el catálogo. No editar a mano.\nwindow.LEMATES_DATA=" + \
         json.dumps({'products': products, 'categories': CATMETA}, ensure_ascii=False) + ";\n"
    open(os.path.join(ROOT, "assets/js/products.js"), "w", encoding="utf-8").write(js)

    print(f"OK: {len(products)} productos | {dict(collections.Counter(p['category'] for p in products))}")


if __name__ == "__main__":
    main()
