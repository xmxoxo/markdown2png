FROM python:3.10-slim-bookworm

RUN apt-get update && apt-get install -y \
    libffi-dev \
    shared-mime-info \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 设置 Playwright 国内镜像
ENV PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright

# 安装浏览器及系统依赖
RUN playwright install chromium --with-deps

COPY . .

VOLUME ["/app/template", "/app/output"]

EXPOSE 8030

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8030"]
