from src.core.model_config import ModelConfig


class SenseVoiceModelConfig(ModelConfig):
    def __init__(self, model_path: str, tokens_path: str, vad_model_path: str, language: str, use_itn: bool,
                 num_threads=2):
        super().__init__(model_path, tokens_path, vad_model_path, num_threads)
        self.language = language
        self.use_itn = use_itn #逆文本归一化参数
