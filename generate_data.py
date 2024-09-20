from PIL import Image
import numpy as np
import plotly.graph_objects as go

# 读取图片并转换为256x64大小的灰度图
image = Image.open('test.jpg').convert('L')
# 获取图像的宽度和高度
width, height = image.size

if width < height:
    image = image.rotate(90, expand=True)

aspect_ratio = width / height

if aspect_ratio > 256 / 64:
    # 如果宽高比大于256/64，则以宽度为基准
    new_width = 256
    new_height = int(256 / aspect_ratio)
else:
    # 否则以高度为基准
    new_height = 64
    new_width = int(64 * aspect_ratio)

# 缩放图像
#image = image.resize((new_width, new_height))

# 创建一个256x64的黑色背景图像
padded_image = Image.new('L', (256, 64), color=0)

# 计算粘贴图像的位置，使其居中
x_offset = (256 - image.width) // 2
y_offset = (64 - image.height) // 2

# 将缩放后的图像粘贴到背景图像上
padded_image.paste(image, (x_offset, y_offset))

# 将图片转换为numpy数组
binary_image = np.array(image.resize((256,64)))
print("1   ",binary_image.shape)
# 将灰度图转换为二值化图像，阈值设为256，得到0或1的矩阵
threshold = 128
binary_image = np.array(binary_image) > threshold
binary_image = binary_image.astype(np.uint8)
print("2   ",binary_image.shape)
# 创建一个带有 0 和 1 的矩阵（0表示黑色，1表示白色）
# 使用plotly绘制这张点阵图
fig = go.Figure(data=go.Heatmap(
    z=binary_image,
    colorscale=[(0, 'black'), (1, 'white')],  # 0 对应黑色，1 对应白色
    showscale=False  # 隐藏色标
))

# 设置图表的外观
fig.update_layout(
    title="256x64点阵图",
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False),
    width=800,
    height=500,
    margin=dict(l=20, r=20, t=40, b=20)
)

# 保存点阵图为图片文件 (PNG格式)
fig.write_image("dot_matrix_image.png")

# 定义块的大小
block_height, block_width = 8, 8

# 计算块的行列数
rows_in_blocks = binary_image.shape[0] // block_height
cols_in_blocks = binary_image.shape[1] // block_width

# 初始化结果列表
result_blocks = []

# 遍历每个块
for row in range(rows_in_blocks):
    for col in range(cols_in_blocks):
        # 提取当前块 8x8
        block = binary_image[row*block_height:(row+1)*block_height, col*block_width:(col+1)*block_width]
        
        # 转换为每行8个像素组成一个字节
        block_bytes = bytearray()
        for i in range(block_height):
            byte = 0
            # 将每一行的8个bit转换为一个字节
            for bit in range(block_width):
                byte |= (block[i, bit] << (7 - bit))  # 高位在前，低位在后
            block_bytes.append(byte)
        
        # 将每个块转换为bytearray格式并保存
        result_blocks.append(block_bytes)


from lcd2usb import LCD,SMILE_SYMBOL,LCD_CTRL_1,LCD_CTRL_0,LCD_DATA,LCD_BOTH
lcd = LCD()
lcd.set_contrast(20)
lcd.set_contrast(20)
lcd.clear()

# 打印结果，每个块8个字节
for block_index, block in enumerate(result_blocks):

    base_address = 0x40 | (0 << 3)
    lcd.command(base_address)
    lcd.write(block)

    if block_index > 191:
        lcd.write_char(0, block_index -192, 3)
    elif block_index > 127:
        lcd.write_char(0, block_index - 128, 2)
    elif block_index > 63:
        lcd.write_char(0, block_index - 64, 1)
    else:
        lcd.write_char(0, block_index , 0)





