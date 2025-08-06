#-*-coding:utf-8-*-

import os
import subprocess
import csv

# 原始文件夹路径
original_folder = "/home/heng/Robot/Dataset/Gesture/beat_english_bvh"

# 遍历原始文件夹中的子文件夹
for subdir, _, files in os.walk(original_folder):
    # 创建CSV文件
    csv_file_path = os.path.join(subdir, 'processing_results.csv')
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File Name', 'Processing Result'])

        # 遍历当前子文件夹中的文件
        for file in files:
            if file.endswith('.bvh'):
                file_path = os.path.join(subdir, file)
                # 获取相对路径
                rel_path = os.path.relpath(file_path, original_folder)
                # 构造命令
                command = f"bvh-converter {rel_path}"
                # 在终端中执行命令
                result = subprocess.run(command, shell=True, cwd=original_folder, capture_output=True, text=True)
                # 写入CSV文件
                if result.returncode == 0:
                    writer.writerow([file, 'success'])
                else:
                    writer.writerow([file, 'fail'])
        print(str(file)+" done!!")