#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PillBuddy 서버 실행 스크립트
환경 변수 확인 후 서버 시작
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    # 프로젝트 루트 디렉토리로 이동
    script_dir = Path(__file__).parent
    backend_dir = script_dir / "backend"
    
    if not backend_dir.exists():
        print("❌ 오류: backend 디렉토리를 찾을 수 없습니다.")
        sys.exit(1)
    
    os.chdir(backend_dir)
    
    # 환경 변수 확인
    required_vars = ["E_YAK_API_KEY", "GEMINI_API_KEY", "AZURE_SPEECH_KEY", "AZURE_SPEECH_REGION"]
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        print("⚠️  경고: 다음 환경 변수가 설정되지 않았습니다:")
        for var in missing:
            print(f"   - {var}")
        print("\n서버 시작을 시도하지만, 환경 변수가 없으면 오류가 발생할 수 있습니다.")
        print("환경 변수 설정 방법은 README_RUN.md를 참고하세요.\n")
        response = input("계속 진행하시겠습니까? (y/n): ")
        if response.lower() != 'y':
            print("서버 시작을 취소했습니다.")
            sys.exit(0)
    
    print("\n" + "=" * 50)
    print("PillBuddy 서버 시작")
    print("=" * 50)
    print(f"프론트엔드: http://localhost:8000/")
    print(f"API 문서: http://localhost:8000/docs")
    print(f"헬스 체크: http://localhost:8000/health")
    print("=" * 50)
    print("\n서버를 중지하려면 Ctrl+C를 누르세요.\n")
    
    # 서버 실행
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n\n서버를 중지했습니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

