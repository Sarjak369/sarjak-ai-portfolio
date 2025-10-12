"""
Portfolio Website UI Preview - EXACT ChatGPT Match
"""
import gradio as gr
from src.ui.custom_css import get_custom_css
from src.utils.helpers import load_json
import config

# Load profile data
profile = load_json(config.PROFILE_DATA)

# Command list for dropdown
COMMANDS = [
    {"cmd": "/projects", "icon": "🚀", "desc": "View my projects"},
    {"cmd": "/experience", "icon": "💼", "desc": "See my work experience"},
    {"cmd": "/skills", "icon": "🎯", "desc": "View my technical skills"},
    {"cmd": "/education", "icon": "🎓", "desc": "See my education"},
    {"cmd": "/contact", "icon": "📧", "desc": "Get contact information"},
]


def create_welcome_screen():
    """Create welcome screen"""
    return """
    <div class="welcome-container">
        <h1 class="welcome-title">Hi, I'm Sarjak! 👋</h1>
        
        <div class="suggestion-grid">
            <div class="suggestion-card" onclick="document.querySelector('textarea').value='/experience'; document.querySelector('textarea').focus();">
                <div style="font-size: 24px; margin-bottom: 8px;">💼</div>
                <div style="font-weight: 500; margin-bottom: 4px; font-size: 15px;">View Experience</div>
                <div style="font-size: 13px; color: var(--text-muted);">Explore my professional journey</div>
            </div>
            
            <div class="suggestion-card" onclick="document.querySelector('textarea').value='/projects'; document.querySelector('textarea').focus();">
                <div style="font-size: 24px; margin-bottom: 8px;">🚀</div>
                <div style="font-weight: 500; margin-bottom: 4px; font-size: 15px;">Explore Projects</div>
                <div style="font-size: 13px; color: var(--text-muted);">Check out my AI/ML projects</div>
            </div>
            
            <div class="suggestion-card" onclick="document.querySelector('textarea').value='/skills'; document.querySelector('textarea').focus();">
                <div style="font-size: 24px; margin-bottom: 8px;">🎯</div>
                <div style="font-weight: 500; margin-bottom: 4px; font-size: 15px;">Technical Skills</div>
                <div style="font-size: 13px; color: var(--text-muted);">See my tech stack</div>
            </div>
            
            <div class="suggestion-card" onclick="document.querySelector('textarea').value='Tell me about your experience'; document.querySelector('textarea').focus();">
                <div style="font-size: 24px; margin-bottom: 8px;">🤖</div>
                <div style="font-weight: 500; margin-bottom: 4px; font-size: 15px;">Ask Me Anything</div>
                <div style="font-size: 13px; color: var(--text-muted);">Chat about my skills</div>
            </div>
        </div>
    </div>
    """


def create_command_dropdown():
    """Create command dropdown HTML"""
    items = ""
    for cmd in COMMANDS:
        items += f"""
        <div class="command-item" onclick="document.querySelector('textarea').value='{cmd['cmd']}'; document.querySelector('textarea').focus(); this.parentElement.style.display='none';">
            <span class="command-icon">{cmd['icon']}</span>
            <div>
                <div class="command-text">{cmd['cmd']}</div>
                <div class="command-desc">{cmd['desc']}</div>
            </div>
        </div>
        """

    return f'<div class="command-dropdown" style="display:none;" id="cmd-dropdown">{items}</div>'


def chat_response(message, history):
    """Handle chat responses"""
    if not message:
        return history, ""

    # Command responses
    if message.startswith('/projects'):
        response = """
<div class="section-card">
    <div class="section-title">🚀 Featured Projects</div>
    <div class="section-content">
        <strong>1. AI Shop Assistant Chatbot</strong><br>
        Built an e-commerce assistant combining GPT-4o with Pinecone for semantic search. Achieved sub-second response times across 100+ catalog items.<br>
        <div style="margin-top: 8px;">
            <span class="tech-tag">Python</span>
            <span class="tech-tag">FastAPI</span>
            <span class="tech-tag">Streamlit</span>
            <span class="tech-tag">GPT-4o</span>
            <span class="tech-tag">Pinecone</span>
        </div>
        <br>
        
        <strong>2. CreditPredictor</strong><br>
        End-to-end ML pipeline with 85% accuracy and AUC 0.95. Deployed on AWS EC2 with 99.9% uptime.<br>
        <div style="margin-top: 8px;">
            <span class="tech-tag">XGBoost</span>
            <span class="tech-tag">Flask</span>
            <span class="tech-tag">AWS</span>
        </div>
        <br>
        
        <strong>3. AdClickOptimizer</strong><br>
        ML models with 96% accuracy for predicting ad click-through rates.<br>
        <div style="margin-top: 8px;">
            <span class="tech-tag">Random Forest</span>
            <span class="tech-tag">Flask</span>
        </div>
    </div>
</div>
        """
    elif message.startswith('/experience'):
        response = """
<div class="section-card">
    <div class="section-title">💼 Professional Experience</div>
    <div class="section-content">
        <strong>AI Engineer @ XNODE Inc.</strong> (Mar 2025 - Aug 2025)<br>
        • Built Workflow Builder Agent with LangChain + LangGraph, cutting process time by 60%<br>
        • Engineered RAG-based knowledge framework<br>
        <div style="margin-top: 8px;">
            <span class="tech-tag">LangChain</span>
            <span class="tech-tag">LangGraph</span>
            <span class="tech-tag">RAG</span>
        </div>
        <br>
        
        <strong>Research Data Scientist @ Behavioral Informatics Labs</strong><br>
        • Assessed healthcare AI models using GPT and Llama LLMs<br>
        <div style="margin-top: 8px;">
            <span class="tech-tag">GPT</span>
            <span class="tech-tag">Llama</span>
            <span class="tech-tag">BlueBERT</span>
        </div>
    </div>
</div>
        """
    elif message.startswith('/skills'):
        response = """
<div class="section-card">
    <div class="section-title">🎯 Technical Skills</div>
    <div class="section-content">
        <strong>Generative & Agentic AI</strong><br>
        <span class="tech-tag">LangChain</span>
        <span class="tech-tag">LangGraph</span>
        <span class="tech-tag">RAG</span>
        <span class="tech-tag">Prompt Engineering</span>
        <br><br>
        
        <strong>Programming & Databases</strong><br>
        <span class="tech-tag">Python</span>
        <span class="tech-tag">MySQL</span>
        <span class="tech-tag">PostgreSQL</span>
        <span class="tech-tag">MongoDB</span>
        <span class="tech-tag">Chroma</span>
    </div>
</div>
        """
    elif message.startswith('/education'):
        response = """
<div class="section-card">
    <div class="section-title">🎓 Education</div>
    <div class="section-content">
        <strong>MS in Information Technology & Analytics</strong><br>
        Rutgers University | GPA: 3.7/4.0 | Aug 2022 - Jan 2024<br><br>
        
        <strong>BE in Information Technology</strong><br>
        University of Mumbai | GPA: 9.3/10 | Jun 2018 - May 2022
    </div>
</div>
        """
    elif message.startswith('/contact'):
        response = """
<div class="section-card">
    <div class="section-title">📧 Contact Information</div>
    <div class="section-content">
        📧 <strong>Email:</strong> sarjakm369@gmail.com<br>
        📱 <strong>Phone:</strong> +1 (908) 549-2264<br>
        💼 <strong>LinkedIn:</strong> linkedin.com/in/Sarjak369<br>
        🐙 <strong>GitHub:</strong> github.com/Sarjak369<br>
        📍 <strong>Location:</strong> Boston, MA, United States
    </div>
</div>
        """
    else:
        response = """
I'm in preview mode! Once the RAG pipeline is connected, I'll intelligently answer any question about my background.

Try these commands:<br>
<span class="command-hint">/projects</span>
<span class="command-hint">/experience</span>
<span class="command-hint">/skills</span>
<span class="command-hint">/education</span>
<span class="command-hint">/contact</span>
        """

    history.append((message, response))
    return history, ""


def create_ui():
    """Create main UI"""

    # Use Blocks without theme parameter - just CSS
    with gr.Blocks(
        css=get_custom_css(),
        title="Sarjak Maniar - Portfolio"
    ) as demo:

        welcome_visible = gr.State(True)

        with gr.Row(equal_height=False):
            # Sidebar - NO GAP!
            with gr.Column(scale=0, min_width=260, elem_classes="sidebar-column"):
                # Header with logo
                gr.HTML("""
                    <div class="sidebar-header">
                        <div class="sidebar-logo">💬</div>
                    </div>
                """)

                # Navigation
                with gr.Column(elem_classes="nav-section"):
                    skills_btn = gr.Button("🎯 Skills", elem_classes="nav-item")
                    exp_btn = gr.Button(
                        "💼 Experience", elem_classes="nav-item")
                    proj_btn = gr.Button("🚀 Projects", elem_classes="nav-item")
                    edu_btn = gr.Button("🎓 Education", elem_classes="nav-item")

                # Profile at bottom
                gr.HTML("""
                    <div class="profile-section" style="margin-top: 200px;">
                        <div class="profile-card">
                            <div class="profile-avatar">SM</div>
                            <div>
                                <div style="font-size: 14px; font-weight: 500; color: var(--text-primary);">Sarjak Maniar</div>
                                <div style="font-size: 12px; color: var(--text-muted);">AI/ML Engineer</div>
                            </div>
                        </div>
                    </div>
                """)

            # Main Chat Area
            with gr.Column(scale=1, elem_classes="chat-column"):
                # Welcome
                welcome = gr.HTML(create_welcome_screen())

                # Chatbot
                chatbot = gr.Chatbot(
                    value=[],
                    height=600,
                    show_label=False,
                    container=False,
                    type="tuples",
                    visible=False,
                    elem_classes="chatbot-container"
                )

                # Input Area
                with gr.Column(elem_classes="input-wrapper"):
                    gr.HTML(create_command_dropdown())

                    with gr.Column(elem_classes="input-inner"):
                        with gr.Row():
                            msg = gr.Textbox(
                                placeholder='Message Sarjak or type "/" for commands...',
                                show_label=False,
                                container=False,
                                scale=1,
                                lines=1,
                                max_lines=8,
                                elem_id="main-input"
                            )

                        # Buttons inside input
                        gr.HTML("""
                            <div class="input-buttons">
                                <button class="input-btn" onclick="alert('Voice feature coming soon!')">🎤</button>
                                <button class="input-btn send" id="send-btn">➤</button>
                            </div>
                            
                            <script>
                            // Show dropdown on /
                            document.querySelector('#main-input textarea').addEventListener('input', function(e) {
                                const dropdown = document.getElementById('cmd-dropdown');
                                if (this.value === '/') {
                                    dropdown.style.display = 'block';
                                } else {
                                    dropdown.style.display = 'none';
                                }
                            });
                            
                            // Hide dropdown on blur
                            document.querySelector('#main-input textarea').addEventListener('blur', function() {
                                setTimeout(() => {
                                    document.getElementById('cmd-dropdown').style.display = 'none';
                                }, 200);
                            });
                            </script>
                        """)

                        # Hints
                        gr.HTML("""
                            <div class="hint-text">
                                <span class="command-hint">/projects</span>
                                <span class="command-hint">/experience</span>
                                <span class="command-hint">/skills</span>
                                <span class="command-hint">/education</span>
                            </div>
                        """)

                # Event handlers
                def handle_message(message, history, is_welcome):
                    if message:
                        new_history, cleared = chat_response(message, history)
                        return new_history, cleared, gr.update(visible=False), gr.update(visible=True), False
                    return history, message, gr.update(), gr.update(), is_welcome

                def sidebar_click(command, history, is_welcome):
                    new_history, _ = chat_response(command, history)
                    return new_history, gr.update(visible=False), gr.update(visible=True), False

                msg.submit(handle_message, [msg, chatbot, welcome_visible], [
                           chatbot, msg, welcome, chatbot, welcome_visible])

                # Sidebar clicks
                skills_btn.click(lambda h, w: sidebar_click(
                    "/skills", h, w), [chatbot, welcome_visible], [chatbot, welcome, chatbot, welcome_visible])
                exp_btn.click(lambda h, w: sidebar_click("/experience", h, w),
                              [chatbot, welcome_visible], [chatbot, welcome, chatbot, welcome_visible])
                proj_btn.click(lambda h, w: sidebar_click(
                    "/projects", h, w), [chatbot, welcome_visible], [chatbot, welcome, chatbot, welcome_visible])
                edu_btn.click(lambda h, w: sidebar_click(
                    "/education", h, w), [chatbot, welcome_visible], [chatbot, welcome, chatbot, welcome_visible])

    return demo


if __name__ == "__main__":
    demo = create_ui()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
