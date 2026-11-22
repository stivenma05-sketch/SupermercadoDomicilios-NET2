using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Supermercado.Core.Data;
using Supermercado.Web.Data;

var builder = WebApplication.CreateBuilder(args);
var rootPath = Path.GetFullPath(Path.Combine(builder.Environment.ContentRootPath, ".."));
var authConn = $"Data Source={Path.Combine(rootPath, "identity.db")}";
var negConn = $"Data Source={Path.Combine(rootPath, "supermercado.db")}";

builder.Services.AddDbContext<ApplicationDbContext>(options => options.UseSqlite(authConn));
builder.Services.AddDbContext<SupermercadoDbContext>(options => options.UseSqlite(negConn));
builder.Services.AddDatabaseDeveloperPageExceptionFilter();

builder.Services.AddDefaultIdentity<IdentityUser>(options => {
        options.SignIn.RequireConfirmedAccount = false;
        options.Password.RequireNonAlphanumeric = false;
        options.Password.RequireUppercase = false;
    })
    .AddRoles<IdentityRole>()
    .AddEntityFrameworkStores<ApplicationDbContext>();

builder.Services.ConfigureApplicationCookie(options =>
{
    options.LoginPath = "/Cuenta/Login";
    options.AccessDeniedPath = "/Cuenta/Login";
});

builder.Services.AddDistributedMemoryCache();
builder.Services.AddSession(options =>
{
    options.IdleTimeout = TimeSpan.FromMinutes(60);
    options.Cookie.HttpOnly = true;
    options.Cookie.IsEssential = true;
});

builder.Services.AddControllersWithViews();
var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
    var services = scope.ServiceProvider;
    services.GetRequiredService<ApplicationDbContext>().Database.EnsureCreated();
    services.GetRequiredService<SupermercadoDbContext>().Database.EnsureCreated();

    var roleManager = services.GetRequiredService<RoleManager<IdentityRole>>();
    var userManager = services.GetRequiredService<UserManager<IdentityUser>>();

    foreach (var rol in new[] { "Admin", "Cliente" })
        if (!await roleManager.RoleExistsAsync(rol)) await roleManager.CreateAsync(new IdentityRole(rol));

    if (await userManager.FindByEmailAsync("dueno@lacosecha.com") == null)
    {
        var admin = new IdentityUser { UserName = "dueno@lacosecha.com", Email = "dueno@lacosecha.com", PhoneNumber = "573001112233", EmailConfirmed = true };
        await userManager.CreateAsync(admin, "Admin123!");
        await userManager.AddToRoleAsync(admin, "Admin");
        await userManager.AddClaimAsync(admin, new System.Security.Claims.Claim("NombreCompleto", "Administrador La Cosecha"));
    }

    if (await userManager.FindByEmailAsync("cliente@lacosecha.com") == null)
    {
        var cliente = new IdentityUser { UserName = "cliente@lacosecha.com", Email = "cliente@lacosecha.com", PhoneNumber = "573114445566", EmailConfirmed = true };
        await userManager.CreateAsync(cliente, "Cliente123!");
        await userManager.AddToRoleAsync(cliente, "Cliente");
        await userManager.AddClaimAsync(cliente, new System.Security.Claims.Claim("NombreCompleto", "Andrea Cliente"));
        await userManager.AddClaimAsync(cliente, new System.Security.Claims.Claim("TelefonoLlamada", "3114445566"));
        await userManager.AddClaimAsync(cliente, new System.Security.Claims.Claim("Direccion", "Calle 30 # 25-14, Palmira"));
    }
}

if (!app.Environment.IsDevelopment()) { app.UseExceptionHandler("/Home/Error"); app.UseHsts(); }
app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseSession();
app.UseAuthentication();
app.UseAuthorization();

app.MapControllerRoute(name: "default", pattern: "{controller=Tienda}/{action=Bienvenida}/{id?}");
app.MapRazorPages();
app.Run();
