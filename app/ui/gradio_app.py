"""
Gradio interface for the AI portfolio assistant.
Polished ChatGPT-style UI with user avatars and perfect layout.
"""

from typing import List, Dict, Optional, Tuple, Any
import gradio as gr
from loguru import logger
from gradio.themes.base import Base
from gradio.themes.utils import fonts
from app.ui.custom_css import CHATGPT_CSS
from app.config import settings
from app.core.email_classifier import EmailClassifier
from app.core.commands import command_handler
from app.core.cache import cache_manager
from app.core.rag import rag_pipeline
from app.core.llm import llm_handler
from app.db.database import SessionLocal, init_db
from app.db.crud import (
    create_user,
    get_user_by_email,
    deduct_credit,
    create_conversation,
    create_analytics_event
)
import time
from pathlib import Path


ASSETS_DIR = Path(__file__).parent / "assets"

# absolute URL => Gradio will NOT send it through gradio_api/file
ASSISTANT_AVATAR = f"{settings.PUBLIC_BASE_URL.rstrip('/')}/assets/profile.png"


class PortfolioAssistant:
    """Main portfolio assistant application."""

    def __init__(self) -> None:
        """Initialize the assistant."""
        self.current_user_email: Optional[str] = None
        self.current_user_name: str = ""
        self.current_user_initials: str = ""
        self.current_user_avatar_url: str = ""
        self.conversation_history: List[Dict[str, str]] = []
        self._initialize_components()

    def _initialize_components(self) -> None:
        """Initialize all backend components."""
        logger.info("Initializing portfolio assistant components...")

        init_db()

        if not rag_pipeline._initialized:
            rag_pipeline.initialize()
            rag_pipeline.load_and_index_documents()

        if not llm_handler._initialized:
            llm_handler.initialize()

        if not cache_manager._initialized:
            cache_manager.initialize()

        logger.info("All components initialized successfully")

    def register_user(
        self,
        first_name: str,
        last_name: str,
        email: str
    ) -> Tuple[str, str, bool, str, str, str]:
        """Register user and return initials + full name + avatar URL."""
        try:
            if not all([first_name, last_name, email]):
                return ("❌ Please fill in all fields.", "", False, "", "", "")

            if "@" not in email or "." not in email:
                return ("❌ Please enter a valid email address.", "", False, "", "", "")

            email = email.lower().strip()
            db = SessionLocal()

            try:
                existing_user = get_user_by_email(db, email)

                if existing_user:
                    self.current_user_email = existing_user.email
                    self.current_user_name = f"{existing_user.first_name} {existing_user.last_name}"
                    self.current_user_initials = f"{existing_user.first_name[0]}{existing_user.last_name[0]}".upper(
                    )
                    self.current_user_avatar_url = f"https://ui-avatars.com/api/?name={self.current_user_initials}&background=10a37f&color=fff&size=128&bold=true"

                    category = existing_user.email_category
                    credits = existing_user.credits_remaining

                    logger.info(f"Existing user logged in: {email}")

                    welcome_msg = f"✅ Welcome back, {existing_user.first_name}! 👋"
                    credit_msg = EmailClassifier.get_welcome_message(
                        category, credits)

                    return (welcome_msg, credit_msg, True, self.current_user_initials, self.current_user_name, self.current_user_avatar_url)

                category, credits = EmailClassifier.classify(email)

                user = create_user(
                    db=db,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    email_category=category,
                    credits=credits
                )

                self.current_user_email = user.email
                self.current_user_name = f"{first_name} {last_name}"
                self.current_user_initials = f"{first_name[0]}{last_name[0]}".upper(
                )
                self.current_user_avatar_url = f"https://ui-avatars.com/api/?name={self.current_user_initials}&background=10a37f&color=fff&size=128&bold=true"

                create_analytics_event(
                    db=db,
                    user_id=user.id,
                    event_type="registration",
                    event_data={"email_category": category}
                )

                logger.info(
                    f"New user registered: {email} ({category}, {credits} credits)")

                welcome_msg = f"✅ Welcome, {first_name}! 🎉"
                credit_msg = EmailClassifier.get_welcome_message(
                    category, credits)

                return (welcome_msg, credit_msg, True, self.current_user_initials, self.current_user_name, self.current_user_avatar_url)

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Error in user registration: {e}")
            return ("❌ An error occurred. Please try again.", "", False, "", "", "")

    def chat(
        self,
        message: str,
        history: List[Dict[str, str]]
    ) -> Tuple[List[Dict[str, str]], str]:
        """Handle chat messages."""
        if not self.current_user_email:
            error_msg: Dict[str, str] = {
                "role": "assistant", "content": "❌ Please register first."}
            return (history + [{"role": "user", "content": message}, error_msg], "")

        start_time = time.time()
        db = SessionLocal()

        try:
            user = get_user_by_email(db, self.current_user_email)

            if not user:
                error_msg = {"role": "assistant",
                             "content": "❌ User not found. Please refresh."}
                return (history + [{"role": "user", "content": message}, error_msg], "")

            # Commands always work (free)
            is_command, command_response = command_handler.handle_command(
                message)

            if is_command and command_response:
                create_conversation(
                    db=db,
                    user_id=user.id,
                    question=message,
                    answer=command_response,
                    used_llm=False,
                    credits_charged=0,
                    response_time=time.time() - start_time
                )

                create_analytics_event(
                    db=db,
                    user_id=user.id,
                    event_type="command_used",
                    event_data={"command": message}
                )

                return (
                    history + [
                        {"role": "user", "content": message},
                        {"role": "assistant", "content": command_response}
                    ],
                    self._format_credit_display(user.credits_remaining)
                )

            # Check credits for non-command queries
            if user.credits_remaining <= 0:
                exhausted_msg = self._get_credits_exhausted_message()
                create_analytics_event(
                    db=db,
                    user_id=user.id,
                    event_type="credit_exhausted"
                )
                return (
                    history + [
                        {"role": "user", "content": message},
                        {"role": "assistant", "content": exhausted_msg}
                    ],
                    self._format_credit_display(0)
                )

            # Check caches
            cached = cache_manager.check_exact_cache(db, message)
            if cached:
                answer, cache_id = cached

                create_conversation(
                    db=db,
                    user_id=user.id,
                    question=message,
                    answer=answer,
                    used_llm=False,
                    credits_charged=0,
                    response_time=time.time() - start_time
                )

                return (
                    history + [
                        {"role": "user", "content": message},
                        {"role": "assistant", "content": answer}
                    ],
                    self._format_credit_display(user.credits_remaining)
                )

            semantic_cached = cache_manager.check_semantic_cache(db, message)
            if semantic_cached:
                answer, cache_id, similarity = semantic_cached

                create_conversation(
                    db=db,
                    user_id=user.id,
                    question=message,
                    answer=answer,
                    used_llm=False,
                    credits_charged=0,
                    response_time=time.time() - start_time
                )

                return (
                    history + [
                        {"role": "user", "content": message},
                        {"role": "assistant", "content": answer}
                    ],
                    self._format_credit_display(user.credits_remaining)
                )

            # Use LLM
            context = rag_pipeline.retrieve_context(message)

            conv_history: List[Dict[str, str]] = []
            for msg in history:
                conv_history.append(
                    {"role": msg["role"], "content": msg["content"]})

            answer = llm_handler.generate_response(
                query=message,
                context=context,
                conversation_history=conv_history
            )

            updated_user = deduct_credit(db, user.id)
            if not updated_user:
                raise ValueError("Failed to deduct credit")

            create_conversation(
                db=db,
                user_id=user.id,
                question=message,
                answer=answer,
                used_llm=True,
                credits_charged=1,
                response_time=time.time() - start_time
            )

            cache_manager.add_to_cache(db, message, answer)

            create_analytics_event(
                db=db,
                user_id=user.id,
                event_type="llm_query",
                event_data={"response_time": time.time() - start_time}
            )

            return (
                history + [
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": answer}
                ],
                self._format_credit_display(updated_user.credits_remaining)
            )

        except Exception as e:
            logger.error(f"Error in chat: {e}")
            error_msg_str = "❌ Error occurred. Please try again or contact sarjakm369@gmail.com"
            return (
                history + [
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": error_msg_str}
                ],
                self._format_credit_display(0)
            )

        finally:
            db.close()

    def _format_credit_display(self, credits: int) -> str:
        """Format credit display."""
        if credits == 1:
            return f"💬 {credits} question left"
        return f"💬 {credits} questions left"

    def _get_credits_exhausted_message(self) -> str:
        """Get message when credits are exhausted."""
        return """**🎯 All Questions Used!**

Thanks for exploring my portfolio!

**📬 Let's Connect:**
- **Email:** sarjakm369@gmail.com
- **LinkedIn:** [linkedin.com/in/Sarjak369](https://linkedin.com/in/Sarjak369)
- **GitHub:** [github.com/Sarjak369](https://github.com/Sarjak369)

**💡 Free Commands:**
`/contact` `/skills` `/projects` `/education` `/resume`"""


def create_gradio_interface() -> gr.Blocks:
    """Create Gradio interface with ChatGPT-style layout."""

    assistant = PortfolioAssistant()

    theme = Base(
        primary_hue="green",
        secondary_hue="emerald",
        neutral_hue="slate",
        font=fonts.GoogleFont("Inter"),
    ).set(
        body_background_fill="#212121",
        background_fill_primary="#2f2f2f",
        background_fill_secondary="#171717",
        color_accent="#10a37f",
        border_color_primary="#3e3e3e",
        block_background_fill="#2f2f2f",
        input_background_fill="#171717",
    )

    with gr.Blocks(
        css=CHATGPT_CSS,
        title="Sarjak's AI Portfolio",
        theme=theme,
        fill_height=True
    ) as demo:

        registered = gr.State(False)
        user_initials_state = gr.State("")
        user_name_state = gr.State("")
        user_avatar_state = gr.State("")

        # Email Gate
        with gr.Column(visible=True, elem_id="email-gate") as email_gate:
            gr.HTML(f"""
                <div style="text-align: center; padding: 40px 20px;">
                    <img src="{ASSISTANT_AVATAR}" alt="Sarjak" class="hero-avatar"/>
                    <h1 style="font-size: 44px; font-weight: 800; letter-spacing:.2px;
                            color: #ececf1; margin: 18px 0 12px;">
                        Sarjak's AI Portfolio
                    </h1>
                    <p style="font-size: 16px; color: #b4b9c3; margin-bottom: 28px;">
                        Ask anything about my experience!
                    </p>
                </div>
            """)

            with gr.Row():
                first_name_input = gr.Textbox(
                    label="First Name", placeholder="John", scale=1)
                last_name_input = gr.Textbox(
                    label="Last Name", placeholder="Doe", scale=1)

            email_input = gr.Textbox(
                label="Email Address", placeholder="john@company.com", type="email")

            register_btn = gr.Button(
                "Start Conversation", variant="primary", size="lg")

            welcome_msg = gr.Markdown(visible=False)
            credit_msg = gr.Markdown(visible=False)

        # Chat Interface with Sidebar
        with gr.Row(visible=False, elem_id="main-container") as chat_interface:

            # Sidebar
            with gr.Column(scale=1, elem_id="sidebar"):
                # Header
                gr.HTML("""
                    <div class="sidebar-header">
                        <h2>💬 Sarjak's Portfolio</h2>
                    </div>
                """)

                # Scrollable content
                with gr.Column(elem_id="sidebar-scroll-content"):
                    gr.Markdown("""
### 🎯 Quick Commands

`/skills` - Technical abilities  
`/projects` - Featured work  
`/education` - Academic background  
`/contact` - Get in touch  
`/resume` - Download CV  
`/help` - All commands

### 💡 Tips

- Natural language works best
- Be specific in questions  
- Use commands for quick info

### 💭 Quote

*"Develop a passion for learning. If you do, you will never cease to grow."*

— Anthony J. D’Angelo
                    """, elem_classes="sidebar-text")

                # Footer: Credits + User (sticky at bottom)
                with gr.Column(elem_id="sidebar-footer"):
                    credit_display = gr.Markdown(
                        "💬 5 questions left", elem_id="credit-display")
                    user_info_display = gr.HTML(
                        "<div class='user-info'>Guest User</div>", elem_id="user-info")

            # Main Chat Area
            with gr.Column(scale=4, elem_id="chat-column"):
                # Clear button (top-right)
                with gr.Row(elem_id="chat-header"):
                    gr.HTML("<div style='flex: 1;'></div>")
                    clear_btn = gr.Button(
                        "🗑️ Clear", size="sm", elem_id="clear-button")

                chatbot = gr.Chatbot(
                    label="Chat",
                    height=600,
                    show_label=False,
                    type="messages",
                    # (user, assistant)
                    avatar_images=(
                        "https://ui-avatars.com/api/?name=SM&background=10a37f&color=fff&size=128&bold=true",
                        ASSISTANT_AVATAR),
                    elem_id="main-chatbot",
                    autoscroll=True
                )

                with gr.Row(elem_id="input-row"):
                    msg_input = gr.Textbox(
                        label="Message",
                        placeholder="Ask about my experience, skills, or projects...",
                        show_label=False,
                        scale=9,
                        container=False,
                        elem_id="message-input"
                    )
                    send_btn = gr.Button(
                        "Send", scale=1, variant="primary", elem_id="send-button")

                with gr.Row(elem_id="suggested-row"):
                    sg1 = gr.Button(
                        "What's your most impressive project?", size="sm")
                    sg2 = gr.Button(
                        "Tell me about your AI experience", size="sm")
                    sg3 = gr.Button("What technologies do you use?", size="sm")

        # Registration logic
        def handle_registration(first_name: str, last_name: str, email: str):
            welcome, credits, success, initials, full_name, avatar_url = assistant.register_user(
                first_name, last_name, email
            )
            if success:
                user_html = f"""
                <div class="user-info">
                    <img src="{avatar_url}" class="user-avatar" alt="{initials}" />
                    <div class="user-name">{full_name}</div>
                </div>
                """
                return (
                    gr.update(visible=False),                   # email_gate
                    # chat_interface
                    gr.update(visible=True),
                    gr.update(value=welcome, visible=True),     # welcome_msg
                    gr.update(value=credits, visible=True),     # credit_msg
                    True,                                       # registered
                    initials,
                    full_name,
                    avatar_url,
                    # user_info_display
                    gr.update(value=user_html),
                    # <-- set user avatar
                    # gr.update(avatar_images=(avatar_url, ASSISTANT_AVATAR))
                    gr.update(
                        value=[],
                        # (user, assistant)
                        avatar_images=(avatar_url, ASSISTANT_AVATAR)
                    ),
                )
            else:
                return (
                    gr.update(visible=True),
                    gr.update(visible=False),
                    gr.update(value=welcome, visible=True),
                    gr.update(value="", visible=False),
                    False, "", "", "",
                    gr.update(),
                    gr.update()  # chatbot (no-op)
                )

        register_btn.click(
            fn=handle_registration,
            inputs=[first_name_input, last_name_input, email_input],
            outputs=[
                email_gate,
                chat_interface,
                welcome_msg,
                credit_msg,
                registered,
                user_initials_state,
                user_name_state,
                user_avatar_state,
                user_info_display,
                chatbot,                    # <-- new output to update avatars
            ],
        )

        # Chat logic
        def handle_message(message, history, user_avatar):
            new_history, credits = assistant.chat(
                message, history if history else [])
            return new_history, credits, ""

        send_btn.click(
            fn=handle_message,
            inputs=[msg_input, chatbot, user_avatar_state],
            outputs=[chatbot, credit_display, msg_input]
        )

        msg_input.submit(
            fn=handle_message,
            inputs=[msg_input, chatbot, user_avatar_state],
            outputs=[chatbot, credit_display, msg_input]
        )

        # Clear chat
        clear_btn.click(lambda: [], outputs=[chatbot])

        # Suggested questions
        sg1.click(lambda: "What's your most impressive project?",
                  outputs=[msg_input])
        sg2.click(lambda: "Tell me about your AI experience",
                  outputs=[msg_input])
        sg3.click(lambda: "What technologies do you use?", outputs=[msg_input])

    return demo


if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
