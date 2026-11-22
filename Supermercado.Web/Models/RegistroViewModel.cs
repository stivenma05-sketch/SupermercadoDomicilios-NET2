using System.ComponentModel.DataAnnotations;

namespace Supermercado.Web.Models;

public class RegistroViewModel
{
    [Required(ErrorMessage = "El nombre completo es obligatorio")]
    public string NombreCompleto { get; set; } = string.Empty;

    [Required(ErrorMessage = "El correo electrónico es obligatorio"), EmailAddress]
    public string Email { get; set; } = string.Empty;

    [Required(ErrorMessage = "El número de WhatsApp es obligatorio")]
    public string TelefonoWhatsApp { get; set; } = string.Empty;

    [Required(ErrorMessage = "El número de llamada es obligatorio")]
    public string TelefonoLlamada { get; set; } = string.Empty;

    [Required(ErrorMessage = "La dirección de entrega es obligatoria")]
    public string Direccion { get; set; } = string.Empty;

    [Required(ErrorMessage = "La contraseña es obligatoria"), MinLength(6)]
    public string Password { get; set; } = string.Empty;

    [Required]
    public string TipoCuenta { get; set; } = "Cliente"; // "Cliente" o "Admin"

    public string? CodigoEmpleado { get; set; }
}

public class LoginViewModel
{
    [Required(ErrorMessage = "Ingrese su correo electrónico"), EmailAddress]
    public string Email { get; set; } = string.Empty;

    [Required(ErrorMessage = "Ingrese su contraseña")]
    public string Password { get; set; } = string.Empty;

    [Required]
    public string RolSeleccionado { get; set; } = "Cliente"; // "Cliente" o "Admin"
}
