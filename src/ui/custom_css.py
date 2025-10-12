"""
Custom CSS - EXACT ChatGPT Color Scheme
"""

CHATGPT_CSS = """
/* ============================================
   EXACT ChatGPT Colors - No Purple!
   ============================================ */

:root {
    --bg-main: #212121;           /* Main background - Mine Shaft */
    --bg-sidebar: #181818;        /* Sidebar - Cod Gray */
    --bg-secondary: #2f2f2f;      /* Secondary elements */
    --bg-input: #40414f;          /* Input box */
    --bg-hover: #2a2b32;          /* Hover state */
    
    --text-primary: #ececf1;      /* Primary text */
    --text-secondary: #c5c5d2;    /* Secondary text */
    --text-muted: #8e8ea0;        /* Muted text */
    
    --border-color: #565869;      /* Borders */
    --border-subtle: #3e3e3e;     /* Subtle borders */
    
    --accent-green: #10a37f;      /* ChatGPT green */
    --accent-blue: #19c37d;       /* Accent blue */
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body, .gradio-container {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif !important;
    background: var(--bg-main) !important;
    color: var(--text-primary) !important;
}

/* ============================================
   Remove ALL Padding/Gaps
   ============================================ */
.gradio-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
    gap: 0 !important;
}

.contain, .gap {
    gap: 0 !important;
    padding: 0 !important;
}

footer {
    display: none !important;
}

/* ============================================
   Sidebar - EXACT ChatGPT Style
   ============================================ */
.sidebar-column {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-subtle) !important;
    padding: 8px !important;
    margin: 0 !important;
    min-height: 100vh !important;
}

/* Sidebar header with logo */
.sidebar-header {
    padding: 12px 12px 8px 12px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
}

.sidebar-logo {
    width: 24px !important;
    height: 24px !important;
    border-radius: 4px !important;
    background: var(--bg-main) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* Navigation items - exact ChatGPT */
.nav-section {
    display: flex !important;
    flex-direction: column !important;
    gap: 2px !important;
    padding: 4px 0 !important;
}

button.nav-item {
    width: 100% !important;
    text-align: left !important;
    padding: 10px 12px !important;
    margin: 0 !important;
    background: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-size: 14px !important;
    font-weight: 400 !important;
    cursor: pointer !important;
    transition: background 0.1s ease !important;
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
}

button.nav-item:hover {
    background: var(--bg-hover) !important;
}

button.nav-item.active {
    background: var(--bg-main) !important;
}

.nav-icon {
    font-size: 16px !important;
    width: 20px !important;
    text-align: center !important;
    opacity: 0.9 !important;
}

/* Profile section */
.profile-section {
    margin-top: auto !important;
    padding: 8px 12px !important;
    border-top: 1px solid var(--border-subtle) !important;
}

.profile-card {
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    padding: 8px !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    transition: background 0.1s ease !important;
}

.profile-card:hover {
    background: var(--bg-hover) !important;
}

.profile-avatar {
    width: 32px !important;
    height: 32px !important;
    border-radius: 50% !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    color: white !important;
}

/* ============================================
   Main Chat Area
   ============================================ */
.chat-column {
    background: var(--bg-main) !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Welcome screen */
.welcome-container {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 80px 20px !important;
    min-height: 70vh !important;
}

.welcome-title {
    font-size: 32px !important;
    font-weight: 600 !important;
    margin-bottom: 48px !important;
    color: var(--text-primary) !important;
}

.suggestion-grid {
    display: grid !important;
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 12px !important;
    max-width: 800px !important;
}

.suggestion-card {
    background: var(--bg-secondary) !important;
    padding: 16px !important;
    border-radius: 8px !important;
    border: 1px solid var(--border-subtle) !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
}

.suggestion-card:hover {
    background: #353535 !important;
    border-color: var(--border-color) !important;
}

/* Chatbot */
.chatbot-container {
    background: var(--bg-main) !important;
    border: none !important;
}

/* ============================================
   Input Box - EXACT ChatGPT Style
   ============================================ */
.input-wrapper {
    background: var(--bg-main) !important;
    padding: 0 0 24px 0 !important;
    border-top: 1px solid var(--border-subtle) !important;
}

.input-inner {
    max-width: 48rem !important;
    margin: 24px auto 0 auto !important;
    padding: 0 24px !important;
    position: relative !important;
}

textarea {
    width: 100% !important;
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-size: 16px !important;
    line-height: 24px !important;
    padding: 12px 52px 12px 16px !important;
    resize: none !important;
    max-height: 200px !important;
    box-shadow: none !important;
}

textarea:focus {
    outline: none !important;
    border-color: var(--border-color) !important;
    box-shadow: 0 0 0 1px var(--border-color) !important;
}

textarea::placeholder {
    color: var(--text-muted) !important;
}

/* Input buttons - positioned inside */
.input-buttons {
    position: absolute !important;
    right: 32px !important;
    bottom: 10px !important;
    display: flex !important;
    gap: 4px !important;
}

.input-btn {
    width: 32px !important;
    height: 32px !important;
    min-width: 32px !important;
    padding: 0 !important;
    background: transparent !important;
    border: none !important;
    border-radius: 6px !important;
    color: var(--text-secondary) !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: background 0.1s ease !important;
}

.input-btn:hover {
    background: var(--bg-hover) !important;
}

.input-btn.send {
    background: var(--accent-green) !important;
    color: white !important;
}

.input-btn.send:hover {
    background: #0e8c6f !important;
}

.input-btn.send:disabled {
    background: var(--bg-hover) !important;
    color: var(--text-muted) !important;
    cursor: not-allowed !important;
}

/* ============================================
   Command Dropdown (/)
   ============================================ */
.command-dropdown {
    position: absolute !important;
    bottom: calc(100% + 8px) !important;
    left: 0 !important;
    right: 0 !important;
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    padding: 8px !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5) !important;
    z-index: 1000 !important;
    max-height: 300px !important;
    overflow-y: auto !important;
}

.command-item {
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    padding: 10px 12px !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    transition: background 0.1s ease !important;
}

.command-item:hover {
    background: var(--bg-hover) !important;
}

.command-icon {
    font-size: 16px !important;
    width: 20px !important;
    text-align: center !important;
}

.command-text {
    flex: 1 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: var(--text-primary) !important;
}

.command-desc {
    font-size: 12px !important;
    color: var(--text-muted) !important;
    margin-top: 2px !important;
}

/* ============================================
   Section Cards in Chat
   ============================================ */
.section-card {
    background: var(--bg-secondary) !important;
    padding: 20px !important;
    border-radius: 12px !important;
    margin: 12px 0 !important;
    border: 1px solid var(--border-subtle) !important;
}

.section-title {
    font-size: 18px !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    margin-bottom: 16px !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}

.section-content {
    color: var(--text-secondary) !important;
    line-height: 1.6 !important;
    font-size: 14px !important;
}

.tech-tag {
    display: inline-block !important;
    background: var(--bg-main) !important;
    color: var(--text-secondary) !important;
    padding: 4px 10px !important;
    border-radius: 12px !important;
    font-size: 12px !important;
    margin: 4px 4px 4px 0 !important;
    border: 1px solid var(--border-subtle) !important;
}

/* ============================================
   Hint Text
   ============================================ */
.hint-text {
    text-align: center !important;
    font-size: 12px !important;
    color: var(--text-muted) !important;
    margin-top: 12px !important;
}

.command-hint {
    display: inline-block !important;
    background: var(--bg-secondary) !important;
    padding: 4px 8px !important;
    border-radius: 8px !important;
    font-size: 11px !important;
    color: var(--text-secondary) !important;
    margin: 0 4px !important;
    border: 1px solid var(--border-subtle) !important;
    font-family: 'SF Mono', Monaco, monospace !important;
}

/* ============================================
   Scrollbar
   ============================================ */
::-webkit-scrollbar {
    width: 8px !important;
}

::-webkit-scrollbar-track {
    background: transparent !important;
}

::-webkit-scrollbar-thumb {
    background: var(--border-color) !important;
    border-radius: 4px !important;
}

::-webkit-scrollbar-thumb:hover {
    background: #6e6e80 !important;
}

/* ============================================
   Gradio Component Overrides
   ============================================ */
.block {
    border: none !important;
    box-shadow: none !important;
}

.form {
    border: none !important;
    background: transparent !important;
}
"""


def get_custom_css():
    """Returns the custom CSS string"""
    return CHATGPT_CSS
