#-*-coding:utf-8-*-
import numpy as np
import math

## class KeypointsToAngles. This class contains methods to receive 3D keypoints and calculate skeleton joint angles  
class KeypointsToAngles(object):
    '''
    # body_mapping = {
            '0':  "HeadEnd",
            '1':  "Neck"
            '2':  "MidShoulder", 
            '3':  "MidHip",
            '4':  "LArm",
            '5':  "LForeArm",
            '6':  "LHand",
            '7':  "LHandIndex",
            '8': "LHandRing",
            '9':  "RArm",
            '10':  "RForeArm",
            '11':  "RHand",
            '12': "HandIndex",
            '13': "RHandRing",
            '14': "LHandIndex1",
            '15': "LHandIndex4",
            '16': "LHandRing1",
            '17': "LHandRing4",
            '18': "RHandIndex1",
            '19': "RHandIndex4",
            '20': "RHandRing1",
            '21': "RHandRing4"}
    '''
    def __init__(self):
        self.start_flag = True 

    ##---------------------  function vector_from_points ----------------------

    #   calculate 3D vector from two points ( vector = P2 - P1 )
    def vector_from_points(self, P1, P2):
        vector = [P2[0] - P1[0], P2[1] - P1[1], P2[2] - P1[2]]
        return vector



    ##----------------    obatin_HeadPitchYaw_angle   -------------------------
    def obatin_HeadPitchYaw_angle(self, P0, P1, P2, P3, P4, P9):
        v_1_0 = self.vector_from_points(P1, P0)
        v_1_2 = self.vector_from_points(P1, P2)
        v_2_0 = self.vector_from_points(P2, P0)
        v_9_4 = self.vector_from_points(P9, P4)
        n_1_0_2 = np.cross(v_1_0, v_1_2)
        Compensation_coefficient_pitch = 1.4
        Compensation_coefficient_yaw = 0.4
        Compensation_pitch_angle = np.pi/20
        # Compensation_yaw_angle = np.pi/10
        
        head_Z = self.vector_from_points(P3, P2) #head Z axis
        head_X = np.cross(v_9_4, head_Z) #head X axis
        head_Y = np.cross(head_Z, head_X) #head Y axis

        cos_angle = np.dot(head_Z, np.cross(head_Y, v_2_0)) / (np.linalg.norm(np.cross(head_Y, v_2_0))*np.linalg.norm(head_Z))
        try:
            HeadPitch = Compensation_coefficient_pitch * (math.acos(cos_angle) - np.pi/2 - Compensation_pitch_angle)
        except ValueError:
            HeadPitch = 0

        if HeadPitch > 0.51:
            HeadPitch = 0.51
        if HeadPitch < -0.67:
            HeadPitch = -0.67

    ##----------------    obatin_HeadYaw_angle   -------------------------
        cos_angle = np.dot(np.cross(v_2_0, head_Z), head_X) / (np.linalg.norm(np.cross(v_2_0, head_Z))*np.linalg.norm(head_X))
        try:
            HeadYaw_angle = Compensation_coefficient_yaw * (np.pi/2 - math.acos(cos_angle))
        except ValueError:
            HeadYaw_angle = 0

        test_angle = np.dot(n_1_0_2, head_X) / (np.linalg.norm(n_1_0_2))*(np.linalg.norm(head_X))
        try:
            intermediate_angle = math.acos(test_angle)
        except ValueError:
            intermediate_angle = np.pi/2

        if intermediate_angle <= np.pi/2 :
            HeadYaw = - HeadYaw_angle 
        else:
            HeadYaw = HeadYaw_angle
        
        if HeadYaw > 2:
            HeadYaw = 2
        if HeadYaw < -2:
            HeadYaw = -2
                    
        return HeadPitch, HeadYaw



    ##--------------------   obtain_LShoulderPitchRoll_angles    ------------------------
    # 
    #   Calculate left shoulder pitch and roll angles
    def obtain_LShoulderPitchRoll_angles(self, P2, P4, P5, P3):
        v_4_2 = self.vector_from_points(P4, P2)
        v_4_5 = self.vector_from_points(P4, P5)

        left_torso_Z = self.vector_from_points(P3, P2) #torso Z axis
        left_torso_X = np.cross(left_torso_Z, v_4_2) #torso X axis
        left_torso_Y = np.cross(left_torso_Z, left_torso_X) #torso Y axis

        #用来判断角度正负
        cos_theta = np.dot(v_4_5, left_torso_Z) / (np.linalg.norm(v_4_5)*np.linalg.norm(left_torso_Z))
        try:
            intermediate_angle = math.acos(cos_theta)
        except ValueError:
            intermediate_angle = np.pi/2
        
        # 计算arm绕y轴的转角，即pitch值
        x = np.dot(left_torso_Z, np.cross(left_torso_Y, v_4_5))/(np.linalg.norm(left_torso_Z) * np.linalg.norm(np.cross(left_torso_Y, v_4_5))) 
        try:
            theta_LSP_module = math.acos(x)
        except ValueError:
            theta_LSP_module = 0

        #在Pepper、NAO机器人中，如果arm和z轴的夹角小于90°，则shoulder pitch值为负
        if intermediate_angle <= np.pi/2 :
            LShoulderPitch = - theta_LSP_module 
        else:
            LShoulderPitch = theta_LSP_module

        if LShoulderPitch > 2.08:
            LShoulderPitch = 2.08
        if LShoulderPitch < -2.08:
            LShoulderPitch = -2.08
    
        # --------------- 计算 LShoulderRoll -----------------
        x = (np.dot(v_4_5, left_torso_Y)) / (np.linalg.norm(v_4_5) * np.linalg.norm(left_torso_Y))
        try:
            LShoulderRoll = (np.pi/2) - math.acos(x)
        except ValueError:
            LShoulderRoll = 0

        if LShoulderRoll > 1.56:
            LShoulderRoll = 1.56
        if LShoulderRoll < 0.1:
            LShoulderRoll = 0.1

        return LShoulderPitch, LShoulderRoll
    


    ##----------------  obtain_RShoulderPitchRoll_angles   ------------------------

    def obtain_RShoulderPitchRoll_angles(self, P2, P9, P10, P3):

        v_9_10 = self.vector_from_points(P9, P10)
        v_2_9 = self.vector_from_points(P2, P9)

        right_torso_Z = self.vector_from_points(P3, P2)# torso Z axis
        right_torso_X = np.cross(right_torso_Z, v_2_9)# torso X axis
        right_torso_Y = np.cross(right_torso_Z,right_torso_X) # torsoY axis
        
        #用来判断角度正负
        x = np.dot(v_9_10, right_torso_Z) / (np.linalg.norm(v_9_10)*np.linalg.norm(right_torso_Z))
        try:
            intermediate_angle = math.acos(x)
        except ValueError:
            intermediate_angle = np.pi/2

        # 计算 RShoulderPitch angle
        x = np.dot(right_torso_Z, np.cross(right_torso_Y, v_9_10))/(np.linalg.norm(right_torso_Z) * np.linalg.norm(np.cross(right_torso_Y, v_9_10)))
        try:
            theta_RSP_module = math.acos(x)
        except ValueError:
            theta_RSP_module = 0

        #在Pepper、NAO机器人中，如果arm和z轴的夹角小于90°，则shoulder pitch值为负
        if intermediate_angle <= np.pi/2 :
            RShoulderPitch = - theta_RSP_module
        else:
            RShoulderPitch = theta_RSP_module

        if RShoulderPitch > 2.08:
            RShoulderPitch = 2.08
        if RShoulderPitch < -2.08:
            RShoulderPitch = -2.08

        # ---------------- 计算RShoulderRoll --------------------
        x = (np.dot(v_9_10, right_torso_Y)) / (np.linalg.norm(v_9_10) * np.linalg.norm(right_torso_Y))
        try:
            RShoulderRoll =  (np.pi/2) - math.acos(x)
        except ValueError:
            RShoulderRoll = np.pi/2

        if RShoulderRoll > -0.1:
            RShoulderRoll = -0.1
        if RShoulderRoll < -1.56:
            RShoulderRoll = -1.56

        return RShoulderPitch, RShoulderRoll



    ##--------------------  obtain_LElbowYawRoll_angle  -----------------

    def obtain_LElbowYawRoll_angle(self, P2, P4, P5, P6):
        # Construct 3D vectors (bones) from points
        v_5_6 = self.vector_from_points(P5, P6)
        v_2_4 = self.vector_from_points(P2, P4)

        left_arm_Z = self.vector_from_points(P5, P4) # Left arm Z axis
        left_arm_X = np.cross(v_2_4, left_arm_Z) # Left arm X axis
        left_arm_Y = np.cross(left_arm_Z, left_arm_X)# Left arm Y axis

        # 计算 LElbowYaw angle
        x = np.dot(left_arm_X, np.cross(left_arm_Z, v_5_6) ) / (np.linalg.norm(left_arm_X) * np.linalg.norm(np.cross(left_arm_Z, v_5_6) ))
        try:
            theta_LEY_module = math.acos(x)
        except ValueError:
            theta_LEY_module = 0

        x = np.dot(v_5_6, left_arm_X) / (np.linalg.norm(v_5_6) * np.linalg.norm(left_arm_X))
        try:
            intermediate_angle_1 = math.acos(x)
        except ValueError:
            intermediate_angle_1 = np.pi/2
 
        x = np.dot(v_5_6, left_arm_Y) / (np.linalg.norm(v_5_6) * np.linalg.norm(left_arm_Y))
        try:
            intermediate_angle_2 = math.acos(x)
        except ValueError:
            intermediate_angle_2 = np.pi/2

        # Choice of the correct LElbowYaw angle using intermediate angles values
        if intermediate_angle_1 <= np.pi/2:
            LElbowYaw = -theta_LEY_module 
        else:
            if intermediate_angle_2 > np.pi/2:
                LElbowYaw = theta_LEY_module 
            elif intermediate_angle_2 <= np.pi/2:
                LElbowYaw = theta_LEY_module

        if LElbowYaw > 2.08:
            LElbowYaw = 2.08
        if LElbowYaw < -2.08:
            LElbowYaw = -2.08

        # --------  Formula for LElbowRoll angle ---------
        x = np.dot(v_5_6, left_arm_Z) / (np.linalg.norm(v_5_6) * np.linalg.norm(left_arm_Z))
        try:
            LElbowRoll = math.acos(x) - np.pi
        except ValueError:
            LElbowRoll = 0
        
        if LElbowRoll > -0.1:
            LElbowRoll = -0.1
        if LElbowRoll < -1.56:
            LElbowRoll = -1.56

        return LElbowYaw, LElbowRoll


 
    ##----------------  function obtain_RElbowYawRoll_angle  ---------------

    def obtain_RElbowYawRoll_angle(self, P2, P9, P10, P11):
        v_10_11 = self.vector_from_points(P10, P11)
        v_2_9 = self.vector_from_points(P2, P9)
        
        left_arm_Z = self.vector_from_points(P10, P9)# Left arm Z axis
        left_arm_X = np.cross(v_2_9, left_arm_Z)# Left arm X axis
        left_arm_Y = np.cross(left_arm_Z, left_arm_X)  # Left arm Y axis

        #计算RElbowYaw angle
        x = np.dot(left_arm_X, np.cross(left_arm_Z, v_10_11)) / (np.linalg.norm(left_arm_X) * np.linalg.norm(np.cross(left_arm_Z, v_10_11)))
        try:
            theta_REY_module = math.acos(x)
        except ValueError:
            theta_REY_module = 0

        #判断RElbowYaw angle符号
        x = np.dot(v_10_11, left_arm_X) / (np.linalg.norm(v_10_11) * np.linalg.norm(left_arm_X))
        try:
            intermediate_angle_1 = math.acos(x)
        except ValueError:
            intermediate_angle_1 =  np.pi/2

        x = np.dot(v_10_11, left_arm_Y) / (np.linalg.norm(v_10_11) * np.linalg.norm(left_arm_Y))
        try:
            intermediate_angle_2 = math.acos(x)
        except ValueError:
            intermediate_angle_2 =  np.pi/2

        if intermediate_angle_1 <= np.pi/2:
            RElbowYaw = -theta_REY_module
        else:
            if intermediate_angle_2 > np.pi/2:
                RElbowYaw = theta_REY_module
            elif intermediate_angle_2 <= np.pi/2:
                RElbowYaw = theta_REY_module 

        if RElbowYaw > 2.08:
            RElbowYaw = 2.08
        if RElbowYaw < -2.08:
            RElbowYaw = -2.08
        
        #---------   Formula for RElbowRoll angle     ------------------
        x = np.dot(v_10_11, left_arm_Z) / (np.linalg.norm(v_10_11) * np.linalg.norm(left_arm_Z))
        try:
            RElbowRoll =  np.pi - math.acos(x)
        except ValueError:
            RElbowRoll =  0

        if RElbowRoll > 1.56:
            RElbowRoll = 1.56
        if RElbowRoll < 0.1:
            RElbowRoll = 0.1

        return RElbowYaw, RElbowRoll
    



    ##---------------------   obatin_LWristYaw_angle    --------------------------------
    def obatin_LWristYaw_angle(self, P4, P5, P6, P7, P8):
     # Construct 3D vectors (bones) from points
        v_4_5 = self.vector_from_points(P4, P5)
        v_8_7 = self.vector_from_points(P8, P7)

        left_hand_Z = self.vector_from_points(P6, P5)
        left_hand_X = np.cross(v_4_5, left_hand_Z)
        left_hand_Y = np.cross(left_hand_Z, left_hand_X)

        cos_angle = np.dot(left_hand_X, np.cross(left_hand_Z, v_8_7)) / (np.linalg.norm(np.cross(left_hand_Z, v_8_7))*np.linalg.norm(left_hand_X))
        try:
            LWristYaw_angle = math.acos(cos_angle)
        except ValueError:
            LWristYaw_angle = 0

        cos_angle = np.dot(left_hand_Y, np.cross(left_hand_Z, v_8_7)) / (np.linalg.norm(np.cross(left_hand_Z, v_8_7)))*(np.linalg.norm(left_hand_Y))
        try:
            intermediate_angle = math.acos(cos_angle)
        except ValueError:
            intermediate_angle = np.pi/2

        if intermediate_angle <= np.pi/2 :
            LWristYaw = - LWristYaw_angle 
        else:
            LWristYaw = LWristYaw_angle

        if LWristYaw > 1.8:
            LWristYaw = 1.8
        if LWristYaw < -1.8:
            LWristYaw = -1.8

        return LWristYaw
    


    ##------------------    obatin_RWristYaw_angle   -----------------------------------
    def obatin_RWristYaw_angle(self, P9, P10, P11, P12, P13):
     # Construct 3D vectors (bones) from points
        v_10_9 = self.vector_from_points(P10, P9)
        v_12_13 = self.vector_from_points(P12, P13)

        right_hand_Z = self.vector_from_points(P11, P10)
        right_hand_X = np.cross(v_10_9, right_hand_Z)
        right_hand_Y = np.cross(right_hand_Z, right_hand_X)

        cos_angle = np.dot(right_hand_X, np.cross(right_hand_Z, v_12_13)) / (np.linalg.norm(np.cross(right_hand_Z, v_12_13))*np.linalg.norm(right_hand_X))
        try:
            RWristYaw_angle = math.acos(cos_angle)
        except ValueError:
            RWristYaw_angle = 0

        cos_angle = np.dot(right_hand_Y, np.cross(right_hand_Z, v_12_13)) / (np.linalg.norm(np.cross(right_hand_Z, v_12_13))*np.linalg.norm(right_hand_Y))
        try:
            intermediate_angle = math.acos(cos_angle)
        except ValueError:
            intermediate_angle = np.pi/2

        if intermediate_angle <= np.pi/2 :
            RWristYaw = - RWristYaw_angle 
        else:
            RWristYaw = RWristYaw_angle

        if RWristYaw > 1.8:
            RWristYaw = 1.8
        if RWristYaw < -1.8:
            RWristYaw = -1.8

        return RWristYaw
    



    ##----------------    obatin_LHand_angle   -------------------------
    def obatin_LHand_angle(self, P7, P8, P14, P15, P16, P17):
        v_7_14 = self.vector_from_points(P7, P14)
        v_14_15 = self.vector_from_points(P14, P15)
        v_8_16 = self.vector_from_points(P8, P16)
        v_16_17 = self.vector_from_points(P16, P17)

        Coefficient = -1.5
        Compensation_coefficient = 0.9
        cos_angle1 = np.dot(v_7_14, v_14_15) / (np.linalg.norm(v_7_14)*np.linalg.norm(v_14_15))
        cos_angle2 = np.dot(v_8_16, v_14_15) / (np.linalg.norm(v_8_16)*np.linalg.norm(v_16_17))

        try:
            #把两组夹角取平均值
            LHead_angle = 0.5 * (math.acos(cos_angle1) + math.acos(cos_angle2))
        except ValueError:
            LHead_angle = 0

        #把夹角平均值映射到[0, 1]
        LHand = Compensation_coefficient * (np.exp(Coefficient * LHead_angle))

        return LHand



    ##----------------    obatin_RHand_angle   -------------------------
    def obatin_RHand_angle(self, P12, P13, P18, P19, P20, P21):
        v_12_18 = self.vector_from_points(P12, P18)
        v_18_19 = self.vector_from_points(P18, P19)
        v_13_20 = self.vector_from_points(P13, P20)
        v_20_21 = self.vector_from_points(P20, P21)

        coefficient = -1.4
        Compensation_coefficient = 0.95
        cos_angle1 = np.dot(v_12_18, v_18_19) / (np.linalg.norm(v_12_18)*np.linalg.norm(v_18_19))
        cos_angle2 = np.dot(v_13_20, v_18_19) / (np.linalg.norm(v_13_20)*np.linalg.norm(v_20_21))

        try:
            #把两组夹角取平均值
            RHead_angle = 0.5 * (math.acos(cos_angle1) + math.acos(cos_angle2))
        except ValueError:
            RHead_angle = 0

        #把夹角平均值映射到[0, 1]
        RHand = Compensation_coefficient * (np.exp(coefficient * RHead_angle))

        return RHand
    