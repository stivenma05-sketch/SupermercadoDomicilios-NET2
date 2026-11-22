using System.Security.Claims;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Supermercado.Web.Models;

namespace Supermercado.Web.Controllers;

public class CuentaController : Controller
{
    private readonly UserManager<IdentityUser> _userManager;
    private readonly SignInManager<IdentityUser> _signInManager;

    public CuentaController(UserManager<IdentityUser> userManager, SignInManager<IdentityUser> signInManager)
    {
        _userManager = userManager;
        _signInManager = signInManager;
    }

    [HttpGet]
    public IActionResult Login() => View();

    [HttpPost]
    public async Task<IActionResult> Login(LoginViewModel model)
    {
        if (!ModelState.IsValid) return View(model);

        var user = await _userManager.FindByEmailAsync(model.Email);
        if (user == null)
        {
            ModelState.AddModelError("", "Correo o contraseña incorrectos.");
            return View(model);
        }

        // Verificar si el usuario pertenece al perfil elegido (Cliente vs Empleado/Dueño)
        bool esEmpleado = await _userManager.IsInRoleAsync(user, "Admin");
        if (model.RolSeleccionado == "Admin" && !esEmpleado)
        {
            ModelState.AddModelError("", "Esta cuenta está registrada como Cliente, no como Empleado/Dueño.");
            return View(model);
        }
        if (model.RolSeleccionado == "Cliente" && esEmpleado)
        {
            ModelState.AddModelError("", "Esta cuenta pertenece a Empleado/Dueño. Seleccione ese perfil para ingresar.");
            return View(model);
        }

        var result = await _signInManager.PasswordSignInAsync(user, model.Password, isPersistent: false, lockoutOnFailure: false);
        if (result.Succeeded)
        {
            return esEmpleado ? RedirectToAction("MisPedidos", "Tienda") : RedirectToAction("Index", "Tienda");
        }

        ModelState.AddModelError("", "Credenciales inválidas. Verifique su contraseña.");
        return View(model);
    }

    [HttpGet]
    public IActionResult Registro() => View();

    [HttpPost]
    public async Task<IActionResult> Registro(RegistroViewModel model)
    {
        if (!ModelState.IsValid) return View(model);

        if (model.TipoCuenta == "Admin" && model.CodigoEmpleado != "COSECHA2026")
        {
            ModelState.AddModelError("CodigoEmpleado", "Código interno inválido para Empleado/Dueño (Use: COSECHA2026).");
            return View(model);
        }

        var user = new IdentityUser
        {
            UserName = model.Email,
            Email = model.Email,
            PhoneNumber = model.TelefonoWhatsApp,
            EmailConfirmed = true
        };

        var result = await _userManager.CreateAsync(user, model.Password);
        if (result.Succeeded)
        {
            await _userManager.AddToRoleAsync(user, model.TipoCuenta);
            await _userManager.AddClaimAsync(user, new Claim("NombreCompleto", model.NombreCompleto));
            await _userManager.AddClaimAsync(user, new Claim("TelefonoLlamada", model.TelefonoLlamada));
            await _userManager.AddClaimAsync(user, new Claim("Direccion", model.Direccion));
            await _signInManager.SignInAsync(user, isPersistent: false);
            return model.TipoCuenta == "Admin" ? RedirectToAction("MisPedidos", "Tienda") : RedirectToAction("Index", "Tienda");
        }

        foreach (var error in result.Errors)
            ModelState.AddModelError("", error.Description);

        return View(model);
    }

    [HttpPost]
    public async Task<IActionResult> CerrarSesion()
    {
        await _signInManager.SignOutAsync();
        return RedirectToAction("Index", "Tienda");
    }
}
