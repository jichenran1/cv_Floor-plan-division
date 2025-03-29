import cv2
import numpy as np
import os


def reliable_floorplan_segmentation(image_path):
    """可靠的户型图分割方案"""
    # 1. 确保图像正确读取
    img = cv2.imread(image_path)
    if img is None:
        print(f"错误：无法读取图像 {image_path}")
        return None

    # 2. 输出图像尺寸
    print(f"图像尺寸: {img.shape}")

    # 3. 优化预处理流程
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 4. 自适应阈值处理
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 5
    )

    # 5. 形态学操作（确保墙体连接）
    kernel = np.ones((3, 3), np.uint8)
    morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)

    # 6. 查找轮廓（只找内部房间）
    contours, hierarchy = cv2.findContours(
        morph, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
    )

    # 7. 准备结果图像（白色背景）
    result = np.ones_like(img) * 255

    # 8. 定义颜色集
    colors = [
        (255, 150, 50),  # 橙色
        (50, 50, 255),  # 红色
        (50, 255, 50),  # 绿色
        (255, 255, 100),  # 浅黄
        (180, 50, 180),  # 紫色
        (50, 200, 200),  # 青色
    ]

    # 9. 绘制每个房间区域
    room_count = 0
    for i, cnt in enumerate(contours):
        if hierarchy[0][i][3] != -1:  # 只处理内部轮廓
            if cv2.contourArea(cnt) > 500:  # 面积过滤
                # 绘制填充颜色
                color = colors[room_count % len(colors)]
                cv2.drawContours(result, [cnt], -1, color, -1)

                # 绘制边界
                cv2.drawContours(result, [cnt], -1, (0, 0, 0), 2)

                # 标记编号
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.putText(
                    result,
                    f"{room_count+1}",
                    (x + w // 2 - 10, y + h // 2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 0),
                    2,
                )
                room_count += 1

    # 10. 保存结果到原始文件夹
    output_path = os.path.join(os.path.dirname(image_path), "segmented.png")
    cv2.imwrite(output_path, result)

    return result


if __name__ == "__main__":
    root_dir = "colorful"

    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file == "model.png":
                image_path = os.path.join(subdir, file)
                print(f"正在处理图像: {image_path}")
                reliable_floorplan_segmentation(image_path)
