import os
from openai import AzureOpenAI

client = AzureOpenAI(
  api_key = "xxx",  
  api_version = "2023-05-15",
  azure_endpoint = "https://xxxxxx.openai.azure.com/"
)

response = client.chat.completions.create(
    model="gpt-35-turbo-16k", # model = "deployment_name".
    messages=[
        # {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
        # {"role": "user", "content": "Who were the founders of Microsoft?"}
        {"role": "system", "content": "日本語で会話してください"},
        {"role": "user", "content": "代休について教えて"}
    ]
)

#print(response)
print(response.model_dump_json(indent=2))
print(response.choices[0].message.content)