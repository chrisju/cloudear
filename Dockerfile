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

# 运行应用
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]

