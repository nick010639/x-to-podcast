"""MiniMax Translation API"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")

def translate_to_chinese(text: str) -> str:
    """Translate English text to Chinese using MiniMax API"""
    
    url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
    
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "abab6.5s-chat",
        "messages": [
            {
                "role": "system",
                "content": "You are a professional translator. Translate the following English text to Chinese. Keep it natural and conversational."
            },
            {
                "role": "user", 
                "content": text
            }
        ]
    }
    
    response = requests.post(url, json=data, headers=headers, timeout=30)
    result = response.json()
    
    if "choices" in result and len(result["choices"]) > 0:
        return result["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Translation failed: {result}")

if __name__ == "__main__":
    test_text = "Hello, this is a test. I want to translate this to Chinese."
    result = translate_to_chinese(test_text)
    print(result)
