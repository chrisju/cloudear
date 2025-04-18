# 使用 Python 运行环境
FROM public.ecr.aws/ubuntu/ubuntu:24.04

# 设置工作目录
WORKDIR /app

# 复制应用代码
COPY . /app

RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git git-lfs cmake make curl    \
    && rm -rf /var/lib/apt/lists/*
RUN git lfs install

# 安装依赖
RUN pip install --user -r requirements.txt --break-system-packages

RUN git clone https://huggingface.co/lovemefan/sense-voice-gguf.git
RUN git clone -b so https://github.com/chrisju/SenseVoice.cpp.git
RUN cd SenseVoice.cpp/ && git submodule sync && git submodule update --init --recursive && cd -
RUN mkdir SenseVoice.cpp/build/ && cd SenseVoice.cpp/build/ && cmake -DCMAKE_BUILD_TYPE=Release .. && make -j 4 && cd -

# 运行应用
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
CMD ["python3","-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
