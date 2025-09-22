"""
图片日期水印工具
从图片EXIF信息中提取拍摄日期，并添加为水印
"""
import os
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ExifTags
from datetime import datetime
import sys

# 支持的图片格式
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.tiff', '.tif'}

# 位置映射
POSITIONS = {
    'top-left': lambda w, h, tw, th: (20, 20),
    'top-center': lambda w, h, tw, th: ((w - tw) // 2, 20),
    'top-right': lambda w, h, tw, th: (w - tw - 20, 20),
    'center': lambda w, h, tw, th: ((w - tw) // 2, (h - th) // 2),
    'bottom-left': lambda w, h, tw, th: (20, h - th - 20),
    'bottom-center': lambda w, h, tw, th: ((w - tw) // 2, h - th - 20),
    'bottom-right': lambda w, h, tw, th: (w - tw - 20, h - th - 20),
}


def get_creation_date(image_path):
    """从图片EXIF信息中获取拍摄时间"""
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            if exif_data is not None:
                for tag, value in exif_data.items():
                    tag_name = ExifTags.TAGS.get(tag, tag)
                    if tag_name in ['DateTime', 'DateTimeOriginal', 'DateTimeDigitized']:
                        try:
                            # 解析EXIF时间格式: "YYYY:MM:DD HH:MM:SS"
                            date_obj = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                            return date_obj.strftime("%Y-%m-%d")
                        except ValueError:
                            continue

            # 如果没有EXIF时间信息，使用文件修改时间
            stat = os.stat(image_path)
            date_obj = datetime.fromtimestamp(stat.st_mtime)
            return date_obj.strftime("%Y-%m-%d")

    except Exception as e:
        print(f"读取 {image_path} 时间信息失败: {e}")
        return None


def parse_color(color_str):
    """解析颜色字符串"""
    color_str = color_str.strip().lower()

    # 预定义颜色
    colors = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'orange': (255, 165, 0),
        'purple': (128, 0, 128),
    }

    if color_str in colors:
        return colors[color_str]

    # 尝试解析十六进制颜色
    if color_str.startswith('#'):
        try:
            hex_color = color_str[1:]
            if len(hex_color) == 6:
                return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        except ValueError:
            pass

    # 尝试解析RGB格式
    if ',' in color_str:
        try:
            rgb = [int(x.strip()) for x in color_str.split(',')]
            if len(rgb) == 3 and all(0 <= x <= 255 for x in rgb):
                return tuple(rgb)
        except ValueError:
            pass

    print(f"无法解析颜色 '{color_str}'，使用默认白色")
    return (255, 255, 255)


def add_watermark(image_path, output_path, date_text, font_size=36, color=(255, 255, 255), position='bottom-right',
                  opacity=200):
    """为图片添加日期水印"""
    try:
        with Image.open(image_path) as img:
            # 转换为RGBA模式以支持透明度
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            # 创建透明图层
            txt_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt_layer)

            # 尝试加载字体
            try:
                # 尝试系统字体
                if sys.platform.startswith('win'):
                    font_paths = [
                        "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
                        "C:/Windows/Fonts/arial.ttf",
                        "C:/Windows/Fonts/calibri.ttf"
                    ]
                elif sys.platform.startswith('darwin'):  # macOS
                    font_paths = [
                        "/System/Library/Fonts/PingFang.ttc",
                        "/System/Library/Fonts/Arial.ttf",
                        "/System/Library/Fonts/Helvetica.ttc"
                    ]
                else:  # Linux
                    font_paths = [
                        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
                    ]

                font = None
                for font_path in font_paths:
                    if os.path.exists(font_path):
                        font = ImageFont.truetype(font_path, font_size)
                        break

                if font is None:
                    font = ImageFont.load_default()

            except Exception:
                font = ImageFont.load_default()

            # 获取文本尺寸
            bbox = draw.textbbox((0, 0), date_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # 计算位置
            img_width, img_height = img.size
            if position in POSITIONS:
                x, y = POSITIONS[position](img_width, img_height, text_width, text_height)
            else:
                x, y = POSITIONS['bottom-right'](img_width, img_height, text_width, text_height)

            # 添加文字阴影效果
            shadow_color = (0, 0, 0, opacity // 2)
            draw.text((x + 2, y + 2), date_text, font=font, fill=shadow_color)

            # 添加主文字
            text_color = (*color, opacity)
            draw.text((x, y), date_text, font=font, fill=text_color)

            # 合并图层
            watermarked = Image.alpha_composite(img, txt_layer)

            # 如果原图不是RGBA，转换回原格式
            if Image.open(image_path).mode != 'RGBA':
                watermarked = watermarked.convert('RGB')

            # 保存图片
            watermarked.save(output_path, quality=95, optimize=True)
            return True

    except Exception as e:
        print(f"处理图片 {image_path} 失败: {e}")
        return False


def process_directory(input_dir, font_size=36, color=(255, 255, 255), position='bottom-right', opacity=200):
    """处理目录中的所有图片"""
    input_path = Path(input_dir)

    if not input_path.exists():
        print(f"目录不存在: {input_dir}")
        return

    if not input_path.is_dir():
        print(f"不是有效的目录: {input_dir}")
        return

    # 创建输出目录
    output_dir = input_path / f"{input_path.name}_watermark"
    output_dir.mkdir(exist_ok=True)

    # 获取所有支持的图片文件
    image_files = []
    for ext in SUPPORTED_FORMATS:
        image_files.extend(input_path.glob(f"*{ext}"))
        image_files.extend(input_path.glob(f"*{ext.upper()}"))

    if not image_files:
        print(f"在目录 {input_dir} 中未找到支持的图片文件")
        return

    print(f"找到 {len(image_files)} 个图片文件")
    print(f"水印图片将保存到: {output_dir}")
    print("-" * 50)

    success_count = 0

    for img_file in image_files:
        print(f"处理: {img_file.name}", end=" ... ")

        # 获取拍摄日期
        date_text = get_creation_date(img_file)
        if not date_text:
            print("跳过（无法获取日期）")
            continue

        # 输出文件路径
        output_file = output_dir / img_file.name

        # 添加水印
        if add_watermark(img_file, output_file, date_text, font_size, color, position, opacity):
            print(f"完成 [{date_text}]")
            success_count += 1
        else:
            print("失败")

    print("-" * 50)
    print(f"处理完成! 成功: {success_count}/{len(image_files)}")


def main():
    parser = argparse.ArgumentParser(
        description="为图片添加基于EXIF拍摄时间的日期水印",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s /path/to/photos
  %(prog)s /path/to/photos --size 48 --color white --position top-left
  %(prog)s /path/to/photos --color "#FF0000" --opacity 180
  %(prog)s /path/to/photos --color "255,255,0" --position center

支持的位置: top-left, top-center, top-right, center, bottom-left, bottom-center, bottom-right
支持的颜色: white, black, red, green, blue, yellow, orange, purple, #RRGGBB, R,G,B
        """)

    parser.add_argument('directory', help='包含图片的目录路径')
    parser.add_argument('--size', '-s', type=int, default=36, help='字体大小 (默认: 36)')
    parser.add_argument('--color', '-c', default='white', help='文字颜色 (默认: white)')
    parser.add_argument('--position', '-p', default='bottom-right',
                        choices=list(POSITIONS.keys()), help='水印位置 (默认: bottom-right)')
    parser.add_argument('--opacity', '-o', type=int, default=200,
                        help='透明度 0-255 (默认: 200)')

    args = parser.parse_args()

    # 验证参数
    if args.opacity < 0 or args.opacity > 255:
        print("透明度必须在 0-255 之间")
        sys.exit(1)

    if args.size < 1 or args.size > 200:
        print("字体大小必须在 1-200 之间")
        sys.exit(1)

    # 解析颜色
    color = parse_color(args.color)

    print("图片日期水印工具")
    print(f"输入目录: {args.directory}")
    print(f"字体大小: {args.size}px")
    print(f"文字颜色: {color}")
    print(f"水印位置: {args.position}")
    print(f"透明度: {args.opacity}")
    print("=" * 50)

    # 处理目录
    process_directory(args.directory, args.size, color, args.position, args.opacity)


if __name__ == "__main__":
    main()