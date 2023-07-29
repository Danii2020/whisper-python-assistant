from modules.templates.templates import (
    productivity_role_template,
    translate_role_template,
    summary_role_template
)

roles_templates = [
    {
        "name": "productivity",
        "description": "Excelente para responder cualquier pregunta de la mejor manera posible",
        "prompt_template": productivity_role_template,
        "input_variables": "input"
    },
    {
        "name": "translator",
        "description": "Excelente para traducir textos del inglés al español",
        "prompt_template": translate_role_template,
        "input_variables": "output"
    },
    {
    "name": "summary",
    "description": "Excelente para resumir cualquier texto por mas complejo que sea",
    "prompt_template": summary_role_template,
    "input_variables": "output"
    }
]