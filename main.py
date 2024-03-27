import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

client = OpenAI(
    api_key = os.environ['OPENAI_API_KEY']
)

messages = []

def get_llm_response(messages):
  response = client.chat.completions.create(
    model = 'gpt-4-turbo-preview',
    messages = messages,
    temperature = 1.0
  )
  content = response.choices[0].message.content
  return content

app = FastAPI()
# TODO: デプロイ時にCORSの範囲を設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 全てのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],  # 全てのHTTPメソッドを許可
    allow_headers=["*"],  # 全てのHTTPヘッダを許可
)

@app.get("/topic")
async def topic_gen():
    template = '''
    今日の話題を10文字程度で提案してください
    〇〇についてどう思いますか？
    みたいな感じでお願いします！
    '''
    messages = [{'role': 'user', 'content': template}]
    llm_response = get_llm_response(messages)
    print('llm_response', llm_response)

    return [{"name": llm_response, "color": "ffffff"}]
