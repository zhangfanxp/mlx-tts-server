import os
import glob
import gradio as gr
import mlx.core as mx

from mlx_audio.tts.utils import load_model
from mlx_audio.tts.generate import generate_audio

from utils import generate_filename, merge_wavs, split_text


# =========================
# GPU 初始化（关键）
# =========================

mx.set_default_device(mx.gpu)


# =========================
# output目录
# =========================

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================
# 模型懒加载
# =========================

_model = None

def get_model():
    global _model
    if _model is None:
        print("Loading Qwen3-TTS...")
        _model = load_model(
            "mlx-community/Qwen3-TTS-12Hz-0.6B-Base-8bit"
        )
        print("Model loaded.")
    return _model


# =========================
# TTS核心逻辑（已升级）
# =========================

def tts(ref_audio, text):

    if not ref_audio:
        raise gr.Error("请上传参考音频")

    if not text or not text.strip():
        raise gr.Error("请输入文本")

    model = get_model()

    final_path = generate_filename(OUTPUT_DIR)
    prefix = final_path.replace(".wav", "")

    try:
        # =========================
        # 1. 文本分段（关键）
        # =========================
        segments = split_text(text, max_len=300)

        for i, seg in enumerate(segments):

            seg_prefix = f"{prefix}_{i}"

            generate_audio(
                model=model,
                text=seg,
                ref_audio=ref_audio,
                file_prefix=seg_prefix,

                # ⭐稳定参数
                stt_model="mlx-community/whisper-large-v3-turbo-asr-fp16",
                max_tokens=2000,
            )

    except Exception as e:
        raise gr.Error(f"生成失败: {str(e)}")

    # =========================
    # 2. 合并 wav
    # =========================

    result = merge_wavs(prefix, final_path)

    if not result:
        raise gr.Error("音频生成失败")

    print("Saved:", result)

    return result, result


# =========================
# UI
# =========================

with gr.Blocks(title="Qwen3-TTS Voice Clone") as demo:

    gr.Markdown("# 🎤 Qwen3-TTS Voice Clone（稳定版）")

    ref_audio = gr.Audio(type="filepath", label="参考音频")
    text = gr.Textbox(label="输入文本", lines=6)

    btn = gr.Button("生成语音")

    audio_out = gr.Audio(label="试听")
    file_out = gr.File(label="下载")

    btn.click(
        fn=tts,
        inputs=[ref_audio, text],
        outputs=[audio_out, file_out]
    )


# =========================
# 启动（稳定关键）
# =========================

demo.queue()
demo.launch()
