#-*-coding:utf-8-*-

import numpy as np
import pandas as pd
import keypointstoangles
import os

keypointsToAngles = keypointstoangles.KeypointsToAngles()

def moving_average_filter(data, window_size, padding='edge'):
    padded_data = np.pad(data, (window_size//2, window_size//2-1), mode=padding)
    filtered_data = np.convolve(padded_data, np.ones(window_size) / window_size, mode='valid')
    return filtered_data

def gesture_angles(csv_file):
    df = pd.read_csv(csv_file)

    # #----------   angle lists  -------------------
    time_list = []
    LShoulderPitch_list = []
    LShoulderRoll_list = []
    RShoulderPitch_list = []
    RShoulderRoll_list = []
    LElbowYaw_list = []
    LElbowRoll_list = []
    RElbowYaw_list = []
    RElbowRoll_list = []
    LWristYaw_list = []
    RWristYaw_list = []
    HeadPitch_list = []
    HeadYaw_list = []
    LHand_list = []
    RHand_list = []

    window_size = 10

    # #----------   Command angles  -------------------
    time_list = df['Time'].values.tolist()
    Hips_X = df['Hips.X'].values.tolist()
    Hips_Y = df['Hips.Y'].values.tolist()
    Hips_Z = df['Hips.Z'].values.tolist()
    HeadEnd_X = df['HeadEnd.X'].values.tolist()
    HeadEnd_Y = df['HeadEnd.Y'].values.tolist()
    HeadEnd_Z = df['HeadEnd.Z'].values.tolist()
    Neck_X = df['Neck1.X'].values.tolist()
    Neck_Y = df['Neck1.Y'].values.tolist()
    Neck_Z = df['Neck1.Z'].values.tolist()
    LeftShoulder_X = df['LeftShoulder.X'].values.tolist()
    LeftShoulder_Y = df['LeftShoulder.Y'].values.tolist()
    LeftShoulder_Z = df['LeftShoulder.Z'].values.tolist()

    LeftArm_X = df['LeftArm.X'].values.tolist()
    LeftArm_Y = df['LeftArm.Y'].values.tolist()
    LeftArm_Z = df['LeftArm.Z'].values.tolist()
    LeftForeArm_X = df['LeftForeArm.X'].values.tolist()
    LeftForeArm_Y = df['LeftForeArm.Y'].values.tolist()
    LeftForeArm_Z = df['LeftForeArm.Z'].values.tolist()
    LeftHand_X = df['LeftHand.X'].values.tolist()
    LeftHand_Y = df['LeftHand.Y'].values.tolist()
    LeftHand_Z = df['LeftHand.Z'].values.tolist()
    LeftHandIndex_X = df['LeftHandIndex.X'].values.tolist()
    LeftHandIndex_Y = df['LeftHandIndex.Y'].values.tolist()
    LeftHandIndex_Z = df['LeftHandIndex.Z'].values.tolist()
    LeftHandIndex1_X = df['LeftHandIndex1.X'].values.tolist()
    LeftHandIndex1_Y = df['LeftHandIndex1.Y'].values.tolist()
    LeftHandIndex1_Z = df['LeftHandIndex1.Z'].values.tolist()
    LeftHandIndex4_X = df['LeftHandIndex4.X'].values.tolist()
    LeftHandIndex4_Y = df['LeftHandIndex4.Y'].values.tolist()
    LeftHandIndex4_Z = df['LeftHandIndex4.Z'].values.tolist()
    LeftHandRing_X = df['LeftHandRing.X'].values.tolist()
    LeftHandRing_Y = df['LeftHandRing.Y'].values.tolist()
    LeftHandRing_Z = df['LeftHandRing.Z'].values.tolist()
    LeftHandRing1_X = df['LeftHandRing1.X'].values.tolist()
    LeftHandRing1_Y = df['LeftHandRing1.Y'].values.tolist()
    LeftHandRing1_Z = df['LeftHandRing1.Z'].values.tolist()
    LeftHandRing4_X = df['LeftHandRing4.X'].values.tolist()
    LeftHandRing4_Y = df['LeftHandRing4.Y'].values.tolist()
    LeftHandRing4_Z = df['LeftHandRing4.Z'].values.tolist()

    RightArm_X = df['RightArm.X'].values.tolist()
    RightArm_Y = df['RightArm.Y'].values.tolist()
    RightArm_Z = df['RightArm.Z'].values.tolist()
    RightForeArm_X = df['RightForeArm.X'].values.tolist()
    RightForeArm_Y = df['RightForeArm.Y'].values.tolist()
    RightForeArm_Z = df['RightForeArm.Z'].values.tolist()
    RightHand_X = df['RightHand.X'].values.tolist()
    RightHand_Y = df['RightHand.Y'].values.tolist()
    RightHand_Z = df['RightHand.Z'].values.tolist()
    RightHandIndex_X = df['RightHandIndex.X'].values.tolist()
    RightHandIndex_Y = df['RightHandIndex.Y'].values.tolist()
    RightHandIndex_Z = df['RightHandIndex.Z'].values.tolist()
    RightHandIndex1_X = df['RightHandIndex1.X'].values.tolist()
    RightHandIndex1_Y = df['RightHandIndex1.Y'].values.tolist()
    RightHandIndex1_Z = df['RightHandIndex1.Z'].values.tolist()
    RightHandIndex4_X = df['RightHandIndex4.X'].values.tolist()
    RightHandIndex4_Y = df['RightHandIndex4.Y'].values.tolist()
    RightHandIndex4_Z = df['RightHandIndex4.Z'].values.tolist()
    RightHandRing_X = df['RightHandRing.X'].values.tolist()
    RightHandRing_Y = df['RightHandRing.Y'].values.tolist()
    RightHandRing_Z = df['RightHandRing.Z'].values.tolist()
    RightHandRing1_X = df['RightHandRing1.X'].values.tolist()
    RightHandRing1_Y = df['RightHandRing1.Y'].values.tolist()
    RightHandRing1_Z = df['RightHandRing1.Z'].values.tolist()
    RightHandRing4_X = df['RightHandRing4.X'].values.tolist()
    RightHandRing4_Y = df['RightHandRing4.Y'].values.tolist()
    RightHandRing4_Z = df['RightHandRing4.Z'].values.tolist()


    for i in range(len(Hips_X)):

        pHead = [HeadEnd_X[i], HeadEnd_Y[i],HeadEnd_Z[i]]
        pNeck = [Neck_X[i], Neck_Y[i],Neck_Z[i]]
        pMidShoulder = [LeftShoulder_X[i], LeftShoulder_Y[i],LeftShoulder_Z[i]]
        pHip = [Hips_X[i], Hips_Y[i],Hips_Z[i]]
        pL_Arm = [LeftArm_X[i], LeftArm_Y[i],LeftArm_Z[i]]
        pL_ForeArm = [LeftForeArm_X[i], LeftForeArm_Y[i],LeftForeArm_Z[i]]
        pL_Hand = [LeftHand_X[i], LeftHand_Y[i],LeftHand_Z[i]]
        pL_Index = [LeftHandIndex_X[i], LeftHandIndex_Y[i],LeftHandIndex_Z[i]]
        pL_Index1 = [LeftHandIndex1_X[i], LeftHandIndex1_Y[i],LeftHandIndex1_Z[i]]
        pL_Index4 = [LeftHandIndex4_X[i], LeftHandIndex4_Y[i],LeftHandIndex4_Z[i]]
        pL_Ring = [LeftHandRing_X[i], LeftHandRing_Y[i],LeftHandRing_Z[i]]
        pL_Ring1 = [LeftHandRing1_X[i], LeftHandRing1_Y[i],LeftHandRing1_Z[i]]
        pL_Ring4 = [LeftHandRing4_X[i], LeftHandRing4_Y[i],LeftHandRing4_Z[i]]
        pR_Arm = [RightArm_X[i], RightArm_Y[i],RightArm_Z[i]]
        pR_ForeArm = [RightForeArm_X[i], RightForeArm_Y[i],RightForeArm_Z[i]]
        pR_Hand = [RightHand_X[i], RightHand_Y[i],RightHand_Z[i]]  
        pR_Index = [RightHandIndex_X[i], RightHandIndex_Y[i],RightHandIndex_Z[i]]
        pR_Index1 = [RightHandIndex1_X[i], RightHandIndex1_Y[i],RightHandIndex1_Z[i]]
        pR_Index4 = [RightHandIndex4_X[i], RightHandIndex4_Y[i],RightHandIndex4_Z[i]]
        pR_Ring = [RightHandRing_X[i], RightHandRing_Y[i],RightHandRing_Z[i]]
        pR_Ring1 = [RightHandRing1_X[i], RightHandRing1_Y[i],RightHandRing1_Z[i]]
        pR_Ring4 = [RightHandRing4_X[i], RightHandRing4_Y[i],RightHandRing4_Z[i]]


        LShoulderPitch, LShoulderRoll = keypointsToAngles.obtain_LShoulderPitchRoll_angles(pMidShoulder, pL_Arm, pL_ForeArm, pHip)
        RShoulderPitch, RShoulderRoll = keypointsToAngles.obtain_RShoulderPitchRoll_angles(pMidShoulder, pR_Arm, pR_ForeArm, pHip)
        LElbowYaw, LElbowRoll = keypointsToAngles.obtain_LElbowYawRoll_angle(pMidShoulder, pL_Arm, pL_ForeArm, pL_Hand)
        RElbowYaw, RElbowRoll = keypointsToAngles.obtain_RElbowYawRoll_angle(pMidShoulder, pR_Arm, pR_ForeArm, pR_Hand)
        LWristYaw = keypointsToAngles.obatin_LWristYaw_angle(pL_Arm, pL_ForeArm, pL_Hand, pL_Index, pL_Ring)
        RWristYaw = keypointsToAngles.obatin_RWristYaw_angle(pR_Arm, pR_ForeArm, pR_Hand, pR_Index, pR_Ring)
        HeadPitch, HeadYaw = keypointsToAngles.obatin_HeadPitchYaw_angle(pHead, pNeck, pMidShoulder, pHip, pL_Arm, pR_Arm)
        LHand = keypointsToAngles.obatin_LHand_angle(pL_Index, pL_Ring, pL_Index1, pL_Index4, pL_Ring1, pL_Ring4)
        RHand = keypointsToAngles.obatin_RHand_angle(pR_Index, pR_Ring, pR_Index1, pR_Index4, pR_Ring1, pR_Ring4)

        LShoulderPitch_list.append(LShoulderPitch)
        LShoulderRoll_list.append(LShoulderRoll)
        LElbowYaw_list.append(LElbowYaw)
        LElbowRoll_list.append(LElbowRoll)
        RShoulderPitch_list.append(RShoulderPitch)
        RShoulderRoll_list.append(RShoulderRoll)
        RElbowYaw_list.append(RElbowYaw)
        RElbowRoll_list.append(RElbowRoll)
        LWristYaw_list.append(LWristYaw)
        RWristYaw_list.append(RWristYaw)
        HeadPitch_list.append(HeadPitch)
        HeadYaw_list.append(HeadYaw)
        LHand_list.append(LHand)
        RHand_list.append(RHand)

    angle_list = [LShoulderPitch_list, LShoulderRoll_list, LElbowYaw_list, LElbowRoll_list,
                        RShoulderPitch_list, RShoulderRoll_list, RElbowYaw_list, RElbowRoll_list,
                        LWristYaw_list, RWristYaw_list, HeadPitch_list, HeadYaw_list, LHand_list, RHand_list]

    angle_list_new = []
    for angle in angle_list:
        angle_filter = moving_average_filter(angle, window_size, padding='edge')
        angle_list_new.append(angle_filter)

    angles = {'Time': time_list,
                        'LShoulderPitch': angle_list_new[0], 'LShoulderRoll': angle_list_new[1], 
                        'LElbowYaw': angle_list_new[2], 'LElbowRoll': angle_list_new[3],
                        'RShoulderPitch': angle_list_new[4], 'RShoulderRoll': angle_list_new[5],
                        'RElbowYaw': angle_list_new[6], 'RElbowRoll': angle_list_new[7],
                        'LWristYaw': angle_list_new[8], 'RWristYaw': angle_list_new[9],
                        'HeadPitch': angle_list_new[10], 'HeadYaw': angle_list_new[11],
                        'LHand': angle_list_new[12], 'RHand': angle_list_new[13]}
    
    return angles


select_column_path = "/home/heng/Robot/Dataset/Gesture/select_column"
gesture_path = "/home/heng/Robot/Dataset/Gesture/gesture"

folders = [f.path for f in os.scandir(select_column_path) if f.is_dir()]
for folder in folders:
    folder_name = os.path.basename(folder)

    gesture_subfolder_path = os.path.join(gesture_path, folder_name)
    if not os.path.exists(gesture_subfolder_path):
        os.makedirs(gesture_subfolder_path)
    
    csv_files = [f.path for f in os.scandir(folder) if f.is_file() and f.name.endswith('.csv')]

    for csv_file in csv_files:
        angles = gesture_angles(csv_file)
        
        # Save processed angles to gesture folder
        gesture_csv_path = os.path.join(gesture_subfolder_path, os.path.basename(csv_file))
        pd.DataFrame.from_dict(angles).to_csv(gesture_csv_path, index=False)
    print(str(folder) + ' done!!!')


