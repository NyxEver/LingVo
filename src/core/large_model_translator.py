from openai import OpenAI
from src.core.logging_config import get_logger

logger = get_logger(__name__)
class Translator:
    def __init__(self,api_key:str,target_language:str):
        self.api_key = api_key
        self.target_language = target_language
        self.client= OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    def translate(self,original_text:str):
        """翻译部分"""
        if not original_text or not original_text.strip():
            return original_text
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": f"You are a professional translator. Translate the following text to {self.target_language}. Only return the translated text, no explanations."},
                    {"role": "user", "content": original_text},
                ],
                stream=True
            )
            translation_text = response.choices[0].message.content.strip()
            return translation_text
        except Exception as error:
            logger.error(f"操作失败{error}")
            return original_text