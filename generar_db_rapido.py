import os

productos = [
    (1, "Salsa de Tomate Fruco Doypack 400g", "Salsas y Condimentos", 6400, 45),
    (2, "Mayonesa Fruco Doypack 380g", "Salsas y Condimentos", 8200, 35),
    (3, "Salsa BBQ Fruco Original 350g", "Salsas y Condimentos", 7500, 30),
    (4, "Salsa de Tomate Heinz 397g", "Salsas y Condimentos", 11900, 25),
    (5, "Aceite de Oliva Extra Virgen 500ml", "Salsas y Condimentos", 29900, 20),
    (6, "Mostaza Fruco Doypack 200g", "Salsas y Condimentos", 4800, 32),

    (7, "Pasta Espagueti Doria 500g", "Pastas y Granos", 3900, 60),
    (8, "Pasta Tornillos Doria 500g", "Pastas y Granos", 4100, 50),
    (9, "Pasta Espagueti La Muñeca 500g", "Pastas y Granos", 3700, 55),
    (10, "Pasta Penne Barilla 500g", "Pastas y Granos", 8500, 32),
    (11, "Arroz Blanco Diana 1000g", "Pastas y Granos", 4900, 80),
    (12, "Arroz Blanco Roa 1000g", "Pastas y Granos", 5100, 75),
    (13, "Frijol Bola Roja Diana 500g", "Pastas y Granos", 6900, 40),

    (14, "Leche Entera Alpina 1100ml", "Lácteos y Huevos", 4600, 50),
    (15, "Leche Deslactosada Alquería 1100ml", "Lácteos y Huevos", 5200, 45),
    (16, "Queso Campesino Alpina 400g", "Lácteos y Huevos", 12400, 30),
    (17, "Yogurt Griego Alpina 150g", "Lácteos y Huevos", 5400, 38),
    (18, "Arequipe Alpina 250g", "Lácteos y Huevos", 7800, 35),

    (19, "Salchicha Tradicional Zenú", "Carnes y Embutidos", 9800, 40),
    (20, "Jamón de Cerdo Pietrán 230g", "Carnes y Embutidos", 11500, 30),
    (21, "Atún Van Camp's en Aceite 160g", "Carnes y Embutidos", 7400, 48),

    (22, "Pan Tajado Blanco Bimbo 600g", "Panadería y Bebidas", 7200, 42),
    (23, "Café Molido Juan Valdez 454g", "Panadería y Bebidas", 26500, 28),
    (24, "Jugo Hit Naranja Piña 1000ml", "Panadería y Bebidas", 4300, 55)
]

resultados_cs = []
for pid, nombre, cat, precio, stock in productos:
    ruta_local = f"/images/productos/prod_{pid}.jpg"
    archivo_fisico = f"Supermercado.Web/wwwroot{ruta_local}"
    if not (os.path.exists(archivo_fisico) and os.path.getsize(archivo_fisico) > 2000):
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
print("Listo en menos de 1 segundo.")
