using Supermercado.Core.Models;

namespace Supermercado.Core.Services;

public class LogisticaService
{
    public Dictionary<int, Producto> CatalogoRapido { get; private set; } = new();
    public Queue<Pedido> ColaDespachos { get; private set; } = new();

    public void CargarCatalogo(IEnumerable<Producto> productos) =>
        CatalogoRapido = productos.ToDictionary(p => p.Id);

    public Producto? BuscarProductoPorId(int id)
    {
        CatalogoRapido.TryGetValue(id, out var producto);
        return producto;
    }

    public void EncolarPedidosPendientes(IEnumerable<Pedido> pedidos)
    {
        ColaDespachos.Clear();
        foreach (var p in pedidos.Where(x => x.Estado == EstadoPedido.Pendiente).OrderBy(x => x.FechaPedido))
            ColaDespachos.Enqueue(p);
    }

    public Pedido? ObtenerSiguienteParaDespacho() =>
        ColaDespachos.Count > 0 ? ColaDespachos.Dequeue() : null;
}
