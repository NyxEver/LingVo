import os
import sherpa_onnx

def main():
    print("--- 开始 VAD 模型加载测试 ---")

    current_dir=os.path.dirname(os.path.abspath(__file__))
    parent_dir=os.path.dirname(current_dir)
    model_dir=os.path.join(parent_dir,'Model')
    vad_model_path=os.path.join(model_dir,'silero_vad.onnx')


    print(f"尝试加载 VAD 模型: {vad_model_path}")

    if not os.path.exists(vad_model_path):
        print(f"错误：VAD 模型文件不存在于路径: {vad_model_path}")
        return

    try:
        vad_config = sherpa_onnx.VadModelConfig()
        vad_config.silero_vad.model = vad_model_path
        vad_config.silero_vad.threshold = 0.5
        vad_config.silero_vad.min_silence_duration = 0.1
        vad_config.silero_vad.min_speech_duration = 0.25
        vad_config.silero_vad.window_size = 512
        vad_config.sample_rate = 16000

        vad = sherpa_onnx.VoiceActivityDetector(vad_config, buffer_size_in_seconds=1)
        print("--- VAD 模型成功加载！ ---")

    except Exception as error:
        print(f"--- VAD 模型加载失败！ ---")
        print(f"错误类型: {type(error).__name__}")
        print(f"错误信息: {error}")

if __name__ == '__main__':
    main()