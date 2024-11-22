import json
import os

from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = AsyncGroq(api_key=api_key)


async def send_message(message):
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """
            Você é um assistente desenhado para avaliar e classificar pedidos de oração.
            Os pedidos de oração serão postados no twitter, então é preciso que as regras da plataforma sejam respeitadas. 
            Não permita nenhum compartilhamento de dados pessoais, links, ou conteúdo que seja ofensivo.
            
            Seu objetivo é determinar se uma mensagem é:

            1. Um pedido válido de oração
            2. Não é um pedido de oração (e.g., perguntas, comentários não relacionados)
            3. Um pedido de oração com conteúdo sensível (violência, discriminação, etc)
            4. Uma piada ou meme, ou algo banal, sem objetivo de ser levado a sério.

            Quando avaliando uma mensagem:

            - Preste atenção em uma linguagem que sugira humor, sarcasmo ou exagero.
            - Considere coisas culturais ou linguísticas do Brasil que possam indicar uma piada.
            - Se inserto, priorize a cautela e classifique como uma piada.

            A resposta, deve ser um JSON, no seguinte formato:

            {
                "isPrayerRequest": boolean,
                "isSensitive": boolean,
                "reason": string
            }

            A chave isSensitive deve ser true se o conteúdo parte do 3 ou 4. A chave reason, deve conter uma explicação para o motivo da classificação.

            Retorne somente o JSON, e nenhuma mensagem adicional. 
            """,
            },
            {"role": "user", "content": message},
        ],
        model="llama3-8b-8192",
        temperature=0,
        max_tokens=1024,
    )

    response = chat_completion.choices[0].message.content

    return json.loads(response)


