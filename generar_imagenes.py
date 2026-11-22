import os

os.makedirs("Supermercado.Web/wwwroot/images/productos", exist_ok=True)

colores_marca = {
    "Fruco": ("#d32f2f", "#fbc02d", "#ffffff"),
    "Heinz": ("#b71c1c", "#ffffff", "#ffd54f"),
    "San Jorge": ("#c62828", "#ff8f00", "#ffffff"),
    "Bary": ("#2e7d32", "#fbc02d", "#ffffff"),
    "Constancia": ("#e65100", "#fff59d", "#ffffff"),
    "Aderezos": ("#558b2f", "#dce775", "#ffffff"),
    "Diana": ("#1565c0", "#ffca28", "#ffffff"),
    "Roa": ("#2e7d32", "#ffeb3b", "#ffffff"),
    "Florhuila": ("#00695c", "#ffd54f", "#ffffff"),
    "Castellano": ("#ad1457", "#f8bbd0", "#ffffff"),
    "Caribe": ("#0277bd", "#81d4fa", "#ffffff"),
    "Sonora": ("#ef6c00", "#ffe082", "#ffffff"),
    "Doria": ("#0d47a1", "#ffeb3b", "#ffffff"),
    "La Muñeca": ("#c62828", "#ffcdd2", "#ffffff"),
    "Conzazoni": ("#1b5e20", "#a5d6a7", "#ffffff"),
    "Monticello": ("#212121", "#d4af37", "#ffffff"),
    "Barilla": ("#1a237e", "#ef5350", "#ffffff"),
    "Roma": ("#bf360c", "#ffccbc", "#ffffff"),
    "Alpina": ("#0277bd", "#e1f5fe", "#ffffff"),
    "Colanta": ("#1b5e20", "#c8e6c9", "#ffffff"),
    "Alquería": ("#c62828", "#ffffff", "#ffcdd2"),
    "Parmalat": ("#1565c0", "#bbdefb", "#ffffff"),
    "Pomar": ("#2e7d32", "#fff9c4", "#ffffff"),
    "Freskaleche": ("#00838f", "#b2ebf2", "#ffffff"),
    "Zenú": ("#b71c1c", "#ffca28", "#ffffff"),
    "Pietrán": ("#2e7d32", "#a5d6a7", "#ffffff"),
    "Ranchera": ("#4e342e", "#ffab91", "#ffffff"),
    "Mac Pollo": ("#d84315", "#ffe0b2", "#ffffff"),
    "Bucanero": ("#c62828", "#fff59d", "#ffffff"),
    "Juan Valdez": ("#4e342e", "#d7ccc8", "#ffffff"),
    "Sello Rojo": ("#b71c1c", "#ffcdd2", "#ffffff"),
    "Águila Roja": ("#d32f2f", "#ffeb3b", "#ffffff"),
    "Bimbo": ("#1565c0", "#ef5350", "#ffffff"),
    "Del Valle": ("#ef6c00", "#c8e6c9", "#ffffff"),
    "La Cosecha": ("#2e7d32", "#f57c00", "#ffffff")
}

iconos_cat = {
    "Pastas y Granos": "🍝",
    "Salsas y Condimentos": "🍅",
    "Frutas y Verduras": "🥑",
    "Lácteos y Huevos": "🥛",
    "Carnes y Pollo": "🍗",
    "Panadería y Bebidas": "🧃"
}

productos_base = [
    ("Pasta Espagueti 500g", "Pastas y Granos", ["Doria", "La Muñeca", "Conzazoni", "Monticello", "Barilla", "Roma", "La Cosecha"]),
    ("Pasta Tornillos Tricolor 500g", "Pastas y Granos", ["Doria", "La Muñeca", "Conzazoni", "Monticello", "Barilla", "Roma", "La Cosecha"]),
    ("Arroz Blanco Premium 1kg", "Pastas y Granos", ["Diana", "Roa", "Florhuila", "Castellano", "Caribe", "Sonora", "La Cosecha"]),
    ("Frijol Bola Roja 500g", "Pastas y Granos", ["Diana", "Del Costal", "La Cosecha", "El Trece", "Aburrá", "Campo Verde", "Supremo"]),
    ("Lenteja Pardina 500g", "Pastas y Granos", ["Diana", "Del Costal", "La Cosecha", "El Trece", "Aburrá", "Campo Verde", "Supremo"]),
    ("Salsa de Tomate 400g", "Salsas y Condimentos", ["Fruco", "Heinz", "San Jorge", "Bary", "Constancia", "Aderezos", "La Cosecha"]),
    ("Mayonesa Tradicional 380g", "Salsas y Condimentos", ["Fruco", "Hellmann's", "San Jorge", "Bary", "Constancia", "Aderezos", "La Cosecha"]),
    ("Salsa Napolitana 350g", "Salsas y Condimentos", ["Fruco", "Monticello", "Barilla", "San Jorge", "Bary", "Aderezos", "La Cosecha"]),
    ("Aceite de Oliva 500ml", "Salsas y Condimentos", ["Carbonell", "Borges", "Ybarra", "Olivetto", "Gourmet", "Premier", "La Cosecha"]),
    ("Salsa BBQ Ahumada 350g", "Salsas y Condimentos", ["Fruco", "Heinz", "San Jorge", "Bary", "Aderezos", "Zafrán", "La Cosecha"]),
    ("Aguacate Hass x2", "Frutas y Verduras", ["Finca Verde", "Huerta Real", "Campo Fresco", "Tierra Viva", "Valle Verde", "Orgánico", "La Cosecha"]),
    ("Tomate Chonto Fresco 1kg", "Frutas y Verduras", ["Finca Verde", "Huerta Real", "Campo Fresco", "Tierra Viva", "Valle Verde", "Orgánico", "La Cosecha"]),
    ("Manzana Roja x4", "Frutas y Verduras", ["Royal Gala", "Red Delicious", "Fuji", "Pink Lady", "Campo Fresco", "Valle Verde", "La Cosecha"]),
    ("Banano Criollo 1kg", "Frutas y Verduras", ["Urabá", "Campo Fresco", "Finca Verde", "Tierra Viva", "Valle Verde", "Orgánico", "La Cosecha"]),
    ("Fresa Seleccionada 500g", "Frutas y Verduras", ["Sabana", "Huerta Real", "Campo Fresco", "Tierra Viva", "Valle Verde", "Orgánico", "La Cosecha"]),
    ("Leche Entera 1L", "Lácteos y Huevos", ["Alpina", "Colanta", "Alquería", "Parmalat", "Pomar", "Freskaleche", "La Cosecha"]),
    ("Huevos Campesinos x30", "Lácteos y Huevos", ["Kikes", "Santa Reyes", "Oro", "Avinal", "Granja Real", "Campo", "La Cosecha"]),
    ("Queso Campesino 500g", "Lácteos y Huevos", ["Alpina", "Colanta", "Del Vecchio", "Alquería", "Pomar", "San Simón", "La Cosecha"]),
    ("Yogurt Griego 150g", "Lácteos y Huevos", ["Alpina", "Colanta", "Finesse", "Alquería", "Danone", "Yogo", "La Cosecha"]),
    ("Mantequilla con Sal 250g", "Lácteos y Huevos", ["Alpina", "Colanta", "Rama", "La Fina", "Campi", "Alquería", "La Cosecha"]),
    ("Pechuga de Pollo 1kg", "Carnes y Pollo", ["Mac Pollo", "Bucanero", "Friko", "Pimpollo", "Avidesa", "Campo", "La Cosecha"]),
    ("Carne Molida Res 500g", "Carnes y Pollo", ["Zenú", "Pietrán", "Ranchera", "Colanta", "Frigocarne", "Premier", "La Cosecha"]),
    ("Salchicha Tradicional x10", "Carnes y Pollo", ["Zenú", "Ranchera", "Pietrán", "Rica", "Suizo", "Koller", "La Cosecha"]),
    ("Jamón Ahumado 250g", "Carnes y Pollo", ["Zenú", "Pietrán", "Rica", "Suizo", "Koller", "Colanta", "La Cosecha"]),
    ("Filete de Salmón 400g", "Carnes y Pollo", ["Antillana", "Ancla y Viento", "Mar y Río", "Pacífico", "Gourmet", "Ocean", "La Cosecha"]),
    ("Pan Integral Tajado", "Panadería y Bebidas", ["Bimbo", "Comapan", "Ramo", "Santa Clara", "Artesano", "Vital", "La Cosecha"]),
    ("Jugo Natural Naranja 1L", "Panadería y Bebidas", ["Del Valle", "Hit", "California", "Alpina", "Country Hill", "Tampico", "La Cosecha"]),
    ("Café Tostado Molido 500g", "Panadería y Bebidas", ["Juan Valdez", "Sello Rojo", "Águila Roja", "Colcafé", "Oma", "Matiz", "La Cosecha"]),
    ("Galletas Integrales Miel", "Panadería y Bebidas", ["Noel", "Tosh", "Festival", "Saltín", "Ducales", "Ramo", "La Cosecha"]),
    ("Té Helado Durazno 1.5L", "Panadería y Bebidas", ["Mr. Tea", "Fuze Tea", "Lipton", "Hatsu", "Nestea", "Postobón", "La Cosecha"])
]

pid = 1
for nombre, cat, marcas in productos_base:
    for idx, marca in enumerate(marcas):
        c1, c2, c3 = colores_marca.get(marca, ("#2e7d32", "#ffb300", "#ffffff"))
        icono = iconos_cat.get(cat, "🛒")
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="320" viewBox="0 0 500 320">
  <defs>
    <linearGradient id="bg{pid}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>
  </defs>
  <rect width="500" height="320" fill="url(#bg{pid})"/>
  <circle cx="430" cy="60" r="95" fill="#ffffff" fill-opacity="0.12"/>
  <circle cx="70" cy="280" r="110" fill="#000000" fill-opacity="0.10"/>
  <rect x="135" y="28" width="230" height="264" rx="26" fill="#ffffff" fill-opacity="0.96"/>
  <rect x="135" y="28" width="230" height="62" rx="22" fill="{c1}"/>
  <text x="250" y="67" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="{c3}" text-anchor="middle">{marca.upper()}</text>
  <text x="250" y="165" font-size="74" text-anchor="middle">{icono}</text>
  <text x="250" y="222" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#212121" text-anchor="middle">{nombre}</text>
  <rect x="180" y="242" width="140" height="28" rx="14" fill="{c2}"/>
  <text x="250" y="261" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#111111" text-anchor="middle">Market Express</text>
</svg>'''
        with open(f"Supermercado.Web/wwwroot/images/productos/prod_{pid}.svg", "w", encoding="utf-8") as f:
            f.write(svg)
        pid += 1
print(f"Generadas {pid - 1} imágenes únicas por marca.")
