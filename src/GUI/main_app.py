"""LingVo 实时语音识别系统主程序
简单易用的语音识别和翻译工具
"""

import sys
import os
import threading
import tkinter as tk

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.GUI.main_gui import MainGUI
from src.core.logging_config import get_logger

logger = get_logger(__name__)


def main():
    """主函数"""
    try:
        logger.info("启动 LingVo 语音识别系统")
        print("正在启动 LingVo GUI...")
        print("请在浏览器中访问: http://localhost:8080")

        # 创建 Tkinter 根窗口（在主线程）
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        
        # 创建 GUI 实例
        gui = MainGUI(root)
        
        # 启动 PyWebIO 服务器（在后台线程）
        from pywebio import start_server
        webio_thread = threading.Thread(
            target=start_server,
            args=(gui.main_interface,),
            kwargs={'port': 8080, 'debug': True}
        )
        webio_thread.daemon = True
        webio_thread.start()
        
        # 在主线程中运行 Tkinter 事件循环
        root.mainloop()

    except KeyboardInterrupt:
        logger.info("用户中断程序")
        print("\n程序已退出")
    except Exception as e:
        logger.error(f"程序运行错误: {e}")
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()