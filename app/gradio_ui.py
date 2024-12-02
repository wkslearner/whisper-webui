import gradio as gr
from .whisper_app import process_transcribe

def create_ui():
    with gr.Blocks(title="Whisper WebUI - 音频转写工具") as interface:
        gr.Markdown("# 🎙️ Whisper WebUI - 音频转写工具")
        gr.Markdown("使用 OpenAI 的 Whisper 模型进行音频转写和翻译")
        
        with gr.Row():
            with gr.Column():
                # 输入选项
                audio_input = gr.Audio(
                    label="上传音频文件",
                    type="filepath"
                )
                
                model_size = gr.Dropdown(
                    choices=["tiny", "base", "small", "medium", "large"],
                    value="base",
                    label="选择模型大小",
                    info="模型越大，准确度越高，但处理速度越慢"
                )
                
                language = gr.Dropdown(
                    choices=["auto", "zh", "en", "ja", "ko"],
                    value="auto",
                    label="选择音频语言",
                    info="auto 为自动检测"
                )
                
                task = gr.Radio(
                    choices=["transcribe", "translate"],
                    value="transcribe",
                    label="选择任务类型",
                    info="transcribe: 转写原文 | translate: 翻译为英文"
                )
                
                process_btn = gr.Button("开始处理", variant="primary")
            
            with gr.Column():
                # 输出区域
                text_output = gr.Textbox(
                    label="转写结果",
                    lines=10,
                    show_copy_button=True
                )
                
                status_output = gr.Textbox(
                    label="状态信息",
                    lines=3
                )
                
                with gr.Row():
                    # 下载按钮
                    txt_download = gr.File(
                        label="下载文本文件",
                        visible=True
                    )
                    srt_download = gr.File(
                        label="下载字幕文件",
                        visible=True
                    )
        
        # 处理按钮事件
        process_btn.click(
            fn=process_transcribe,
            inputs=[
                audio_input,
                model_size,
                language,
                task
            ],
            outputs=[
                text_output,
                status_output,
                txt_download,
                srt_download
            ]
        )
        
        # 使用说明
        gr.Markdown("""
        ## 📝 使用说明
        1. 上传音频文件（支持多种格式）
        2. 选择合适的模型大小（建议先用 base 测试）
        3. 选择音频语言（如果不确定可选择 auto）
        4. 选择任务类型：
           - transcribe：转写为原始语言文本
           - translate：翻译为英文
        5. 点击"开始处理"按钮
        6. 使用下载按钮获取结果文件
        
        ## ⚠️ 注意事项
        - 大型模型需要较长处理时间
        - 建议上传质量较好的音频以获得更好的效果
        - 中文结果会自动转换为简体中文
        """)
    
    return interface

# 创建并启动界面
if __name__ == "__main__":
    demo = create_ui()
    demo.launch(share=True, server_name="0.0.0.0")