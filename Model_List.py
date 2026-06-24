from mistralai.client import Mistral

client = Mistral(api_key="")

models = client.models.list()

print(models)