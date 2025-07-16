from abc import ABC
import os
from src.core.logging_config import get_logger


class ModelConfig(ABC):
    def __init__(self,model_path:str,vad_model_path:str,tokens_path:str,num_threads=2):
        self.model_path = model_path
        self.vad_model_path = vad_model_path
        self.tokens_path = tokens_path
        self.num_threads = num_threads
        self.check_model_path()

    def check_model_path(self) -> bool:
        logger = get_logger(__name__)
        """验证目录文件"""
        if not os.path.exists(self.model_path):
            #print(f'模型不存在:{self.model_path}')
            logger.critical(f'模型不存在:{self.model_path}')
            raise FileNotFoundError(f'模型不存在:{self.model_path}')
        if not os.path.exists(self.vad_model_path):
            logger.critical(f'VAD模型不存在:{self.vad_model_path}')
            raise FileNotFoundError(f'VAD模型不存在:{self.vad_model_path}')
        if not os.path.exists(self.tokens_path):
            #print(f'tokens不存在:{self.tokens_path}')
            logger.critical(f'tokens不存在:{self.tokens_path}')
            raise FileNotFoundError(f'tokens不存在:{self.tokens_path}')
        return True

#    def create_recognizer(self) -> bool:
#        """初始化识别器"""
#        pass
