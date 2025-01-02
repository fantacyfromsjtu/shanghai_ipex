import os
# import signal
import paddle
from paddlespeech.cli.tts import TTSExecutor
from IPython import display
from datetime import datetime
from IPython.display import Audio, display, clear_output, HTML

tts_executor = TTSExecutor()

def extract_chinese_from_file(file_path, output_path=None):
    chinese_lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            chinese_lines.append(line)
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write('\n'.join(chinese_lines))
    return chinese_lines


# input_file = 'your_input_file.txt' 
# chinese_content = extract_chinese_from_file(input_file)
# chinese_lines = []
# cnt = 0

texts = '你好你好你好'

# with open(input_file, 'r', encoding='utf-8') as file:
#     for line in file:
#         cnt += 1

current_time = datetime.now()
time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

wav_file = tts_executor(
    text='你好呀',
    output=f'./output/output.wav',
    am='fastspeech2_csmsc', # csmsc
    am_config=None,
    am_ckpt=None,
    am_stat=None,
    spk_id=0,
    phones_dict=None,
    tones_dict=None,
    speaker_dict=None,
    voc='pwgan_csmsc',
    voc_config=None,
    voc_ckpt=None,
    voc_stat=None,
    lang='zh',
    device=paddle.get_device())

# display.Audio(f'./output/output.wav')
# clear_output(wait=True)
# audio = Audio(filename='./output/output.wav')
# display(audio)

# wav_file = os.path.abspath('./output/output.wav')
# playsound(wav_file)

wav_path = './output/output.wav'
os.system(f'start {wav_path}')