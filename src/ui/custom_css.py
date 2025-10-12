"""
Custom CSS - ChatGPT Style - FINAL WORKING VERSION
"""

CHATGPT_CSS = """
/* Colors */
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
    height: 100vh !important;
    overflow: hidden !important;
}

/* Kill ALL Gradio defaults */
.gradio-container, .contain, .gap, .block, .form {
    padding: 0 !important;
    margin: 0 !important;
    gap: 0 !important;
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
    max-width: 100% !important;
}

footer {
    display: none !important;
}

/* ============= LAYOUT FIX ============= */
.gradio-container > .main {
    height: 100vh !important;
}

.gradio-container .main > .contain {
    height: 100vh !important;
}

/* ============= SIDEBAR ============= */
.sidebar-column {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-subtle) !important;
    width: 260px !important;
    min-width: 260px !important;
    height: 100vh !important;
    padding: 8px !important;
    position: fixed !important;
    left: 0 !important;
    top: 0 !important;
    z-index: 50 !important;
    transition: transform 0.2s !important;
}

.sidebar-column.collapsed {
    transform: translateX(-260px) !important;
}

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
    margin-bottom: 2px !important;
}

button.nav-item:hover {
    background: #2a2b32 !important;
}

.profile-section {
    position: absolute !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    padding: 12px !important;
    border-top: 1px solid var(--border-subtle) !important;
}

/* ============= TOGGLE & CLEAR ============= */
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
    font-size: 20px !important;
    transition: left 0.2s !important;
}

.toggle-btn.sidebar-closed {
    left: 8px !important;
}

.toggle-btn:hover {
    background: rgba(255,255,255,0.1) !important;
}

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
    font-size: 18px !important;
}

.clear-btn:hover {
    background: rgba(255,255,255,0.1) !important;
}

/* Hide duplicate buttons */
button:not(.toggle-btn):not(.clear-btn):not(.nav-item)[value*="☰"],
button:not(.toggle-btn):not(.clear-btn):not(.nav-item)[value*="🗑"] {
    display: none !important;
}

/* ============= MAIN CONTENT ============= */
.main-content {
    margin-left: 260px !important;
    height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
    transition: margin-left 0.2s !important;
}

.main-content.sidebar-closed {
    margin-left: 0 !important;
}

/* Force proper column structure */
.main-content > .block {
    display: flex !important;
    flex-direction: column !important;
    height: 100vh !important;
}

/* ============= WELCOME ============= */
.welcome-screen {
    flex: 1 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 40px !important;
    overflow: hidden !important;
}

/* ============= CHAT AREA - TAKES MOST SPACE ============= */
.chatbot-wrapper {
    flex: 1 !important;
    overflow-y: auto !important;
    background: var(--bg-main) !important;
    min-height: 0 !important;
}

/* Remove ALL Gradio styling */
.chatbot-wrapper > div,
.chatbot-wrapper .block,
.chatbot-wrapper .contain {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
    height: 100% !important;
}

/* ============= MESSAGES - RIGHT FOR USER, LEFT FOR BOT ============= */
.chat-message {
    width: 100% !important;
    padding: 20px 24px !important;
    margin: 0 !important;
    display: flex !important;
    justify-content: flex-start !important;
}

.chat-message.user-message {
    background: var(--bg-main) !important;
    justify-content: flex-end !important;
}

.chat-message.bot-message {
    background: var(--bg-secondary) !important;
    justify-content: flex-start !important;
}

.message-bubble {
    max-width: 65% !important;
    display: flex !important;
    gap: 12px !important;
    align-items: flex-start !important;
}

.message-avatar {
    width: 32px !important;
    height: 32px !important;
    min-width: 32px !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 16px !important;
}

.user-avatar {
    background: #5436DA !important;
    order: 2 !important;
}

.bot-avatar {
    background: var(--accent-green) !important;
    order: 1 !important;
}

.message-text {
    flex: 1 !important;
    color: var(--text-primary) !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
}

.user-message .message-text {
    order: 1 !important;
    text-align: right !important;
}

.bot-message .message-text {
    order: 2 !important;
}

/* Remove boxes from content */
.message-text > div,
.message-text > p {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 0 8px 0 !important;
}

.message-text h2 {
    font-size: 18px !important;
    font-weight: 600 !important;
    margin: 0 0 12px 0 !important;
}

.message-text h3 {
    font-size: 16px !important;
    font-weight: 600 !important;
    margin: 12px 0 6px 0 !important;
}

/* Cards in responses */
.message-text div[style*="rgba(255,255,255,0.03)"] {
    margin: 8px 0 !important;
    padding: 14px !important;
    text-align: left !important;
}

/* ============= INPUT AREA - MINIMAL AT BOTTOM ============= */
.input-area {
    flex-shrink: 0 !important;
    padding: 12px 24px 16px 24px !important;
    background: var(--bg-main) !important;
    border-top: 1px solid var(--border-subtle) !important;
}

.input-container {
    max-width: 48rem !important;
    margin: 0 auto !important;
}

.input-container > .block {
    margin: 0 !important;
    padding: 0 !important;
}

textarea {
    width: 100% !important;
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-size: 15px !important;
    padding: 10px 14px !important;
    resize: none !important;
    min-height: 44px !important;
    max-height: 200px !important;
}

textarea:focus {
    outline: none !important;
    border-color: #565869 !important;
}

.hint-text {
    text-align: center !important;
    font-size: 11px !important;
    color: var(--text-muted) !important;
    margin-top: 8px !important;
    overflow: hidden !important;
    white-space: nowrap !important;
}

.command-hint {
    background: var(--bg-secondary) !important;
    padding: 3px 6px !important;
    border-radius: 4px !important;
    margin: 0 3px !important;
    font-family: monospace !important;
    font-size: 10px !important;
}

/* Remove scroller from hints */
.hint-text::-webkit-scrollbar {
    display: none !important;
}

/* ============= SCROLLBAR ============= */
.chatbot-wrapper::-webkit-scrollbar {
    width: 8px !important;
}

.chatbot-wrapper::-webkit-scrollbar-track {
    background: transparent !important;
}

.chatbot-wrapper::-webkit-scrollbar-thumb {
    background: #565869 !important;
    border-radius: 4px !important;
}

/* ============= RESPONSIVE ============= */
@media (max-width: 768px) {
    .main-content {
        margin-left: 0 !important;
    }
    
    .sidebar-column {
        z-index: 100 !important;
    }
    
    .toggle-btn {
        left: 8px !important;
    }
    
    .toggle-btn.sidebar-open {
        left: 268px !important;
    }
    
    .message-bubble {
        max-width: 85% !important;
    }
}
"""


def get_custom_css():
    """Returns the custom CSS string"""
    return CHATGPT_CSS
