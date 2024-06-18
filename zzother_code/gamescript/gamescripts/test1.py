from PIL import Image

# 打开图像
image = Image.open("caigang.jpg")

# 转换为RGB模式（如果图像不是RGB模式）
image = image.convert("RGB")

# 获取图像的像素数据
pixels = image.load()

# 图像的宽度和高度
width, height = image.size

# 遍历每个像素
for y in range(height):
    for x in range(width):
        # 获取当前像素的RGB值
        r, g, b = pixels[x, y]

        # 如果是白色，则替换为蓝色
        if r == 255 and g == 255 and b == 255:
            pixels[x, y] = (0, 0, 255)  # 设置为蓝色

# 保存修改后的图像
image.save("modified_image.jpg")