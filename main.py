from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from openai import OpenAI

# OpenAI API key
client = OpenAI(api_key="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")

app = FastAPI()

# static papka
STATIC_DIR = Path("static")
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML sahifa
@app.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# AI javob olish
def get_ai_reply(user_message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # tejamkor va tez
        messages=[
            {"role": "system", "content": "Siz foydalanuvchiga yordam beradigan o‘zbekcha sun’iy intellekt asistentsiz."},
            {"role": "user", "content": user_message},
        ],
        max_tokens=200
    )
    return response.choices[0].message.content.strip()

# Chat API
@app.post("/chat")
async def chat(message: str = Form(...)):
    reply = get_ai_reply(message)
    return {"message": reply}

