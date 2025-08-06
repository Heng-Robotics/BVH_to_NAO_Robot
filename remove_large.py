#-*-coding:utf-8-*-

import os
import shutil

# 原始文件夹路径
original_wav_folder = "/home/heng/Robot/Dataset/Gesture/beat_english_wav"
original_bvh_folder = "/home/heng/Robot/Dataset/Gesture/beat_english_bvh"
# 目标文件夹路径
target_wav_folder = "/home/heng/Robot/Dataset/Gesture/beat_english_wav_long"
target_bvh_folder = "/home/heng/Robot/Dataset/Gesture/beat_english_bvh_long"

# 创建目标文件夹
if not os.path.exists(target_wav_folder):
    os.makedirs(target_wav_folder)
if not os.path.exists(target_bvh_folder):
    os.makedirs(target_bvh_folder)

# 遍历原始wav文件夹中的子文件夹
for subdir in os.listdir(original_wav_folder):
    subdir_path = os.path.join(original_wav_folder, subdir)
    if os.path.isdir(subdir_path):
        # 创建目标wav文件夹中的子文件夹，名称与原始文件夹相同
        target_subdir_path = os.path.join(target_wav_folder, subdir)
        if not os.path.exists(target_subdir_path):
            os.makedirs(target_subdir_path)
        
        # 遍历当前子文件夹中的文件
        for file in os.listdir(subdir_path):
            file_path = os.path.join(subdir_path, file)
            # 检查文件大小是否大于10MB
            if os.path.getsize(file_path) > 10 * 1024 * 1024:  # 10MB
                # 移动文件到目标文件夹的相应子文件夹下
                shutil.move(file_path, target_subdir_path)
print("done!")
# 遍历原始bvh文件夹中的子文件夹
for subdir in os.listdir(original_bvh_folder):
    subdir_path = os.path.join(original_bvh_folder, subdir)
    if os.path.isdir(subdir_path):
        # 创建目标bvh文件夹中的子文件夹，名称与原始文件夹相同
        target_subdir_path = os.path.join(target_bvh_folder, subdir)
        if not os.path.exists(target_subdir_path):
            os.makedirs(target_subdir_path)
        
        # 遍历当前子文件夹中的文件
        for file in os.listdir(subdir_path):
            file_path = os.path.join(subdir_path, file)
            # 检查是否存在对应的wav文件
            wav_file_path = os.path.join(target_wav_folder, subdir, file.replace('.bvh', '.wav'))
            if os.path.exists(wav_file_path):
                # 移动文件到目标文件夹的相应子文件夹下
                shutil.move(file_path, target_subdir_path)
print("done!!!!!!")