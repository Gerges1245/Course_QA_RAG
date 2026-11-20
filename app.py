
import gradio as gr
from rag_core import rag_answer, COURSES


# ==========================================
# 1. Suggested Questions
# ==========================================

SUGGESTIONS = {
    "Python Programming": [
        "What is a Python function?",
        "What is a Python list?",
        "Explain Python dictionaries."
    ],
    "Database Systems": [
        "What is a primary key?",
        "What is database normalization?",
        "What is an ER model?"
    ],
    "Computer Networks": [
        "What is an IP address?",
        "What is a computer network?",
        "Explain network routing."
    ]
}


# ==========================================
# 2. Welcome Message
# ==========================================

def welcome_messages(course="Python Programming"):
    return [
        {
            "role": "assistant",
            "content": (
                "👋 **Welcome to Course AI Assistant!**\n\n"
                f"📚 Selected Course: **{course}**\n\n"
                "I'm ready to answer questions using "
                "your course materials.\n\n"
                "You can type a question below or "
                "choose one of the suggested questions.\n\n"
                "My answers include retrieved source "
                "references whenever available."
            )
        }
    ]


# ==========================================
# 3. Format Sources
# ==========================================

def format_sources(sources):

    if not sources:
        return ""

    lines = [
        "\n\n---",
        "### 📚 Retrieved Sources",
        ""
    ]

    for i, source in enumerate(sources, 1):

        filename = str(
            source.get("source", "Unknown")
        ).replace("`", "")

        file_type = source.get(
            "type", "Unknown"
        )

        page = source.get("page", -1)

        page_label = (
            f"Page {page}"
            if isinstance(page, int) and page >= 1
            else "Page unavailable"
        )

        # Short text preview
        preview = " ".join(
            source.get("text", "").split()
        )[:200]

        lines.append(
            f"**[Source {i}]** "
            f"`{filename}` | "
            f"**{file_type}** | {page_label}"
        )

        if preview:
            lines.append(
                f"> {preview}..."
            )

        lines.append("")

    return "\n\n".join(lines)


# ==========================================
# 4. Add Student Message
# ==========================================

def add_user_message(message, history):

    history = list(history or [])

    if not message or not message.strip():
        return history, ""

    history.append({
        "role": "user",
        "content": message.strip()
    })

    return history, ""



def normalize_question(content):

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, str):
                parts.append(item)

            elif isinstance(item, dict):
                text = item.get("text", "")

                if isinstance(text, str):
                    parts.append(text)

        return " ".join(parts).strip()

    raise TypeError(
        f"Unsupported question type: {type(content)}"
    )

# ==========================================
# 5. Generate RAG Answer
# ==========================================

def generate_answer(
    history,
    selected_course,
    file_type
):

    history = list(history or [])

    if not history:
        return history

    if history[-1]["role"] != "user":
        return history

    
    question = normalize_question(
        history[-1]["content"]
    )

    if not question:
        history.append({
            "role": "assistant",
            "content": "Please enter a valid question."
        })
        return history

    print("Question:", question)
    print("Question Type:", type(question))


    try:

        answer, sources = rag_answer(
            question,
            COURSES[selected_course],
            file_type
        )

        # Add retrieved sources
        if sources:
            answer += format_sources(sources)

        history.append({
            "role": "assistant",
            "content": answer
        })

    
    except Exception as e:
        import traceback

        print("\n========== RAG ERROR ==========")
        traceback.print_exc()
        print("================================\n")

        history.append({
            "role": "assistant",
            "content": (
                "⚠️ **An error occurred.**\n\n"
                "Check the VS Code terminal for details."
            )
        })


    return history


# ==========================================
# 6. Clear Chat
# ==========================================

def clear_chat(course):
    return welcome_messages(course), ""


# ==========================================
# 7. Reset When Course Changes
# ==========================================

def on_course_change(course):

    questions = SUGGESTIONS[course]

    return (
        welcome_messages(course),
        "",
        gr.update(value=questions[0]),
        gr.update(value=questions[1]),
        gr.update(value=questions[2])
    )


# ==========================================
# 8. Custom CSS
# ==========================================

CUSTOM_CSS = """
.gradio-container {
    max-width: 1600px !important;
    margin: auto !important;
    padding: 18px 28px !important;
}

#hero {
    background: linear-gradient(
        120deg,
        #102b50,
        #185a9d
    );
    border-radius: 20px;
    padding: 28px 36px;
    margin-bottom: 22px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

#hero h1 {
    color: white !important;
    font-size: 32px !important;
}

#hero p {
    color: #e4efff !important;
    font-size: 15px !important;
}

#sidebar {
    border-radius: 16px;
    padding: 18px;
    background: #172238;
}

#course-chat {
    border-radius: 16px;
    overflow: hidden;
}

#question-input {
    border-radius: 12px;
}

#footer {
    text-align: center;
    margin-top: 24px;
    opacity: 0.75;
}

@media (max-width: 768px) {
    .gradio-container {
        padding: 12px !important;
    }

    #hero {
        padding: 18px;
    }

    #hero h1 {
        font-size: 23px !important;
    }
}
"""


# ==========================================
# 9. Build Gradio Interface
# ==========================================

with gr.Blocks(
    title="Course AI Assistant",
    fill_width=True
) as demo:

    # ---------- Header ----------

    gr.Markdown(
        """
        # 🎓 Course AI Assistant

        Your intelligent learning companion.
        Ask questions from your course materials
        and get AI-powered answers with references.
        """,
        elem_id="hero"
    )

    with gr.Row(equal_height=False):

        # ---------- Sidebar ----------

        with gr.Column(
            scale=1,
            min_width=290,
            elem_id="sidebar"
        ):

            gr.Markdown("## ⚙️ Course Settings")

            course = gr.Dropdown(
                choices=list(COURSES.keys()),
                value="Python Programming",
                label="Select Course",
                interactive=True
            )

            file_type = gr.Dropdown(
                choices=[
                    "All Files",
                    "PDF",
                    "DOCX",
                    "CSV",
                    "TXT"
                ],
                value="All Files",
                label="File Type",
                interactive=True
            )

            clear_btn = gr.Button(
                "🗑️ Clear Chat",
                variant="secondary"
            )

            gr.Markdown(
                """
                ---

                ### 📚 Available Courses

                🐍 **Python Programming**

                🗄️ **Database Systems**

                🌐 **Computer Networks**

                ---

                ### 💡 How It Works

                1. Select your course.
                2. Choose the file type.
                3. Ask a question.
                4. Read the answer and sources.

                ---

                ### ✅ System Features

                - Semantic Search
                - Context-Based Answers
                - Source Attribution
                - Multi-Format Support
                - Gemini AI
                """
            )

        # ---------- Chat Section ----------

        with gr.Column(
            scale=4,
            min_width=420
        ):

            gr.Markdown("## 💬 Ask Your Course")

            chatbot = gr.Chatbot(
                value=welcome_messages(),
                height=570,
                layout="bubble",
                show_label=False,
                elem_id="course-chat",
                buttons=["copy"]
            )

            # Message Input
            with gr.Row():

                message = gr.Textbox(
                    placeholder=(
                        "Ask a question about "
                        "your course..."
                    ),
                    show_label=False,
                    lines=2,
                    max_lines=4,
                    scale=8,
                    elem_id="question-input"
                )

                send_btn = gr.Button(
                    "➤ Send",
                    variant="primary",
                    scale=1,
                    min_width=110
                )

            # Suggested Questions
            gr.Markdown(
                "### ✨ Suggested Questions"
            )

            with gr.Row():

                q1 = gr.Button(
                    SUGGESTIONS[
                        "Python Programming"
                    ][0],
                    variant="secondary"
                )

                q2 = gr.Button(
                    SUGGESTIONS[
                        "Python Programming"
                    ][1],
                    variant="secondary"
                )

                q3 = gr.Button(
                    SUGGESTIONS[
                        "Python Programming"
                    ][2],
                    variant="secondary"
                )

    # ======================================
    # 10. Event Handlers
    # ======================================

    # Send button
    send_event = send_btn.click(
        fn=add_user_message,
        inputs=[message, chatbot],
        outputs=[chatbot, message],
        queue=False
    )

    send_event.then(
        fn=generate_answer,
        inputs=[chatbot, course, file_type],
        outputs=chatbot
    )

    # Enter key
    submit_event = message.submit(
        fn=add_user_message,
        inputs=[message, chatbot],
        outputs=[chatbot, message],
        queue=False
    )

    submit_event.then(
        fn=generate_answer,
        inputs=[chatbot, course, file_type],
        outputs=chatbot
    )

    # Clear chat button
    clear_btn.click(
        fn=clear_chat,
        inputs=course,
        outputs=[chatbot, message],
        queue=False
    )

    # Auto clear when course changes
    course.change(
        fn=on_course_change,
        inputs=course,
        outputs=[
            chatbot,
            message,
            q1,
            q2,
            q3
        ],
        queue=False
    )

    # Auto clear when file type changes
    file_type.change(
        fn=clear_chat,
        inputs=course,
        outputs=[chatbot, message],
        queue=False
    )

    # Suggested question buttons
    q1.click(
        fn=lambda c: SUGGESTIONS[c][0],
        inputs=course,
        outputs=message,
        queue=False
    )

    q2.click(
        fn=lambda c: SUGGESTIONS[c][1],
        inputs=course,
        outputs=message,
        queue=False
    )

    q3.click(
        fn=lambda c: SUGGESTIONS[c][2],
        inputs=course,
        outputs=message,
        queue=False
    )

    # ---------- Footer ----------

    gr.Markdown(
        """
        ---
        **Course Q&A RAG System**

        Powered by Sentence Transformers,
        ChromaDB, Gemini AI & Gradio
        """,
        elem_id="footer"
    )


# ==========================================
# 11. Launch Application
# ==========================================

if __name__ == "__main__":

    demo.queue(
        default_concurrency_limit=1
    )

    demo.launch(
        theme=gr.themes.Soft(),
        css=CUSTOM_CSS,
        inbrowser=True,
        share=False
    )
