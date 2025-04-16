import os
import easycpp


s2t_ctx = None

'''
    cpp = easycpp.easycpp('build/lib/libsense-voice.so')
        cmdarg = '-m ../sense-voice-gguf/sense-voice-small-q8_0.gguf -t 18 -ng --max_speech_duration_ms 5000  --min_silence_duration_ms 550'.encode('utf-8')
        print(f'cmdarg: {cmdarg}')
        r = cpp.sense_voice_load(cmdarg)
        print(f'sense_voice_load: {r}')
        audio = open(sys.argv[1], 'rb').read()
        r = cpp.sense_voice_speechbuff2text(cmdarg, audio, len(audio))
        '''
def loads2t(param):
    '''
    参数对应ctx？
    累计识别数量大后重新初始化？ TODO
    '''
    global s2t_ctx
    if s2t_ctx is None:
        print("prepare sensvoice...")
        s2t_ctx = easycpp.easycpp('/app/SenseVoice.cpp/build/lib/libsense-voice.so')
        s2t_ctx.sense_voice_speechbuff2text.argtypes = [
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_char_p)
        ]
        s2t_ctx.sense_voice_speechbuff2text.restype = ctypes.c_int
        r = s2t_ctx.sense_voice_load(param)
        print(f'sense_voice_load: {r}')
        if r != 0:
            s2t_ctx = None
    return s2t_ctx
    ...

def speech2text(user, password, audio, exparam, targetlang):
    '''
    targetlang 不为空则翻译
    '''
    param = exparam + ' -m /app/sense-voice-gguf/sense-voice-small-q8_0.gguf'
    param = param.strip().encode('utf-8')

    if not is_valid_account(user, password):
        return {'txt': '', 'error':'acount invalid.'}

    s2t_ctx = loads2t(param_)

    out_ptr = ctypes.c_char_p()
    r = s2t_ctx.sense_voice_speechbuff2text(param, audio, len(audio), ctypes.byref(out_ptr))
    print(f'sense_voice_speechbuff2text: {r, out_ptr}')
    if r > 0:
        return {'txt': out_ptr, 'error':''}
    else:
        return {'txt': '', 'error':f'sense_voice_speechbuff2text failed: {r}'}

def text2text(user, password, txt, sourcelang, targetlang):
    '''
    mode '0' 只识别
    mode '1' 识别+翻译
    '''
    if not is_valid_account(user, password):
        return {'txt': '', 'error':'acount invalid.'}
    ...
    result = f'{len(txt)}'
    return {'txt': result, 'error':''}

#use GPT
#def translate(text, inputlang, outputlang):
'''
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
'''

def is_valid_account(user, password):
    '''
    检查用户是否有效
    '''
    #datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return True
    ...

def adduser(adminpass, user, password, days):
    '''
    检查admin帐号的密码
    增加user或更新user的password和过期date
    '''
    return True


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
