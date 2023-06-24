import os
import gradio as gr
from suggest import Suggest
from edit import Editor
from config import configure_logging
from utils import diff_texts


configure_logging()


with gr.Blocks() as demo:
    
    title = gr.Button("PaperGPT", interactive=True)
    key = gr.Textbox(label="openai_key", value=os.environ.get('OPENAI_API_KEY'))
    
    with gr.Row():
        with gr.Tab("Edit"):

            handler = Editor()
            txt_in = gr.Textbox(label="Input", lines=11, max_lines=11, value=handler.sample_content)
            btn = gr.Button("Edit")
            txt_out = gr.Textbox(label="Output", lines=11, max_lines=11, value="GPT will serve as your editor and modify the paragraph for you.")
            btn.click(handler.generate, inputs=[txt_in, key], outputs=[txt_out])

        with gr.Tab("Suggest"):

            max_ideas = 5
            handler = Suggest(max_ideas)

            def select(name: str):
                for i in handler.idea_list:
                    if i['title'] == name:
                        return [
                            gr.Textbox.update(value=i["thought"], label="thought", visible=True),
                            gr.Textbox.update(value=i["action"], label="action", visible=True),
                            gr.Textbox.update(value=i["original"], label="original", visible=True, max_lines=5, lines=5),
                            gr.Textbox.update(value=i["improved"], label="improved", visible=True, max_lines=5, lines=5),
                            gr.HighlightedText.update(value=diff_texts(i["original"], i["improved"]), visible=True)
                        ]

            with gr.Row().style(equal_height=True):
                with gr.Column(scale=0.95):
                    txt_in = gr.Textbox(label="Input", lines=11, max_lines=11, value=handler.sample_content[2048+2048+256-45:])
                with gr.Column(scale=0.05):
                    upload = gr.File(file_count="single", file_types=["tex", ".pdf"])
                    btn = gr.Button("Analyze")
                    upload.change(handler.read_file, inputs=upload, outputs=txt_in)

            textboxes = []
            sug = gr.Textbox("GPT will give suggestions and help you improve the paper quality.", interactive=False, show_label=False, lines=11).style(text_align="center")
            with gr.Row():
                with gr.Column(scale=0.4):
                    for i in range(max_ideas):
                        t = gr.Button("", visible=False)
                        textboxes.append(t)
                with gr.Column(scale=0.6):
                    thought = gr.Textbox(label="thought", visible=False, interactive=False)
                    action = gr.Textbox(label="action", visible=False, interactive=False)
                    original = gr.Textbox(label="original", visible=False, max_lines=5, lines=5, interactive=False)
                    improved = gr.Textbox(label="improved", visible=False, max_lines=5, lines=5, interactive=False)
                    diff = gr.HighlightedText(
                        label="Diff",
                        combine_adjacent=True,
                        show_legend=True,
                        visible=False,
                        max_lines=5,
                        lines=5,
                        interactive=False
                    ).style(color_map={"+": "green", "-": "red"})

            btn.click(handler.generate, inputs=[txt_in, key], outputs=[sug, btn, thought, action, original, improved] + textboxes)
            for i in textboxes:
                i.click(select, inputs=[i], outputs=[thought, action, original, improved, diff])
            
    with gr.Row():
        with gr.Tab("Issue"):
            gr.Textbox(show_label=False, value="https://github.com/j40903272/PaperGPT/issues", interactive=False)
        with gr.Tab("Author"):
            gr.JSON(show_label=False, value={'author': 'YDTsai', 'email': 'bb04902103@gmail.com', 'source': 'https://github.com/j40903272/PaperGPT'})

    demo.launch(server_name="0.0.0.0", server_port=7653, share=True, enable_queue=True)
    # demo.launch(enable_queue=True)
