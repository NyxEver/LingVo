import tkinter as tk
from tkinter import ttk
import threading
import time
from src.core.logging_config import get_logger

logger = get_logger(__name__)


class SubtitleDesktop:
    """桌面字幕窗口 - 可拖拽调整的实时字幕"""

    def __init__(self, master=None):
        # 保存主窗口引用
        self.master = master
        self.window = None
        self.text_label = None
        self.current_text = ""
        self.is_visible = False

        # 窗口属性
        self.font_size = 24
        self.font_color = "white"
        self.bg_alpha = 0.7

        # 拖拽相关
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        # 调整大小相关
        self.resize_start_x = 0
        self.resize_start_y = 0
        self.resize_start_width = 0
        self.resize_start_height = 0
        self.is_resizing = False
        
        # 创建窗口（延迟到主线程）
        if master:
            master.after(0, self.create_window)

    def create_window(self):
        """创建字幕窗口"""
        self.window = tk.Toplevel(self.master)
        self.window.withdraw()  # 初始时隐藏窗口
        self.window.title("LingVo 字幕")

        # 设置窗口属性
        self.window.attributes('-topmost', True)  # 置顶
        self.window.attributes('-alpha', self.bg_alpha)  # 透明度
        self.window.overrideredirect(True)  # 无边框

        # 设置窗口大小和位置
        self.window.geometry("800x100+100+100")
        self.window.configure(bg='black')

        # 创建主框架
        self.main_frame = tk.Frame(self.window, bg='black')
        self.main_frame.pack(expand=True, fill="both")

        # 创建文本标签
        self.text_label = tk.Label(
            self.main_frame,
            text="等待语音输入...",
            font=("Microsoft YaHei", self.font_size, "bold"),
            fg=self.font_color,
            bg="black",
            wraplength=780,
            justify="center"
        )
        self.text_label.pack(expand=True, fill="both", padx=10, pady=10)

        # 创建调整大小的边框
        self.resize_frame = tk.Frame(self.window, bg='gray', height=5)
        self.resize_frame.pack(side="bottom", fill="x")
        
        # 创建右下角调整大小的控制点
        self.resize_corner = tk.Frame(self.window, bg='gray', width=15, height=15)
        self.resize_corner.place(relx=1.0, rely=1.0, anchor="se")

        # 绑定拖拽事件
        self.text_label.bind("<Button-1>", self.start_drag)
        self.text_label.bind("<B1-Motion>", self.on_drag)
        self.main_frame.bind("<Button-1>", self.start_drag)
        self.main_frame.bind("<B1-Motion>", self.on_drag)

        # 绑定调整大小事件
        self.resize_frame.bind("<Button-1>", self.start_resize)
        self.resize_frame.bind("<B1-Motion>", self.on_resize)
        self.resize_frame.bind("<ButtonRelease-1>", self.end_resize)
        self.resize_corner.bind("<Button-1>", self.start_resize)
        self.resize_corner.bind("<B1-Motion>", self.on_resize)
        self.resize_corner.bind("<ButtonRelease-1>", self.end_resize)
        
        # 设置鼠标样式
        self.resize_frame.configure(cursor="sb_v_double_arrow")
        self.resize_corner.configure(cursor="bottom_right_corner")

        # 绑定右键菜单
        self.text_label.bind("<Button-3>", self.show_context_menu)

        logger.info("字幕窗口已创建")

    def start_resize(self, event):
        """开始调整大小"""
        self.is_resizing = True
        self.resize_start_x = event.x_root
        self.resize_start_y = event.y_root
        self.resize_start_width = self.window.winfo_width()
        self.resize_start_height = self.window.winfo_height()

    def on_resize(self, event):
        """调整大小过程"""
        if not self.is_resizing:
            return
            
        # 计算新的宽度和高度
        new_width = max(200, self.resize_start_width + (event.x_root - self.resize_start_x))
        new_height = max(50, self.resize_start_height + (event.y_root - self.resize_start_y))
        
        # 更新窗口大小
        current_x = self.window.winfo_x()
        current_y = self.window.winfo_y()
        self.window.geometry(f"{new_width}x{new_height}+{current_x}+{current_y}")
        
        # 更新文本标签的wraplength
        if self.text_label:
            self.text_label.configure(wraplength=new_width - 20)

    def end_resize(self, event):
        """结束调整大小"""
        self.is_resizing = False

    def start_drag(self, event):
        """开始拖拽"""
        if self.is_resizing:
            return
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_drag(self, event):
        """拖拽过程"""
        if self.is_resizing:
            return
        x = self.window.winfo_x() + event.x - self.drag_start_x
        y = self.window.winfo_y() + event.y - self.drag_start_y
        self.window.geometry(f"+{x}+{y}")

    def show_context_menu(self, event):
        """显示右键菜单"""
        context_menu = tk.Menu(self.window, tearoff=0)
        context_menu.add_command(label="隐藏字幕", command=self.hide)
        context_menu.add_separator()
        context_menu.add_command(label="增大字体", command=self.increase_font)
        context_menu.add_command(label="减小字体", command=self.decrease_font)
        context_menu.add_separator()
        context_menu.add_command(label="重置大小", command=self.reset_size)

        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def reset_size(self):
        """重置窗口大小"""
        current_x = self.window.winfo_x()
        current_y = self.window.winfo_y()
        self.window.geometry(f"800x100+{current_x}+{current_y}")
        if self.text_label:
            self.text_label.configure(wraplength=780)

    def show(self):
        """显示字幕窗口"""
        if not self.window and self.master:
            # 如果窗口还没创建，先创建
            self.master.after(0, self.create_window)
            # 创建后延迟显示
            self.master.after(100, self._show_window)
        elif self.window:
            # 窗口已创建，直接显示
            self.master.after(0, self._show_window)
        
        self.is_visible = True
        logger.info("字幕窗口已显示")

    def _show_window(self):
        """在主线程中执行窗口显示操作"""
        if self.window:
            self.window.deiconify()
            self.is_visible = True
            logger.info("字幕窗口已显示")

    def increase_font(self):
        """增大字体"""
        self.font_size = min(self.font_size + 2, 48)
        self.update_font()

    def decrease_font(self):
        """减小字体"""
        self.font_size = max(self.font_size - 2, 12)
        self.update_font()

    def update_font(self):
        """更新字体"""
        if self.text_label:
            self.text_label.configure(font=("Microsoft YaHei", self.font_size, "bold"))

    def show(self):
        """显示字幕窗口"""
        if not self.window:
            self.create_window()

        # 在主线程中执行窗口显示
        self.window.after(0, self._show_window)
        self.is_visible = True
        logger.info("字幕窗口已显示")

    def _show_window(self):
        """在主线程中执行窗口显示操作"""
        self.window.deiconify()
        self.is_visible = True
        logger.info("字幕窗口已显示")

    def hide(self):
        """隐藏字幕窗口"""
        if self.window:
            self.window.withdraw()
        self.is_visible = False
        logger.info("字幕窗口已隐藏")

    def update_text(self, text: str):
        """更新字幕文本 - 流式效果"""
        if not self.is_visible or not self.text_label:
            return

        self.current_text = text

        # 在主线程中更新UI
        self.window.after(0, self._update_text_ui, text)

    def _update_text_ui(self, text: str):
        """在主线程中更新文本UI"""
        if self.text_label:
            self.text_label.configure(text=text)

    def destroy(self):
        """销毁窗口"""
        if self.window:
            self.window.destroy()
            self.window = None
        logger.info("字幕窗口已销毁")