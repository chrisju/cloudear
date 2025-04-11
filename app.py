'''
加载模型
接收语音文件及语言类型，转为文本
接收文本，源语言，目标语言，返回翻译结果
接收时带上用户名密码
'''
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from datetime import datetime
from utils import *


app = FastAPI()

class CheckRequest(BaseModel):
    adminpass: str
    user: str
    password: str
    days: str

@app.post("/hereadduser")
def hereadduser(req: CheckRequest):
    result = adduser(req.adminpass, req.user, req.password, req.days)
    return {"success": result}

@app.post("/s2t")
async def s2t(
    file: UploadFile = File(...),
    user: str = Form(...),
    password: str = Form(...),
    exparam: str = Form(...),
    targetlang: str = Form(...),
):
    audio = await file.read()
    result = speech2text(user, password, audio, exparam, targetlang)
    return result

@app.post("/t2t")
async def t2t(
    file: UploadFile = File(...),
    user: str = Form(...),
    password: str = Form(...),
    sourcelang: str = Form(...),
    targetlang: str = Form(...),
):
    txt = (await file.read()).decode("utf-8")
    result = text2text(user, password, txt, sourcelang, targetlang)
    return result

@app.get("/", response_class=PlainTextResponse)
def root():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\nHello, Cloud Run!"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

