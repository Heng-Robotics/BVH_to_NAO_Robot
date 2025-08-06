#-*-coding:utf-8-*-

import os
import shutil

# 原始文件夹路径
original_folder = "/home/heng/Robot/Dataset/Gesture/beat_english"
# 目标文件夹路径
target_folder = "/home/heng/Robot/Dataset/Gesture/beat_english_wav"

# 创建目标文件夹
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 遍历原始文件夹中的子文件夹
for subdir in os.listdir(original_folder):
    subdir_path = os.path.join(original_folder, subdir)
    if os.path.isdir(subdir_path):
        # 创建目标文件夹中的子文件夹，名称与原始文件夹相同
        target_subdir_path = os.path.join(target_folder, subdir)
        if not os.path.exists(target_subdir_path):
            os.makedirs(target_subdir_path)
        
        # 遍历当前子文件夹中的文件
        for file in os.listdir(subdir_path):
            file_path = os.path.join(subdir_path, file)
            # 复制 .bvh 文件到目标文件夹的相应子文件夹下
            if file.endswith('.wav'):
                shutil.copy(file_path, target_subdir_path)

print("done!!")