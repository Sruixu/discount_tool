# 折扣计算器

屏幕截图识别数字，快速计算折扣价。

## 功能

- 屏幕画框截取数字
- OCR 识别阿拉伯数字
- 支持多个数字同时计算
- 满减换算折扣率
- 美观的现代界面

## 演示

![演示](演示.gif)

## 安装

### 1. 安装 Tesseract OCR

下载 Windows 安装包：https://github.com/UB-Mannheim/tesseract/wiki

安装时选择：
- 默认路径 `C:\Program Files\Tesseract-OCR\`
- 勾选 English 语言包

### 2. 安装 Python 依赖

```bash
pip install pyautogui pytesseract pillow
```

## 使用

```bash
python discount_tool.py
```

### 操作步骤

1. 输入折扣率（如 `80` 表示 8折）
2. 或使用满减换算：输入"满 X 减 Y"，点击"换算"
3. 点击"开始截图选区"
4. 在屏幕上拖动画矩形框框住数字
5. 松开鼠标，自动计算并显示结果

## 技术栈

- Python 3
- tkinter - GUI
- pyautogui - 截图
- pytesseract - OCR 识别
- Pillow - 图像处理
- Tesseract OCR - 开源 OCR 引擎
