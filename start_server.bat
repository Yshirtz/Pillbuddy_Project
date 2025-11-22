@echo off
chcp 65001 >nul
echo ========================================
echo   PillBuddy Server 시작
echo ========================================
echo.

REM 현재 스크립트의 디렉토리로 이동
cd /d "%~dp0"

REM 환경 변수 확인
set MISSING_VARS=0
if not defined E_YAK_API_KEY (
    echo [경고] E_YAK_API_KEY 환경 변수가 설정되지 않았습니다.
    set MISSING_VARS=1
)
if not defined GEMINI_API_KEY (
    echo [경고] GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.
    set MISSING_VARS=1
)
if not defined AZURE_SPEECH_KEY (
    echo [경고] AZURE_SPEECH_KEY 환경 변수가 설정되지 않았습니다.
    set MISSING_VARS=1
)
if not defined AZURE_SPEECH_REGION (
    echo [경고] AZURE_SPEECH_REGION 환경 변수가 설정되지 않았습니다.
    set MISSING_VARS=1
)

if %MISSING_VARS%==1 (
    echo.
    echo [중요] 필요한 환경 변수가 누락되었습니다.
    echo README_RUN.md 파일을 참고하여 환경 변수를 설정해주세요.
    echo.
    echo 계속 진행하시겠습니까? (서버 시작이 실패할 수 있습니다)
    pause
)

echo.
echo 서버 시작 중...
echo 프론트엔드: http://localhost:8000/
echo API 문서: http://localhost:8000/docs
echo.
echo 서버를 중지하려면 Ctrl+C를 누르세요.
echo.

cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause

