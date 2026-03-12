"""MiniMax TTS API"""
import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

# Use dev API key for testing
MINIMAX_API_KEY = "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"

def text_to_speech(text: str, output_path: str, voice_id: str = "male-qn-qingse") -> str:
    """Convert Chinese text to speech using MiniMax TTS API"""
    
    url = "https://api.minimax.chat/v1/t2a_v2"
    
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "speech-01-turbo",
        "text": text,
        "voice_setting": {
            "voice_id": voice_id
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3"
        }
    }
    
    response = requests.post(url, json=data, headers=headers, timeout=60)
    result = response.json()
    
    if "data" in result and "audio" in result["data"]:
        audio_data = result["data"]["audio"]
        audio_bytes = base64.b64decode(audio_data)
        
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
        
        return output_path
    else:
        raise Exception(f"TTS failed: {result}")

if __name__ == "__main__":
    test_text = "你好，这是一个测试。"
    output = "/tmp/test_tts.mp3"
    result = text_to_speech(test_text, output)
    print(f"Saved to: {result}")
