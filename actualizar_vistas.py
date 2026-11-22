with open("Supermercado.Web/Views/Shared/_Layout.cshtml", "r", encoding="utf-8") as f:
    layout = f.read()
layout = layout.replace("Catálogo (210 Productos)", "Catálogo de Productos")
with open("Supermercado.Web/Views/Shared/_Layout.cshtml", "w", encoding="utf-8") as f:
    f.write(layout)

with open("Supermercado.Web/Views/Tienda/Index.cshtml", "r", encoding="utf-8") as f:
    idx = f.read()

diccionario_viejo = '''    var iconosCategoria = new Dictionary<string, string>
    {
        { "Salsas y Condimentos", "🍅" },
        { "Pastas y Granos", "🍝" },
        { "Lácteos y Huevos", "🥛" },
        { "Carnes y Embutidos", "🍗" },
        { "Panadería y Bebidas", "🧃" },
        { "Snacks y Dulces", "🍫" }
    };'''

diccionario_nuevo = '''    var iconosCategoria = new Dictionary<string, string>
    {
        { "Salsas y Condimentos", "🍅" },
        { "Pastas y Granos", "🍝" },
        { "Harinas y Panadería", "🌾" },
        { "Lácteos y Huevos", "🥛" },
        { "Carnes y Embutidos", "🥩" },
        { "Verduras y Hortalizas", "🥦" },
        { "Frutas Frescas", "🍎" },
        { "Bebidas y Jugos", "🧃" },
        { "Confitería y Snacks", "🍫" }
    };'''

idx = idx.replace(diccionario_viejo, diccionario_nuevo)
with open("Supermercado.Web/Views/Tienda/Index.cshtml", "w", encoding="utf-8") as f:
    f.write(idx)
