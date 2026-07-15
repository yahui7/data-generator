# 金融数据生成器
FROM python:3.13-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源码
COPY . .

# 确保数据目录存在
RUN mkdir -p data

EXPOSE 8001

CMD ["python", "main.py"]
