from ollama_python.endpoints import GenerateAPI

api = GenerateAPI(base_url="http://localhost:8000", model="mistral")
result = api.generate(prompt="Hello World", options=dict(num_tokens=10), format="json")