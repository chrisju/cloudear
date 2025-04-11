'''
加载模型
接收语音文件及语言类型，转为文本
接收文本，源语言，目标语言，返回翻译结果
接收时带上用户名密码
'''
from flask import Flask

app = Flask(__name__)

model = None

def get_model():
    global model
    if model is None:
        print("Loading model...")
        model = load_model("/app/models/my_model.pth")
    return model

@app.route("/")
def home():
    return "Hello, Cloud Run!"

@app.route("/predict", methods=["POST"])
def predict():
    mdl = get_model()
    return mdl.predict(request.json)

@app.route("/s2t", methods=["POST"])
def transcribe():
    file = request.files.get("file")
    if not file:
        return {"error": "No file provided"}, 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
        file.save(temp.name)

        transcript = utils.call_whisper_api(temp.name)
        return transcript

@app.get("/get_subtitles/")
async def get_subtitles(file_hash: str, username: str = "", password: str = ""):
    bilingual_srt_filename = f"{file_hash}_bilingual.srt"
    
    try:
        with open(bilingual_srt_filename, "r") as file:
            subtitles = file.read()
        return {"status": "success", "subtitles": subtitles}
    except FileNotFoundError:
        return {"status": "error", "message": "Subtitles not found."}


'''
def transcribe_audio(file_hash: str, audio_file):
    # 载入 Whisper 模型
    model = whisper.load_model("base")  # 可以选择 'small', 'medium', 'large'
    
    # 读取音频并进行推理
    audio = whisper.load_audio(audio_file)
    result = model.transcribe(audio)

    # 保存为 SRT 文件
    srt_filename = f"{file_hash}.srt"
    with open(srt_filename, "w") as f:
        for segment in result["segments"]:
            f.write(f"{segment['start']} --> {segment['end']}\n")
            f.write(f"{segment['text']}\n\n")
'''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
