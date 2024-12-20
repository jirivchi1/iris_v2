import openai
import base64
from dotenv import load_dotenv
import os

load_dotenv()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_openai_response(question, image_path):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    base64_image = encode_image(image_path)

    # Combinar la pregunta con la instrucción adicional
    combined_question = f"{question} Responde en Máximo 10 palabras."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": combined_question},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        max_tokens=50,
    )
    return response.choices[0].message.content


def generate_solution_description(image_path):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    base64_image = encode_image(image_path)

    fixed_prompt = "Eres un sistema experto en describir imágenes. Normalmente son cantidades de cosas. Di números. ¡Sé directo y describe lo que ves en la imagen como máximo 5 palabras!"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": fixed_prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        max_tokens=50,
    )
    return response.choices[0].message.content
