#-*-coding:utf-8-*-

import os
import pandas as pd

# 列名集合
columns_to_copy = ['Hips.X', 'Hips.Y', 'Hips.Z', 'LeftUpLeg.X', 'LeftUpLeg.Y', 'LeftUpLeg.Z',
                   'RightUpLeg.X', 'RightUpLeg.Y', 'RightUpLeg.Z', 'LeftShoulder.X', 'LeftShoulder.Y', 'LeftShoulder.Z',
                   'LeftArm.X', 'LeftArm.Y', 'LeftArm.Z', 'LeftForeArm.X', 'LeftForeArm.Y', 'LeftForeArm.Z',
                   'LeftHand.X', 'LeftHand.Y', 'LeftHand.Z', 'RightShoulder.X', 'RightShoulder.Y', 'RightShoulder.Z',
                   'RightArm.X', 'RightArm.Y', 'RightArm.Z', 'RightForeArm.X', 'RightForeArm.Y', 'RightForeArm.Z',
                   'RightHand.X', 'RightHand.Y', 'RightHand.Z', 'Neck1.X', 'Neck1.Y', 'Neck1.Z',
                   'Head.X', 'Head.Y', 'Head.Z', 'HeadEnd.X', 'HeadEnd.Y', 'HeadEnd.Z']

# 主函数
def main():
    # 源文件夹和目标文件夹路径
    csv_down_sample_path = '/home/heng/Robot/Dataset/Gesture/csv_down_sample'
    select_column_path = '/home/heng/Robot/Dataset/Gesture/select_column'

    # 遍历csv_down_sample文件夹下的子文件夹
    for subdir, _, files in os.walk(csv_down_sample_path):
        for file in files:
            # 只处理csv文件
            if file.endswith('.csv'):
                # 构建输入文件路径
                input_file_path = os.path.join(subdir, file)
                # 构建输出文件路径
                output_subdir = os.path.relpath(subdir, csv_down_sample_path)
                output_file_path = os.path.join(select_column_path, output_subdir, file)

                # 确保输出文件夹存在
                output_folder = os.path.dirname(output_file_path)
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

                # 读取csv文件
                df = pd.read_csv(input_file_path)
                # 选择需要的列
                selected_columns = df[columns_to_copy]
                # 将数据写入输出文件
                selected_columns.to_csv(output_file_path, index=False)

if __name__ == "__main__":
    main()
