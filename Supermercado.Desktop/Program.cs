using Microsoft.EntityFrameworkCore;
using Supermercado.Core.Data;
using Supermercado.Core.Models;
using Supermercado.Core.Services;

var logistica = new LogisticaService();

while (true)
{
    Console.Clear();
    Console.WriteLine("=========================================================================");
    Console.WriteLine("      CENTRAL DE DESPACHOS FIFO - SUPERMERCADO EXPRESS (DESKTOP)         ");
    Console.WriteLine("=========================================================================");

    using var db = new SupermercadoDbContext();
    db.Database.EnsureCreated();

    var pendientes = db.Pedidos.Include(p => p.Detalles).Where(p => p.Estado == EstadoPedido.Pendiente).ToList();
    logistica.EncolarPedidosPendientes(pendientes);

    Console.WriteLine($"Pedidos en cola FIFO pendientes: {logistica.ColaDespachos.Count}\n");
    foreach (var p in logistica.ColaDespachos)
    {
        Console.WriteLine($"[#{p.Id}] Hora: {p.FechaPedido:HH:mm:ss} | Cliente: {p.ClienteNombre} (Tel: {p.TelefonoContacto})");
        Console.WriteLine($"       Dirección: {p.DireccionEntrega} | Pago: {p.MetodoPago} | Total: ${p.Total:N0}");
        Console.WriteLine("-------------------------------------------------------------------------");
    }

    Console.WriteLine("\n[1] Despachar siguiente pedido en turno (Dequeue) | [2] Actualizar | [0] Salir");
    Console.Write("Opción: ");
    var op = Console.ReadLine();
    if (op == "0") break;
    if (op == "1")
    {
        var sig = logistica.ObtenerSiguienteParaDespacho();
        if (sig != null)
        {
            sig.Estado = EstadoPedido.EnCamino;
            sig.HoraDespacho = DateTime.Now;
            sig.MensajeDomiciliario = $"Despachado desde Bodega Desktop a las {DateTime.Now:HH:mm:ss}. Dirección: {sig.DireccionEntrega}. Pago: {sig.MetodoPago}.";
            db.SaveChanges();
            Console.WriteLine($"\n[OK] Pedido #{sig.Id} despachado a {sig.DireccionEntrega} ({sig.MetodoPago}).");
        }
        else Console.WriteLine("\nNo hay pedidos pendientes.");
        Console.WriteLine("Presione ENTER..."); Console.ReadLine();
    }
}
