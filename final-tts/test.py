from paddlespeech.cli.tts import TTSExecutor
import paddle

# 初始化 TTSExecutor
tts_executor = TTSExecutor()

# 测试输入文本
text = "你好呀"

# 设置输出文件名
output_file = "./output.wav"

# 调用 TTSExecutor
wav_file = tts_executor(
    text=text,
    output=output_file,
    am="fastspeech2_csmsc",  # 声学模型
    voc="pwgan_csmsc",       # 声码器
    lang="zh",               # 语言
    spk_id=None,             # 单说话人模型
    device="cpu"             # 指定 CPU 或 GPU
)

print(f"语音文件保存在: {wav_file}")
