import urllib.request
import urllib.parse
import json
import os
from concurrent.futures import ThreadPoolExecutor

headers = {'User-Agent': 'MarketExpressColombia/4.0 (contacto@marketexpress.co)'}

# Consultas por categoría en Open Food Facts (1 sola petición rápida de 35 resultados por categoría)
categorias_api = [
    ("Salsas y Condimentos", "sauces", 6500),
    ("Pastas y Granos", "pastas", 4200),
    ("Harinas y Panadería", "flours", 4800),
    ("Lácteos y Huevos", "dairies", 5500),
    ("Carnes y Embutidos", "meats", 11500),
    ("Bebidas y Jugos", "beverages", 4600),
    ("Confitería y Snacks", "sweet-snacks", 5200)
]

# Productos frescos reales (Verduras y Frutas) con fotografías verificadas de cada alimento exacto
frescos_verificados = [
    # Verduras y Hortalizas (10)
    ("Tomate Chonto Fresco 1kg", "Verduras y Hortalizas", 4200, "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=500&q=80"),
    ("Cebolla Cabezona Blanca 1kg", "Verduras y Hortalizas", 3800, "https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=500&q=80"),
    ("Zanahoria Fresca Seleccionada 1kg", "Verduras y Hortalizas", 3400, "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=500&q=80"),
    ("Papa Pastusa Lavada 1kg", "Verduras y Hortalizas", 3600, "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=500&q=80"),
    ("Brócoli Fresco Unidad 500g", "Verduras y Hortalizas", 5200, "https://images.unsplash.com/photo-1459411621453-7b03977f4bfc?w=500&q=80"),
    ("Pimentón Rojo Dulce 500g", "Verduras y Hortalizas", 4500, "https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=500&q=80"),
    ("Lechuga Batavia Fresca Unidad", "Verduras y Hortalizas", 3100, "https://images.unsplash.com/photo-1622206151226-18ca2c9ab4a1?w=500&q=80"),
    ("Pepino Cohombro Fresco 500g", "Verduras y Hortalizas", 2900, "https://images.unsplash.com/photo-1449300079323-02e209d9d3a6?w=500&q=80"),
    ("Espinaca Bogotana Manojo 500g", "Verduras y Hortalizas", 3900, "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=500&q=80"),
    ("Ajo Nacional Malla x3 Cabezas", "Verduras y Hortalizas", 4100, "https://images.unsplash.com/photo-1540148426945-6cf22a6b2383?w=500&q=80"),

    # Frutas Frescas (10)
    ("Manzana Roja Importada x4 Und", "Frutas Frescas", 8500, "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=500&q=80"),
    ("Banano Criollo Racimo 1kg", "Frutas Frescas", 3200, "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=500&q=80"),
    ("Aguacate Hass Seleccionado x2", "Frutas Frescas", 6800, "https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?w=500&q=80"),
    ("Fresa Seleccionada Bandeja 500g", "Frutas Frescas", 7400, "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=500&q=80"),
    ("Naranja Valencia Jugosa 1kg", "Frutas Frescas", 4300, "https://images.unsplash.com/photo-1547514701-42782101795e?w=500&q=80"),
    ("Piña Oro Miel Entera Unidad", "Frutas Frescas", 5900, "https://images.unsplash.com/photo-1550258987-190a2d41a8ba?w=500&q=80"),
    ("Mango Tommy Maduro x2 Und", "Frutas Frescas", 5400, "https://images.unsplash.com/photo-1553279768-865429fa0078?w=500&q=80"),
    ("Uva Red Globe Importada 500g", "Frutas Frescas", 9200, "https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=500&q=80"),
    ("Sandía Baby Dulce Unidad", "Frutas Frescas", 7800, "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=500&q=80"),
    ("Limón Tahití Fresco 1kg", "Frutas Frescas", 4600, "https://images.unsplash.com/photo-1590502593747-42a996133562?w=500&q=80")
]

candidatos = []
nombres_vistos = set()

def obtener_por_categoria_api(item):
    cat_es, tag_en, precio_base = item
    lista = []
    try:
        url = f"https://es.openfoodfacts.org/category/{tag_en}.json?page_size=40"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for p in data.get("products", []):
                nombre = (p.get("product_name_es") or p.get("product_name") or "").strip()
                marca = (p.get("brands") or "").split(",")[0].strip()
                img = p.get("image_front_url") or p.get("image_url")
                if not nombre or len(nombre) < 4 or not img or not img.startswith("http"):
                    continue
                titulo = nombre if (not marca or marca.lower() in nombre.lower()) else f"{nombre} - {marca}"
                titulo = titulo.replace('"', '').replace("'", "").replace("\n", " ")[:52]
                lista.append((titulo, cat_es, precio_base, img))
    except Exception as e:
        print(f"[AVISO API] {cat_es}: {e}")
    return lista

print("Consultando productos reales en español por categoría...")
with ThreadPoolExecutor(max_workers=7) as ex:
    for cat_info, grupo in zip(categorias_api, ex.map(obtener_por_categoria_api, categorias_api)):
        cat_nombre = cat_info[0]
        agregados_cat = 0
        for titulo, cat, precio_base, img in grupo:
            if titulo.lower() not in nombres_vistos and agregados_cat < 14:
                nombres_vistos.add(titulo.lower())
                candidatos.append((titulo, cat, precio_base + (agregados_cat * 450), img))
                agregados_cat += 1
        print(f" -> {cat_nombre}: {agregados_cat} candidatos listos")

for titulo, cat, precio, img in frescos_verificados:
    candidatos.append((titulo, cat, precio, img))

def descargar_foto(args):
    idx, (titulo, cat, precio, img_url) = args
    ruta_local = f"/images/productos/prod_{idx}.jpg"
    archivo = f"Supermercado.Web/wwwroot{ruta_local}"
    try:
        req = urllib.request.Request(img_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            datos = r.read()
            if len(datos) > 3000:
                with open(archivo, "wb") as f:
                    f.write(datos)
                return (titulo, cat, precio, ruta_local)
    except Exception:
        pass
    return None

print("Descargando fotografías reales...")
verificados_por_cat = {}
with ThreadPoolExecutor(max_workers=14) as ex:
    for res in ex.map(descargar_foto, enumerate(candidatos, start=1)):
        if res:
            titulo, cat, precio, ruta = res
            verificados_por_cat.setdefault(cat, [])
            if len(verificados_por_cat[cat]) < 10:
                verificados_por_cat[cat].append(res)

lineas_cs = []
pid = 1
for cat, items in verificados_por_cat.items():
    print(f"[OK] Categoría '{cat}': {len(items)} productos con foto real.")
    for titulo, c, precio, ruta in items:
        stock = 20 + ((pid * 3) % 45)
        lineas_cs.append(f'            new Producto {{ Id = {pid}, Nombre = "{titulo}", Categoria = "{c}", Precio = {precio}, Stock = {stock}, ImagenUrl = "{ruta}" }}')
        pid += 1

cs_code = f'''using Microsoft.EntityFrameworkCore;
using Supermercado.Core.Models;

namespace Supermercado.Core.Data;

public class SupermercadoDbContext : DbContext
{{
    public DbSet<Producto> Productos => Set<Producto>();
    public DbSet<Pedido> Pedidos => Set<Pedido>();
    public DbSet<DetallePedido> DetallesPedido => Set<DetallePedido>();

    public SupermercadoDbContext(DbContextOptions<SupermercadoDbContext> options) : base(options) {{ }}
    public SupermercadoDbContext() {{ }}

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {{
        if (!optionsBuilder.IsConfigured)
        {{
            var dbPath = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "supermercado.db"));
            optionsBuilder.UseSqlite($"Data Source={{dbPath}}");
        }}
    }}

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {{
        modelBuilder.Entity<Producto>().HasData(
{",\n".join(lineas_cs)}
        );
    }}
}}
'''

with open("Supermercado.Core/Data/SupermercadoDbContext.cs", "w", encoding="utf-8") as f:
    f.write(cs_code)

print(f"\n¡TOTAL GUARDADO: {pid - 1} PRODUCTOS REALES CON FOTOS VERIFICADAS!")
