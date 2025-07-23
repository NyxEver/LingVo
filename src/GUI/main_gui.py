import threading
import os
import time
from pywebio import start_server
from pywebio.session import register_thread
from pywebio.input import input_group, checkbox, select, input, PASSWORD
from pywebio.output import put_markdown, put_buttons, put_text
from src.GUI.app_controller import AppController
from src.GUI.subtitle_desktop import SubtitleDesktop
from src.core.logging_config import get_logger
from src.core.sense_voice_model_config import SenseVoiceModelConfig

logger = get_logger(__name__)

class MainGUI:
    def __init__(self, root):
        self.app_controller = None
        self.subtitle_desktop = None
        self.is_running = None
        
        # 保存 Tkinter 根窗口引用
        self.root = root
        
        # 添加翻译配置属性
        self.translation_enabled = False
        self.translation_api_key = ""
        self.translation_target_language = "English"

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
            select('语言',name='language',options=['zh','en','ja','ko','auto'],value='auto'),
            checkbox("启动逆文本归一化",name='use_itn',options=['启动逆文本归一化'])
        ])

        #翻译部分
        put_markdown("翻译设置（可选）")
        translation_config = input_group("翻译配置",[
            checkbox('启用翻译',name='enable_translation',options=['启用大模型翻译']),
            input('API KEY',name='api_key',type=PASSWORD,placeholder='输入DEEPSEEK API'),
            input('目标语言',name='target_language',value='English')
        ])
        
        # 保存翻译配置
        self.translation_enabled = '启用大模型翻译' in translation_config['enable_translation']
        self.translation_api_key = translation_config['api_key']
        self.translation_target_language = translation_config['target_language']

        #字幕设置
        put_markdown("字幕设置")
        put_buttons(['启动识别','停止','显示字幕窗口'],onclick=[self.start_recognition,self.stop_recognition,self.show_subtitle_desktop])
        #状态显示
        put_markdown("软件状态")
        put_text('',scope='status')
        #实时文本
        put_markdown("实时结果")
        put_text('等待识别中...',scope='realtime_text')
        #启动状态更新线程
        status_thread = threading.Thread(target=self.update_status, daemon=True)
        register_thread(status_thread)  # 注册线程到 PyWebIO
        status_thread.start()

        # 启动 Tkinter 事件循环
        threading.Thread(target=self._run_tkinter_mainloop, daemon=True).start()

    def _run_tkinter_mainloop(self):
        """在主线程中运行 Tkinter 事件循环"""
        self.root.mainloop()

    def show_subtitle_desktop(self):
        """显示字幕窗口"""
        if not self.subtitle_desktop:
            self.subtitle_desktop = SubtitleDesktop(master=self.root)  # 传入根窗口
        self.subtitle_desktop.show()
        put_text('字幕窗口已显示', scope='status')

    def update_status(self):
        """更新状态和实时文本"""
        while True:
            try:
                if self.app_controller and self.is_running:
                    # 获取最新文本
                    latest_text = self.app_controller.get_latest_text()
                    if latest_text:
                        put_text(f'{latest_text}', scope='realtime_text')

                        # 更新字幕窗口
                        if self.subtitle_desktop:
                            self.subtitle_desktop.update_text(latest_text)

                time.sleep(0.1)  # 100ms更新一次
            except Exception as e:
                logger.error(f"状态更新错误: {e}")
                time.sleep(1)

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
            self.app_controller=AppController(config)
            
            # 设置翻译器
            if self.translation_enabled and self.translation_api_key:
                self.app_controller.set_translator(
                    self.translation_api_key,
                    self.translation_target_language
                )
                put_text('翻译已启用', scope='status')
                logger.info(f'翻译已启用，目标语言: {self.translation_target_language}')
            
            self.app_controller.start_recognition()
            self.is_running=True
            if not self.subtitle_desktop:
                self.subtitle_desktop= SubtitleDesktop(master=self.root)
                self.subtitle_desktop.show()
            put_text('识别启动',scope='status')
            logger.info('语音识别启动')
        except Exception as error:
            put_text(f'启动失败{str(error)}',scope='status')
            logger.error(f'启动失败{str(error)}')

    def stop_recognition(self):
        """停止识别"""
        try:
            if self.app_controller:
                self.app_controller.stop_recognition()
            self.is_running=False
            if self.subtitle_desktop:
                self.subtitle_desktop.hide()
            put_text('识别停止',scope='status')
            logger.info('语音识别停止')
        except Exception as error:
            put_text(f'停止失败{str(error)}', scope='status')
            logger.error(f'停止失败{str(error)}')

def start_gui():
        """启动GUI"""
        gui = MainGUI()
        start_server(gui.main_interface, port=8080, debug=True)

if __name__ == '__main__':
        start_gui()