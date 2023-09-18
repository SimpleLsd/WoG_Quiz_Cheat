from PIL import Image
import os

# 输入图片文件夹路径和输出文件夹路径
source_folder = 'input_folder'
output_folder = 'output_folder'

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 裁剪框的坐标和尺寸（左上角坐标 x, y 和裁剪框的宽度和高度）
crop_box = (90, 18, 237 + 90, 158 + 18)

# 遍历输入文件夹中的所有图片文件
for filename in os.listdir(source_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # 打开源图片
        with Image.open(os.path.join(source_folder, filename)) as img:
            # 裁剪图片
            cropped_img = img.crop(crop_box)

            # 保存裁剪后的图片到目标文件夹，使用BILINEAR插值方法
            output_path = os.path.join(output_folder, filename)
            cropped_img.save(output_path, interpolation=Image.BILINEAR)

print("批量裁剪完成！")
