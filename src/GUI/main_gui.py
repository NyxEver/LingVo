import threading
from pywebio.input import input_group, checkbox, select
from pywebio.output import put_markdown, put_buttons, put_text
import os
from src.core.logging_config import get_logger
from src.core.sense_voice_model_config import SenseVoiceModelConfig

logger = get_logger(__name__)

class MainWindow:
    def __init__(self):
        self.app_controller = None
        self.subtitle_desktop= None
        self.is_running = None

    def main_interface(self):
        """主界面"""
        put_markdown("LingVo 实时翻译")
        put_markdown("--------------")

        # 模型配置区域
        current_dir = os.path.dirname(os.path.abspath(__file__))
        main_dir = os.path.dirname(current_dir)
        model_dir = os.path.join(main_dir, 'Model')
        model_path=os.path.join(model_dir, 'model.onnx')
        vad_model_path = os.path.join(model_dir, 'silero_vad.onnx')
        tokens_path=os.path.join(model_dir, 'tokens.txt')
        put_markdown("模型配置")
        model_config = input_group("模型设置",[
            input('模型路径',name='model_path',value=model_path),
            input('VAD模型路径', name='vad_model_path', value=vad_model_path),
            input('Tokens路径', name='tokens_path', value=tokens_path),
            select('语言',name='language',option=['zh','en','ja','ko','auto'],value='auto'),
            checkbox("启动逆文本归一化",name='use_itn',options=['启动逆文本归一化'])
        ])

        #翻译部分
        put_markdown("翻译设置（可选）")
        translation_config = input_group("翻译配置",[
            checkbox('启用翻译',name='enable_translation',options='启用大模型翻译'),
            input('API KEY',name='api_key',type=PASSWORD,placeholder='输入DEEPSEEK API'),
            input('目标语言',name='target_language',value='English')
        ])

        #字幕设置
        put_markdown("字幕设置")
        put_buttons(['启动识别','停止','显示字幕窗口'],onclick=[self.start_recognition,self.stop.recognition,self.show_subtitle_desktop])
        #状态显示
        put_markdown("软件状态")
        put_text('',scope='status')
        #实时文本
        put_markdown("实时结果")
        put_text('等待识别中...',scope='realtime_text')
        #启动状态更新线程
        threading.Thread(target=self.update_status,deamon=True).start()

    def start_recognition(self):
        """启动识别"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            main_dir = os.path.dirname(os.path.dirname(current_dir))
            model_dir = os.path.join(main_dir,'Model')
            model_path = os.path.join(model_dir,'model.onnx')
            vad_model_path = os.path.join(model_dir, 'silero_vad.onnx')
            tokens_path=os.path.join(model_dir,'tokens.txt')
            config = SenseVoiceModelConfig(
                model_path=model_path,
                vad_model_path=vad_model_path,
                tokens_path=tokens_path,
                language="auto",
                use_itn=True
            )
            self.app_controller
        except Exception as error:
            pass
