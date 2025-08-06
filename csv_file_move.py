#-*-coding:utf-8-*-

import os
import shutil

import os
import shutil

# 原始文件夹路径
original_path = "/home/heng/Robot/Dataset/Gesture/beat_english_bvh"
# 目标文件夹路径
destination_path = "/home/heng/Robot/Dataset/Gesture/beat_english_csv"

# 确保目标文件夹存在，如果不存在则创建
if not os.path.exists(destination_path):
    os.makedirs(destination_path)

# 遍历原始文件夹中的所有子文件夹
for folder_name in os.listdir(original_path):
    folder_path = os.path.join(original_path, folder_name)
    # 如果是文件夹
    if os.path.isdir(folder_path):
        # 创建对应的目标文件夹
        destination_folder_path = os.path.join(destination_path, folder_name)
        os.makedirs(destination_folder_path, exist_ok=True)
        # 遍历当前子文件夹中的所有文件
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            # 如果是.csv文件
            if file_name.endswith(".csv"):
                # 构造目标文件名，去掉'_worldpos'
                destination_file_name = file_name.replace("_worldpos", "")
                destination_file_path = os.path.join(destination_folder_path, destination_file_name)
                # 将文件剪切并粘贴到目标文件夹中
                shutil.move(file_path, destination_file_path)
        
        print("finish one!")


print("done!!")