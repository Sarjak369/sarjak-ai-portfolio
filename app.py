"""
Sarjak's AI/ML Portfolio - ACTUALLY WORKING VERSION
"""
import os
import gradio as gr
from typing import List
from src.ui.custom_css import get_custom_css
from src.agent.conversation import ConversationManager
from src.utils.logger import logger
import config

conversation_manager = None


def get_manager():
    """Create the ConversationManager on first use."""
    global conversation_manager
    if conversation_manager is None:
        logger.info("Initializing portfolio (lazy)…")
        from src.agent.conversation import ConversationManager
        # NOTE: keep defaults; avoid heavy work until first call
        conversation_manager = ConversationManager()
        logger.info("✅ Portfolio initialized")
    return conversation_manager


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
                            💬 Sarjak's AI Portfolio
                        </div>
                    </div>
                    <div class="nav-section">
                """)

                # Navigation buttons
                skills_btn = gr.Button("🎯 Skills", elem_classes="nav-item")
                exp_btn = gr.Button("💼 Experience", elem_classes="nav-item")
                proj_btn = gr.Button("🚀 Projects", elem_classes="nav-item")
                edu_btn = gr.Button("🎓 Education", elem_classes="nav-item")
                contact_btn = gr.Button("📧 Contact", elem_classes="nav-item")

                # ---- FOOTER PROFILE CARD ----

                gr.HTML(""" 
                        <div 
                        style=" display: flex; 
                        align-items: center; 
                        gap: 10px; 
                        padding: 12px 16px; 
                        border-top: 1px solid rgba(255,255,255,0.08); 
                        background: rgba(0,0,0,0.15); 
                        margin-top: auto; /* pushes footer to bottom of sidebar */ 
                        position: sticky; bottom: 0; "> 
                        
                        <div style=" background: linear-gradient(135deg, #19c37d, #0e8b6b); 
                        color: white; font-weight: 600; font-size: 14px; width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; ">SM</div> <div style="display: flex; flex-direction: column; line-height: 1.2;"> <span style="color: #ececf1; font-size: 14px; font-weight: 600;">Sarjak Maniar</span> <span style="color: #8e8ea0; font-size: 12px;">AI/ML Engineer</span> </div> </div> """)

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
                    render_markdown=False,
                    show_copy_button=False,
                    visible=False,
                    type="messages",  # new format for Gradio ≥ 4.31
                )

                # Hidden HTML used to run tiny scripts (e.g., autoscroll)
                scroll_exec = gr.HTML("", visible=False)

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
                # also clear scroll runner
                return history, "", gr.update(), gr.update(), gr.update(value="")

            # ===== USER MESSAGE BUBBLE =====
            user_msg = f'''
                <div style="
                    display: flex;
                    justify-content: flex-end;
                    padding: 8px 20px;
                ">
                <div style="
                    display: flex;
                    align-items: center; /* keep avatar level with bubble */
                    gap: 10px;
                    max-width: 80%;
                ">
                    <div style="
                        flex: 1;
                        width: fit-content;
                        max-width: 520px;                /* ⬆ wider user bubble */
                        word-wrap: break-word;
                        background: linear-gradient(135deg, #3a3a3a 0%, #2f2f2f 100%);
                        padding: 6px 12px 8px 12px;       /* ⬆ tighter top padding */
                        border-radius: 16px 16px 0 16px;
                        color: #f5f5f5;
                        font-size: 15px;
                        line-height: 1.45;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.25);
                        border: 1px solid rgba(255,255,255,0.05);
                        text-align: left;
                    ">{message}</div>
                    <div style="
                        width: 34px;
                        height: 34px;
                        border-radius: 50%;
                        background: linear-gradient(135deg, #5436DA 0%, #7154FF 100%);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 16px;
                        flex-shrink: 0;
                        box-shadow: 0 0 8px rgba(84,54,218,0.3);
                        color: #fff;
                    ">👤</div>
                </div>
                </div>
                '''

            # Show typing indicator
            typing_msg = (
                '<div style="display:flex;justify-content:flex-start;padding:16px 24px;background:#2f2f2f;margin:2px 0;">'
                '<div style="max-width:80%;display:flex;gap:12px;align-items:flex-start;">'
                '<div style="width:32px;height:32px;min-width:32px;border-radius:50%;background:#10a37f;display:flex;align-items:center;'
                'justify-content:center;font-size:16px;box-shadow:0 2px 8px rgba(16,163,127,0.3);">🤖</div>'
                '<div class="typing-indicator"><span></span><span></span><span></span></div>'
                '</div></div>'
            )

            temp_history = history + [
                {"role": "user", "content": user_msg},
                {"role": "assistant", "content": typing_msg},
            ]

            # Get response
            # response = conversation_manager.process_message(message.strip())
            mgr = get_manager()
            response = mgr.process_message(message.strip())

            # ===== BOT MESSAGE BUBBLE =====
            bot_msg = f'''
                <div style="
                    display: flex;
                    justify-content: flex-start;
                    padding: 8px 20px;
                ">
                <div style="
                    display: flex;
                    align-items: flex-start;
                    gap: 10px;
                    max-width: 80%;
                ">
                    <div style="
                        width: 34px;
                        height: 34px;
                        border-radius: 50%;
                        background: linear-gradient(135deg, #10a37f 0%, #0e8b6b 100%);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 16px;
                        flex-shrink: 0;
                        box-shadow: 0 0 8px rgba(16,163,127,0.3);
                        color: #fff;
                    ">🤖</div>
                    <div style="
                        flex: 1;
                        width: fit-content;
                        max-width: clamp(520px, 62vw, 760px);
                        clamp(520px, 62vw, 760px);               
                        word-wrap: break-word;
                        background: linear-gradient(135deg, #262626 0%, #2e2e2e 100%);
                        padding: 10px 14px;
                        border-radius: 16px 16px 16px 0;
                        color: #ececf1;
                        font-size: 15px;
                        line-height: 1.6;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.25);
                        border: 1px solid rgba(255,255,255,0.05);
                        text-align: left;
                    ">{response}</div>
                </div>
                </div>
                '''

            # Replace typing with actual response (append as two role messages)
            history.append({"role": "user", "content": user_msg})
            history.append({"role": "assistant", "content": bot_msg})

            # tiny script: scroll chat panel to bottom (smooth)
            scroll_script = """
            <script>
            setTimeout(() => {
                const el = document.querySelector('.chatbot-wrapper');
                if (el) el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' });
            }, 0);
            </script>
            """

            return (
                history,           # chatbot value
                "",                # clear textbox
                gr.update(visible=False),  # hide welcome
                gr.update(visible=True),   # show chatbot
                gr.update(value=scroll_script)  # run scroll
            )

        def clear_chat():
            """Clear chat history"""
            return [], gr.update(visible=True), gr.update(visible=False), gr.update(value="")

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
            # response = conversation_manager.process_message(cmd)
            mgr = get_manager()
            response = mgr.process_message(cmd)

            user_msg = f'''
                <div style="display:flex;justify-content:flex-end;padding:8px 20px;">
                <div style="display:flex;align-items:center;gap:10px;max-width:80%;">
                    <div style="
                        flex:1;width:fit-content;max-width:520px;word-wrap:break-word;
                        background:linear-gradient(135deg,#3a3a3a 0%,#2f2f2f 100%);
                        padding:6px 12px 8px 12px;border-radius:16px 16px 0 16px;color:#f5f5f5;
                        font-size:15px;line-height:1.45;box-shadow:0 2px 6px rgba(0,0,0,0.25);
                        border:1px solid rgba(255,255,255,0.05);text-align:left;"
                    >{cmd}</div>
                    <div style="width:34px;height:34px;border-radius:50%;
                        background:linear-gradient(135deg,#5436DA 0%,#7154FF 100%);display:flex;align-items:center;justify-content:center;
                        font-size:16px;flex-shrink:0;box-shadow:0 0 8px rgba(84,54,218,0.3);color:#fff;">👤</div>
                </div></div>
            '''

            bot_msg = f'''
                <div style="display:flex;justify-content:flex-start;padding:8px 20px;">
                <div style="display:flex;align-items:flex-start;gap:10px;max-width:80%;">
                    <div style="width:34px;height:34px;border-radius:50%;
                        background:linear-gradient(135deg,#10a37f 0%,#0e8b6b 100%);display:flex;align-items:center;justify-content:center;
                        font-size:16px;flex-shrink:0;box-shadow:0 0 8px rgba(16,163,127,0.3);color:#fff;">🤖</div>
                    <div style="
                        flex:1;width:fit-content;max-width: clamp(520px, 62vw, 760px);word-wrap:break-word;
                        background:linear-gradient(135deg,#262626 0%,#2e2e2e 100%);
                        padding:10px 14px;border-radius:16px 16px 16px 0;color:#ececf1;font-size:15px;line-height:1.6;
                        box-shadow:0 2px 6px rgba(0,0,0,0.25);border:1px solid rgba(255,255,255,0.05);text-align:left;"
                    >{response}</div>
                </div></div>
            '''

            history.append({"role": "user", "content": user_msg})
            history.append({"role": "assistant", "content": bot_msg})

            scroll_script = """
            <script>
            setTimeout(() => {
                const el = document.querySelector('.chatbot-wrapper');
                if (el) el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' });
            }, 0);
            </script>
            """

            return history, gr.update(visible=False), gr.update(visible=True), gr.update(value=scroll_script)

        # Connect events
        msg.submit(send_message, [msg, chatbot], [
                   chatbot, msg, welcome, chatbot, scroll_exec])
        clear_btn.click(clear_chat, [], [
                        chatbot, welcome, chatbot, scroll_exec])
        toggle_btn.click(toggle_sidebar, [sidebar_open], [
                         sidebar, toggle_btn, main, sidebar_open])

        skills_btn.click(lambda h: handle_command("/skills", h),
                         [chatbot], [chatbot, welcome, chatbot, scroll_exec])
        exp_btn.click(lambda h: handle_command("/experience", h),
                      [chatbot], [chatbot, welcome, chatbot, scroll_exec])
        proj_btn.click(lambda h: handle_command("/projects", h),
                       [chatbot], [chatbot, welcome, chatbot, scroll_exec])
        edu_btn.click(lambda h: handle_command("/education", h),
                      [chatbot], [chatbot, welcome, chatbot, scroll_exec])
        contact_btn.click(lambda h: handle_command(
            "/contact", h), [chatbot], [chatbot, welcome, chatbot, scroll_exec])

        def _warmup():
            try:
                get_manager()
            except Exception as e:
                logger.error(f"Warmup failed: {e}")
        app.load(_warmup, queue=False)  # runs after Gradio has bound the port

    return app


if __name__ == "__main__":
    demo = create_app()

    port = int(os.getenv("PORT", "10000"))
    logger.info(f"🚀 Starting server on 0.0.0.0:{port} ...")

    # Background preload thread for Render cold starts
    import threading
    from src.agent.conversation import ConversationManager

    def preload_model():
        try:
            logger.info("⚙️ Preloading ConversationManager and RAG model...")
            ConversationManager()  # triggers lazy model load only once (cached globally)
            logger.info(
                "✅ Model preloaded successfully (Render warm start ready)")
        except Exception as e:
            logger.warning(f"Preload failed: {e}")

    # Start preload in background thread (non-blocking)
    threading.Thread(target=preload_model, daemon=True).start()

    # Optional queue; useful for back-pressure on Render
    demo.queue(default_concurrency_limit=2).launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False,
        show_error=True,
    )
