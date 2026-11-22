import urllib.request
import urllib.parse
import json
import os
from concurrent.futures import ThreadPoolExecutor

consultas = [
    ("Salsas y Condimentos", "fruco", 6500),
    ("Salsas y Condimentos", "salsa de tomate", 5800),
    ("Salsas y Condimentos", "mayonesa", 7400),
    ("Salsas y Condimentos", "heinz", 11500),
    ("Pastas y Granos", "pasta doria", 4100),
    ("Pastas y Granos", "spaghetti", 4300),
    ("Pastas y Granos", "arroz diana", 4900),
    ("Pastas y Granos", "frijol", 6800),
    ("Lácteos y Huevos", "alpina", 5600),
    ("Lácteos y Huevos", "alqueria", 5200),
    ("Lácteos y Huevos", "colanta", 6400),
    ("Lácteos y Huevos", "queso campesino", 11800),
    ("Carnes y Embutidos", "zenu", 9800),
    ("Carnes y Embutidos", "pietran", 11200),
    ("Carnes y Embutidos", "atun van camps", 7600),
    ("Panadería y Bebidas", "bimbo", 7400),
    ("Panadería y Bebidas", "juan valdez", 24500),
    ("Panadería y Bebidas", "jugo hit", 4200),
    ("Snacks y Dulces", "galletas noel", 4900),
    ("Snacks y Dulces", "chocolatina jet", 5500)
]

headers = {'User-Agent': 'MarketExpressColombia/3.0'}
productos_validos = []
nombres_vistos = set()

def buscar_categoria(item):
    cat, termino, precio_base = item
    encontrados = []
    try:
        q = urllib.parse.quote(termino)
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={q}&search_simple=1&action=process&json=1&page_size=12"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for p in data.get("products", []):
                nombre_raw = (p.get("product_name_es") or p.get("product_name") or "").strip()
                marca = (p.get("brands") or "").split(",")[0].strip()
                img_url = p.get("image_front_url") or p.get("image_url")
                if not nombre_raw or len(nombre_raw) < 4 or not img_url or not img_url.startswith("http"):
                    continue
                titulo = nombre_raw if (not marca or marca.lower() in nombre_raw.lower()) else f"{nombre_raw} - {marca}"
                titulo = titulo.replace('"', '').replace("'", "")[:55]
                encontrados.append((titulo, cat, precio_base, img_url))
    except Exception:
        pass
    return encontrados

print("Buscando productos reales verificados...")
with ThreadPoolExecutor(max_workers=8) as ex:
    for grupo in ex.map(buscar_categoria, consultas):
        for titulo, cat, precio_base, img_url in grupo:
            clave = titulo.lower()
            if clave not in nombres_vistos and len(productos_validos) < 72:
                nombres_vistos.add(clave)
                productos_validos.append((len(productos_validos) + 1, titulo, cat, precio_base + ((len(productos_validos) * 350) % 4500), img_url))

def descargar_imagen(prod):
    pid, titulo, cat, precio, img_url = prod
    ruta_local = f"/images/productos/prod_{pid}.jpg"
    archivo = f"Supermercado.Web/wwwroot{ruta_local}"
    try:
        req = urllib.request.Request(img_url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as r:
            datos = r.read()
            if len(datos) > 3500:
                with open(archivo, "wb") as f:
                    f.write(datos)
                return (pid, titulo, cat, precio, ruta_local)
    except Exception:
        pass
    return None

print(f"Descargando {len(productos_validos)} fotografías reales en paralelo...")
finales = []
with ThreadPoolExecutor(max_workers=12) as ex:
    for res in ex.map(descargar_imagen, productos_validos):
        if res:
            finales.append(res)

# Reindexar IDs consecutivos 1..N
lineas_cs = []
for idx, (_, titulo, cat, precio, ruta_local) in enumerate(finales, start=1):
    stock = 18 + ((idx * 3) % 42)
    lineas_cs.append(f'            new Producto {{ Id = {idx}, Nombre = "{titulo}", Categoria = "{cat}", Precio = {precio}, Stock = {stock}, ImagenUrl = "{ruta_local}" }}')

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

print(f"¡Éxito! {len(finales)} productos reales guardados con su fotografía exacta.")
