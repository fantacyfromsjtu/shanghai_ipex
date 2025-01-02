# # -*- coding: utf-8 -*-
# # @Author : yxn
# # @Date : 2022/10/22 17:11 
# # @IDE : PyCharm(2022.2.3) Python3.9.13
# """
# wav.scp wav_id --- wav_path 音频id对于音频路径
# """
# import os


# def sava_data(data, filename):
#     """保存文件函数"""
#     with open(os.path.join(save_path, filename), 'w', encoding="utf-8") as f:
#         for i in data:
#             f.writelines(i[0] + " " + i[1] + "\n")

#     print("%s Saving succeeded!" % filename)


# def get_wav_scp():
#     """该函数用于生成wav.scp"""
#     wav_scp = []  # 存放wav_scp 的数据
#     # 遍历音频
#     for file_name in os.listdir(data_path):
#         # 判断后缀名是否为wav
#         if file_name[-3:] == "wav":
#             wav_scp.append([file_name.split(".")[0], os.path.join(data_path, file_name)])

#     # 保存到文件
#     sava_data(wav_scp, "wav.scp")


# if __name__ == '__main__':
#     # 数据文件存放路径
#     data_path = r"C:\Users\陈楠\Desktop\Shanghaiese_dataset\WAV\WAV"
#     # 保存的路径
#     save_path = r"C:\Users\陈楠\Desktop\Shanghaiese_dataset\WAV" 
#     # 生成wav.scp
#     get_wav_scp()














# -*- coding: utf-8 -*-
# @Author : yxn
# @Date : 2022/10/22 17:11 
# @IDE : PyCharm(2022.2.3) Python3.9.13
# """
# wav_id --- speaker_id 音频文件名对应说话人id
# """
# import os


# def save_data(data, filename):
#     """保存文件"""
#     with open(os.path.join(save_path, filename), "w", encoding="utf-8") as f:
#         for i in data:
#             f.writelines(i + "\n")

#     print("%s Saving succeeded!" % filename)


# def get_utt2spk():
#     """生成utt2spk"""
#     utt2spk = []
#     for filename in os.listdir(data_path):
#         if filename[-3:] == "wav":
#             utt = filename.split(".")[0]  # 音频id
#             spk = utt[-10:-5]  # 说话人id
#             utt2spk.append(utt + " " + spk)

#     # 保存文件
#     save_data(utt2spk, "utt2spk")


# if __name__ == '__main__':
#     # 数据文件存放路径
#     data_path = r"C:\Users\陈楠\Desktop\Shanghaiese_dataset\WAV\WAV"  # /root/kaldi/data/S0/
#     # 保存的路径
#     save_path = r"C:\Users\陈楠\Desktop\Shanghaiese_dataset\WAV"  # /root/kaldi/data/kaldi_file/
#     # 生成utt2spk
#     get_utt2spk()





















# -*- coding: utf-8 -*-
# @Author : yxn
# @Date : 2022/10/22 17:11 
# @IDE : PyCharm(2022.2.3) Python3.9.13
# """
# speaker_id --- wav_id 说话人id对应音频文件名
# """
# import os


# def save_data(data, filename):
#     """保存文件"""
#     with open(os.path.join(save_path, filename), "w", encoding="utf-8") as f:
#         for i in data:
#             f.writelines(i + "\n")

#     print("%s Saving succeeded!" % filename)


# def get_spk2utt():
#     """生成spk2utt"""
#     spk2utt = {}
#     for filename in os.listdir(data_path):
#         if filename[-3:] == "wav":
#             utt = filename.split(".")[0]  # 音频id
#             spk = utt[-10:-5]  # 说话人id
#             if spk in spk2utt:
#                 spk2utt[spk].append(utt)
#             else:
#                 spk2utt[spk] = []
#     # {'S0150': ['BAC009S0150W0002', 'BAC009S0150W0003',...'BAC009S0252W0500'],
#     # 'S0252': ['BAC009S0252W0002', 'BAC009S0252W0003',... 'BAC009S0252W0500'] }

#     write_spk2utt = []
#     for key in spk2utt.keys():
#         write_spk2utt.append(str(key) + " " + " ".join(spk2utt[key]))

#     # 保存到文件
#     save_data(write_spk2utt, "spk2utt")


# if __name__ == '__main__':
#     # 数据文件存放路径
#     data_path = r"C:\Users\陈楠\Desktop\Shanghaiese_dataset\WAV\WAV"  # /root/kaldi/data/S0/
#     # 保存的路径
#     save_path = r"C:\Users\陈楠\Desktop\Shanghaiese_dataset\WAV" # /root/kaldi/data/kaldi_file/
#     # 生成spk2utt
#     get_spk2utt()

# -*- coding: utf-8 -*-
# @Author : yxn
# @Date : 2022/10/2 19:55 
# @IDE : PyCharm(2022.2.1) Python3.9.13



