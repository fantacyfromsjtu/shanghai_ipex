import os
import subprocess
from pydub import AudioSegment
import json


def get_audio_stream(video_file, languages=("上海话", "沪语")):
    """
    自动检测指定语言的音轨索引。
    如果视频只有一个音轨，则直接选择该音轨。
    :param video_file: 视频文件路径
    :param languages: 目标音轨的标题列表
    :return: 音轨索引字符串（如 0:1）
    """
    try:
        command = [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "a",
            "-show_entries",
            "stream=index:stream_tags=title",
            "-of",
            "json",
            video_file,
        ]
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            encoding="utf-8",
        )
        streams = json.loads(result.stdout).get("streams", [])

        # 如果只有一个音轨，直接返回第一个音轨
        if len(streams) == 1:
            return f"0:{streams[0]['index']}"

        # 查找匹配的音轨标题
        for stream in streams:
            title = stream.get("tags", {}).get("title", "")
            if title in languages:
                return f"0:{stream['index']}"

        # 如果没有找到匹配的语言音轨，抛出错误
        raise ValueError(f"未找到标题为 {languages} 的音轨")

    except json.JSONDecodeError as e:
        raise ValueError(f"无法解析 ffprobe 输出，请检查 ffprobe 是否可用：{e}")
    except subprocess.CalledProcessError as e:
        raise ValueError(f"ffprobe 命令执行失败，请检查视频文件：{e}")


def extract_audio_from_video(video_file, audio_file, audio_stream):
    """
    从指定的视频中提取音轨。
    :param video_file: 视频文件路径
    :param audio_file: 输出音频文件路径
    :param audio_stream: 指定的音轨索引（如 0:1）
    """
    command = [
        "ffmpeg",
        "-i",
        video_file,
        "-map",
        f"{audio_stream}",
        "-q:a",
        "0",
        audio_file,
    ]
    subprocess.run(command, check=True)
    print(f"提取音频到 {audio_file} (音轨: {audio_stream})")


def parse_srt(srt_file):
    """解析 SRT 文件并提取时间戳和字幕"""
    with open(srt_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    segments = []
    index = 0

    while index < len(lines):
        if lines[index].strip().isdigit():
            # 检查时间戳是否包含有效的分隔符
            timestamp = lines[index + 1].strip()
            if " --> " not in timestamp:
                print(f"跳过无效时间戳: {timestamp}")
                index += 4  # 跳过该条字幕
                continue

            # 提取时间戳
            start_time, end_time = timestamp.split(" --> ")
            start_time = convert_to_milliseconds(start_time)
            end_time = convert_to_milliseconds(end_time)

            # 提取字幕
            subtitle = lines[index + 2].strip()
            segments.append((start_time, end_time, subtitle))
            index += 4
        else:
            index += 1

    return segments


def convert_to_milliseconds(timestamp):
    """将时间戳（hh:mm:ss,ms）转换为毫秒"""
    h, m, s = timestamp.split(":")
    s, ms = s.split(",")
    return (int(h) * 3600 + int(m) * 60 + int(s)) * 1000 + int(ms)


def split_audio(audio_file, srt_file, output_folder, video_name, buffer=300):
    """根据 SRT 文件的时间戳拆分音频"""
    # 加载音频
    audio = AudioSegment.from_file(audio_file)

    # 解析 SRT 文件
    segments = parse_srt(srt_file)

    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    for i, (start_time, end_time, subtitle) in enumerate(segments):
        # 添加缓冲时间，确保分割更精准
        adjusted_start_time = max(0, start_time - buffer)
        adjusted_end_time = min(len(audio), end_time + buffer)

        # 提取音频片段
        segment = audio[adjusted_start_time:adjusted_end_time]

        # 保存音频文件
        audio_filename = os.path.join(output_folder, f"{video_name}_{i + 1:03d}.wav")
        segment.export(audio_filename, format="wav")

        # 保存字幕文件
        subtitle_filename = os.path.join(output_folder, f"{video_name}_{i + 1:03d}.txt")
        with open(subtitle_filename, "w", encoding="utf-8") as f:
            f.write(subtitle)

        print(f"Saved {audio_filename} and {subtitle_filename}")


def process_videos(
    video_folder, srt_folder, output_folder, languages=("上海话", "沪语")
):
    """主程序，处理所有视频"""
    for video_file in os.listdir(video_folder):
        # 检查文件是否为 mp4 或 mkv 格式
        if video_file.endswith(".mp4") or video_file.endswith(".mkv"):
            video_path = os.path.join(video_folder, video_file)
            video_name, _ = os.path.splitext(video_file)  # 去掉文件扩展名

            # 检查是否已经处理过
            video_output_folder = os.path.join(output_folder, video_name)
            if os.path.exists(video_output_folder):
                print(f"跳过已处理的文件夹: {video_output_folder}")
                continue

            # 找到对应的 SRT 文件
            srt_file = os.path.join(srt_folder, f"{video_name}.srt")
            if not os.path.exists(srt_file):
                print(f"未找到 {video_name} 的 SRT 文件，跳过...")
                continue

            # 创建视频的输出文件夹
            os.makedirs(video_output_folder, exist_ok=True)

            # 检测音轨索引
            try:
                audio_stream = get_audio_stream(video_path, languages=languages)
            except ValueError as e:
                print(e)
                continue

            # 提取音频文件
            audio_file = os.path.join(video_output_folder, f"{video_name}.wav")
            extract_audio_from_video(video_path, audio_file, audio_stream)

            # 拆分音频和字幕
            split_audio(audio_file, srt_file, video_output_folder, video_name)


if __name__ == "__main__":
    # 定义文件夹路径
    video_folder = "video"  # 存放视频文件的文件夹
    srt_folder = "srt"  # 存放 SRT 文件的文件夹
    output_folder = "split"  # 输出文件夹

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 处理视频文件，提取 "上海话" 或 "沪语" 音轨
    process_videos(
        video_folder, srt_folder, output_folder, languages=("上海话", "沪语")
    )
