import os

print("文件对比-------------------------------------------------------------------")

# 定义两个文件夹的路径
folder_A = 'output_folder'
folder_B = 'options'

# 获取文件夹A中的所有文件名（去掉后缀）
files_in_folder_A = set(os.path.splitext(
    file)[0] for file in os.listdir(folder_A))

# 遍历文件夹B中的文件名（去掉后缀），找出不在文件夹A中的文件
files_not_in_folder_A = []
for file_B in os.listdir(folder_B):
    file_B_base, _ = os.path.splitext(file_B)
    if file_B_base not in files_in_folder_A:
        files_not_in_folder_A.append(file_B)

# 打印文件夹B中不在文件夹A中的文件名
for file_name in files_not_in_folder_A:
    print(file_name)
