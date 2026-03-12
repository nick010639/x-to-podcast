
"""
X Video to Podcast - Complete Pipeline (Free Edition)
"""

import os
import sys
import json
import asyncio
import subprocess
import uuid
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
import edge_tts

load_dotenv()

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

class Pipeline:
    def __init__(self):
        self.data_dir = DATA_DIR
        
    def download(self, url: str) -> str:
        video_id = str(uuid.uuid4())[:8]
        output_path = self.data_dir / f"{video_id}.mp4"
        
        print(f"📥 Downloading: {url}")
        
        cmd = ["yt-dlp", "--no-check-certificate", "-f", "best", "-o", str(output_path), url, "--no-warnings"]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0 and not output_path.exists():
            raise Exception(f"Download failed: {result.stderr}")
            
        print(f"✅ Downloaded: {output_path}")
        return str(output_path)
    
    def extract_audio(self, video_path: str) -> str:
        audio_path = str(Path(video_path).with_suffix(".mp3"))
        
        cmd = ["ffmpeg", "-i", video_path, "-vn", "-acodec", "libmp3lame", "-q:a", "2", "-y", audio_path]
        
        print(f"🎵 Extracting audio...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Audio extraction failed: {result.stderr}")
            
        print(f"✅ Audio extracted: {audio_path}")
        return audio_path
    
    def transcribe(self, audio_path: str) -> str:
        print(f"🎙️ Transcribing with Whisper...")
        
        try:
            from faster_whisper import WhisperModel
            model = WhisperModel("base", device="cpu", compute_type="int8")
            segments, info = model.transcribe(audio_path)
            text = " ".join([segment.text for segment in segments])
        except Exception as e:
            print(f"⚠️ Whisper failed: {e}")
            text = "Transcription failed."
        
        transcript_path = audio_path.replace(".mp3", "_en.txt")
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(text)
            
        print(f"✅ Transcribed: {len(text)} chars")
        return text
    
    def translate(self, text: str) -> str:
        print(f"🌐 Translating to Chinese (free)...")
        
        try:
            translator = GoogleTranslator(source="en", target="zh-CN")
            chinese_text = translator.translate(text)
        except Exception as e:
            print(f"⚠️ Translation failed: {e}")
            chinese_text = "[翻译失败]"
        
        return chinese_text
    
    def generate_title(self, transcript: str) -> str:
        print(f"📝 Generating title...")
        
        transcript_lower = transcript.lower()
        
        keywords = []
        if "back pain" in transcript_lower or "spine" in transcript_lower:
            keywords.append("背痛")
        if "ai" in transcript_lower or "artificial intelligence" in transcript_lower:
            keywords.append("AI")
        if "health" in transcript_lower or "longevity" in transcript_lower:
            keywords.append("健康")
        if "david sinclair" in transcript_lower:
            keywords.append("David Sinclair")
        if "sleep" in transcript_lower:
            keywords.append("睡眠")
        
        if keywords:
            title = "聊聊" + "、".join(keywords[:3])
        else:
            title = "X 视频分享"
        
        print(f"✅ Title: {title}")
        return title
    
    def generate_tts(self, text: str, output_path: str) -> str:
        print(f"🔊 Generating TTS (free edge-tts)...")
        
        tts_path = output_path.replace(".mp3", "_zh.mp3")
        
        try:
            communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
            asyncio.run(communicate.save(tts_path))
            print(f"✅ TTS generated: {tts_path}")
        except Exception as e:
            print(f"⚠️ TTS failed: {e}")
            tts_path = output_path.replace(".mp3", "_zh.txt")
            with open(tts_path, "w", encoding="utf-8") as f:
                f.write(text)
        
        return tts_path
    
    def run(self, url: str) -> dict:
        print(f"\n🚀 Starting pipeline for: {url}\n")
        
        try:
            video_path = self.download(url)
            audio_path = self.extract_audio(video_path)
            english_text = self.transcribe(audio_path)
            chinese_text = self.translate(english_text)
            title = self.generate_title(english_text)
            tts_path = self.generate_tts(chinese_text, audio_path)
            
            # Save files
            with open(audio_path.replace(".mp3", "_title.txt"), "w", encoding="utf-8") as f:
                f.write(title)
            with open(audio_path.replace(".mp3", "_zh.txt"), "w", encoding="utf-8") as f:
                f.write(chinese_text)
            
            result = {
                "status": "completed",
                "title": title,
                "video_path": video_path,
                "audio_path": audio_path,
                "tts_path": tts_path,
                "created_at": datetime.now().isoformat()
            }
            
            print(f"\n✅ Pipeline completed!")
            return result
            
        except Exception as e:
            print(f"\n❌ Pipeline failed: {e}")
            return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pipeline.py <x_video_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    pipeline = Pipeline()
    result = pipeline.run(url)
    print(json.dumps(result, indent=2))
