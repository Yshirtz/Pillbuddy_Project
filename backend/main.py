import asyncio
import base64
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from services import rag_service, tts_service, vision_service

app = FastAPI(title="PillBuddy Backend", version="0.1.0")
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_storage: Dict[str, str] = {}


def extract_drug_name(raw_label: str) -> str:
    if not raw_label:
        return raw_label
    parts = raw_label.split("_")
    if len(parts) >= 3:
        core = "_".join(parts[1:-1]) or parts[1]
        return core
    if len(parts) == 2:
        return parts[1]
    return raw_label


class FollowupRequest(BaseModel):
    session_id: str
    question: str


class TTSRequest(BaseModel):
    text: str


@app.get("/health")
async def health_check():
    return {"message": "PillBuddy Backend is running!"}


@app.post("/api/v1/pills/identify")
async def identify_pill(
    session_id: str = Query(..., description="세션 식별자"),
    file: UploadFile = File(...),
):
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="이미지 파일을 업로드해주세요.")

    raw_pill_name = vision_service.identify_pill(contents)
    if not raw_pill_name:
        raise HTTPException(status_code=422, detail="약을 식별하지 못했습니다. 다시 촬영해주세요.")

    pill_name = extract_drug_name(raw_pill_name) or raw_pill_name

    drug_info = rag_service.fetch_drug_info(pill_name)
    if drug_info:
        script = rag_service.generate_summary_with_rag(drug_info)
    else:
        # rag_service.generate_summary_backup이 존재한다고 가정합니다.
        script = rag_service.generate_summary_backup(pill_name)

    session_storage[session_id] = pill_name

    audio_bytes = tts_service.synthesize_speech(script)
    if audio_bytes:
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
    else:
        audio_base64 = None

    return {
        "pill_name": pill_name,
        "script": script,
        "audio_base64": audio_base64,
    }


@app.post("/api/v1/pills/followup")
async def followup_question(payload: FollowupRequest):
    pill_name = session_storage.get(payload.session_id)
    if not pill_name:
        raise HTTPException(status_code=400, detail="먼저 약을 촬영해주세요.")

    answer = rag_service.answer_followup_question(pill_name, payload.question)
    audio_bytes = tts_service.synthesize_speech(answer)
    audio_base64 = (
        base64.b64encode(audio_bytes).decode("utf-8") if audio_bytes else None
    )

    return {
        "pill_name": pill_name,
        "question": payload.question,
        "answer": answer,
        "audio_base64": audio_base64,
    }


@app.post("/api/v1/tts")
async def synthesize_tts(payload: TTSRequest):
    loop = asyncio.get_running_loop()
    audio_bytes = await loop.run_in_executor(
        None, tts_service.synthesize_speech, payload.text
    )
    if not audio_bytes:
        raise HTTPException(
            status_code=500, detail="음성 합성에 실패했습니다. 다시 시도해주세요."
        )
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
    return {"audio_base64": audio_base64}


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/", include_in_schema=False)
async def serve_frontend():
    index_file = FRONTEND_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="프론트엔드 파일을 찾을 수 없습니다.")
    return FileResponse(index_file)

