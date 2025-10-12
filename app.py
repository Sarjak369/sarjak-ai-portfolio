"""
Sarjak's AI/ML Portfolio - ACTUALLY WORKING VERSION
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


def create_app():
    """Create Gradio app"""

    with gr.Blocks(css=get_custom_css(), title=config.APP_TITLE) as app:

        # State
        chat_history = gr.State([])
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

                # Welcome screen
                welcome = gr.HTML("""
                    <div style="display: flex; align-items: center; justify-content: center; height: 60vh; padding: 40px;">
                        <div style="max-width: 700px; text-align: center;">
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
                    </div>
                """, visible=True)

                # Chatbot - using standard Gradio Chatbot
                chatbot = gr.Chatbot(
                    value=[],
                    height=600,
                    show_label=False,
                    container=False,
                    elem_classes="chatbot-wrapper",
                    avatar_images=(None, None),
                    bubble_full_width=False,
                    render_markdown=False,
                    show_copy_button=False,
                    visible=False
                )

                # Input
                with gr.Column(elem_classes="input-area"):
                    msg = gr.Textbox(
                        placeholder='Message Sarjak or type "/" for commands...',
                        show_label=False,
                        container=False,
                        lines=1,
                        max_lines=4
                    )

                    gr.HTML("""
                        <div class="hint-text">
                            Try: <span class="command-hint">/projects</span> <span class="command-hint">/experience</span> <span class="command-hint">/skills</span>
                        </div>
                    """)

        # EVENT HANDLERS

        def send_message(message: str, history: List):
            """Send message and get response"""
            if not message or not message.strip():
                return history, "", gr.update(), gr.update()

            # Add user message immediately
            user_msg = f'<div style="display:flex;justify-content:flex-end;padding:16px 24px;margin:2px 0;"><div style="max-width:70%;display:flex;gap:12px;align-items:flex-start;"><div style="flex:1;text-align:left;color:#ececf1;font-size:15px;line-height:1.6;">{message}</div><div style="width:32px;height:32px;min-width:32px;border-radius:50%;background:#5436DA;display:flex;align-items:center;justify-content:center;font-size:16px;box-shadow:0 2px 8px rgba(84,54,218,0.3);">👤</div></div></div>'

            # Show typing indicator
            typing_msg = '<div style="display:flex;justify-content:flex-start;padding:16px 24px;background:#2f2f2f;margin:2px 0;"><div style="max-width:70%;display:flex;gap:12px;align-items:flex-start;"><div style="width:32px;height:32px;min-width:32px;border-radius:50%;background:#10a37f;display:flex;align-items:center;justify-content:center;font-size:16px;box-shadow:0 2px 8px rgba(16,163,127,0.3);">🤖</div><div class="typing-indicator"><span></span><span></span><span></span></div></div></div>'

            temp_history = history + [[user_msg, typing_msg]]

            # Get response
            response = conversation_manager.process_message(message.strip())

            # Replace typing with actual response
            bot_msg = f'<div style="display:flex;justify-content:flex-start;padding:16px 24px;background:#2f2f2f;margin:2px 0;border-top:1px solid rgba(255,255,255,0.05);border-bottom:1px solid rgba(255,255,255,0.05);"><div style="max-width:70%;display:flex;gap:12px;align-items:flex-start;"><div style="width:32px;height:32px;min-width:32px;border-radius:50%;background:#10a37f;display:flex;align-items:center;justify-content:center;font-size:16px;box-shadow:0 2px 8px rgba(16,163,127,0.3);">🤖</div><div style="flex:1;color:#ececf1;font-size:15px;line-height:1.6;">{response}</div></div></div>'

            history.append([user_msg, bot_msg])

            return history, "", gr.update(visible=False), gr.update(visible=True)

        def clear_chat():
            """Clear chat history"""
            return [], gr.update(visible=True), gr.update(visible=False)

        def toggle_sidebar(is_open: bool):
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

        def handle_command(cmd: str, history: List):
            """Handle sidebar button click"""
            response = conversation_manager.process_message(cmd)

            user_msg = f'<div style="display:flex;justify-content:flex-end;padding:16px 24px;"><div style="max-width:70%;display:flex;gap:10px;align-items:flex-start;"><div style="flex:1;text-align:left;">{cmd}</div><div style="width:30px;height:30px;min-width:30px;border-radius:50%;background:#5436DA;display:flex;align-items:center;justify-content:center;font-size:16px;">👤</div></div></div>'

            bot_msg = f'<div style="display:flex;justify-content:flex-start;padding:16px 24px;background:#2f2f2f;"><div style="max-width:70%;display:flex;gap:10px;align-items:flex-start;"><div style="width:30px;height:30px;min-width:30px;border-radius:50%;background:#10a37f;display:flex;align-items:center;justify-content:center;font-size:16px;">🤖</div><div style="flex:1;">{response}</div></div></div>'

            history.append([user_msg, bot_msg])
            return history, gr.update(visible=False), gr.update(visible=True)

        # Connect events
        msg.submit(send_message, [msg, chatbot], [
                   chatbot, msg, welcome, chatbot])
        clear_btn.click(clear_chat, [], [chatbot, welcome, chatbot])
        toggle_btn.click(toggle_sidebar, [sidebar_open], [
                         sidebar, toggle_btn, main, sidebar_open])

        skills_btn.click(lambda h: handle_command("/skills", h),
                         [chatbot], [chatbot, welcome, chatbot])
        exp_btn.click(lambda h: handle_command("/experience", h),
                      [chatbot], [chatbot, welcome, chatbot])
        proj_btn.click(lambda h: handle_command("/projects", h),
                       [chatbot], [chatbot, welcome, chatbot])
        edu_btn.click(lambda h: handle_command("/education", h),
                      [chatbot], [chatbot, welcome, chatbot])
        contact_btn.click(lambda h: handle_command(
            "/contact", h), [chatbot], [chatbot, welcome, chatbot])

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
