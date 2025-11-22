# PillBuddy 서버 실행 가이드

## 필요한 환경 변수

백엔드 서버를 실행하기 전에 다음 환경 변수들을 설정해야 합니다:

1. **E_YAK_API_KEY**: 의약품 정보 API 키
2. **GEMINI_API_KEY**: Google Gemini API 키  
3. **AZURE_SPEECH_KEY**: Azure Speech 서비스 키
4. **AZURE_SPEECH_REGION**: Azure Speech 서비스 지역 (예: "koreacentral", "eastus")

## 환경 변수 설정 방법

### 방법 1: .env 파일 생성

프로젝트 루트 또는 `backend/` 디렉토리에 `.env` 파일을 만들고 다음 내용을 추가하세요:

```
E_YAK_API_KEY=your_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=your_azure_region_here
```

### 방법 2: 시스템 환경 변수 설정

Windows에서:
1. 시스템 속성 > 고급 > 환경 변수
2. 사용자 변수 또는 시스템 변수에 추가

PowerShell에서 임시로 설정:
```powershell
$env:E_YAK_API_KEY="your_key"
$env:GEMINI_API_KEY="your_key"
$env:AZURE_SPEECH_KEY="your_key"
$env:AZURE_SPEECH_REGION="your_region"
```

## 서버 실행 방법

### 방법 1: 배치 파일 사용 (Windows)
```cmd
start_server.bat
```

### 방법 2: PowerShell 스크립트 사용
```powershell
.\start_server.ps1
```

### 방법 3: 직접 실행
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 접속 주소

서버가 시작되면 다음 주소에서 접속할 수 있습니다:

- **프론트엔드**: http://localhost:8000/
- **API 문서**: http://localhost:8000/docs
- **헬스 체크**: http://localhost:8000/health

## 문제 해결

서버가 시작되지 않는 경우:

1. 필요한 패키지가 설치되어 있는지 확인:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. 환경 변수가 제대로 설정되었는지 확인

3. 포트 8000이 사용 중인지 확인:
   ```powershell
   netstat -ano | findstr :8000
   ```

4. Python 버전 확인 (3.8 이상 필요):
   ```bash
   python --version
   ```

