from openai import OpenAI

client = OpenAI(
    api_key="sk-fae5081ef05545ef8f24fa650dff26d6",
    base_url="https://ki-toolbox.scc.kit.edu/api/v1"
)

models = client.models.list()
for model in models:
    print(model.id)
