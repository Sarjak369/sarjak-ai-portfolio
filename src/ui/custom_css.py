"""
Custom CSS - EXACT ChatGPT Style - FIXED VERSION
"""

CHATGPT_CSS = """
/* ============================================
   EXACT ChatGPT Colors
   ============================================ */
:root {
    --bg-main: #212121;
    --bg-sidebar: #171717;
    --bg-secondary: #2f2f2f;
    --text-primary: #ececf1;
    --text-secondary: #c5c5d2;
    --text-muted: #8e8ea0;
    --border-subtle: #3e3e3e;
    --accent-green: #10a37f;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body, .gradio-container {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    background: var(--bg-main) !important;
    color: var(--text-primary) !important;
}

/* Remove all default Gradio spacing */
.gradio-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
    gap: 0 !important;
}

.contain, .gap, .block, .form {
    gap: 0 !important;
    padding: 0 !important;
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

footer {
    display: none !important;
}

html, body, .gradio-container {
    height: 100vh !important;
    overflow: hidden !important;
}

/* ============================================
   SIDEBAR - Fixed 260px
   ============================================ */
.sidebar-column {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-subtle) !important;
    width: 260px !important;
    min-width: 260px !important;
    max-width: 260px !important;
    height: 100vh !important;
    padding: 8px !important;
    position: fixed !important;
    left: 0 !important;
    top: 0 !important;
    z-index: 50 !important;
    transition: transform 0.2s ease !important;
    display: flex !important;
    flex-direction: column !important;
}

.sidebar-column.collapsed {
    transform: translateX(-260px) !important;
}

/* Sidebar buttons */
button.nav-item {
    width: 100% !important;
    text-align: left !important;
    padding: 10px 12px !important;
    background: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-size: 14px !important;
    cursor: pointer !important;
    transition: background 0.1s ease !important;
    margin-bottom: 2px !important;
}

button.nav-item:hover {
    background: #2a2b32 !important;
}

/* Profile at bottom */
.profile-section {
    margin-top: auto !important;
    padding: 12px !important;
    border-top: 1px solid var(--border-subtle) !important;
}

/* ============================================
   TOGGLE BUTTON - Like ChatGPT
   ============================================ */
.toggle-btn {
    position: fixed !important;
    top: 8px !important;
    left: 268px !important;
    width: 36px !important;
    height: 36px !important;
    background: transparent !important;
    border: none !important;
    border-radius: 6px !important;
    color: var(--text-secondary) !important;
    cursor: pointer !important;
    z-index: 100 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 20px !important;
    transition: all 0.2s ease !important;
}

.toggle-btn:hover {
    background: rgba(255,255,255,0.1) !important;
}

.toggle-btn.sidebar-closed {
    left: 8px !important;
}

/* ============================================
   MAIN CONTENT AREA
   ============================================ */
.main-content {
    margin-left: 260px !important;
    height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
    background: var(--bg-main) !important;
    transition: margin-left 0.2s ease !important;
}

.main-content.sidebar-closed {
    margin-left: 0 !important;
}

/* ============================================
   WELCOME SCREEN - Centered, No Scroll
   ============================================ */
.welcome-screen {
    flex: 1 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 40px !important;
    text-align: center !important;
    overflow: hidden !important;
}

/* ============================================
   CHATBOT AREA - Clean ChatGPT Style
   ============================================ */
.chatbot-wrapper {
    flex: 1 !important;
    overflow-y: auto !important;
    padding: 0 !important;
}

/* Hide Gradio's chatbot container styling */
.chatbot-wrapper .block,
.chatbot-wrapper .contain {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
    padding: 0 !important;
}

/* Message container - alternating backgrounds */
.message-wrap {
    width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
    background: transparent !important;
}

/* User message - dark background */
.message-wrap:nth-child(odd) {
    background: var(--bg-main) !important;
}

/* Bot message - lighter background */
.message-wrap:nth-child(even) {
    background: var(--bg-secondary) !important;
}

/* Message content - centered, max-width */
.message {
    max-width: 48rem !important;
    margin: 0 auto !important;
    padding: 24px !important;
    display: flex !important;
    gap: 16px !important;
    align-items: flex-start !important;
}

/* Remove all Gradio default styling */
.chatbot-wrapper .prose {
    max-width: 100% !important;
}

.chatbot-wrapper .message-wrap > div {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
    padding: 0 !important;
}

/* ============================================
   AVATARS - Clean & Simple
   ============================================ */
.avatar {
    width: 32px !important;
    height: 32px !important;
    min-width: 32px !important;
    border-radius: 4px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

.user-avatar {
    background: #5436DA !important;
    color: white !important;
}

.bot-avatar {
    background: var(--accent-green) !important;
    color: white !important;
    font-size: 18px !important;
}

/* ============================================
   INPUT AREA - Bottom Fixed
   ============================================ */
.input-area {
    padding: 16px 24px 24px 24px !important;
    background: var(--bg-main) !important;
    border-top: 1px solid var(--border-subtle) !important;
}

.input-container {
    max-width: 48rem !important;
    margin: 0 auto !important;
    position: relative !important;
}

textarea {
    width: 100% !important;
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-size: 16px !important;
    padding: 12px 16px !important;
    resize: none !important;
    max-height: 200px !important;
}

textarea:focus {
    outline: none !important;
    border-color: #565869 !important;
}

textarea::placeholder {
    color: var(--text-muted) !important;
}

/* Hint text below input */
.hint-text {
    text-align: center !important;
    font-size: 12px !important;
    color: var(--text-muted) !important;
    margin-top: 12px !important;
}

.command-hint {
    background: var(--bg-secondary) !important;
    padding: 4px 8px !important;
    border-radius: 6px !important;
    margin: 0 4px !important;
    font-family: monospace !important;
}

/* ============================================
   CLEAR BUTTON - Top Right
   ============================================ */
.clear-btn {
    position: fixed !important;
    top: 8px !important;
    right: 16px !important;
    width: 36px !important;
    height: 36px !important;
    background: transparent !important;
    border: none !important;
    border-radius: 6px !important;
    color: var(--text-secondary) !important;
    cursor: pointer !important;
    z-index: 100 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 18px !important;
}

.clear-btn:hover {
    background: rgba(255,255,255,0.1) !important;
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
    background: #565869 !important;
    border-radius: 4px !important;
}

::-webkit-scrollbar-thumb:hover {
    background: #6e6e80 !important;
}

/* ============================================
   HIDE GRADIO DEFAULTS
   ============================================ */
.chatbot .avatar-container {
    display: none !important;
}

.chatbot .message-buttons-bot,
.chatbot .message-buttons-user {
    display: none !important;
}

/* Remove duplicate buttons */
button[value="🗑️"]:not(.clear-btn) {
    display: none !important;
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 768px) {
    .sidebar-column {
        position: fixed !important;
        z-index: 100 !important;
    }
    
    .main-content {
        margin-left: 0 !important;
    }
    
    .toggle-btn {
        left: 8px !important;
    }
    
    .toggle-btn.sidebar-open {
        left: 268px !important;
    }
}
"""


def get_custom_css():
    """Returns the custom CSS string"""
    return CHATGPT_CSS
