using Microsoft.EntityFrameworkCore;
using Supermercado.Core.Models;

namespace Supermercado.Core.Data;

public class SupermercadoDbContext : DbContext
{
    public DbSet<Producto> Productos => Set<Producto>();
    public DbSet<Pedido> Pedidos => Set<Pedido>();
    public DbSet<DetallePedido> DetallesPedido => Set<DetallePedido>();

    public SupermercadoDbContext(DbContextOptions<SupermercadoDbContext> options) : base(options) { }
    public SupermercadoDbContext() { }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        if (!optionsBuilder.IsConfigured)
        {
            var dbPath = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "supermercado.db"));
            optionsBuilder.UseSqlite($"Data Source={dbPath}");
        }
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Producto>().HasData(
            new Producto { Id = 1, Nombre = "Salsa de Tomate Clásica 400g", Categoria = "Salsas y Condimentos", Precio = 6400, Stock = 21, ImagenUrl = "/images/productos/prod_1.jpg" },
            new Producto { Id = 2, Nombre = "Mayonesa Cremosa Tradicional 380g", Categoria = "Salsas y Condimentos", Precio = 7800, Stock = 24, ImagenUrl = "/images/productos/prod_2.jpg" },
            new Producto { Id = 3, Nombre = "Salsa Napolitana con Albahaca 350g", Categoria = "Salsas y Condimentos", Precio = 9200, Stock = 27, ImagenUrl = "/images/productos/prod_3.jpg" },
            new Producto { Id = 4, Nombre = "Aceite de Oliva Extra Virgen 500ml", Categoria = "Salsas y Condimentos", Precio = 28500, Stock = 30, ImagenUrl = "/images/productos/prod_4.jpg" },
            new Producto { Id = 5, Nombre = "Salsa BBQ Ahumada Original 350g", Categoria = "Salsas y Condimentos", Precio = 7500, Stock = 33, ImagenUrl = "/images/productos/prod_5.jpg" },
            new Producto { Id = 6, Nombre = "Mostaza Amarilla Clásica 250g", Categoria = "Salsas y Condimentos", Precio = 4900, Stock = 36, ImagenUrl = "/images/productos/prod_6.jpg" },
            new Producto { Id = 7, Nombre = "Miel Pura de Abejas Frasco 350g", Categoria = "Salsas y Condimentos", Precio = 14500, Stock = 39, ImagenUrl = "/images/productos/prod_7.jpg" },
            new Producto { Id = 8, Nombre = "Sal Marina Refinada 500g", Categoria = "Salsas y Condimentos", Precio = 2800, Stock = 42, ImagenUrl = "/images/productos/prod_8.jpg" },
            new Producto { Id = 9, Nombre = "Pimienta Negra Molida Frasco 60g", Categoria = "Salsas y Condimentos", Precio = 6200, Stock = 45, ImagenUrl = "/images/productos/prod_9.jpg" },
            new Producto { Id = 10, Nombre = "Salsa Pesto Genovés Frasco 200g", Categoria = "Salsas y Condimentos", Precio = 12900, Stock = 48, ImagenUrl = "https://images.unsplash.com/photo-1593001874117-c99c800e3eb7?w=500&q=80" },
            new Producto { Id = 11, Nombre = "Pasta Espagueti Tradicional 500g", Categoria = "Pastas y Granos", Precio = 3900, Stock = 51, ImagenUrl = "/images/productos/prod_11.jpg" },
            new Producto { Id = 12, Nombre = "Pasta Tornillos Tricolor 500g", Categoria = "Pastas y Granos", Precio = 4500, Stock = 54, ImagenUrl = "/images/productos/prod_12.jpg" },
            new Producto { Id = 13, Nombre = "Pasta Penne Rigate 500g", Categoria = "Pastas y Granos", Precio = 4300, Stock = 57, ImagenUrl = "/images/productos/prod_13.jpg" },
            new Producto { Id = 14, Nombre = "Pasta Fetuccini Artesanal 500g", Categoria = "Pastas y Granos", Precio = 5200, Stock = 18, ImagenUrl = "/images/productos/prod_14.jpg" },
            new Producto { Id = 15, Nombre = "Arroz Blanco Premium 1kg", Categoria = "Pastas y Granos", Precio = 4900, Stock = 21, ImagenUrl = "/images/productos/prod_15.jpg" },
            new Producto { Id = 16, Nombre = "Arroz Integral Seleccionado 1kg", Categoria = "Pastas y Granos", Precio = 5600, Stock = 24, ImagenUrl = "/images/productos/prod_16.jpg" },
            new Producto { Id = 17, Nombre = "Frijol Bola Roja 500g", Categoria = "Pastas y Granos", Precio = 6800, Stock = 27, ImagenUrl = "/images/productos/prod_17.jpg" },
            new Producto { Id = 18, Nombre = "Lenteja Pardina Seleccionada 500g", Categoria = "Pastas y Granos", Precio = 4200, Stock = 30, ImagenUrl = "/images/productos/prod_18.jpg" },
            new Producto { Id = 19, Nombre = "Garbanzo Seleccionado 500g", Categoria = "Pastas y Granos", Precio = 5400, Stock = 33, ImagenUrl = "/images/productos/prod_19.jpg" },
            new Producto { Id = 20, Nombre = "Maíz Pira para Crispetas 500g", Categoria = "Pastas y Granos", Precio = 3800, Stock = 36, ImagenUrl = "/images/productos/prod_20.jpg" },
            new Producto { Id = 21, Nombre = "Harina de Trigo Fortificada 1kg", Categoria = "Harinas y Panadería", Precio = 4100, Stock = 39, ImagenUrl = "/images/productos/prod_21.jpg" },
            new Producto { Id = 22, Nombre = "Harina de Maíz Blanco Precocida 1kg", Categoria = "Harinas y Panadería", Precio = 4500, Stock = 42, ImagenUrl = "/images/productos/prod_22.jpg" },
            new Producto { Id = 23, Nombre = "Avena en Hojuelas Tradicional 500g", Categoria = "Harinas y Panadería", Precio = 4800, Stock = 45, ImagenUrl = "/images/productos/prod_23.jpg" },
            new Producto { Id = 24, Nombre = "Pan Tajado Blanco Familiar 600g", Categoria = "Harinas y Panadería", Precio = 6900, Stock = 48, ImagenUrl = "/images/productos/prod_24.jpg" },
            new Producto { Id = 25, Nombre = "Pan Integral con Semillas 500g", Categoria = "Harinas y Panadería", Precio = 7600, Stock = 51, ImagenUrl = "/images/productos/prod_25.jpg" },
            new Producto { Id = 26, Nombre = "Croissant de Mantequilla x4 Und", Categoria = "Harinas y Panadería", Precio = 8200, Stock = 54, ImagenUrl = "/images/productos/prod_26.jpg" },
            new Producto { Id = 27, Nombre = "Baguette Artesanal Fresca", Categoria = "Harinas y Panadería", Precio = 4500, Stock = 57, ImagenUrl = "/images/productos/prod_27.jpg" },
            new Producto { Id = 28, Nombre = "Tortillas de Harina de Trigo x10", Categoria = "Harinas y Panadería", Precio = 6400, Stock = 18, ImagenUrl = "/images/productos/prod_28.jpg" },
            new Producto { Id = 29, Nombre = "Pan para Hamburguesa Brioche x6", Categoria = "Harinas y Panadería", Precio = 7200, Stock = 21, ImagenUrl = "/images/productos/prod_29.jpg" },
            new Producto { Id = 30, Nombre = "Tostadas Integrales Crujientes x12", Categoria = "Harinas y Panadería", Precio = 5100, Stock = 24, ImagenUrl = "/images/productos/prod_30.jpg" },
            new Producto { Id = 31, Nombre = "Leche Entera Larga Vida 1L", Categoria = "Lácteos y Huevos", Precio = 4500, Stock = 27, ImagenUrl = "/images/productos/prod_31.jpg" },
            new Producto { Id = 32, Nombre = "Leche Deslactosada 1L", Categoria = "Lácteos y Huevos", Precio = 5100, Stock = 30, ImagenUrl = "/images/productos/prod_32.jpg" },
            new Producto { Id = 33, Nombre = "Huevos Campesinos AA x30 Und", Categoria = "Lácteos y Huevos", Precio = 17500, Stock = 33, ImagenUrl = "/images/productos/prod_33.jpg" },
            new Producto { Id = 34, Nombre = "Queso Campesino Fresco 500g", Categoria = "Lácteos y Huevos", Precio = 11800, Stock = 36, ImagenUrl = "/images/productos/prod_34.jpg" },
            new Producto { Id = 35, Nombre = "Queso Mozzarella Tajado 250g", Categoria = "Lácteos y Huevos", Precio = 9400, Stock = 39, ImagenUrl = "/images/productos/prod_35.jpg" },
            new Producto { Id = 36, Nombre = "Yogurt Griego Natural 150g", Categoria = "Lácteos y Huevos", Precio = 5300, Stock = 42, ImagenUrl = "/images/productos/prod_36.jpg" },
            new Producto { Id = 37, Nombre = "Mantequilla con Sal 250g", Categoria = "Lácteos y Huevos", Precio = 8600, Stock = 45, ImagenUrl = "/images/productos/prod_37.jpg" },
            new Producto { Id = 38, Nombre = "Crema de Leche Entera 200ml", Categoria = "Lácteos y Huevos", Precio = 4900, Stock = 48, ImagenUrl = "/images/productos/prod_38.jpg" },
            new Producto { Id = 39, Nombre = "Queso Parmesano Rallado 100g", Categoria = "Lácteos y Huevos", Precio = 7900, Stock = 51, ImagenUrl = "/images/productos/prod_39.jpg" },
            new Producto { Id = 40, Nombre = "Yogurt de Fresa Familiar 1L", Categoria = "Lácteos y Huevos", Precio = 8900, Stock = 54, ImagenUrl = "/images/productos/prod_40.jpg" },
            new Producto { Id = 41, Nombre = "Pechuga de Pollo Sin Hueso 1kg", Categoria = "Carnes y Embutidos", Precio = 18200, Stock = 57, ImagenUrl = "/images/productos/prod_41.jpg" },
            new Producto { Id = 42, Nombre = "Carne de Res Molida Especial 500g", Categoria = "Carnes y Embutidos", Precio = 14200, Stock = 18, ImagenUrl = "/images/productos/prod_42.jpg" },
            new Producto { Id = 43, Nombre = "Lomo de Res Seleccionado 500g", Categoria = "Carnes y Embutidos", Precio = 21500, Stock = 21, ImagenUrl = "/images/productos/prod_43.jpg" },
            new Producto { Id = 44, Nombre = "Costilla de Cerdo Carnuda 500g", Categoria = "Carnes y Embutidos", Precio = 13900, Stock = 24, ImagenUrl = "/images/productos/prod_44.jpg" },
            new Producto { Id = 45, Nombre = "Salchicha Tradicional x10 Und", Categoria = "Carnes y Embutidos", Precio = 9600, Stock = 27, ImagenUrl = "/images/productos/prod_45.jpg" },
            new Producto { Id = 46, Nombre = "Jamón de Cerdo Ahumado 250g", Categoria = "Carnes y Embutidos", Precio = 10400, Stock = 30, ImagenUrl = "/images/productos/prod_46.jpg" },
            new Producto { Id = 47, Nombre = "Filete de Salmón Fresco 400g", Categoria = "Carnes y Embutidos", Precio = 27900, Stock = 33, ImagenUrl = "/images/productos/prod_47.jpg" },
            new Producto { Id = 48, Nombre = "Chorizo Santarrosano x5 Und", Categoria = "Carnes y Embutidos", Precio = 12800, Stock = 36, ImagenUrl = "/images/productos/prod_48.jpg" },
            new Producto { Id = 49, Nombre = "Tocineta Ahumada Tajada 200g", Categoria = "Carnes y Embutidos", Precio = 11200, Stock = 39, ImagenUrl = "/images/productos/prod_49.jpg" },
            new Producto { Id = 50, Nombre = "Muslos de Pollo Campesino 1kg", Categoria = "Carnes y Embutidos", Precio = 12500, Stock = 42, ImagenUrl = "/images/productos/prod_50.jpg" },
            new Producto { Id = 51, Nombre = "Tomate Chonto Fresco 1kg", Categoria = "Verduras y Hortalizas", Precio = 4200, Stock = 45, ImagenUrl = "/images/productos/prod_51.jpg" },
            new Producto { Id = 52, Nombre = "Cebolla Cabezona Blanca 1kg", Categoria = "Verduras y Hortalizas", Precio = 3800, Stock = 48, ImagenUrl = "/images/productos/prod_52.jpg" },
            new Producto { Id = 53, Nombre = "Zanahoria Fresca Seleccionada 1kg", Categoria = "Verduras y Hortalizas", Precio = 3400, Stock = 51, ImagenUrl = "/images/productos/prod_53.jpg" },
            new Producto { Id = 54, Nombre = "Papa Pastusa Lavada 1kg", Categoria = "Verduras y Hortalizas", Precio = 3600, Stock = 54, ImagenUrl = "/images/productos/prod_54.jpg" },
            new Producto { Id = 55, Nombre = "Brócoli Fresco Unidad 500g", Categoria = "Verduras y Hortalizas", Precio = 5200, Stock = 57, ImagenUrl = "/images/productos/prod_55.jpg" },
            new Producto { Id = 56, Nombre = "Pimentón Rojo Dulce 500g", Categoria = "Verduras y Hortalizas", Precio = 4500, Stock = 18, ImagenUrl = "/images/productos/prod_56.jpg" },
            new Producto { Id = 57, Nombre = "Lechuga Batavia Fresca Unidad", Categoria = "Verduras y Hortalizas", Precio = 3100, Stock = 21, ImagenUrl = "/images/productos/prod_57.jpg" },
            new Producto { Id = 58, Nombre = "Pepino Cohombro Fresco 500g", Categoria = "Verduras y Hortalizas", Precio = 2900, Stock = 24, ImagenUrl = "/images/productos/prod_58.jpg" },
            new Producto { Id = 59, Nombre = "Espinaca Bogotana Manojo 500g", Categoria = "Verduras y Hortalizas", Precio = 3900, Stock = 27, ImagenUrl = "/images/productos/prod_59.jpg" },
            new Producto { Id = 60, Nombre = "Ajo Nacional Malla x3 Cabezas", Categoria = "Verduras y Hortalizas", Precio = 4100, Stock = 30, ImagenUrl = "/images/productos/prod_60.jpg" },
            new Producto { Id = 61, Nombre = "Manzana Roja Importada x4 Und", Categoria = "Frutas Frescas", Precio = 8500, Stock = 33, ImagenUrl = "/images/productos/prod_61.jpg" },
            new Producto { Id = 62, Nombre = "Banano Criollo Racimo 1kg", Categoria = "Frutas Frescas", Precio = 3200, Stock = 36, ImagenUrl = "/images/productos/prod_62.jpg" },
            new Producto { Id = 63, Nombre = "Aguacate Hass Seleccionado x2", Categoria = "Frutas Frescas", Precio = 6800, Stock = 39, ImagenUrl = "/images/productos/prod_63.jpg" },
            new Producto { Id = 64, Nombre = "Fresa Seleccionada Bandeja 500g", Categoria = "Frutas Frescas", Precio = 7400, Stock = 42, ImagenUrl = "/images/productos/prod_64.jpg" },
            new Producto { Id = 65, Nombre = "Naranja Valencia Jugosa 1kg", Categoria = "Frutas Frescas", Precio = 4300, Stock = 45, ImagenUrl = "/images/productos/prod_65.jpg" },
            new Producto { Id = 66, Nombre = "Piña Oro Miel Entera Unidad", Categoria = "Frutas Frescas", Precio = 5900, Stock = 48, ImagenUrl = "/images/productos/prod_66.jpg" },
            new Producto { Id = 67, Nombre = "Mango Tommy Maduro x2 Und", Categoria = "Frutas Frescas", Precio = 5400, Stock = 51, ImagenUrl = "/images/productos/prod_67.jpg" },
            new Producto { Id = 68, Nombre = "Uva Red Globe Importada 500g", Categoria = "Frutas Frescas", Precio = 9200, Stock = 54, ImagenUrl = "/images/productos/prod_68.jpg" },
            new Producto { Id = 69, Nombre = "Sandía Baby Dulce Unidad", Categoria = "Frutas Frescas", Precio = 7800, Stock = 57, ImagenUrl = "/images/productos/prod_69.jpg" },
            new Producto { Id = 70, Nombre = "Limón Tahití Fresco 1kg", Categoria = "Frutas Frescas", Precio = 4600, Stock = 18, ImagenUrl = "/images/productos/prod_70.jpg" },
            new Producto { Id = 71, Nombre = "Jugo Natural de Naranja 1L", Categoria = "Bebidas y Jugos", Precio = 5900, Stock = 21, ImagenUrl = "/images/productos/prod_71.jpg" },
            new Producto { Id = 72, Nombre = "Café Tostado Molido 500g", Categoria = "Bebidas y Jugos", Precio = 21500, Stock = 24, ImagenUrl = "/images/productos/prod_72.jpg" },
            new Producto { Id = 73, Nombre = "Té Helado Durazno 1.5L", Categoria = "Bebidas y Jugos", Precio = 4800, Stock = 27, ImagenUrl = "/images/productos/prod_73.jpg" },
            new Producto { Id = 74, Nombre = "Agua Mineral Sin Gas 600ml", Categoria = "Bebidas y Jugos", Precio = 2400, Stock = 30, ImagenUrl = "/images/productos/prod_74.jpg" },
            new Producto { Id = 75, Nombre = "Gaseosa Cola Familiar 1.5L", Categoria = "Bebidas y Jugos", Precio = 5500, Stock = 33, ImagenUrl = "/images/productos/prod_75.jpg" },
            new Producto { Id = 76, Nombre = "Jugo Verde Detox 500ml", Categoria = "Bebidas y Jugos", Precio = 6400, Stock = 36, ImagenUrl = "/images/productos/prod_76.jpg" },
            new Producto { Id = 77, Nombre = "Leche de Almendras Sin Azúcar 1L", Categoria = "Bebidas y Jugos", Precio = 12900, Stock = 39, ImagenUrl = "/images/productos/prod_77.jpg" },
            new Producto { Id = 78, Nombre = "Limonada de Coco Natural 500ml", Categoria = "Bebidas y Jugos", Precio = 5200, Stock = 42, ImagenUrl = "/images/productos/prod_78.jpg" },
            new Producto { Id = 79, Nombre = "Chocolate en Pastilla Tradicional 500g", Categoria = "Bebidas y Jugos", Precio = 9800, Stock = 45, ImagenUrl = "/images/productos/prod_79.jpg" },
            new Producto { Id = 80, Nombre = "Té Verde en Bolsitas x20 Und", Categoria = "Bebidas y Jugos", Precio = 6200, Stock = 48, ImagenUrl = "/images/productos/prod_80.jpg" },
            new Producto { Id = 81, Nombre = "Chocolatina Leche Cremosa x4 Und", Categoria = "Confitería y Snacks", Precio = 5600, Stock = 51, ImagenUrl = "/images/productos/prod_81.jpg" },
            new Producto { Id = 82, Nombre = "Galletas con Chips de Chocolate", Categoria = "Confitería y Snacks", Precio = 5200, Stock = 54, ImagenUrl = "/images/productos/prod_82.jpg" },
            new Producto { Id = 83, Nombre = "Papas Fritas Naturales Paquete 150g", Categoria = "Confitería y Snacks", Precio = 4900, Stock = 57, ImagenUrl = "/images/productos/prod_83.jpg" },
            new Producto { Id = 84, Nombre = "Gomitas Frutales Surtidas 200g", Categoria = "Confitería y Snacks", Precio = 4500, Stock = 18, ImagenUrl = "/images/productos/prod_84.jpg" },
            new Producto { Id = 85, Nombre = "Maní Salado Tostado 200g", Categoria = "Confitería y Snacks", Precio = 4800, Stock = 21, ImagenUrl = "/images/productos/prod_85.jpg" },
            new Producto { Id = 86, Nombre = "Barra de Cereal con Almendras x6", Categoria = "Confitería y Snacks", Precio = 8400, Stock = 24, ImagenUrl = "/images/productos/prod_86.jpg" },
            new Producto { Id = 87, Nombre = "Brownie de Chocolate Artesanal x4", Categoria = "Confitería y Snacks", Precio = 9500, Stock = 27, ImagenUrl = "/images/productos/prod_87.jpg" },
            new Producto { Id = 88, Nombre = "Nueces Mixtas Premium 150g", Categoria = "Confitería y Snacks", Precio = 11200, Stock = 30, ImagenUrl = "/images/productos/prod_88.jpg" },
            new Producto { Id = 89, Nombre = "Donas Glaseadas Surtidas x4 Und", Categoria = "Confitería y Snacks", Precio = 8900, Stock = 33, ImagenUrl = "/images/productos/prod_89.jpg" },
            new Producto { Id = 90, Nombre = "Galletas Integrales con Miel", Categoria = "Confitería y Snacks", Precio = 4700, Stock = 36, ImagenUrl = "/images/productos/prod_90.jpg" }
        );
    }
}
