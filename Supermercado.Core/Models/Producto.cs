namespace Supermercado.Core.Models;

public class Producto
{
    public int Id { get; set; }
    public string Nombre { get; set; } = string.Empty;
    public string Categoria { get; set; } = string.Empty;
    public decimal Precio { get; set; }
    public string ImagenUrl { get; set; } = string.Empty;

    private int _stock;
    public int Stock
    {
        get => _stock;
        set
        {
            if (value < 0) throw new ArgumentException("El stock no puede ser negativo.");
            _stock = value;
        }
    }

    public void DescontarStock(int cantidad)
    {
        if (cantidad <= 0 || cantidad > _stock) throw new InvalidOperationException("Cantidad no disponible.");
        _stock -= cantidad;
    }
}
