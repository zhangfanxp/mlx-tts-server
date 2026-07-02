# 🎤 MLX Qwen3-TTS Voice Clone

基于 **MLX + Qwen3-TTS + Whisper ASR** 的本地语音克隆系统（支持 Mac M 系列芯片）。

---

## 🚀 项目特点

- 🎙️ 支持 Zero-shot Voice Cloning（上传参考音频）
- 🧠 使用 Qwen3-TTS 进行高质量语音生成
- 🎧 Whisper ASR 自动语音分析
- ⚡ MLX GPU 加速（Apple Silicon 优化）
- 📄 支持长文本自动分段生成
- 🔗 自动合并多段 wav 音频
- 💾 自动按日期生成文件名
- 🖥️ Gradio Web UI（本地可视化）

---

## 📦 技术栈

- MLX (Apple Silicon AI Framework)
- mlx-audio
- Qwen3-TTS (0.6B Base)
- Whisper Large V3 Turbo (ASR)
- Gradio
- Python 3.10+

---

## 📁 项目结构

```
mlx-tts-server/
├── run.py              # 主程序
├── utils.py            # 工具函数
├── output/             # 生成音频
├── requirements.txt
└── README.md
```

---

## ⚙️ 环境要求

- macOS (Apple Silicon：M1/M2/M3/M4/M5)
- Python 3.10 ~ 3.11
- 内存 ≥ 16GB（推荐 32GB）

---

## 📥 安装依赖

```bash
pip install -r requirements.txt
```

---

## 🚀 运行项目

```bash
python run.py
```

访问：

http://127.0.0.1:7860

---

## 🎤 使用方法

1. 上传参考音频（用于克隆音色）
2. 输入需要生成的文本
3. 点击「生成语音」
4. 自动生成 wav 文件并支持下载

---

## 📦 输出文件格式

生成文件自动存储在：

output/

命名规则：

20260702_0001.wav
20260702_0002.wav

---

## 🧠 技术说明

### Voice Clone 流程

参考音频 → Whisper ASR → Qwen3-TTS → 音频生成 → 自动合并

---

### 长文本处理

- 自动按 300 字分段
- 分段生成语音
- 自动拼接 wav

---

### MLX GPU 加速

- Apple Metal GPU 推理
- 本地运行，无需云 API
- 低延迟 TTS

---

## ⚠️ 已知限制

- 首次加载模型较慢
- 长文本生成耗时较长
- 依赖 ffmpeg 合并音频（brew install ffmpeg）

---

## 🛠 常见问题

### 音频只生成一半？
已启用自动分段生成

### GPU Stream error？
已修复 MLX + Gradio 线程问题

### 文件未生成？
自动 fallback chunk 合并

---

## 🔥 Roadmap

- OpenAI API 兼容接口
- streaming TTS
- 多音色系统
- Redis缓存
- R2存储
- Next.js 播放器
- Docker部署

---

## 📜 License

MIT
