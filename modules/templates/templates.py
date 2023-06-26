summary_role_template = """Eres alguien que es capaz de resumir \
cualquier tipo de texto por mas complejo que este sea.\
Resume el siguiente texto en PUNTOS CLAVE que consideres importante, \
recuerda incluir saltos de linea en cada punto y hazlo de la mejor manera \
posible y SOLO TRADUCE el texto al ESPAÑOL.

Aqui tienes el texto:
{output}

Regresa tu respuesta en un formato JSON con dos \
claves, "title" y "content" siendo "title" el nombre del input que \
recibiste y "content" el resumen que generaste con los puntos clave
traducidos al español.

Toma el siguiente ejemplo de formato:
{format_instructions}
"""