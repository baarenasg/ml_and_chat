# Microservicio RAG con Arquitectura Limpia

Este proyecto implementa un microservicio de **Generación Aumentada por Recuperación (RAG)** utilizando FastAPI y siguiendo principios de Arquitectura Limpia para mantener el código organizado, escalable y fácil de mantener.

## Descripción General

El microservicio está diseñado para:
1.  Recibir una pregunta o consulta a través de un endpoint de API.
2.  Utilizar un modelo de embeddings para convertir la consulta en un vector.
3.  Buscar en una base de datos vectorial (PostgreSQL con pgvector) los documentos o "chunks" de información más relevantes para la consulta.
4.  Enviar el contexto recuperado junto con la pregunta original a un Modelo de Lenguaje Grande (LLM) de OpenAI.
5.  Devolver la respuesta generada por el LLM al usuario.

---

## Arquitectura y Componentes

El proyecto está dividido en tres capas principales, inspiradas en la Arquitectura Limpia:

### 1. `src/domain`
Esta capa contiene la lógica de negocio y las entidades principales. No depende de ninguna otra capa.
-   **`model`**: Define los modelos de datos y las interfaces (Gateways) que dictan cómo la lógica de negocio interactuará con el mundo exterior (ej. `LLMRepository`, `VectorDBRepository`).
-   **`usecases`**: Contiene los casos de uso que orquestan el flujo de la lógica de negocio. Por ejemplo, `GenerateAnswerUseCase` coordina la recuperación de información y la generación de la respuesta.

### 2. `src/infrastructure`
Esta capa contiene las implementaciones concretas de las interfaces definidas en el dominio. Es el puente entre la lógica de negocio y las herramientas externas.
-   **`driven_adapters`**: Implementaciones de los gateways.
    -   `openia_adapter`: Adaptador para interactuar con la API de OpenAI.
    -   `pgvector_adapter`: Adaptador para conectarse y realizar búsquedas en la base de datos PostgreSQL/pgvector.
-   **`entry_points`**: Puntos de entrada a la aplicación.
    -   `fast_api`: Contiene la configuración de FastAPI, las rutas (`rag_router.py`), los manejadores de peticiones (`rag_handler.py`) y la configuración de la aplicación (`application.py`).
-   **`helpers`**: Utilidades y funciones auxiliares.

### 3. `src/applications`
Esta capa conecta todo. Se encarga de la configuración, la inyección de dependencias y el arranque de la aplicación.
-   **`app_service`**: Punto de entrada que inicializa la aplicación FastAPI.
-   **`config`**: Manejo de la configuración y variables de entorno a través de Pydantic. Aquí se encuentra el archivo `.env.local`.
-   **`settings`**: Clases de Pydantic para validar y gestionar las variables de entorno.
-   **`di_container`**: Contenedor de inyección de dependencias que construye y provee las instancias de los adaptadores y casos de uso.

---

## Guía de Instalación y Puesta en Marcha

### Requisitos Previos
-   Python 3.11 o superior.
-   Docker y Docker Compose.
-   Una cuenta de OpenAI y una API Key.

### 1. Clonar el Repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd ml_and_chat/RAG
```

### 2. Configurar el Entorno Virtual
Se recomienda utilizar un entorno virtual para gestionar las dependencias.
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
Crea un archivo `.env.local` dentro de `src/applications/config/` a partir del ejemplo.

```bash
# src/applications/config/.env.local

# Configuración de la Base de Datos
Crear la siguiente variable de ambientes para la conexión con la base de datos: 

PG_CONNECTION_STRING = "postgresql://postgres-user:postgres-pass@localhost:5432"
# Configuración de OpenAI
OPENAI_API_KEY="sk-..."
```

### 5. Iniciar la Base de Datos con Docker
Para levantar una instancia de PostgreSQL con la extensión `pgvector`, puedes usar el siguiente comaando para levanta la base de datos: 


sudo service docker start
docker rm -f postgres-qs || true
docker run --name postgres-qs -e POSTGRES_USER=postgres-user -e POSTGRES_PASSWORD=postgres-pass -p 5432:5432 -d 


### 6. Ejecutar el Microservicio
Utiliza el script `local_run.py` para iniciar la aplicación con Uvicorn.
```bash
python local_run.py
```
El servidor estará disponible en `http://0.0.0.0:8000`.

---

## Uso de la API


### Ejemplo de Petición al Endpoint de Chat
Puedes usar `curl` para probar el endpoint `/api/chat`:
```bash
curl --request POST \
  --url http://localhost:8000/api/chat \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/11.3.0' \
  --data '{
    "model": "gpt-4.1-nano",
    "messages": [
        {
            "role": "user",
            "content": "Pelicula parecida a titanic"
        }
    ],
    "stream": false
}'
```

---



**Respuesta (Response):**

```json
{
  "message": {
    "role": "assistant",
    "content": "Los Goonies es una película de aventuras sobre un grupo de amigos que descubren un antiguo mapa del tesoro y se embarcan en una búsqueda para salvar sus hogares de ser embargados."
  }
}
```

## Ejecutar los Tests
Para ejecutar las pruebas unitarias y de integración, utiliza `pytest`:
```bash
pytest
```
-   `rag/retriever.py`: Contiene la lógica central del sistema RAG. Es responsable de:
    -   Conectarse a la base de datos vectorial (PGVector).
    -   Recuperar los documentos o "nodos" más relevantes para una consulta específica.
    -   Interactuar con el LLM de OpenAI para generar una respuesta basada en el contexto recuperado.
-   `requirements.txt`: Define todas las dependencias de Python necesarias para que el proyecto funcione correctamente.
-   `gen_load_embeddings/`: Incluye scripts para procesar datos y cargarlos como embeddings en la base de datos vectorial.
-   `tests/`: Contiene las pruebas unitarias para verificar el correcto funcionamiento de los endpoints y la lógica de negocio.

# .env
OPENAI_API_KEY="tu_api_key_de_openai"
PG_CONNECTION_STRING="postgresql://postgres-user:postgres-pass@localhost:5432/vector_bd_movies"
```

**Nota:** Asegúrate de que la base de datos `vector_bd_movies` exista en tu instancia de PostgreSQL.

### 5. Levantar la Base de Datos (Opcional)

Si no tienes una instancia de PostgreSQL, puedes usar Docker para levantar una. Asegúrate de tener un archivo `docker-compose.yml` configurado para el servicio de base de datos.

```bash
docker-compose up -d
```

### 6. Cargar los Embeddings (si es necesario)

Antes de poder hacer consultas, necesitas poblar tu base de datos. Utiliza el script proporcionado para generar y cargar los embeddings.

```bash
# (Ejecuta el script correspondiente desde gen_load_embeddings/)
python gen_load_embedings.py
```

