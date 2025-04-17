from locust import HttpUser, task, between
import json
import random

class TriviaUser(HttpUser):
    """
    Clase que simula un usuario jugando al juego de trivia.
    Realiza el flujo completo: iniciar juego, obtener preguntas, responder y ver puntuación.
    """
    # Tiempo de espera entre tareas (simulando tiempo de lectura/pensamiento del usuario)
    wait_time = between(1, 5)
    
    def on_start(self):
        """
        Método que se ejecuta cuando un usuario comienza la simulación.
        Inicia un juego nuevo y almacena el ID.
        """
        self.quiz_id = None
        self.current_question = None
        self.questions_answered = 0
        self.max_questions = 10  # Máximo de preguntas por juego
        
        # Iniciar un juego nuevo
        with self.client.get("/start-game", catch_response=True) as response:
            if response.status_code == 200:
                response_data = response.json()
                if "quiz_id" in response_data:
                    self.quiz_id = response_data["quiz_id"]
                    self.client.get("/")  # Visitar página principal después de iniciar
            else:
                response.failure(f"No se pudo iniciar un juego nuevo: {response.status_code}")
    
    @task(3)  # Peso 3: esta tarea se ejecuta con más frecuencia
    def get_next_question(self):
        """
        Obtiene la siguiente pregunta del juego actual.
        """
        if not self.quiz_id or self.questions_answered >= self.max_questions:
            # Si no hay juego activo o ya se respondieron todas las preguntas, iniciar nuevo juego
            with self.client.get("/start-game", catch_response=True) as response:
                if response.status_code == 200:
                    response_data = response.json()
                    if "quiz_id" in response_data:
                        self.quiz_id = response_data["quiz_id"]
                        self.questions_answered = 0
                else:
                    response.failure(f"No se pudo iniciar un juego nuevo: {response.status_code}")
            return
        
        # Obtener la siguiente pregunta
        with self.client.get(f"/game/{self.quiz_id}/next-question", catch_response=True) as response:
            if response.status_code == 200:
                response_data = response.json()
                if "message" in response_data and "No hay más preguntas" in response_data["message"]:
                    # No hay más preguntas, reiniciar
                    self.quiz_id = None
                    return
                
                if "options" in response_data:
                    self.current_question = response_data
            else:
                response.failure(f"Error al obtener la siguiente pregunta: {response.status_code}")
    
    @task(4)  # Peso 4: responder preguntas es la tarea más frecuente
    def answer_question(self):
        """
        Responde a la pregunta actual con una respuesta aleatoria.
        """
        if not self.quiz_id or not self.current_question:
            return
        
        # Simular al usuario seleccionando una respuesta (aleatoria)
        if "options" in self.current_question and self.current_question["options"]:
            options = self.current_question["options"]
            selected_answer = random.choice(options)
            
            # Extraer el ID de la pregunta del path o usar un valor simulado
            question_id = 1  # Esto debería obtenerse de la respuesta real, simplificado para el ejemplo
            
            # Enviar la respuesta
            payload = {
                "question_id": question_id,
                "answer": selected_answer
            }
            
            with self.client.post(
                f"/game/{self.quiz_id}/answer", 
                json=payload,
                catch_response=True
            ) as response:
                if response.status_code == 200:
                    self.questions_answered += 1
                    # Eliminar la pregunta actual para forzar obtener una nueva
                    self.current_question = None
                else:
                    response.failure(f"Error al responder pregunta: {response.status_code}")
    
    @task(1)  # Peso 1: consultar puntuación menos frecuentemente
    def get_score(self):
        """
        Consulta la puntuación actual del juego.
        """
        if not self.quiz_id:
            return
        
        with self.client.get(f"/game/{self.quiz_id}/score", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Error al obtener puntuación: {response.status_code}")
    
    @task(1)  # Peso 1: algunas veces el usuario simplemente visita la página principal
    def visit_homepage(self):
        """
        Visita la página principal de la aplicación.
        """
        with self.client.get("/", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Error al visitar página principal: {response.status_code}")


class CasualTriviaUser(TriviaUser):
    """
    Usuario casual que juega con menos frecuencia y espera más tiempo entre acciones.
    """
    wait_time = between(3, 10)  # Espera más tiempo entre tareas


class PowerTriviaUser(TriviaUser):
    """
    Usuario avanzado que juega rápidamente y con más frecuencia.
    """
    wait_time = between(0.5, 2)  # Espera menos tiempo entre tareas