import os
import subprocess


def convert_svg_to_png(svg_path, output_path=None):
    if output_path is None:
        output_path = svg_path.replace(".svg", ".png")

    # 方法1: 使用cairosvg
    try:
        import cairosvg

        cairosvg.svg2png(url=svg_path, write_to=output_path)
        if os.path.exists(output_path):
            return output_path
    except ImportError:
        pass

    # 方法2: 使用inkscape
    try:
        subprocess.run(["inkscape", svg_path, "-o", output_path], check=True)
        if os.path.exists(output_path):
            return output_path
    except:
        pass

    # 方法3: 使用svglib
    try:
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM

        drawing = svg2rlg(svg_path)
        renderPM.drawToFile(drawing, output_path, fmt="PNG")
        return output_path
    except:
        print(f"所有转换方法均失败: {svg_path}")
        return None


def convert_dataset(dataset_path):

    print(f"开始转换数据集，路径: {dataset_path}")

    success_count = 0
    for folder in os.listdir(dataset_path):
        folder_path = os.path.join(dataset_path, folder)
        if os.path.isdir(folder_path):
            svg_path = os.path.join(folder_path, "model.svg")
            if os.path.exists(svg_path):
                print(f"正在转换: {svg_path}")
                png_path = convert_svg_to_png(svg_path)

                if png_path and os.path.exists(png_path):
                    success_count += 1
                    print(f"转换成功: {png_path}")
                else:
                    print(f"转换失败: {svg_path}")

    print(f"\n转换完成。成功转换 {success_count} 个文件。")
    if success_count == 0:
        print("没有成功转换任何文件！")


if __name__ == "__main__":
    dataset_path = "colorful"
    if not os.path.exists(dataset_path):
        print(f"错误: 数据集路径不存在: {dataset_path}")
    else:
        convert_dataset(dataset_path)
