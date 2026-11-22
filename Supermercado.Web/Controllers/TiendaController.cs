using System.Text.Json;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Supermercado.Core.Data;
using Supermercado.Core.Models;
using Supermercado.Core.Services;

namespace Supermercado.Web.Controllers;

public class TiendaController : Controller
{
    private readonly SupermercadoDbContext _context;
    private readonly UserManager<IdentityUser> _userManager;
    private readonly LogisticaService _logistica = new();

    public TiendaController(SupermercadoDbContext context, UserManager<IdentityUser> userManager)
    {
        _context = context;
        _userManager = userManager;
    }

    private List<DetallePedido> ObtenerCarrito()
    {
        var json = HttpContext.Session.GetString("Carrito");
        return string.IsNullOrEmpty(json) ? new List<DetallePedido>() : JsonSerializer.Deserialize<List<DetallePedido>>(json)!;
    }

    private void GuardarCarrito(List<DetallePedido> carrito)
    {
        HttpContext.Session.SetString("Carrito", JsonSerializer.Serialize(carrito));
    }

    public IActionResult Bienvenida() => View();

    public async Task<IActionResult> Index(string? categoria, string? buscar)
    {
        var query = _context.Productos.AsQueryable();

        if (!string.IsNullOrWhiteSpace(categoria))
            query = query.Where(p => p.Categoria == categoria);

        if (!string.IsNullOrWhiteSpace(buscar))
            query = query.Where(p => p.Nombre.ToLower().Contains(buscar.ToLower()));

        ViewBag.Categorias = await _context.Productos.Select(p => p.Categoria).Distinct().ToListAsync();
        ViewBag.CategoriaActual = categoria;
        ViewBag.BuscarActual = buscar;
        ViewBag.Carrito = ObtenerCarrito();

        if (User.Identity?.IsAuthenticated == true)
        {
            var user = await _userManager.GetUserAsync(User);
            if (user != null)
            {
                var claims = await _userManager.GetClaimsAsync(user);
                ViewBag.DireccionUsuario = claims.FirstOrDefault(c => c.Type == "Direccion")?.Value ?? "";
                ViewBag.WhatsAppUsuario = user.PhoneNumber ?? "";
                ViewBag.LlamadaUsuario = claims.FirstOrDefault(c => c.Type == "TelefonoLlamada")?.Value ?? "";
            }
        }

        return View(await query.ToListAsync());
    }

    [Authorize]
    [HttpPost]
    public async Task<IActionResult> AgregarAlCarrito(int productoId, int cantidad)
    {
        var producto = await _context.Productos.FindAsync(productoId);
        if (producto != null && cantidad > 0 && producto.Stock >= cantidad)
        {
            var carrito = ObtenerCarrito();
            var existente = carrito.FirstOrDefault(c => c.ProductoId == productoId);
            if (existente != null)
                existente.Cantidad += cantidad;
            else
                carrito.Add(new DetallePedido { ProductoId = producto.Id, NombreProducto = producto.Nombre, Cantidad = cantidad, PrecioUnitario = producto.Precio });

            GuardarCarrito(carrito);
            TempData["Mensaje"] = $"Agregado al carrito: {cantidad} x {producto.Nombre}";
        }
        return RedirectToAction(nameof(Index));
    }

    [Authorize]
    [HttpPost]
    public IActionResult QuitarDelCarrito(int productoId)
    {
        var carrito = ObtenerCarrito();
        var item = carrito.FirstOrDefault(c => c.ProductoId == productoId);
        if (item != null)
        {
            carrito.Remove(item);
            GuardarCarrito(carrito);
            TempData["Mensaje"] = $"Producto quitado del carrito: {item.NombreProducto}";
        }
        return RedirectToAction(nameof(Index));
    }

    [Authorize]
    [HttpPost]
    public async Task<IActionResult> ConfirmarPedidoCarrito(string direccion, string whatsapp, string llamada, string metodoPago)
    {
        var carrito = ObtenerCarrito();
        if (!carrito.Any() || string.IsNullOrWhiteSpace(direccion))
        {
            TempData["Error"] = "El carrito está vacío o falta la dirección de entrega.";
            return RedirectToAction(nameof(Index));
        }

        _logistica.CargarCatalogo(await _context.Productos.ToListAsync());
        foreach (var item in carrito)
        {
            var prod = _logistica.BuscarProductoPorId(item.ProductoId);
            if (prod == null || prod.Stock < item.Cantidad)
            {
                TempData["Error"] = $"Stock insuficiente para {item.NombreProducto}.";
                return RedirectToAction(nameof(Index));
            }
            prod.DescontarStock(item.Cantidad);
        }

        var user = await _userManager.GetUserAsync(User);
        var claims = user != null ? await _userManager.GetClaimsAsync(user) : new List<System.Security.Claims.Claim>();
        var nombreCliente = claims.FirstOrDefault(c => c.Type == "NombreCompleto")?.Value ?? User.Identity?.Name ?? "Cliente";

        var pedido = new Pedido
        {
            ClienteNombre = nombreCliente,
            ClienteEmail = User.Identity?.Name ?? "",
            TelefonoWhatsApp = whatsapp,
            TelefonoLlamada = llamada,
            DireccionEntrega = direccion,
            MetodoPago = metodoPago,
            FechaPedido = DateTime.Now,
            Estado = EstadoPedido.Pendiente,
            Detalles = carrito
        };

        _context.Pedidos.Add(pedido);
        await _context.SaveChangesAsync();
        GuardarCarrito(new List<DetallePedido>());

        TempData["Mensaje"] = $"¡Pedido #{pedido.Id} enviado a Super La Cosecha a las {pedido.FechaPedido:HH:mm:ss}!";
        return RedirectToAction(nameof(MisPedidos));
    }

    [Authorize]
    public async Task<IActionResult> MisPedidos()
    {
        var query = _context.Pedidos.Include(p => p.Detalles).AsQueryable();
        if (User.IsInRole("Admin"))
        {
            var todos = await query.OrderBy(p => p.FechaPedido).ToListAsync();
            _logistica.EncolarPedidosPendientes(todos);
            ViewBag.SiguienteTurnoId = _logistica.ColaDespachos.Count > 0 ? _logistica.ColaDespachos.Peek().Id : 0;
            return View(todos);
        }
        return View(await query.Where(p => p.ClienteEmail == User.Identity!.Name).OrderByDescending(p => p.FechaPedido).ToListAsync());
    }

    [Authorize(Roles = "Admin")]
    [HttpPost]
    public async Task<IActionResult> CrearProductoReal(string nombre, string categoria, decimal precio, int stock, IFormFile? archivoImagen, string? urlExterna)
    {
        string rutaFinal = "/images/logo.png";

        if (archivoImagen != null && archivoImagen.Length > 0)
        {
            var carpeta = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot", "images", "productos");
            Directory.CreateDirectory(carpeta);
            var nombreArchivo = $"{Guid.NewGuid()}_{Path.GetFileName(archivoImagen.FileName)}";
            var rutaFisica = Path.Combine(carpeta, nombreArchivo);
            using var stream = new FileStream(rutaFisica, FileMode.Create);
            await archivoImagen.CopyToAsync(stream);
            rutaFinal = $"/images/productos/{nombreArchivo}";
        }
        else if (!string.IsNullOrWhiteSpace(urlExterna))
        {
            rutaFinal = urlExterna;
        }

        _context.Productos.Add(new Producto
        {
            Nombre = nombre,
            Categoria = categoria,
            Precio = precio,
            Stock = stock,
            ImagenUrl = rutaFinal
        });
        await _context.SaveChangesAsync();
        TempData["Mensaje"] = $"Producto '{nombre}' agregado con su fotografía real.";
        return RedirectToAction(nameof(Index));
    }

    [Authorize(Roles = "Admin")]
    [HttpPost]
    public async Task<IActionResult> DespacharSiguiente()
    {
        var pendientes = await _context.Pedidos.Where(p => p.Estado == EstadoPedido.Pendiente).ToListAsync();
        _logistica.EncolarPedidosPendientes(pendientes);
        var siguiente = _logistica.ObtenerSiguienteParaDespacho();
        if (siguiente != null)
        {
            siguiente.Estado = EstadoPedido.EnCamino;
            siguiente.HoraDespacho = DateTime.Now;
            siguiente.MensajeDomiciliario = $"¡En camino! Salió a las {DateTime.Now:HH:mm:ss} hacia {siguiente.DireccionEntrega}. Cobro: {siguiente.MetodoPago}.";
            await _context.SaveChangesAsync();
            TempData["Mensaje"] = $"Pedido #{siguiente.Id} despachado hacia {siguiente.DireccionEntrega}.";
        }
        return RedirectToAction(nameof(MisPedidos));
    }

    [Authorize(Roles = "Admin")]
    [HttpPost]
    public async Task<IActionResult> ConfirmarPagoEmpleado(int pedidoId)
    {
        var pedido = await _context.Pedidos.FindAsync(pedidoId);
        if (pedido != null)
        {
            pedido.PagoConfirmado = true;
            pedido.Estado = EstadoPedido.Entregado;
            pedido.MensajeDomiciliario = $"💰 Pago confirmado ({pedido.MetodoPago}) y pedido entregado a las {DateTime.Now:HH:mm:ss}.";
            await _context.SaveChangesAsync();
            TempData["Mensaje"] = $"Pago de ${pedido.Total:N0} ({pedido.MetodoPago}) confirmado para el Pedido #{pedidoId}.";
        }
        return RedirectToAction(nameof(MisPedidos));
    }

    [Authorize]
    [HttpPost]
    public async Task<IActionResult> ConfirmarRecepcionCliente(int pedidoId)
    {
        var pedido = await _context.Pedidos.FindAsync(pedidoId);
        if (pedido != null && pedido.ClienteEmail == User.Identity?.Name)
        {
            pedido.RecibidoPorCliente = true;
            pedido.Estado = EstadoPedido.Entregado;
            pedido.MensajeDomiciliario = $"✅ El cliente confirmó recepción conforme del pedido a las {DateTime.Now:HH:mm:ss}.";
            await _context.SaveChangesAsync();
            TempData["Mensaje"] = $"¡Gracias! Has confirmado la recepción del Pedido #{pedidoId}.";
        }
        return RedirectToAction(nameof(MisPedidos));
    }

    [Authorize(Roles = "Admin")]
    [HttpPost]
    public async Task<IActionResult> EnviarMensajeCliente(int pedidoId, string mensaje)
    {
        var pedido = await _context.Pedidos.FindAsync(pedidoId);
        if (pedido != null && !string.IsNullOrWhiteSpace(mensaje))
        {
            pedido.MensajeDomiciliario = $"[Super La Cosecha {DateTime.Now:HH:mm}]: {mensaje}";
            await _context.SaveChangesAsync();
        }
        return RedirectToAction(nameof(MisPedidos));
    }
}
