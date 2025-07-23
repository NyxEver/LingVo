import threading

from src.core.large_model_translator import Translator
from src.core.logging_config import get_logger
from src.core.model_config import ModelConfig
from src.core.real_time_stt import RealTimeSTT

logger = get_logger(__name__)
class AppController:
    def __init__(self,model_config:ModelConfig):
        self.model_config =model_config
        self.stt_engine=None
        self.translator=None
        self.recognition_thread=None
        self.is_running=False
        self.enable_translation=False
    def set_translator(self,api_key:str,target_language:str):
        try:
            self.translator = Translator(api_key,target_language)
            self.enable_translation=True
            logger.info("翻译启用")
        except Exception as error:
            logger.error(f"翻译功能设置失败{error}")
            self.enable_translation= False

    def run_recognition(self):
        try:
            self.stt_engine.record_run()
        except Exception as error:
            logger.error(f"运行错误{error}")
            self.is_running=False
            
    def start_recognition(self):
        """启动语音识别"""
        if self.is_running:
            logger.warning("识别正在运行")
            return
        try:
            self.stt_engine=RealTimeSTT(self.model_config)
            self.recognition_thread = threading.Thread(target=self.run_recognition,daemon=True)
            self.is_running=True
            self.recognition_thread.start()
            logger.info("识别启动")
        except Exception as error:
            logger.error(f"启动识别失败{error}")
            self.is_running=False

    def stop_recognition(self):
        """停止语音识别"""
        self.is_running=False
        if self.stt_engine:
            self.stt_engine.killed=True
        if self.recognition_thread and self.recognition_thread.is_alive():
            self.recognition_thread.join(timeout=2)
        logger.info("识别停止")

    def get_latest_text(self):
        """获取最新文本"""
        if not self.stt_engine:
            logger.warning("识别没有运行")
            return " "
        original_text=self.stt_engine.get_latest_text()
        if self.enable_translation and self.translator and original_text:
            try:
                translation_text=self.translator.translate(original_text)
                return f"{original_text}|{translation_text}"
            except Exception as error:
                logger.error(f"翻译失败{error}")
                return original_text
        return original_text

    def is_recognition_running(self):
        return self.is_running
