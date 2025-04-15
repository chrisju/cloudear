# 使用 Python 运行环境
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制应用代码
COPY . /app

# 安装依赖
RUN pip install -r requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt
#EXPOSE 8080

RUN git clone https://huggingface.co/lovemefan/sense-voice-gguf.git
RUN git clone -b so https://github.com/chrisju/SenseVoice.cpp.git
RUN mkdir SenseVoice.cpp/build/
RUN cd SenseVoice.cpp/build/ && cmake -DCMAKE_BUILD_TYPE=Release .. && make -j 4 && cd -

# 运行应用
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
