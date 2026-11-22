import urllib.request
from concurrent.futures import ThreadPoolExecutor

headers = {'User-Agent': 'Mozilla/5.0'}

catalogo = [
    # 1. Salsas y Condimentos (10)
    ("Salsa de Tomate Clásica 400g", "Salsas y Condimentos", 6400, "https://images.unsplash.com/photo-1607305387299-a3d9611cd469?w=500&q=80"),
    ("Mayonesa Cremosa Tradicional 380g", "Salsas y Condimentos", 7800, "https://images.unsplash.com/photo-1585238342024-78d387f4a707?w=500&q=80"),
    ("Salsa Napolitana con Albahaca 350g", "Salsas y Condimentos", 9200, "https://images.unsplash.com/photo-1572441713132-c542fc4fe282?w=500&q=80"),
    ("Aceite de Oliva Extra Virgen 500ml", "Salsas y Condimentos", 28500, "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=500&q=80"),
    ("Salsa BBQ Ahumada Original 350g", "Salsas y Condimentos", 7500, "https://images.unsplash.com/photo-1528750997573-59b89d56f4f7?w=500&q=80"),
    ("Mostaza Amarilla Clásica 250g", "Salsas y Condimentos", 4900, "https://images.unsplash.com/photo-1528750997573-59b89d56f4f7?w=500&q=80"),
    ("Miel Pura de Abejas Frasco 350g", "Salsas y Condimentos", 14500, "https://images.unsplash.com/photo-1587049352851-8d4e89133924?w=500&q=80"),
    ("Sal Marina Refinada 500g", "Salsas y Condimentos", 2800, "https://images.unsplash.com/photo-1518110925495-5fe2fda0442c?w=500&q=80"),
    ("Pimienta Negra Molida Frasco 60g", "Salsas y Condimentos", 6200, "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=500&q=80"),
    ("Salsa Pesto Genovés Frasco 200g", "Salsas y Condimentos", 12900, "https://images.unsplash.com/photo-1593001874117-c99c800e3eb7?w=500&q=80"),

    # 2. Pastas y Granos (10)
    ("Pasta Espagueti Tradicional 500g", "Pastas y Granos", 3900, "https://images.unsplash.com/photo-1551462147-ff29053bfc14?w=500&q=80"),
    ("Pasta Tornillos Tricolor 500g", "Pastas y Granos", 4500, "https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=500&q=80"),
    ("Pasta Penne Rigate 500g", "Pastas y Granos", 4300, "https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb?w=500&q=80"),
    ("Pasta Fetuccini Artesanal 500g", "Pastas y Granos", 5200, "https://images.unsplash.com/photo-1645112411341-6c4fd023714a?w=500&q=80"),
    ("Arroz Blanco Premium 1kg", "Pastas y Granos", 4900, "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=500&q=80"),
    ("Arroz Integral Seleccionado 1kg", "Pastas y Granos", 5600, "https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6?w=500&q=80"),
    ("Frijol Bola Roja 500g", "Pastas y Granos", 6800, "https://images.unsplash.com/photo-1551462147-37885acc36f1?w=500&q=80"),
    ("Lenteja Pardina Seleccionada 500g", "Pastas y Granos", 4200, "https://images.unsplash.com/photo-1515543904379-3d757afe72e4?w=500&q=80"),
    ("Garbanzo Seleccionado 500g", "Pastas y Granos", 5400, "https://images.unsplash.com/photo-1515543904379-3d757afe72e4?w=500&q=80"),
    ("Maíz Pira para Crispetas 500g", "Pastas y Granos", 3800, "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=500&q=80"),

    # 3. Harinas y Panadería (10)
    ("Harina de Trigo Fortificada 1kg", "Harinas y Panadería", 4100, "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=500&q=80"),
    ("Harina de Maíz Blanco Precocida 1kg", "Harinas y Panadería", 4500, "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=500&q=80"),
    ("Avena en Hojuelas Tradicional 500g", "Harinas y Panadería", 4800, "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?w=500&q=80"),
    ("Pan Tajado Blanco Familiar 600g", "Harinas y Panadería", 6900, "https://images.unsplash.com/photo-1598373182133-52452f7691ef?w=500&q=80"),
    ("Pan Integral con Semillas 500g", "Harinas y Panadería", 7600, "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=500&q=80"),
    ("Croissant de Mantequilla x4 Und", "Harinas y Panadería", 8200, "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=500&q=80"),
    ("Baguette Artesanal Fresca", "Harinas y Panadería", 4500, "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?w=500&q=80"),
    ("Tortillas de Harina de Trigo x10", "Harinas y Panadería", 6400, "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=500&q=80"),
    ("Pan para Hamburguesa Brioche x6", "Harinas y Panadería", 7200, "https://images.unsplash.com/photo-1586190848861-99aa4a171e90?w=500&q=80"),
    ("Tostadas Integrales Crujientes x12", "Harinas y Panadería", 5100, "https://images.unsplash.com/photo-1584776296944-ab6fb57b0bdd?w=500&q=80"),

    # 4. Lácteos y Huevos (10)
    ("Leche Entera Larga Vida 1L", "Lácteos y Huevos", 4500, "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=500&q=80"),
    ("Leche Deslactosada 1L", "Lácteos y Huevos", 5100, "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=500&q=80"),
    ("Huevos Campesinos AA x30 Und", "Lácteos y Huevos", 17500, "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=500&q=80"),
    ("Queso Campesino Fresco 500g", "Lácteos y Huevos", 11800, "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=500&q=80"),
    ("Queso Mozzarella Tajado 250g", "Lácteos y Huevos", 9400, "https://images.unsplash.com/photo-1552767059-ce182ead6c1b?w=500&q=80"),
    ("Yogurt Griego Natural 150g", "Lácteos y Huevos", 5300, "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=500&q=80"),
    ("Mantequilla con Sal 250g", "Lácteos y Huevos", 8600, "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=500&q=80"),
    ("Crema de Leche Entera 200ml", "Lácteos y Huevos", 4900, "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=500&q=80"),
    ("Queso Parmesano Rallado 100g", "Lácteos y Huevos", 7900, "https://images.unsplash.com/photo-1452195100486-9cc805987862?w=500&q=80"),
    ("Yogurt de Fresa Familiar 1L", "Lácteos y Huevos", 8900, "https://images.unsplash.com/photo-1571212515416-fef01fc43637?w=500&q=80"),

    # 5. Carnes y Embutidos (10)
    ("Pechuga de Pollo Sin Hueso 1kg", "Carnes y Embutidos", 18200, "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=500&q=80"),
    ("Carne de Res Molida Especial 500g", "Carnes y Embutidos", 14200, "https://images.unsplash.com/photo-1588168333986-5078d3ae3976?w=500&q=80"),
    ("Lomo de Res Seleccionado 500g", "Carnes y Embutidos", 21500, "https://images.unsplash.com/photo-1603048297172-c92544798d5a?w=500&q=80"),
    ("Costilla de Cerdo Carnuda 500g", "Carnes y Embutidos", 13900, "https://images.unsplash.com/photo-1544025162-d76694265947?w=500&q=80"),
    ("Salchicha Tradicional x10 Und", "Carnes y Embutidos", 9600, "https://images.unsplash.com/photo-1612392062631-94dd858cba88?w=500&q=80"),
    ("Jamón de Cerdo Ahumado 250g", "Carnes y Embutidos", 10400, "https://images.unsplash.com/photo-1524438418049-ab2acb7aa48f?w=500&q=80"),
    ("Filete de Salmón Fresco 400g", "Carnes y Embutidos", 27900, "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=500&q=80"),
    ("Chorizo Santarrosano x5 Und", "Carnes y Embutidos", 12800, "https://images.unsplash.com/photo-1585325701956-60dd9c8553bc?w=500&q=80"),
    ("Tocineta Ahumada Tajada 200g", "Carnes y Embutidos", 11200, "https://images.unsplash.com/photo-1606851094655-b2593a9af63f?w=500&q=80"),
    ("Muslos de Pollo Campesino 1kg", "Carnes y Embutidos", 12500, "https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=500&q=80"),

    # 6. Verduras y Hortalizas (10)
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

    # 7. Frutas Frescas (10)
    ("Manzana Roja Importada x4 Und", "Frutas Frescas", 8500, "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=500&q=80"),
    ("Banano Criollo Racimo 1kg", "Frutas Frescas", 3200, "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=500&q=80"),
    ("Aguacate Hass Seleccionado x2", "Frutas Frescas", 6800, "https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?w=500&q=80"),
    ("Fresa Seleccionada Bandeja 500g", "Frutas Frescas", 7400, "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=500&q=80"),
    ("Naranja Valencia Jugosa 1kg", "Frutas Frescas", 4300, "https://images.unsplash.com/photo-1547514701-42782101795e?w=500&q=80"),
    ("Piña Oro Miel Entera Unidad", "Frutas Frescas", 5900, "https://images.unsplash.com/photo-1550258987-190a2d41a8ba?w=500&q=80"),
    ("Mango Tommy Maduro x2 Und", "Frutas Frescas", 5400, "https://images.unsplash.com/photo-1553279768-865429fa0078?w=500&q=80"),
    ("Uva Red Globe Importada 500g", "Frutas Frescas", 9200, "https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=500&q=80"),
    ("Sandía Baby Dulce Unidad", "Frutas Frescas", 7800, "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=500&q=80"),
    ("Limón Tahití Fresco 1kg", "Frutas Frescas", 4600, "https://images.unsplash.com/photo-1590502593747-42a996133562?w=500&q=80"),

    # 8. Bebidas y Jugos (10)
    ("Jugo Natural de Naranja 1L", "Bebidas y Jugos", 5900, "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=500&q=80"),
    ("Café Tostado Molido 500g", "Bebidas y Jugos", 21500, "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=500&q=80"),
    ("Té Helado Durazno 1.5L", "Bebidas y Jugos", 4800, "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=500&q=80"),
    ("Agua Mineral Sin Gas 600ml", "Bebidas y Jugos", 2400, "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=500&q=80"),
    ("Gaseosa Cola Familiar 1.5L", "Bebidas y Jugos", 5500, "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500&q=80"),
    ("Jugo Verde Detox 500ml", "Bebidas y Jugos", 6400, "https://images.unsplash.com/photo-1610970881699-44a5587cabec?w=500&q=80"),
    ("Leche de Almendras Sin Azúcar 1L", "Bebidas y Jugos", 12900, "https://images.unsplash.com/photo-1600788886242-5c96aabe3757?w=500&q=80"),
    ("Limonada de Coco Natural 500ml", "Bebidas y Jugos", 5200, "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=500&q=80"),
    ("Chocolate en Pastilla Tradicional 500g", "Bebidas y Jugos", 9800, "https://images.unsplash.com/photo-1542990253-0d0f5be5f0ed?w=500&q=80"),
    ("Té Verde en Bolsitas x20 Und", "Bebidas y Jugos", 6200, "https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=500&q=80"),

    # 9. Confitería y Snacks (10)
    ("Chocolatina Leche Cremosa x4 Und", "Confitería y Snacks", 5600, "https://images.unsplash.com/photo-1511381939415-e44015466834?w=500&q=80"),
    ("Galletas con Chips de Chocolate", "Confitería y Snacks", 5200, "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=500&q=80"),
    ("Papas Fritas Naturales Paquete 150g", "Confitería y Snacks", 4900, "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=500&q=80"),
    ("Gomitas Frutales Surtidas 200g", "Confitería y Snacks", 4500, "https://images.unsplash.com/photo-1582058091505-f87a2e55a40f?w=500&q=80"),
    ("Maní Salado Tostado 200g", "Confitería y Snacks", 4800, "https://images.unsplash.com/photo-1567892737950-30c4db37cd89?w=500&q=80"),
    ("Barra de Cereal con Almendras x6", "Confitería y Snacks", 8400, "https://images.unsplash.com/photo-1590080875515-8a3a8dc5735e?w=500&q=80"),
    ("Brownie de Chocolate Artesanal x4", "Confitería y Snacks", 9500, "https://images.unsplash.com/photo-1564355808539-22fda35bed7e?w=500&q=80"),
    ("Nueces Mixtas Premium 150g", "Confitería y Snacks", 11200, "https://images.unsplash.com/photo-1599599810769-bcde5a160d32?w=500&q=80"),
    ("Donas Glaseadas Surtidas x4 Und", "Confitería y Snacks", 8900, "https://images.unsplash.com/photo-1551024601-bec78aea704b?w=500&q=80"),
    ("Galletas Integrales con Miel", "Confitería y Snacks", 4700, "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=500&q=80")
]

def descargar(args):
    pid, (nombre, cat, precio, url) = args
    ruta_local = f"/images/productos/prod_{pid}.jpg"
    archivo = f"Supermercado.Web/wwwroot{ruta_local}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            datos = r.read()
            if len(datos) > 2000:
                with open(archivo, "wb") as f:
                    f.write(datos)
                return (pid, nombre, cat, precio, ruta_local)
    except Exception:
        pass
    return (pid, nombre, cat, precio, url)

print("Descargando las 90 fotografías de las 9 categorías...")
resultados = []
with ThreadPoolExecutor(max_workers=15) as ex:
    for r in ex.map(descargar, enumerate(catalogo, start=1)):
        resultados.append(r)

lineas = []
for pid, nombre, cat, precio, ruta in resultados:
    stock = 18 + ((pid * 3) % 42)
    lineas.append(f'            new Producto {{ Id = {pid}, Nombre = "{nombre}", Categoria = "{cat}", Precio = {precio}, Stock = {stock}, ImagenUrl = "{ruta}" }}')

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
{",\n".join(lineas)}
        );
    }}
}}
'''

with open("Supermercado.Core/Data/SupermercadoDbContext.cs", "w", encoding="utf-8") as f:
    f.write(cs_code)

print(f"¡Listo! {len(resultados)} productos en 9 categorías guardados.")
