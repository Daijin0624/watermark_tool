# 📸 Photo Date Watermark Tool

一个基于图片 EXIF 信息自动添加日期水印的 Python 命令行工具。从照片的拍摄时间信息中提取日期，并以美观的水印形式添加到图片上。

## ✨ 功能特性

- 🕒 **智能日期提取** - 自动从 EXIF 数据中读取拍摄时间，无 EXIF 时使用文件时间
- 🎨 **灵活自定义** - 支持字体大小、颜色、位置、透明度的完全自定义
- 📁 **批量处理** - 一次性处理整个目录中的所有图片
- 🛡️ **原图保护** - 在新目录中保存水印图片，绝不覆盖原文件
- 🔄 **多格式支持** - JPG、PNG、TIFF 等主流图片格式
- 🌐 **跨平台兼容** - 支持 Windows、macOS、Linux 系统
- 💫 **视觉优化** - 自动添加阴影效果，提高水印可读性

## 🚀 快速开始

### 环境要求
- Python 3.6 或更高版本
- 操作系统：Windows / macOS / Linux

### 安装

```bash
# 克隆项目
git clone https://github.com/yourusername/photo-watermark-tool.git
cd photo-watermark-tool

# 安装依赖
pip install -r requirements.txt
```

### 基本用法

```bash
# 最简单的使用方式
python src/watermark_tool.py /path/to/your/photos

# 自定义水印样式
python src/watermark_tool.py /path/to/photos --size 48 --color white --position top-left

# 使用十六进制颜色
python src/watermark_tool.py /path/to/photos --color "#FF6B6B" --opacity 180
```

## 📖 详细说明

### 命令行参数

| 参数 | 短参数 | 默认值 | 说明 |
|------|--------|--------|------|
| `directory` | - | 必需 | 包含图片的目录路径 |
| `--size` | `-s` | 36 | 字体大小 (1-200) |
| `--color` | `-c` | white | 文字颜色 |
| `--position` | `-p` | bottom-right | 水印位置 |
| `--opacity` | `-o` | 200 | 透明度 (0-255) |

### 支持的位置

- `top-left` - 左上角
- `top-center` - 上方居中  
- `top-right` - 右上角
- `center` - 正中央
- `bottom-left` - 左下角
- `bottom-center` - 下方居中
- `bottom-right` - 右下角（默认）

### 支持的颜色格式

```bash
# 预定义颜色
--color white, black, red, green, blue, yellow, orange, purple

# 十六进制颜色
--color "#FF0000"  # 红色
--color "#00FF00"  # 绿色

# RGB 格式
--color "255,0,0"    # 红色
--color "0,255,0"    # 绿色
```

## 🎯 使用示例

### 基础示例
```bash
# 使用默认设置（白色水印，右下角，36px）
python src/watermark_tool.py ~/Pictures/vacation

# 大字体红色水印，居中显示
python src/watermark_tool.py ~/Pictures/vacation --size 60 --color red --position center
```

### 高级示例
```bash
# 半透明橙色水印，左上角
python src/watermark_tool.py ~/Pictures/vacation \
    --size 42 \
    --color "#FF6B35" \
    --position top-left \
    --opacity 150

# 专业摄影作品水印（小字体，低透明度）
python src/watermark_tool.py ~/Pictures/portfolio \
    --size 28 \
    --color "200,200,200" \
    --position bottom-right \
    --opacity 120
```

### 批处理脚本

**Windows (batch file)**
```batch
@echo off
echo 正在处理 2023 年照片...
python src/watermark_tool.py "C:\Photos\2023" --size 40 --color white

echo 正在处理 2024 年照片...
python src/watermark_tool.py "C:\Photos\2024" --size 40 --color white

echo 处理完成！
pause
```

**macOS/Linux (shell script)**
```bash
#!/bin/bash
echo "正在处理照片目录..."

for dir in ~/Pictures/*/; do
    echo "处理目录: $dir"
    python src/watermark_tool.py "$dir" --size 38 --color white --position bottom-right
done

echo "所有目录处理完成！"
```

## 🔧 工作原理

1. **扫描目录** - 识别所有支持的图片文件（.jpg, .jpeg, .png, .tiff, .tif）
2. **提取时间** - 从 EXIF 数据中读取 `DateTime`, `DateTimeOriginal`, `DateTimeDigitized` 等字段
3. **生成水印** - 将日期格式化为 `YYYY-MM-DD` 格式
4. **智能定位** - 根据指定位置和文字尺寸计算最佳坐标
5. **渲染效果** - 添加阴影效果并应用透明度
6. **安全保存** - 在 `原目录名_watermark` 子目录中保存结果

## 📊 输出示例

```
🖼️  图片日期水印工具
📂 输入目录: /Users/john/Pictures/vacation
🎨 字体大小: 36px
🌈 文字颜色: (255, 255, 255)
📍 水印位置: bottom-right
👻 透明度: 200
==================================================
🎯 找到 15 个图片文件
💾 水印图片将保存到: /Users/john/Pictures/vacation/vacation_watermark
--------------------------------------------------
📸 处理: IMG_1001.jpg ... ✅ 完成 [2024-03-15]
📸 处理: IMG_1002.jpg ... ✅ 完成 [2024-03-15]
📸 处理: IMG_1003.jpg ... ✅ 完成 [2024-03-16]
...
--------------------------------------------------
🎉 处理完成! 成功: 15/15
```

## 🧪 运行测试

```bash
# 运行单元测试
python -m pytest tests/

# 或使用内置测试
python tests/test_watermark.py

# 创建测试环境
mkdir test_photos
# 添加一些测试图片到 test_photos 目录
python src/watermark_tool.py test_photos
```

## ❓ 常见问题

<details>
<summary><strong>Q: 提示"找不到图片文件"怎么办？</strong></summary>

**A:** 确保目录中包含支持的图片格式（.jpg, .jpeg, .png, .tiff, .tif）。程序会自动跳过不支持的文件格式。
</details>

<details>
<summary><strong>Q: 水印看不清楚怎么办？</strong></summary>

**A:** 尝试以下调整：
- 调整透明度：`--opacity 255`（完全不透明）
- 更改颜色：深色背景用 `--color white`，浅色背景用 `--color black`
- 增大字体：`--size 48` 或更大
</details>

<details>
<summary><strong>Q: 程序处理速度很慢？</strong></summary>

**A:** 可能的原因和解决方案：
- 图片文件过大：考虑先压缩图片
- 内存不足：一次处理较少的图片
- 磁盘空间不足：清理磁盘空间
</details>

<details>
<summary><strong>Q: 某些图片没有显示正确的日期？</strong></summary>

**A:** 如果图片没有 EXIF 数据，程序会使用文件的修改时间。对于扫描的老照片或经过处理的图片，可能需要手动管理文件时间。
</details>

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 更新日志

### v1.0 (2024-03-XX)
- ✨ 初始版本发布
- 🎨 支持基于 EXIF 的日期水印
- 📁 批量图片处理功能
- 🛡️ 完整的错误处理机制
- 📚 详细的文档和测试用例

<p align="center">
  Made with ❤️ by <a href="https://github.com/Daijin0624">Dai Jin</a>
</p>
