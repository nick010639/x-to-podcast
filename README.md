# X Video to Podcast 🎧

把 X 上的英文视频转换为中文播客，随时随地听起来！

## 功能

- 📥 从 X/Twitter 下载视频
- 🎙️ 用 Whisper 本地语音识别
- 🌐 免费 Google Translate 翻译成中文
- 🔊 免费 edge-tts 生成中文语音
- 📱 移动端友好的网页播放器

## 免费技术栈

| 模块 | 技术 | 费用 |
|------|------|------|
| 视频提取 | yt-dlp | 免费 |
| 语音识别 | faster-whisper | 免费 (本地) |
| 翻译 | deep-translator | 免费 |
| TTS | edge-tts (微软) | 免费 |
| 前端 | HTML + JS | 免费 |
| 后端 | FastAPI | 免费 |

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

requirements.txt:
```
yt-dlp
faster-whisper
ffmpeg
deep-translator
edge-tts
fastapi
uvicorn
```

### 2. 运行后端

```bash
cd backend
python api.py
```

后端运行在 http://localhost:8000

### 3. 打开前端

直接在浏览器打开 `frontend/index.html`

或者使用静态服务器：

```bash
cd frontend
python -m http.server 3000
```

然后访问 http://localhost:3000

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/process` | POST | 处理视频 URL |
| `/list` | GET | 获取播客列表 |
| `/audio/{id}` | GET | 获取音频文件 |
| `/transcript/{id}` | GET | 获取文字稿 |

## 本地测试

```bash
# 测试 pipeline
cd backend
python pipeline.py "https://x.com/i/status/XXXXX"
```

## 目录结构

```
x-to-podcast/
├── backend/
│   ├── api.py          # FastAPI 后端
│   ├── pipeline.py     # 处理流程
│   ├── translate_free.py
│   ├── tts_free.py
│   └── requirements.txt
├── frontend/
│   └── index.html      # 播放器页面
├── data/               # 音视频存储
└── README.md
```

## 部署到 Vercel

1. 把前端部署到 Vercel (static hosting)
2. 后端需要自托管 (本地/服务器/VPS)

## 状态

🚧 开发中 - 核心功能已完成
