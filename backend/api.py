"""
Simple API for X to Podcast
"""
import os
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pipeline import Pipeline
import uuid

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path(__file__).parent.parent / "data"
PIPELINE = Pipeline()

class ProcessRequest(BaseModel):
    url: str

class PodcastItem(BaseModel):
    id: str
    title: str
    created_at: str

@app.post("/process")
async def process_video(req: ProcessRequest):
    """Process X video URL"""
    try:
        result = PIPELINE.run(req.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list")
async def list_podcasts():
    """List all podcasts"""
    podcasts = []
    
    for audio_file in DATA_DIR.glob("*_zh.mp3"):
        podcast_id = audio_file.stem.replace("_zh", "")
        txt_file = DATA_DIR / f"{podcast_id}_zh.txt"
        
        # Read title
        title_path = DATA_DIR / f"{podcast_id}_title.txt"
        title = "X 视频"
        if title_path.exists():
            with open(title_path, 'r', encoding='utf-8') as f:
                title = f.read().strip()
        if txt_file.exists():
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read()[:50]
                    title = content + "..." if len(content) >= 50 else content
            except:
                pass
        
        # Get creation time
        created = audio_file.stat().st_mtime
        
        podcasts.append({
            "id": podcast_id,
            "title": title,
            "created_at": str(created)
        })
    
    # Sort by date
    podcasts.sort(key=lambda x: x['created_at'], reverse=True)
    
    return podcasts

@app.get("/audio/{podcast_id}")
async def get_audio(podcast_id: str):
    """Get audio file"""
    audio_path = DATA_DIR / f"{podcast_id}_zh.mp3"
    
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Audio not found")
    
    from fastapi.responses import FileResponse
    return FileResponse(
        audio_path, 
        media_type="audio/mpeg",
        headers={"Content-Disposition": f"inline; filename={podcast_id}.mp3"}
    )

@app.get("/transcript/{podcast_id}")
async def get_transcript(podcast_id: str):
    """Get transcript"""
    transcript_path = DATA_DIR / f"{podcast_id}_zh.txt"
    
    if not transcript_path.exists():
        raise HTTPException(status_code=404, detail="Transcript not found")
    
    with open(transcript_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return {"transcript": content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
