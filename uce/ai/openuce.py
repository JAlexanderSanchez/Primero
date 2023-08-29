import openai
from pydantic import BaseModel

openai.organization = 'org-vgmFNY6C1ojYlplUUiJYB0vi'
openai.api_key = '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'

class Document(BaseModel):
    item: str = 'pizza'

def process_inference(user_prompt) -> str:
    print('[PROCESANDO]'.center(40, '-'))
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """Eres un chef que lista los ingredientes de los platillos que se te proporcionan.
        E.G
        pan
        Ingredientes:
        harina
        huevos
        agua
        azucar
        ...
        """},
            {"role": "user", "content": user_prompt}
        ]
    )

    response = completion.choices[0].message.content
    total_tokens: completion[0].usage.total_tokens

    return [response, total_tokens]