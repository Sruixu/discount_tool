# Tesseract OCR 安装指南

## 1. 下载 Tesseract

访问 GitHub 下载 Windows 安装包：
https://github.com/UB-Mannheim/tesseract/wiki

下载 `tesseract-ocr-w64-setup-*.exe`（64位版本）

## 2. 安装步骤

1. 双击运行安装程序
2. **安装路径**：建议使用默认路径 `C:\Program Files\Tesseract-OCR\`
3. **组件选择**：确保勾选 English 语言包
4. 完成安装

## 3. 验证安装

打开命令提示符（CMD），运行：
```
tesseract --version
```

如果显示版本信息，说明安装成功。

## 4. 运行折扣工具

安装完 Tesseract 后，在命令行运行：
```
python discount_tool.py
```

## 注意事项

- 如果程序报告找不到 tesseract，请确认安装路径是否为 `C:\Program Files\Tesseract-OCR\tesseract.exe`
- 如果路径不同，请修改 `discount_tool.py` 第9行的路径
