"""
Sarjak's AI/ML Portfolio - FINAL WORKING VERSION
"""
import gradio as gr
from typing import List
from src.ui.custom_css import get_custom_css
from src.agent.conversation import ConversationManager
from src.utils.logger import logger
import config


logger.info("Initializing portfolio...")
conversation_manager = ConversationManager()
logger.info("✅ Ready!")


def welcome_html() -> str:
    """Clean welcome screen"""
    return """
    <div style="max-width: 700px;">
        <h1 style="font-size: 48px; font-weight: 600; margin-bottom: 16px;">
            Hi, I'm Sarjak! 👋
        </h1>
        <p style="font-size: 20px; color: #c5c5d2; margin-bottom: 48px;">
            Data Scientist | AI & ML Engineer
        </p>
        <p style="font-size: 16px; color: #8e8ea0; line-height: 1.8; margin-bottom: 40px;">
            Welcome to my interactive AI portfolio! I'm passionate about building intelligent systems 
            that solve real-world problems. Feel free to ask me anything about my experience, projects, 
            or technical skills.
        </p>
        <div style="padding: 24px; background: rgba(255,255,255,0.03); border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
            <p style="font-size: 14px; color: #8e8ea0; font-style: italic; margin: 0;">
                "Develop a passion for learning. If you do, you will never cease to grow."<br>
                <span style="color: #c5c5d2; font-weight: 500; margin-top: 8px; display: inline-block;">
                    - Anthony J. D'Angelo
                </span>
            </p>
        </div>
    </div>
    """


def format_user_message(content: str) -> str:
    """Format user message - RIGHT ALIGNED"""
    return f"""
    <div class="chat-message user-message">
        <div class="message-bubble">
            <div class="message-text">{content}</div>
            <div class="message-avatar user-avatar">👤</div>
        </div>
    </div>
    """


def format_bot_message(content: str) -> str:
    """Format bot message - LEFT ALIGNED"""
    return f"""
    <div class="chat-message bot-message">
        <div class="message-bubble">
            <div class="message-avatar bot-avatar">🤖</div>
            <div class="message-text">{content}</div>
        </div>
    </div>
    """


def create_app():
    """Create Gradio app"""

    with gr.Blocks(css=get_custom_css(), title=config.APP_TITLE) as app:

        # State
        chat_started = gr.State(False)
        sidebar_open = gr.State(True)

        with gr.Row():

            # SIDEBAR
            with gr.Column(elem_classes="sidebar-column") as sidebar:
                gr.HTML("""
                    <div style="padding: 12px; margin-bottom: 8px;">
                        <div style="font-size: 16px; font-weight: 600;">
                            💬 Sarjak's Portfolio
                        </div>
                    </div>
                """)

                skills_btn = gr.Button("🎯 Skills", elem_classes="nav-item")
                exp_btn = gr.Button("💼 Experience", elem_classes="nav-item")
                proj_btn = gr.Button("🚀 Projects", elem_classes="nav-item")
                edu_btn = gr.Button("🎓 Education", elem_classes="nav-item")
                contact_btn = gr.Button("📧 Contact", elem_classes="nav-item")

                gr.HTML("""
                    <div class="profile-section">
                        <div style="display: flex; align-items: center; gap: 12px; padding: 8px;">
                            <div style="width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 13px; color: white;">
                                SM
                            </div>
                            <div>
                                <div style="font-size: 14px; font-weight: 500; color: #ececf1;">Sarjak Maniar</div>
                                <div style="font-size: 12px; color: #8e8ea0;">AI/ML Engineer</div>
                            </div>
                        </div>
                    </div>
                """)

            # MAIN CONTENT
            with gr.Column(elem_classes="main-content") as main:

                # Buttons
                toggle_btn = gr.Button("☰", elem_classes="toggle-btn")
                clear_btn = gr.Button("🗑️", elem_classes="clear-btn")

                # Welcome
                welcome = gr.HTML(welcome_html(), visible=True,
                                  elem_classes="welcome-screen")

                # Chatbot - using HTML for full control
                chatbot = gr.HTML(
                    value="",
                    visible=False,
                    elem_classes="chatbot-wrapper"
                )

                # Input - MINIMAL SPACE
                with gr.Column(elem_classes="input-area"):
                    with gr.Column(elem_classes="input-container"):
                        msg = gr.Textbox(
                            placeholder='Message Sarjak or type "/" for commands...',
                            show_label=False,
                            container=False,
                            lines=1,
                            max_lines=4
                        )

                        gr.HTML("""
                            <div class="hint-text">
                                Try: <span class="command-hint">/projects</span> <span class="command-hint">/experience</span> <span class="command-hint">/skills</span> or ask anything!
                            </div>
                        """)

        # EVENT HANDLERS

        def process_msg(message: str, chat_html: str, started: bool):
            """Process user message"""
            if not message or not message.strip():
                return chat_html, "", gr.update(), gr.update(), started

            # Get AI response
            response = conversation_manager.process_message(message.strip())

            # Format messages - USER RIGHT, BOT LEFT
            user_html = format_user_message(message)
            bot_html = format_bot_message(response)
            new_chat_html = chat_html + user_html + bot_html

            return (
                new_chat_html,
                "",
                gr.update(visible=False),
                gr.update(visible=True, value=new_chat_html),
                True
            )

        def clear():
            """Clear chat"""
            return (
                "",
                gr.update(visible=True),
                gr.update(visible=False, value=""),
                False
            )

        def toggle(is_open: bool):
            """Toggle sidebar"""
            new_state = not is_open
            if new_state:
                return (
                    gr.update(elem_classes="sidebar-column"),
                    gr.update(elem_classes="toggle-btn"),
                    gr.update(elem_classes="main-content"),
                    new_state
                )
            else:
                return (
                    gr.update(elem_classes="sidebar-column collapsed"),
                    gr.update(elem_classes="toggle-btn sidebar-closed"),
                    gr.update(elem_classes="main-content sidebar-closed"),
                    new_state
                )

        def handle_cmd(cmd: str, chat_html: str, started: bool):
            """Handle sidebar commands"""
            response = conversation_manager.process_message(cmd)

            # Format messages
            user_html = format_user_message(cmd)
            bot_html = format_bot_message(response)
            new_chat_html = chat_html + user_html + bot_html

            return (
                new_chat_html,
                gr.update(visible=False),
                gr.update(visible=True, value=new_chat_html),
                True
            )

        # Connect events
        msg.submit(
            process_msg,
            [msg, chatbot, chat_started],
            [chatbot, msg, welcome, chatbot, chat_started]
        )

        clear_btn.click(
            clear,
            [],
            [chatbot, welcome, chatbot, chat_started]
        )

        toggle_btn.click(
            toggle,
            [sidebar_open],
            [sidebar, toggle_btn, main, sidebar_open]
        )

        skills_btn.click(
            lambda h, s: handle_cmd("/skills", h, s),
            [chatbot, chat_started],
            [chatbot, welcome, chatbot, chat_started]
        )

        exp_btn.click(
            lambda h, s: handle_cmd("/experience", h, s),
            [chatbot, chat_started],
            [chatbot, welcome, chatbot, chat_started]
        )

        proj_btn.click(
            lambda h, s: handle_cmd("/projects", h, s),
            [chatbot, chat_started],
            [chatbot, welcome, chatbot, chat_started]
        )

        edu_btn.click(
            lambda h, s: handle_cmd("/education", h, s),
            [chatbot, chat_started],
            [chatbot, welcome, chatbot, chat_started]
        )

        contact_btn.click(
            lambda h, s: handle_cmd("/contact", h, s),
            [chatbot, chat_started],
            [chatbot, welcome, chatbot, chat_started]
        )

    return app


if __name__ == "__main__":
    demo = create_app()
    stats = conversation_manager.get_stats()
    logger.info(f"Ready: {stats}")

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
