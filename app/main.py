from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.llm import chat_with_llm
from app.redis_client import save_history, get_history


class ChatRequest(BaseModel):
    user_id: str
    message: str


app = FastAPI()


@app.get("/")
async def home():
    return {"message": "Welcome to the chatbot API!"}


@app.post("/chat")
async def chat_endpoint(req: ChatRequest):

    system_prompt = """
    You are top notch AI assistant. You are helpful, creative, clever, funny and very friendly.
    Respond in a clear and concise manner.
    """
    messages = [{"role": "system", "content": system_prompt}]
    try:
        # get history
        history = get_history(req.user_id)

        # add history to messages
        messages.extend(history)

        # Add the new user message
        messages.append({"role": "user", "content": req.message})

        response = chat_with_llm(messages)

        # Save the updated history
        history.append({"role": "user", "content": req.message})
        history.append({"role": "assistant", "content": response})
        save_history(req.user_id, history)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

