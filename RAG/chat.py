
from fastapi import FastAPI, Request
import time
from fastapi import Response
from rag.retriever import get_response

app = FastAPI()


@app.get("/v1/models")
async def list_models():
    """
    Mocks the OpenAI API endpoint for listing available models.
    """
    response = {
        "object": "list",
        "data": [
          {
            "id": "brayan",
            "object": "model",
            "created": 1754014226,
            "owned_by": "library"
          }
        ]
      }

    return response


@app.options("/v1/models")
async def list_models_2():
  """
  Mocks the OpenAI API endpoint for listing available models.
  """
  return Response(status_code=204)



@app.get("/api/version")
async def list_models_2():
  """
  Mocks the OpenAI API endpoint for listing available models.
  """
  response = {
	"version": "0.10.1"
    }
  return response

@app.get("/api/ps")
async def list_models_2():
  """
  Mocks the OpenAI API endpoint for listing available models.
  """
  response = {
      "models": []
    }
  return response


@app.get("/api/tags")
async def list_models_2():
  """
  Mocks the OpenAI API endpoint for listing available models.
  """
  response = {
	"models": [
		{
			"name": "brayan_local:latest",
			"model": "brayan_local:latest",
			"modified_at": "2025-07-31T21:10:26.862356844-05:00",
			"size": 4372824384,
			"digest": "6577803aa9a036369e481d648a2baebb381ebc6e897f2bb9a766a2aa7bfbc1cf",
			"details": {
				"parent_model": "",
				"format": "gguf",
				"family": "llama",
				"families": [
					"llama"
				],
				"parameter_size": "7.2B",
				"quantization_level": "Q4_K_M"
			}
		}
	]
}
  return response

@app.post("/api/chat")
async def chat_endpoint(request: Request):
  """
  Mocks the OpenAI API endpoint for chat and prints the request body.
  """
  body = await request.json()
  print("Received request body:", body)
  answer = get_response(body["messages"][-1])


  response = {
    "message": {
      "role": "assistant",
      "content": str(answer)
    },

  }

  print("este es el response:", response)
  return response

