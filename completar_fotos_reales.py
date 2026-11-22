import urllib.request
import urllib.parse
import json
import os

productos = [
    (1, "Salsa de Tomate Fruco Doypack 400g", "Salsas y Condimentos", 6400, 45, ["salsa tomate fruco", "salsa de tomate fruco", "tomato ketchup"]),
    (2, "Mayonesa Fruco Doypack 380g", "Salsas y Condimentos", 8200, 35, ["mayonesa fruco", "mayonesa", "mayonnaise"]),
    (3, "Salsa BBQ Fruco Original 350g", "Salsas y Condimentos", 7500, 30, ["salsa bbq fruco", "salsa bbq", "barbecue sauce"]),
    (4, "Salsa de Tomate Heinz 397g", "Salsas y Condimentos", 11900, 25, ["heinz tomato ketchup", "salsa tomate heinz", "ketchup heinz"]),
    (5, "Aceite de Oliva Extra Virgen 500ml", "Salsas y Condimentos", 29900, 20, ["aceite de oliva", "olive oil extra virgin", "aceite oliva"]),
    (6, "Mostaza Fruco Doypack 200g", "Salsas y Condimentos", 4800, 32, ["mostaza fruco", "mostaza", "mustard"]),

    (7, "Pasta Espagueti Doria 500g", "Pastas y Granos", 3900, 60, ["espagueti doria", "pasta doria", "spaghetti pasta"]),
    (8, "Pasta Tornillos Doria 500g", "Pastas y Granos", 4100, 50, ["tornillos doria", "pasta tornillos"]),
    (9, "Pasta Espagueti La Muñeca 500g", "Pastas y Granos", 3700, 55, ["espagueti la muneca", "spaghetti barilla", "spaghetti"]),
    (10, "Pasta Penne Barilla 500g", "Pastas y Granos", 8500, 32, ["penne rigate barilla", "barilla penne", "penne pasta"]),
    (11, "Arroz Blanco Diana 1000g", "Pastas y Granos", 4900, 80, ["arroz diana", "arroz blanco", "white rice"]),
    (12, "Arroz Blanco Roa 1000g", "Pastas y Granos", 5100, 75, ["arroz roa", "arroz florhuila", "arroz"]),
    (13, "Frijol Bola Roja Diana 500g", "Pastas y Granos", 6900, 40, ["frijol bola roja", "frijol rojo", "red beans"]),

    (14, "Leche Entera Alpina 1100ml", "Lácteos y Huevos", 4600, 50, ["leche entera alpina", "leche alpina", "leche entera"]),
    (15, "Leche Deslactosada Alquería 1100ml", "Lácteos y Huevos", 5200, 45, ["leche alqueria", "leche deslactosada", "milk"]),
    (16, "Queso Campesino Alpina 400g", "Lácteos y Huevos", 12400, 30, ["queso campesino alpina", "queso alpina", "queso fresco"]),
    (17, "Yogurt Griego Alpina 150g", "Lácteos y Huevos", 5400, 38, ["yogurt griego alpina", "yogurt alpina", "greek yogurt"]),
    (18, "Arequipe Alpina 250g", "Lácteos y Huevos", 7800, 35, ["arequipe alpina", "dulce de leche", "arequipe"]),

    (19, "Salchicha Tradicional Zenú", "Carnes y Embutidos", 9800, 40, ["salchicha zenu", "salchicha", "hot dog sausages"]),
    (20, "Jamón de Cerdo Pietrán 230g", "Carnes y Embutidos", 11500, 30, ["jamon pietran", "jamon de cerdo", "sliced ham"]),
    (21, "Atún Van Camp's en Aceite 160g", "Carnes y Embutidos", 7400, 48, ["atun van camps", "atun en aceite", "tuna can"]),

    (22, "Pan Tajado Blanco Bimbo 600g", "Panadería y Bebidas", 7200, 42, ["pan bimbo", "pan blanco bimbo", "sliced bread"]),
    (23, "Café Molido Juan Valdez 454g", "Panadería y Bebidas", 26500, 28, ["cafe juan valdez", "juan valdez coffee", "cafe molido"]),
    (24, "Jugo Hit Naranja Piña 1000ml", "Panadería y Bebidas", 4300, 55, ["jugo hit", "jugo de naranja", "orange juice"])
]

headers = {'User-Agent': 'MarketExpressApp/2.0 (contacto@marketexpress.co)'}
resultados_cs = []

for pid, nombre, cat, precio, stock, queries in productos:
    ruta_local = f"/images/productos/prod_{pid}.jpg"
    archivo_fisico = f"Supermercado.Web/wwwroot{ruta_local}"
    descargado = os.path.exists(archivo_fisico) and os.path.getsize(archivo_fisico) > 4000

    if not descargado:
        for query in queries:
            try:
                q = urllib.parse.quote(query)
                url_api = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={q}&search_simple=1&action=process&json=1&page_size=6"
                req = urllib.request.Request(url_api, headers=headers)
                with urllib.request.urlopen(req, timeout=20) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    for p in data.get("products", []):
                        img_url = p.get("image_front_url") or p.get("image_url")
                        if img_url and img_url.startswith("http"):
                            req_img = urllib.request.Request(img_url, headers=headers)
                            with urllib.request.urlopen(req_img, timeout=20) as img_resp:
                                contenido = img_resp.read()
                                if len(contenido) > 4000:
                                    with open(archivo_fisico, "wb") as f_out:
                                        f_out.write(contenido)
                                    descargado = True
                                    print(f"[OK] {nombre} ({query})")
                                    break
                if descargado:
                    break
            except Exception:
                continue

    if not descargado:
        ruta_local = "/images/logo.png"
        print(f"[PENDIENTE] {nombre}")

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
