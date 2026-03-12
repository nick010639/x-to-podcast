"""Free TTS using edge-tts (Microsoft)"""
import asyncio
import edge_tts
import os

async def generate_speech(text: str, output_path: str, voice: str = "zh-CN-XiaoxiaoNeural") -> str:
    """Generate Chinese speech using free edge-tts"""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    return output_path

def text_to_speech(text: str, output_path: str) -> str:
    """Sync wrapper for edge-tts"""
    return asyncio.run(generate_speech(text, output_path))

if __name__ == "__main__":
    test_text = "你好，这是一个测试。我是微软的免费语音服务。"
    output = "/tmp/test_free_tts.mp3"
    result = text_to_speech(test_text, output)
    print(f"✅ Saved to: {result}")
