# 1. 베이스 이미지
FROM python:3.10-slim

# 2. 시스템 패키지 설치
RUN apt-get update && \
    apt-get install -y --no-install-recommends libgl1 libglib2.0-0 && \ax lo
    rm -rf /var/lib/apt/lists/*

# 3. 작업 폴더 설정
WORKDIR /app

# 4. 의존성 설치
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. 소스 코드 복사
COPY backend /app/backend
COPY frontend /app/frontend

# 6. 실행 경로 이동
WORKDIR /app/backend

# 7. 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    