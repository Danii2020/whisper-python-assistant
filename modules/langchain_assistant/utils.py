from langchain.prompts import PromptTemplate

def create_prompt_template(role_template, format_instructions=None):
    prompt = role_template.get("prompt_template", "")
    format_response = {
        "format_instructions": format_instructions
    } if role_template.get("name") == "summary" else {}
    return PromptTemplate(
        template=prompt,
        input_variables=[role_template.get("input_variables", "")],
        partial_variables=format_response
    )

def check_format(response):
    if not 'json' in response:
        response = f"""
        ```json\n
        {response}
        ```
        """
    return response