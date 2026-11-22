namespace Supermercado.Core.Models;

public abstract class Persona
{
    public int Id { get; set; }
    public string Nombre { get; set; } = string.Empty;
    public string Telefono { get; set; } = string.Empty;
    public virtual string ObtenerResumenRol() => $"Usuario: {Nombre}";
}

public class ClienteDomicilio : Persona
{
    public string Email { get; set; } = string.Empty;
    public string DireccionEntrega { get; set; } = string.Empty;
    public override string ObtenerResumenRol() => $"Cliente: {Nombre} | Dirección: {DireccionEntrega}";
}

public class Repartidor : Persona
{
    public string PlacaVehiculo { get; set; } = string.Empty;
    public override string ObtenerResumenRol() => $"Repartidor: {Nombre} | Placa: {PlacaVehiculo}";
}
