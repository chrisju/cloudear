import openai
import os

s2t_ctx = None

def loads2t():
    global s2t_ctx
    if s2t_ctx is None:
        print("prepare sensvoice...")
        s2t_ctx = load_model("/app/models/my_model.pth")
    return s2t_ctx
    ...

def speech2text(audio, lang, param):
    s2t_ctx = loads2t()

#use GPT
#def translate(text, inputlang, outputlang):

openai.api_key = os.environ.get("OPENAI_API_KEY")

def call_whisper_api(file_path):
    audio_file = open(file_path, "rb")
    result = openai.Audio.transcribe(
        model="whisper-1",
        file=audio_file,
        response_format="verbose_json",
        word_timestamps=True,
        temperature=0.2,
        language="zh"
    )
    return result

from googletrans import Translator

def generate_bilingual_subtitles(file_hash: str, target_language: str):
    # 读取原始 SRT 文件
    srt_filename = f"{file_hash}.srt"
    with open(srt_filename, "r") as file:
        lines = file.readlines()

    # 初始化翻译器
    translator = Translator()

    bilingual_subtitles = []
    for i in range(0, len(lines), 3):  # 每条字幕由 3 行组成
        timestamp = lines[i].strip()
        text = lines[i + 1].strip()

        # 翻译字幕文本
        translation = translator.translate(text, dest=target_language).text

        # 双语字幕（原文 + 翻译）
        bilingual_subtitles.append(f"{timestamp}\n{text} ({translation})\n\n")

    # 保存双语字幕文件
    bilingual_srt_filename = f"{file_hash}_bilingual.srt"
    with open(bilingual_srt_filename, "w") as file:
        file.writelines(bilingual_subtitles)

