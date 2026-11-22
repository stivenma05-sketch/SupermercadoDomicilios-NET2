import urllib.request
import urllib.parse
import json
import os

productos = [
    (1, "Salsa de Tomate Fruco Doypack 400g", "Salsas y Condimentos", 6400, 45, "salsa tomate fruco"),
    (2, "Mayonesa Fruco Doypack 380g", "Salsas y Condimentos", 8200, 35, "mayonesa fruco"),
    (3, "Salsa BBQ Fruco Original 350g", "Salsas y Condimentos", 7500, 30, "salsa bbq fruco"),
    (4, "Salsa de Tomate Heinz 397g", "Salsas y Condimentos", 11900, 25, "heinz tomato ketchup"),
    (5, "Aceite de Oliva Extra Virgen 500ml", "Salsas y Condimentos", 29900, 20, "aceite de oliva extra virgen"),
    (6, "Mostaza Fruco Doypack 200g", "Salsas y Condimentos", 4800, 32, "mostaza fruco"),

    (7, "Pasta Espagueti Doria 500g", "Pastas y Granos", 3900, 60, "spaghetti doria"),
    (8, "Pasta Tornillos Doria 500g", "Pastas y Granos", 4100, 50, "tornillos doria"),
    (9, "Pasta Espagueti La Muñeca 500g", "Pastas y Granos", 3700, 55, "pasta la muneca"),
    (10, "Pasta Penne Barilla 500g", "Pastas y Granos", 8500, 32, "penne barilla"),
    (11, "Arroz Blanco Diana 1000g", "Pastas y Granos", 4900, 80, "arroz diana"),
    (12, "Arroz Blanco Roa 1000g", "Pastas y Granos", 5100, 75, "arroz roa"),
    (13, "Frijol Bola Roja Diana 500g", "Pastas y Granos", 6900, 40, "frijol diana"),

    (14, "Leche Entera Alpina 1100ml", "Lácteos y Huevos", 4600, 50, "leche entera alpina"),
    (15, "Leche Deslactosada Alquería 1100ml", "Lácteos y Huevos", 5200, 45, "leche alqueria"),
    (16, "Queso Campesino Alpina 400g", "Lácteos y Huevos", 12400, 30, "queso campesino alpina"),
    (17, "Yogurt Griego Alpina 150g", "Lácteos y Huevos", 5400, 38, "yogurt griego alpina"),
    (18, "Arequipe Alpina 250g", "Lácteos y Huevos", 7800, 35, "arequipe alpina"),

    (19, "Salchicha Tradicional Zenú", "Carnes y Embutidos", 9800, 40, "salchicha zenu"),
    (20, "Jamón de Cerdo Pietrán 230g", "Carnes y Embutidos", 11500, 30, "jamon pietran"),
    (21, "Atún Van Camp's en Aceite 160g", "Carnes y Embutidos", 7400, 48, "atun van camps"),

    (22, "Pan Tajado Blanco Bimbo 600g", "Panadería y Bebidas", 7200, 42, "pan bimbo blanco"),
    (23, "Café Molido Juan Valdez 454g", "Panadería y Bebidas", 26500, 28, "cafe juan valdez"),
    (24, "Jugo Hit Naranja Piña 1000ml", "Panadería y Bebidas", 4300, 55, "jugo hit")
]

headers = {'User-Agent': 'MarketExpressApp/1.0 (stiven@lacosecha.com)'}
resultados_cs = []

for pid, nombre, cat, precio, stock, query in productos:
    ruta_local = f"/images/productos/prod_{pid}.jpg"
    archivo_fisico = f"Supermercado.Web/wwwroot{ruta_local}"
    descargado = False

    try:
        q = urllib.parse.quote(query)
        url_api = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={q}&search_simple=1&action=process&json=1&page_size=5"
        req = urllib.request.Request(url_api, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for p in data.get("products", []):
                img_url = p.get("image_front_url") or p.get("image_url")
                if img_url and img_url.startswith("http"):
                    req_img = urllib.request.Request(img_url, headers=headers)
                    with urllib.request.urlopen(req_img, timeout=10) as img_resp:
                        contenido = img_resp.read()
                        if len(contenido) > 3000:
                            with open(archivo_fisico, "wb") as f_out:
                                f_out.write(contenido)
                            descargado = True
                            print(f"[OK] {nombre} -> {img_url}")
                            break
    except Exception as e:
        print(f"[AVISO] {nombre}: {e}")

    if not descargado:
        ruta_local = "/images/logo.png"

    resultados_cs.append(f'            new Producto {{ Id = {pid}, Nombre = "{nombre}", Categoria = "{cat}", Precio = {precio}, Stock = {stock}, ImagenUrl = "{ruta_local}" }}')

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
{",\n".join(resultados_cs)}
        );
    }}
}}
'''

with open("Supermercado.Core/Data/SupermercadoDbContext.cs", "w", encoding="utf-8") as f:
    f.write(cs_code)

print("Catálogo actualizado con fotografías reales de alimentos.")
