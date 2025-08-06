#-*-coding:utf-8-*-

import os

# 目标文件夹路径
target_folder = "/home/heng/Robot/Dataset/Gesture/beat_english_csv"

# 遍历目标文件夹下的子文件夹
for subdir in os.listdir(target_folder):
    subdir_path = os.path.join(target_folder, subdir)
    # 如果是文件夹
    if os.path.isdir(subdir_path):
        # 统计子文件夹下的文件数量
        file_count = len([name for name in os.listdir(subdir_path) if os.path.isfile(os.path.join(subdir_path, name))])
        print(f"子文件夹 {subdir} 中的文件数量为：{file_count}")
