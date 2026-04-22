import tkinter as tk
from tkinter import ttk
import pyautogui
import pytesseract
import re
from PIL import Image, ImageEnhance, ImageFilter

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

COLORS = {
    'bg': '#1a1a2e',
    'card': '#16213e',
    'accent': '#e94560',
    'accent2': '#0f3460',
    'text': '#eaeaea',
    'text_secondary': '#a0a0a0',
    'success': '#4ecca3'
}

class ModernWindow:
    def __init__(self, parent, title=''):
        self.win = tk.Toplevel(parent)
        self.win.title(title)
        self.win.attributes('-topmost', True)
        self.win.configure(bg=COLORS['bg'])

    def center(self, width, height, offset_x=0, offset_y=0):
        screen_w = self.win.winfo_screenwidth()
        screen_h = self.win.winfo_screenheight()
        x = (screen_w - width) // 2 + offset_x
        y = (screen_h - height) // 2 + offset_y
        self.win.geometry(f'{width}x{height}+{x}+{y}')

class DiscountTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("折扣计算器")
        self.root.configure(bg=COLORS['bg'])

        self.discount = tk.StringVar(value="80")
        self.start_x = 0
        self.start_y = 0

        self.setup_main_window()

    def setup_main_window(self):
        card = tk.Frame(self.root, bg=COLORS['card'], padx=30, pady=30)
        card.pack(padx=20, pady=20)

        title = tk.Label(card, text="折扣计算器", font=('Microsoft YaHei UI', 24, 'bold'),
                         bg=COLORS['card'], fg=COLORS['accent'])
        title.pack(pady=(0, 20))

        discount_frame = tk.Frame(card, bg=COLORS['card'])
        discount_frame.pack()

        tk.Label(discount_frame, text="满", font=('Microsoft YaHei UI', 12),
                bg=COLORS['card'], fg=COLORS['text']).pack(side=tk.LEFT)
        self.full_var = tk.StringVar()
        full_entry = tk.Entry(discount_frame, textvariable=self.full_var, font=('Microsoft YaHei UI', 14),
                             width=6, bg=COLORS['bg'], fg=COLORS['accent'], bd=0,
                             insertbackground=COLORS['accent'], justify='center')
        full_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(discount_frame, text="减", font=('Microsoft YaHei UI', 12),
                bg=COLORS['card'], fg=COLORS['text']).pack(side=tk.LEFT)
        self.sub_var = tk.StringVar()
        sub_entry = tk.Entry(discount_frame, textvariable=self.sub_var, font=('Microsoft YaHei UI', 14),
                            width=6, bg=COLORS['bg'], fg=COLORS['accent'], bd=0,
                            insertbackground=COLORS['accent'], justify='center')
        sub_entry.pack(side=tk.LEFT, padx=5)
        calc_btn = tk.Button(discount_frame, text="换算", font=('Microsoft YaHei UI', 10, 'bold'),
                            bg=COLORS['success'], fg='white', padx=10, pady=3,
                            bd=0, cursor='hand2', command=self.calc_discount_from_full)
        calc_btn.pack(side=tk.LEFT, padx=5)

        label = tk.Label(card, text="输入折扣率", font=('Microsoft YaHei UI', 12),
                        bg=COLORS['card'], fg=COLORS['text'])
        label.pack(pady=(15, 0))

        input_frame = tk.Frame(card, bg=COLORS['card'])
        input_frame.pack(pady=15)

        entry = tk.Entry(input_frame, textvariable=self.discount, font=('Microsoft YaHei UI', 18),
                        width=8, bg=COLORS['bg'], fg=COLORS['accent'], bd=0,
                        insertbackground=COLORS['accent'], justify='center')
        entry.pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(input_frame, text="%", font=('Microsoft YaHei UI', 18),
                bg=COLORS['card'], fg=COLORS['text']).pack(side=tk.LEFT)

        btn = tk.Button(card, text="开始截图选区", font=('Microsoft YaHei UI', 12, 'bold'),
                       bg=COLORS['accent'], fg='white', padx=30, pady=12,
                       bd=0, cursor='hand2', command=self.start_capture)
        btn.pack(pady=(10, 0))

        tk.Label(card, text="提示：拖动画框框住要计算的数字", font=('Microsoft YaHei UI', 9),
                bg=COLORS['card'], fg=COLORS['text_secondary']).pack(pady=(15, 0))

        self.root.update_idletasks()
        w = self.root.winfo_reqwidth()
        h = self.root.winfo_reqheight()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 3
        self.root.geometry(f'{w}x{h}+{x}+{y}')

    def calc_discount_from_full(self):
        try:
            full = float(self.full_var.get())
            sub = float(self.sub_var.get())
            if full > 0:
                rate = (full - sub) / full * 100
                self.discount.set(f"{rate:.2f}")
        except ValueError:
            pass

    def preprocess_image(self, img):
        w, h = img.size
        new_size = (w * 3, h * 3)
        resized = img.resize(new_size, Image.LANCZOS)
        gray = resized.convert('L')
        threshold = 128
        return gray.point(lambda x: 0 if x < threshold else 255, '1')

    def start_capture(self):
        self.root.withdraw()
        self.selection_window = tk.Toplevel()
        self.selection_window.attributes('-fullscreen', True)
        self.selection_window.attributes('-alpha', 0.3)
        self.selection_window.attributes('-topmost', True)
        self.selection_window.configure(bg='gray30', cursor='cross')

        self.canvas = tk.Canvas(self.selection_window, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.rect = None
        self.selection_window.bind('<Button-1>', self.on_press)
        self.selection_window.bind('<B1-Motion>', self.on_drag)
        self.selection_window.bind('<ButtonRelease-1>', self.on_release)
        self.selection_window.bind('<Escape>', lambda e: self.cancel_selection())

        instruction = tk.Label(self.selection_window,
                               text="拖动画框选择区域，按 ESC 取消",
                               font=('Microsoft YaHei UI', 16),
                               bg='#e94560', fg='white', padx=20, pady=10)
        instruction.place(relx=0.5, y=50, anchor='center')

    def cancel_selection(self):
        self.selection_window.destroy()
        self.root.deiconify()

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=4, dash=(5, 2), tags='rect'
        )
        self.rect = 'rect'

    def on_drag(self, event):
        self.canvas.coords('rect', self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        end_x, end_y = event.x, event.y
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)

        self.selection_window.destroy()

        if abs(x2 - x1) < 10 or abs(y2 - y1) < 10:
            self.root.deiconify()
            return

        try:
            screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
            processed = self.preprocess_image(screenshot)
            text = pytesseract.image_to_string(processed, config='--psm 6')
            text = text.strip()
            numbers = re.findall(r'\d+(?:\.\d+)?', text)
            numbers = [float(n) for n in numbers if float(n) > 0]

            if numbers:
                discount_val = float(self.discount.get()) / 100
                results = [(n, n * discount_val) for n in numbers]
                self.show_results(results, discount_val)
            else:
                self.show_error("未识别到数字")
        except Exception as e:
            self.show_error(f"识别失败: {str(e)}")

        self.root.deiconify()

    def show_results(self, results, discount):
        win = ModernWindow(self.root, "计算结果")
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        max_visible = 6
        show = results[:max_visible]
        win_height = 110 + len(show) * 58 + 60
        win_height = min(win_height, int(screen_h * 0.85))

        x = (screen_w - 360) // 2
        y = (screen_h - win_height) // 2
        win.win.geometry(f'360x{win_height}+{x}+{y}')

        main_frame = tk.Frame(win.win, bg=COLORS['card'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        header = tk.Frame(main_frame, bg=COLORS['card'])
        header.pack(fill='x')
        tk.Label(header, text="计算结果", font=('Microsoft YaHei UI', 14, 'bold'),
                bg=COLORS['card'], fg=COLORS['success']).pack()
        tk.Label(header, text=f"{float(self.discount.get()):.2f}%",
                font=('Microsoft YaHei UI', 24, 'bold'),
                bg=COLORS['card'], fg=COLORS['accent']).pack()

        list_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        list_frame.pack(fill='x', pady=8)

        for original, result in show:
            item = tk.Frame(list_frame, bg=COLORS['card'])
            item.pack(fill='x', pady=2, padx=5)
            inner = tk.Frame(item, bg=COLORS['card'])
            inner.pack(expand=True)
            tk.Label(inner, text=f"¥{original:.2f}", font=('Microsoft YaHei UI', 14),
                    bg=COLORS['card'], fg=COLORS['text_secondary']).pack(side='left')
            tk.Label(inner, text=" → ", font=('Microsoft YaHei UI', 14),
                    bg=COLORS['card'], fg=COLORS['text_secondary']).pack(side='left')
            tk.Label(inner, text=f"¥{result:.2f}", font=('Microsoft YaHei UI', 16, 'bold'),
                    bg=COLORS['card'], fg=COLORS['accent']).pack(side='left')

        if len(results) > max_visible:
            tk.Label(list_frame, text=f"... 还有 {len(results) - max_visible} 个",
                    font=('Microsoft YaHei UI', 11), bg=COLORS['bg'],
                    fg=COLORS['accent']).pack(pady=5)

        footer = tk.Frame(main_frame, bg=COLORS['card'])
        footer.pack(fill='x')
        tk.Button(footer, text="关闭", font=('Microsoft YaHei UI', 11),
                 bg=COLORS['accent2'], fg='white', padx=20, pady=6,
                 bd=0, cursor='hand2', command=win.win.destroy).pack(pady=5)

    def show_error(self, msg):
        win = ModernWindow(self.root, "提示")
        win.center(280, 120, offset_y=50)

        card = tk.Frame(win.win, bg=COLORS['card'], padx=20, pady=20)
        card.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tk.Label(card, text="⚠", font=('Arial', 24)).pack()
        tk.Label(card, text=msg, font=('Microsoft YaHei UI', 12),
                bg=COLORS['card'], fg=COLORS['accent']).pack(pady=10)
        tk.Button(card, text="关闭", font=('Microsoft YaHei UI', 10),
                 bg=COLORS['accent2'], fg='white', padx=20, pady=5,
                 bd=0, cursor='hand2', command=win.win.destroy).pack()

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    DiscountTool().run()
