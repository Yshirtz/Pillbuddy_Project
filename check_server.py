#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
서버 실행 전 환경 변수 및 의존성 확인 스크립트
"""
import sys
import os
from pathlib import Path

def check_environment():
    """필요한 환경 변수 확인"""
    required_vars = {
        "E_YAK_API_KEY": "의약품 정보 API 키",
        "GEMINI_API_KEY": "Google Gemini API 키",
        "AZURE_SPEECH_KEY": "Azure Speech 서비스 키",
        "AZURE_SPEECH_REGION": "Azure Speech 서비스 지역"
    }
    
    missing = []
    print("=" * 50)
    print("환경 변수 확인")
    print("=" * 50)
    
    for var, desc in required_vars.items():
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: 설정됨")
        else:
            print(f"❌ {var}: 설정되지 않음 ({desc})")
            missing.append(var)
    
    print("=" * 50)
    return missing

def check_imports():
    """서비스 모듈 임포트 확인"""
    print("\n서비스 모듈 확인 중...")
    backend_dir = Path(__file__).parent / "backend"
    sys.path.insert(0, str(backend_dir))
    
    try:
        os.chdir(backend_dir)
        from services import rag_service
        print("✅ rag_service 임포트 성공")
    except Exception as e:
        print(f"❌ rag_service 임포트 실패: {e}")
        return False
    
    try:
        from services import tts_service
        print("✅ tts_service 임포트 성공")
    except Exception as e:
        print(f"❌ tts_service 임포트 실패: {e}")
        return False
    
    try:
        from services import vision_service
        print("✅ vision_service 임포트 성공")
    except Exception as e:
        print(f"❌ vision_service 임포트 실패: {e}")
        return False
    
    return True

if __name__ == "__main__":
    missing_vars = check_environment()
    imports_ok = check_imports()
    
    print("\n" + "=" * 50)
    if missing_vars:
        print(f"⚠️  경고: {len(missing_vars)}개의 환경 변수가 누락되었습니다.")
        print("서버는 시작되지만 일부 기능이 작동하지 않을 수 있습니다.")
    else:
        print("✅ 모든 환경 변수가 설정되었습니다.")
    
    if imports_ok:
        print("✅ 모든 서비스 모듈이 정상적으로 로드되었습니다.")
    else:
        print("❌ 일부 서비스 모듈 로드에 실패했습니다.")
        print("환경 변수를 설정한 후 다시 시도해주세요.")
        sys.exit(1)
    
    print("=" * 50)
    print("\n서버를 시작하려면 다음 명령을 실행하세요:")
    print("  cd backend")
    print("  python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    print("\n또는 start_server.bat 파일을 실행하세요.")

