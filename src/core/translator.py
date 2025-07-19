from openai import OpenAI
from src.core.logging_config import get_logger

logger = get_logger(__name__)
class Translator:
    def __init__(self,api_key:str,target_language:str):
        self.api_key = api_key
        self.target_language = target_language
        self.client= OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    def translate(self,text:str):
        """翻译部分"""
        if not text or not text.strip():
            return text
        try:
            pass
        except Exception as error:
            pass