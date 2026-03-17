#!/usr/bin/env python3
"""
应用图标生成器
生成 Windows、macOS、Linux 三个平台的应用图标
"""

from PIL import Image, ImageDraw
import os

def create_icon(size, bg_color=(33, 150, 243)):
    """
    创建基础图标
    
    Args:
        size: 图标尺寸
        bg_color: 背景色 (R, G, B)
    """
    # 创建圆角矩形背景
    img = Image.new('RGBA', (size, size), (*bg_color, 255))
    draw = ImageDraw.Draw(img)
    
    # 绘制圆角矩形
    radius = size // 5
    draw.rounded_rectangle(
        [(0, 0), (size-1, size-1)], 
        radius=radius, 
        fill=(*bg_color, 255)
    )
    
    # 绘制文档图标（白色）
    doc_color = (255, 255, 255)
    doc_width = size // 2
    doc_height = size // 2.5
    doc_x = (size - doc_width) // 2
    doc_y = (size - doc_height) // 2 - size // 10
    
    # 文档主体
    draw.rectangle(
        [doc_x, doc_y, doc_x + doc_width, doc_y + doc_height],
        fill=doc_color
    )
    
    # 文档折叠角
    fold_size = size // 10
    draw.polygon([
        (doc_x + doc_width - fold_size, doc_y),
        (doc_x + doc_width, doc_y + fold_size),
        (doc_x + doc_width - fold_size, doc_y + fold_size)
    ], fill=(200, 200, 200))
    
    # 绘制整理箭头（橙色）
    arrow_color = (255, 152, 0)
    arrow_size = size // 8
    arrow_y = doc_y + doc_height + size // 10
    
    # 左箭头
    draw.polygon([
        (doc_x, arrow_y),
        (doc_x + arrow_size, arrow_y - arrow_size // 2),
        (doc_x + arrow_size, arrow_y + arrow_size // 2)
    ], fill=arrow_color)
    
    # 右箭头
    draw.polygon([
        (doc_x + doc_width, arrow_y),
        (doc_x + doc_width - arrow_size, arrow_y - arrow_size // 2),
        (doc_x + doc_width - arrow_size, arrow_y + arrow_size // 2)
    ], fill=arrow_color)
    
    # 文档线条
    line_height = size // 30
    line_gap = size // 15
    line_start = doc_x + size // 20
    line_end = doc_x + doc_width - size // 20
    
    for i in range(3):
        y = doc_y + size // 8 + i * line_gap
        draw.rectangle(
            [line_start, y, line_end, y + line_height],
            fill=(200, 200, 200)
        )
    
    return img

def generate_windows_icons():
    """生成 Windows .ico 图标"""
    print("生成 Windows 图标...")
    
    sizes = [16, 32, 48, 256]
    images = []
    
    for size in sizes:
        img = create_icon(size)
        images.append(img)
    
    # 保存为 .ico
    images[-1].save(
        'icon.ico',
        format='ICO',
        sizes=[(size, size) for size in sizes]
    )
    print("✓ Windows 图标生成完成: icon.ico")

def generate_macos_icons():
    """生成 macOS .icns 图标"""
    print("生成 macOS 图标...")
    
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    images = []
    
    for size in sizes:
        img = create_icon(size)
        img.save(f'icon_{size}x{size}.png')
        images.append(img)
    
    # 保存为 .icns（需要使用 iconutil 或 png2icns）
    print("✓ macOS 图标生成完成: icon_*.png")
    print("  提示: 使用 iconutil 转换为 .icns")
    print("  命令: iconutil -c icns icon.iconset")

def generate_linux_icons():
    """生成 Linux .png 图标"""
    print("生成 Linux 图标...")
    
    sizes = [128, 256, 512]
    
    for size in sizes:
        img = create_icon(size)
        img.save(f'icon_{size}x{size}.png')
    
    print("✓ Linux 图标生成完成: icon_*.png")

def main():
    """主函数"""
    output_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(output_dir)
    
    print("=" * 50)
    print("简历整理工具 - 图标生成器")
    print("=" * 50)
    print()
    
    try:
        generate_windows_icons()
        print()
        generate_macos_icons()
        print()
        generate_linux_icons()
        
        print()
        print("=" * 50)
        print("所有图标生成完成！")
        print("=" * 50)
        
    except Exception as e:
        print(f"错误: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
