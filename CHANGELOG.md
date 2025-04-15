# Changelog

Todas las modificaciones importantes de este proyecto se documentarán en este archivo.

---
## [v1.0-day6] - 2025-04-14 (part1) & 2025-04-15 (part2)

### Agregado
- CI/CD:
    Configuracion GitHub Actions para ejecutar pruebas unitarias e integración.
    Se incluyo análisis de código estático (SonarQube/SonarCloud) y pruebas de integración para la API de FastAPI.
- Pruebas de integración:
    Se implemento pruebas de integración utilizando httpx y TestClient de FastAPI.
- Documentación del pipeline:
- Se creo el archivo de workflow (.github/workflows/ci.yml).

## [v1.0-day5] - 2025-04-13

### Agregado
- Interfaz de consola:
    Se refino la presentación de preguntas y respuestas en la consola.
    Se agrego mensajes de bienvenida y resumen final detallado.
- Características adicionales:
    Se incorporo niveles de dificultad (por ejemplo, ajustar la selección de preguntas según el rendimiento).
---

## [v1.0-day4] - 2025-04-12

### Agregado
- Ampliar la clase Quiz:
    Agregue atributos para puntaje: correct_answers y incorrect_answers.
    Implemente el método answer_question para actualizar la puntuación.
- Manejo de rondas:
    Defini la lógica para las 10 rondas y la terminación del juego.
- Pruebas unitarias:
    Agregue test_quiz para validar el sistema de puntuación.
---

## [v1.0-day3] - 2025-04-11

### Agregado
- Clase Quiz:
    Desarrollo de la clase Quiz para manejar el flujo del juego (agregando preguntas y obteniendo la siguiente).
- Integración básica:
    Creacion de la clase manager_trivia para conectar la lógica de Question y Quiz para permitir la presentación de preguntas.
    Creacion de la clase consoleUI para manejar la consola mediante la cual interactuara el usuario con el juego.
---

## [v1.0-day2] - 2025-04-10

### Agregado
- Clase Question:
    Implementacion de la clase Question en Python para gestionar preguntas y respuestas.
- Pruebas unitarias:
    Configuracion de pytest e implementacion pruebas básicas para validar la funcionalidad de is_correct.

---
## [v1.0-day1] - 2025-04-09

### Agregado
- Configuración del proyecto:
    Creacion de la carpeta del proyecto y configurar el entorno virtual.
    Instalacion de FastAPI, Uvicorn, asyncpg, databases y otras dependencias.
- Docker y Docker Compose:
    Creacion del Dockerfile para la aplicación.
    Configuracion del archivo docker-compose.yml para levantar PostgreSQL y el servicio web.
---
### Cambiado
N/A

### Corregido
N/A

### Eliminado
N/A