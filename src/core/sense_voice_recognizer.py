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

    def create_vad(self, sample_rate):
        """VAD配置"""
        vad_config = sherpa_onnx.VadModelConfig()
        vad_config.silero_vad.model = self.config.vad_model_path
        vad_config.silero_vad.threshold = 0.4 #检测阈值
        vad_config.silero_vad.min_silence_duration = 0.08 # 最小静音持续时间
        vad_config.silero_vad.min_speech_duration = 0.2 # 最小语音持续时间
        vad_config.silero_vad.max_speech_duration = 5 # 最大语音持续时间(秒)
        vad_config.sample_rate = sample_rate #采样率
        try:
            vad = sherpa_onnx.VoiceActivityDetector(vad_config, buffer_size_in_seconds=100)
            logger.info("VAD加载成功。")
            return vad
        except Exception as error:
            logger.critical(f"加载VAD失败: {error}")
            return False

    def create_stream(self):
        return self.recognizer.create_stream()
    def decode_stream(self,stream):
        return self.recognizer.decode_stream(stream)