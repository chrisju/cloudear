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

def is_valid_account(user, password):
    '''
    检查用户是否有效
    '''
    ...

def adduser(adminpass, user, password, date):
    '''
    检查admin帐号的密码
    增加user或更新user的password和过期date
    '''
    mdl = get_model()
    return mdl.predict(request.json)


'''
-- 创建数据库
CREATE DATABASE my_database;

-- 使用数据库
USE my_database;

-- 创建表，使用 username 作为主键
CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    expiry_date DATE NOT NULL
);
======================
import os
import sqlalchemy

# 设置数据库连接信息
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")
cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")

# 使用 SQLAlchemy 连接到 Cloud SQL
db = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_pass,
        database=db_name,
        query={
            "unix_socket": f"/cloudsql/{cloud_sql_connection_name}"
        }
    )
)

# Flask 应用示例
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
    with db.connect() as conn:
        result = conn.execute("SELECT * FROM users").fetchall()
        users = [dict(row) for row in result]
        return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
'''
