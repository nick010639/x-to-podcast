"""Free translation using Google Translate"""
from deep_translator import GoogleTranslator

def translate_to_chinese(text: str) -> str:
    """Translate English to Chinese using free Google Translate"""
    translator = GoogleTranslator(source='en', target='zh-CN')
    return translator.translate(text)

if __name__ == "__main__":
    test = "Hello, this is a test. I want to translate this to Chinese."
    result = translate_to_chinese(test)
    print(f"✅ Translated: {result}")
