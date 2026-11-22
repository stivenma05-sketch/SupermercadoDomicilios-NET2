namespace Supermercado.Core.Models;

public enum EstadoPedido { Pendiente, EnCamino, Entregado }

public class Pedido
{
    public int Id { get; set; }
    public string ClienteNombre { get; set; } = string.Empty;
    public string ClienteEmail { get; set; } = string.Empty;
    public string TelefonoWhatsApp { get; set; } = string.Empty;
    public string TelefonoLlamada { get; set; } = string.Empty;
    public string DireccionEntrega { get; set; } = string.Empty;
    public string MetodoPago { get; set; } = "Efectivo contra entrega";
    public DateTime FechaPedido { get; set; } = DateTime.Now;
    public DateTime? HoraDespacho { get; set; }
    public EstadoPedido Estado { get; set; } = EstadoPedido.Pendiente;
    public bool PagoConfirmado { get; set; } = false;
    public bool RecibidoPorCliente { get; set; } = false;
    public string MensajeDomiciliario { get; set; } = "Pedido recibido en Market Express. En cola de alistamiento.";
    public List<DetallePedido> Detalles { get; set; } = new();
    public decimal Total => Detalles.Sum(d => d.Subtotal);
}

public class DetallePedido
{
    public int Id { get; set; }
    public int PedidoId { get; set; }
    public int ProductoId { get; set; }
    public string NombreProducto { get; set; } = string.Empty;
    public int Cantidad { get; set; }
    public decimal PrecioUnitario { get; set; }
    public decimal Subtotal => Cantidad * PrecioUnitario;
}
