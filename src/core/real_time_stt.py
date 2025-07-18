import queue
import threading
import time
import numpy as np
import sounddevice as sound
from src.core.model_config import ModelConfig
from src.core.sense_voice_recognizer import SenseVoiceRecognizer


class RealTimeSTT:
    def __init__(self, config: ModelConfig):
        self.sample_rate = 16000
        self.config = config
        self.recognizer = SenseVoiceRecognizer(config)
        self.vad = self.recognizer.create_vad(self.sample_rate)
        self.audio_queue = queue.Queue()
        self.killed = False
        self.recording_thread = None

    def start_recording(self):
        """启动录音线程"""
        samples_read = int(0.1 * self.sample_rate)
        with sound.InputStream(channels=1, dtype="float32", samplerate=self.sample_rate) as stream:
            while not self.killed:
                samples, overflow = stream.read(samples_read)
                self.audio_queue.put(samples.reshape(-1).copy())

    def record_run(self):
        """主处理循环"""
        self.recording_thread = threading.Thread(target=self.start_recording)
        self.recording_thread.start()  # 启动线程

        buffer = np.array([], dtype=np.float32)  # 缓冲区，存储积累的数据
        offset = 0
        window_size = self.vad.config.silero_vad.window_size
        speech_start = False
        speech_start_time = None
        print("开始识别...")
        try:
            while not self.killed:
                samples = self.audio_queue.get()#从队列获取数组
                buffer = np.concatenate([buffer, samples])
                while offset + window_size < len(buffer):#数据处理
                    is_speech=self.vad.accept_waveform(buffer[offset:offset + window_size])
                    if not speech_start and is_speech:#检测语音开始
                        speech_start =True
                        speech_start_time=time.time()
                    offset += window_size
                if speech_start and time.time() - speech_start_time >0.2: #处理中间结果
                    stream =self.recognizer.create_stream()# 创建新的识别流
                    stream.accept_waveform(self.sample_rate, buffer)
                    self.recognizer.decode_stream(stream)# 解码音频
                    text=stream.result.text.strip()
                    if text:
                        print(f"中间结果：{text}")
                    speech_start_time=time.time()# 更新开始时间，准备下一次识别
                while not self.vad.empty():#处理完整语音段
                    stream=self.recognizer.create_stream()
                    stream.accept_waveform(self.sample_rate, self.vad.front.samples)#获取检测到的完整语音
                    self.vad.pop()#移除已处理语音
                    self.recognizer.decode_stream(stream)
                    text = stream.result.text.strip()
                    if text:
                        print(f"最终结果：{text}")
                    buffer=np.array([],dtype=np.float32)#清空缓冲区
                    offset=0
                    speech_start_time=False
                    speech_start_time=None
        except KeyboardInterrupt:
            print("\n 停止识别")
        finally:
            self.killed =True
            if self.recording_thread:
                self.recording_thread.join()
