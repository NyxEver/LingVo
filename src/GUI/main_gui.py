from pywebio.input import input_group, checkbox, select
from pywebio.output import put_markdown
import os
from src.core.logging_config import get_logger

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