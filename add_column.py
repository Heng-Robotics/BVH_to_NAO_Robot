#-*-coding:utf-8-*-

import os
import shutil
import pandas as pd

# 定义源文件夹和目标文件夹的路径
source_folder = "/home/heng/Robot/Dataset/Gesture/Gesture_Audio_Process/csv_down_sample"
target_folder = "/home/heng/Robot/Dataset/Gesture/select_column"

# 获取源文件夹下的所有子文件夹名称
subfolders = os.listdir(source_folder)

# 遍历每个子文件夹
for folder in subfolders:
    source_subfolder = os.path.join(source_folder, folder)
    target_subfolder = os.path.join(target_folder, folder)
    
    # 获取当前子文件夹下的所有文件名
    files = os.listdir(source_subfolder)
    
    # 遍历每个文件
    for file in files:
        source_file = os.path.join(source_subfolder, file)
        target_file = os.path.join(target_subfolder, file)
        
        # 读取源文件
        df = pd.read_csv(source_file)
        
        # 选择指定列
        # selected_columns = ['LeftHandIndex4.X', 'LeftHandIndex4.Y', 'LeftHandIndex4.Z',
        #                     'LeftHandRing1.X', 'LeftHandRing1.Y', 'LeftHandRing1.Z',
        #                     'RightHandIndex4.X', 'RightHandIndex4.Y', 'RightHandIndex4.Z',
        #                     'RightHandRing1.X', 'RightHandRing1.Y', 'RightHandRing1.Z']
        selected_columns = ['Time']
        selected_df = df[selected_columns]
        
        # 如果目标文件已存在，读取已有数据
        if os.path.exists(target_file):
            existing_df = pd.read_csv(target_file)
            # 合并新数据到已有数据后面
            updated_df = pd.concat([existing_df, selected_df], axis=1)
            updated_df.to_csv(target_file, index=False)
        else:
            # 直接写入新数据
            selected_df.to_csv(target_file, index=False)
    print(str(file) + ' done!!')
