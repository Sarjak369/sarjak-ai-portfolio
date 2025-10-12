"""
Custom CSS for ChatGPT-style interface
Exact colors, fonts, and styling from ChatGPT
"""

CHATGPT_CSS = """
/* Global Styles - ChatGPT Theme */
:root {
    --bg-primary: #343541;
    --bg-secondary: #444654;
    --bg-sidebar: #202123;
    --text-primary: #ececf1;
    --text-secondary: #c5c5d2;
    --text-muted: #8e8ea0;
    --border-color: #565869;
    --accent-green: #19c37d;
    --accent-purple: #5436da;
    --hover-bg: #2a2b32;
}

/* Main Container */
.gradio-container {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif !important;
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

/* Remove Gradio branding */
footer {
    display: none !important;
}

/* Chatbot Container */
.chatbot-container {
    background: var(--bg-primary) !important;
    border: none !important;
    border-radius: 0 !important;
}

/* Chat Messages */
.message {
    padding: 24px !important;
    border-radius: 0 !important;
    margin: 0 !important;
}

.message.user {
    background: var(--bg-primary) !important;
}

.message.bot {
    background: var(--bg-secondary) !important;
}

/* Input Box - ChatGPT Style */
.input-box textarea {
    background: #40414f !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-size: 15px !important;
    padding: 14px 16px !important;
    resize: none !important;
}

.input-box textarea:focus {
    border-color: var(--accent-green) !important;
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(25, 195, 125, 0.1) !important;
}

/* Buttons */
button {
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

.primary-btn {
    background: var(--accent-green) !important;
    color: white !important;
    border: none !important;
}

.primary-btn:hover {
    background: #1a9f6a !important;
}

.secondary-btn {
    background: transparent !important;
    border: 1px solid var(--border-color) !important;
    color: var(--text-primary) !important;
}

.secondary-btn:hover {
    background: var(--hover-bg) !important;
}

/* Sidebar Styling */
.sidebar {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid #404040 !important;
    padding: 12px !important;
}

.nav-item {
    padding: 12px !important;
    margin: 4px 0 !important;
    border-radius: 6px !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    transition: all 0.2s ease !important;
    color: var(--text-primary) !important;
}

.nav-item:hover {
    background: var(--hover-bg) !important;
}

/* Marquee Header */
.marquee-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    text-align: center;
    overflow: hidden;
    position: relative;
}

.marquee-text {
    animation: scroll 25s linear infinite;
    white-space: nowrap;
    font-size: 18px;
    font-weight: 500;
    color: white;
}

@keyframes scroll {
    0% { transform: translateX(100%); }
    100% { transform: translateX(-100%); }
}

.quote-text {
    font-size: 13px;
    opacity: 0.9;
    font-style: italic;
    margin-top: 8px;
    color: white;
}

/* Command Suggestions */
.command-hint {
    display: inline-block;
    background: #40414f;
    padding: 6px 12px;
    border-radius: 12px;
    font-size: 12px;
    color: var(--text-secondary);
    margin: 4px;
}

/* Loading Animation */
.loading-dots::after {
    content: '...';
    animation: dots 1.5s steps(4, end) infinite;
}

@keyframes dots {
    0%, 20% { content: '.'; }
    40% { content: '..'; }
    60%, 100% { content: '...'; }
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-sidebar);
}

::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #6e6e80;
}

/* Section Cards */
.section-card {
    background: var(--bg-secondary);
    padding: 20px;
    border-radius: 12px;
    margin: 12px 0;
    border: 1px solid #404040;
}

.section-card:hover {
    border-color: var(--border-color);
}

.section-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 12px;
}

.section-content {
    color: var(--text-secondary);
    line-height: 1.6;
}

/* Tags */
.tech-tag {
    display: inline-block;
    background: #40414f;
    color: var(--text-secondary);
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 12px;
    margin: 4px 4px 4px 0;
}

/* Toggle Button for Sidebar */
.sidebar-toggle {
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 1000;
    background: var(--bg-sidebar) !important;
    border: 1px solid var(--border-color) !important;
    color: var(--text-primary) !important;
    width: 40px;
    height: 40px;
    border-radius: 8px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}

.sidebar-toggle:hover {
    background: var(--hover-bg) !important;
}

/* Responsive Design */
@media (max-width: 768px) {
    .sidebar {
        position: fixed;
        left: -260px;
        transition: left 0.3s ease;
        z-index: 999;
        height: 100vh;
    }
    
    .sidebar.open {
        left: 0;
    }
}

/* Voice Button Animation */
.voice-btn {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}

/* Gradient Text */
.gradient-text {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 600;
}

/* Command Dropdown */
.command-dropdown {
    position: absolute;
    bottom: 100%;
    left: 0;
    right: 0;
    background: #40414f;
    border: 1px solid var(--border-color);
    border-radius: 12px;
    margin-bottom: 8px;
    padding: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.command-item {
    padding: 10px 12px;
    border-radius: 6px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--text-primary);
}

.command-item:hover {
    background: var(--hover-bg);
}

.command-icon {
    font-size: 16px;
}

.command-text {
    flex: 1;
}

.command-desc {
    font-size: 12px;
    color: var(--text-muted);
}
"""


def get_custom_css():
    """Returns the custom CSS string"""
    return CHATGPT_CSS
