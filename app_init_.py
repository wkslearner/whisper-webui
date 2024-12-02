from app.gradio_ui import create_ui

if __name__ == "__main__":
    demo = create_ui()
    demo.launch(share=True, server_name="0.0.0.0")