import os
from src.core.real_time_stt import RealTimeSTT
from src.core.sense_voice_model_config import SenseVoiceModelConfig
import sounddevice as sound

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_dir = os.path.join(os.path.dirname(current_dir), 'Model')
    model_path = os.path.join(main_dir, 'model.onnx')
    vad_model_path = os.path.join(main_dir, 'silero_vad.onnx')
    tokens_path = os.path.join(main_dir, 'tokens.txt')
    # 配置模型路径 - 请根据实际路径修改
    config = SenseVoiceModelConfig(
        model_path=model_path,
        vad_model_path=vad_model_path,
        tokens_path=tokens_path,
        language="auto",
        use_itn=True,
        num_threads=4
    )

    #print(sound.query_devices())
    # 创建并运行实时语音识别
    stt = RealTimeSTT(config)
    stt.record_run()