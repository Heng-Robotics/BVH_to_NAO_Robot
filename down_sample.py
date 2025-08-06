#-*-coding:utf-8-*-

import os
import csv
import shutil

import os
import csv
import shutil

# 定义函数，用于复制每四行数据
def copy_every_four_lines(input_file, output_file):
    with open(input_file, 'r', newline='') as infile, \
         open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        # 复制标题行
        writer.writerow(next(reader))
        count = 0
        for row in reader:
            count += 1
            # 每四行复制一行
            if count % 4 == 0:
                writer.writerow(row)

# 主函数
def main():
    # 源文件夹和目标文件夹路径
    beat_english_csv_path = '/home/heng/Robot/Dataset/Gesture/beat_english_csv'
    csv_down_sample_path = '/home/heng/Robot/Dataset/Gesture/csv_down_sample'

    # 遍历beat_english_csv文件夹下的子文件夹
    for subdir, _, files in os.walk(beat_english_csv_path):
        for file in files:
            # 只处理csv文件
            if file.endswith('.csv'):
                # 构建输入文件路径
                input_file_path = os.path.join(subdir, file)
                # 构建输出文件路径
                output_subdir = os.path.relpath(subdir, beat_english_csv_path)
                output_file_path = os.path.join(csv_down_sample_path, output_subdir, file)

                # 确保输出文件夹存在
                output_folder = os.path.dirname(output_file_path)
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

                # 调用函数复制数据
                copy_every_four_lines(input_file_path, output_file_path)

if __name__ == "__main__":
    main()
