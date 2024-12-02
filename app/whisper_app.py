import whisper
import os
from datetime import datetime
from pathlib import Path
from opencc import OpenCC

# 初始化繁简转换器
cc = OpenCC('t2s')  # 繁体转简体

def format_timestamp(seconds):
    """将秒数转换为SRT格式时间戳"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def process_transcribe(audio_path, model_size, language, task):
    """处理音频转写"""
    try:
        # 获取当前文件夹路径
        current_dir = Path(audio_path).parent
        
        # 加载模型
        model = whisper.load_model(model_size)
        
        # 转写音频
        result = model.transcribe(
            audio_path,
            language=None if language == "auto" else language,
            task=task
        )
        
        # 获取转写文本并转换为简体中文
        transcribed_text = result["text"]
        if language in ["zh", "auto"]:
            transcribed_text = cc.convert(transcribed_text)
        
        # 生成输出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = Path(audio_path).stem
        output_base = f"{base_name}_{timestamp}"
        
        # 保存文本文件到当前文件夹
        txt_path = current_dir / f"{output_base}.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(transcribed_text)
            
        # 保存SRT字幕文件到当前文件夹
        srt_path = current_dir / f"{output_base}.srt"
        if "segments" in result:
            with open(srt_path, "w", encoding="utf-8") as f:
                for i, segment in enumerate(result["segments"], start=1):
                    start = format_timestamp(segment["start"])
                    end = format_timestamp(segment["end"])
                    text = segment["text"].strip()
                    if language in ["zh", "auto"]:
                        text = cc.convert(text)
                    f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
        
        message = f"转写完成！文件已保存在音频文件所在目录"
        return transcribed_text, message, str(txt_path), str(srt_path)
        
    except Exception as e:
        return "", f"错误: {str(e)}", None, None