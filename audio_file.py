#-*-coding:utf-8-*-

import os
import shutil

# 原始文件夹路径
original_csv_path = "/home/heng/Robot/Dataset/Gesture/beat_english_csv"
original_wav_path = "/home/heng/Robot/Dataset/Gesture/beat_english_wav"
# 目标文件夹路径
destination_audio_path = "/home/heng/Robot/Dataset/Gesture/audio"

# 遍历beat_english_csv下的所有子文件夹
for csv_folder_name in os.listdir(original_csv_path):
    csv_folder_path = os.path.join(original_csv_path, csv_folder_name)
    # 如果是文件夹
    if os.path.isdir(csv_folder_path):
        # 构造对应的beat_english_wav子文件夹路径
        wav_folder_path = os.path.join(original_wav_path, csv_folder_name)
        # 如果该子文件夹存在
        if os.path.exists(wav_folder_path):
            # 创建对应的目标文件夹
            destination_folder_path = os.path.join(destination_audio_path, csv_folder_name)
            os.makedirs(destination_folder_path, exist_ok=True)
            # 遍历beat_english_wav子文件夹中的所有文件
            for wav_file_name in os.listdir(wav_folder_path):
                # 如果文件名称和beat_english_csv子文件夹中的文件名称相同（不包含后缀）
                if os.path.splitext(wav_file_name)[0] in [os.path.splitext(csv_file_name)[0] for csv_file_name in os.listdir(csv_folder_path)]:
                    # 构造目标文件路径
                    destination_file_path = os.path.join(destination_folder_path, os.path.splitext(wav_file_name)[0])
                    # 将文件移动到目标文件夹中
                    shutil.move(os.path.join(wav_folder_path, wav_file_name), destination_file_path)
            print("done!")