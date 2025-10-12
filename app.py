"""
Sarjak's AI/ML Portfolio - Complete Application
ChatGPT-inspired interactive portfolio with RAG-powered chat
"""
import gradio as gr
from typing import List, Tuple, Any
from src.ui.custom_css import get_custom_css
from src.agent.conversation import ConversationManager
from src.utils.logger import logger
import config


# Initialize conversation manager (will load RAG system)
logger.info("Initializing portfolio application...")
conversation_manager = ConversationManager()
logger.info("✅ Portfolio application ready!")


def create_welcome_message() -> str:
    """Create welcome message HTML"""
    return """
    <div style="padding: 60px 40px; text-align: center;">
        <h1 style="font-size: 36px; font-weight: 600; margin-bottom: 16px; color: #ececf1;">
            Hi, I'm Sarjak! 👋
        </h1>
        <p style="font-size: 18px; color: #c5c5d2; margin-bottom: 40px;">
            Data Scientist | AI & ML Engineer
        </p>
        
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; max-width: 800px; margin: 0 auto;">
            
            <div style="background: #2f2f2f; padding: 24px; border-radius: 12px; border: 1px solid #3e3e3e; cursor: pointer;" 
                 onclick="document.querySelector('textarea').value='/experience'; document.querySelector('textarea').focus();">
                <div style="font-size: 32px; margin-bottom: 12px;">💼</div>
                <h3 style="font-size: 16px; font-weight: 600; margin-bottom: 8px; color: #ececf1;">View Experience</h3>
                <p style="font-size: 13px; color: #8e8ea0;">Explore my professional journey</p>
            </div>
            
            <div style="background: #2f2f2f; padding: 24px; border-radius: 12px; border: 1px solid #3e3e3e; cursor: pointer;"
                 onclick="document.querySelector('textarea').value='/projects'; document.querySelector('textarea').focus();">
                <div style="font-size: 32px; margin-bottom: 12px;">🚀</div>
                <h3 style="font-size: 16px; font-weight: 600; margin-bottom: 8px; color: #ececf1;">Explore Projects</h3>
                <p style="font-size: 13px; color: #8e8ea0;">Check out my AI/ML projects</p>
            </div>
            
            <div style="background: #2f2f2f; padding: 24px; border-radius: 12px; border: 1px solid #3e3e3e; cursor: pointer;"
                 onclick="document.querySelector('textarea').value='/skills'; document.querySelector('textarea').focus();">
                <div style="font-size: 32px; margin-bottom: 12px;">🎯</div>
                <h3 style="font-size: 16px; font-weight: 600; margin-bottom: 8px; color: #ececf1;">Technical Skills</h3>
                <p style="font-size: 13px; color: #8e8ea0;">See my tech stack</p>
            </div>
            
            <div style="background: #2f2f2f; padding: 24px; border-radius: 12px; border: 1px solid #3e3e3e; cursor: pointer;"
                 onclick="document.querySelector('textarea').value='Tell me about your AI experience'; document.querySelector('textarea').focus();">
                <div style="font-size: 32px; margin-bottom: 12px;">🤖</div>
                <h3 style="font-size: 16px; font-weight: 600; margin-bottom: 8px; color: #ececf1;">Ask Me Anything</h3>
                <p style="font-size: 13px; color: #8e8ea0;">Chat about my skills</p>
            </div>
            
        </div>
        
        <div style="margin-top: 40px; padding: 20px; background: #2f2f2f; border-radius: 12px; border: 1px solid #3e3e3e; max-width: 600px; margin-left: auto; margin-right: auto;">
            <p style="font-size: 14px; color: #8e8ea0; font-style: italic; margin: 0;">
                "Develop a passion for learning. If you do, you will never cease to grow."<br>
                <span style="color: #c5c5d2;">- Anthony J. D'Angelo</span>
            </p>
        </div>
    </div>
    """


def handle_message(message: str, history: List[Tuple[str, str]]) -> Tuple[List[Tuple[str, str]], str]:
    """
    Handle user message and generate response

    Args:
        message: User message
        history: Chat history

    Returns:
        Updated history and empty message box
    """
    if not message or not message.strip():
        return history, ""

    # Process message through conversation manager
    response = conversation_manager.process_message(message)

    # Add to history
    history.append((message, response))

    return history, ""


def handle_sidebar_click(command: str, history: List[Tuple[str, str]]) -> Tuple[List[Tuple[str, str]], Any, Any]:
    """
    Handle sidebar button click

    Args:
        command: Command to execute
        history: Current chat history

    Returns:
        Updated history, hidden welcome, visible chatbot
    """
    response = conversation_manager.process_message(command)
    history.append((command, response))

    return history, gr.update(visible=False), gr.update(visible=True)


def create_app():
    """Create and configure the Gradio application"""

    with gr.Blocks(
        css=get_custom_css(),
        title=config.APP_TITLE
    ) as app:

        # State for welcome visibility
        chat_started = gr.State(False)

        with gr.Row(equal_height=False):

            # ========================================
            # LEFT SIDEBAR
            # ========================================
            with gr.Column(scale=0, min_width=260):

                # Sidebar header
                gr.HTML("""
                    <div style="padding: 12px; margin-bottom: 8px;">
                        <div style="font-size: 16px; font-weight: 600; color: #ececf1;">
                            💬 Sarjak's Portfolio
                        </div>
                    </div>
                """)

                # Navigation buttons
                with gr.Column():
                    skills_btn = gr.Button("🎯 Skills", size="lg")
                    exp_btn = gr.Button("💼 Experience", size="lg")
                    proj_btn = gr.Button("🚀 Projects", size="lg")
                    edu_btn = gr.Button("🎓 Education", size="lg")
                    contact_btn = gr.Button("📧 Contact", size="lg")

                # Profile section at bottom
                gr.HTML("""
                    <div style="margin-top: 200px; padding: 12px; border-top: 1px solid #3e3e3e;">
                        <div style="display: flex; align-items: center; gap: 12px; padding: 8px; border-radius: 8px;">
                            <div style="width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 14px; color: white;">
                                SM
                            </div>
                            <div>
                                <div style="font-size: 14px; font-weight: 500; color: #ececf1;">Sarjak Maniar</div>
                                <div style="font-size: 12px; color: #8e8ea0;">AI/ML Engineer</div>
                            </div>
                        </div>
                    </div>
                """)

            # ========================================
            # MAIN CHAT AREA
            # ========================================
            with gr.Column(scale=1):

                # Welcome screen
                welcome = gr.HTML(create_welcome_message(), visible=True)

                # Chatbot
                chatbot = gr.Chatbot(
                    value=[],
                    height=600,
                    show_label=False,
                    container=False,
                    visible=False,
                    render_markdown=False,
                    sanitize_html=False
                )

                # Input area
                with gr.Column():
                    with gr.Column():
                        msg = gr.Textbox(
                            placeholder='Message Sarjak or type "/" for commands...',
                            show_label=False,
                            container=False,
                            lines=1,
                            max_lines=8
                        )

                        # Hint text
                        gr.HTML("""
                            <div style="text-align: center; font-size: 12px; color: #8e8ea0; margin-top: 12px;">
                                Try: 
                                <span style="display: inline-block; background: #40414f; padding: 4px 8px; border-radius: 8px; font-size: 11px; margin: 0 4px; border: 1px solid #565869; font-family: monospace;">/projects</span>
                                <span style="display: inline-block; background: #40414f; padding: 4px 8px; border-radius: 8px; font-size: 11px; margin: 0 4px; border: 1px solid #565869; font-family: monospace;">/experience</span>
                                <span style="display: inline-block; background: #40414f; padding: 4px 8px; border-radius: 8px; font-size: 11px; margin: 0 4px; border: 1px solid #565869; font-family: monospace;">/skills</span>
                                or ask anything!
                            </div>
                        """)

                # Event handlers
                def on_message(message: str, history: List[Tuple[str, str]], is_started: bool):
                    if message:
                        new_history, cleared = handle_message(message, history)
                        return new_history, cleared, gr.update(visible=False), gr.update(visible=True), True
                    return history, message, gr.update(), gr.update(), is_started

                msg.submit(
                    on_message,
                    [msg, chatbot, chat_started],
                    [chatbot, msg, welcome, chatbot, chat_started]
                )

                # Sidebar button handlers
                def on_sidebar_click(command: str):
                    def handler(history: List[Tuple[str, str]], is_started: bool):
                        new_history, welcome_update, chatbot_update = handle_sidebar_click(
                            command, history)
                        return new_history, welcome_update, chatbot_update, True
                    return handler

                skills_btn.click(
                    on_sidebar_click("/skills"),
                    [chatbot, chat_started],
                    [chatbot, welcome, chatbot, chat_started]
                )

                exp_btn.click(
                    on_sidebar_click("/experience"),
                    [chatbot, chat_started],
                    [chatbot, welcome, chatbot, chat_started]
                )

                proj_btn.click(
                    on_sidebar_click("/projects"),
                    [chatbot, chat_started],
                    [chatbot, welcome, chatbot, chat_started]
                )

                edu_btn.click(
                    on_sidebar_click("/education"),
                    [chatbot, chat_started],
                    [chatbot, welcome, chatbot, chat_started]
                )

                contact_btn.click(
                    on_sidebar_click("/contact"),
                    [chatbot, chat_started],
                    [chatbot, welcome, chatbot, chat_started]
                )

    return app


if __name__ == "__main__":
    # Create and launch app
    demo = create_app()

    # Get system stats
    stats = conversation_manager.get_stats()
    logger.info(f"System ready: {stats}")

    # Launch
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
