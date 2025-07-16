import sherpa_onnx
from src.core.logging_config import get_logger
from src.core.model_config import ModelConfig
from src.core.recognizer import Recognizer

logger = get_logger(__name__)
class SenseVoiceRecognizer(Recognizer):
    def __init__(self,config: ModelConfig):
        super().__init__(config)
        try:
            self.recognizer = sherpa_onnx.OfflineRecognizer.from_sense_voice(
                model=self.config.model_path,
                tokens=self.config.tokens_path,
                num_threads=self.config.num_threads,
                use_itn=self.config.use_itn
            )
            logger.info("模型成功加载")
        except Exception as error:
            logger.critical(f'创建失败{error}')
            return False