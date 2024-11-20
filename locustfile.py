from locust import HttpUser, task, between
import random

class QuizTestUser(HttpUser):
    wait_time = between(1, 5)  # Tiempo entre solicitudes (1-5 segundos)

    @task
    def submit_quiz(self):
        # Datos aleatorios para simular respuestas
        user_name = f"TestUser{random.randint(1, 100)}"
        age = random.randint(18, 60)
        career_profession = random.choice(["Ingeniero", "Estudiante", "Médico"])

        # Respuestas ficticias a las preguntas
        data = {
            "user_name": user_name,
            "age": age,
            "career_profession": career_profession,
            "question_1": "Esto es una respuesta para renos.",
            "question_2": "Esto es una respuesta para uvas.",
            "question_3": "Esto es una respuesta para plátano.",
        }

        # Enviar la solicitud POST
        self.client.post("/quiz/test", data=data)
