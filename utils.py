import os
import datetime
import threading
import glob
import subprocess


# =========================
# 文件名生成（线程安全）
# =========================

_lock = threading.Lock()
_counter = {}


def generate_filename(output_dir="output"):
    date = datetime.datetime.now().strftime("%Y%m%d")

    with _lock:
        _counter.setdefault(date, 0)
        _counter[date] += 1
        idx = _counter[date]

    os.makedirs(output_dir, exist_ok=True)

    return os.path.join(output_dir, f"{date}_{idx:04d}.wav")


# =========================
# wav 合并（关键）
# =========================

def merge_wavs(prefix, final_path):
    files = sorted(glob.glob(prefix + "*.wav"))

    if not files:
        return None

    # 单文件直接返回
    if len(files) == 1:
        return files[0]

    list_file = final_path + ".txt"

    with open(list_file, "w") as f:
        for wf in files:
            f.write(f"file '{os.path.abspath(wf)}'\n")

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        final_path
    ])

    return final_path


# =========================
# 文本分段（核心）
# =========================

def split_text(text, max_len=300):
    """
    防止 Qwen3-TTS ICL 截断
    """
    return [text[i:i+max_len] for i in range(0, len(text), max_len)]
