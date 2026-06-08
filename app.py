import gradio as gr
from scripts.query import ask


def handle_query(question: str):
    if not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="The Unofficial Berkeley CS Guide") as demo:
    gr.Markdown("# 🎓 The Unofficial Berkeley CS Guide")
    gr.Markdown(
        "Ask questions about UC Berkeley CS courses and professors. "
        "Answers are grounded in student reviews and course guides — "
        "if the documents don't cover your question, the system will say so."
    )
    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g. What do students say about the workload in CS 61B?",
    )
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=3)
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()
