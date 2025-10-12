"""
Custom CSS - PERFECTED & POLISHED VERSION
"""

CHATGPT_CSS = """
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

.gradio-container {
    max-width: 100% !important;
}

footer {
    display: none !important;
}

/* ===== ANIMATIONS ===== */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes pulse {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: 0.5;
    }
}

/* ===== SIDEBAR ===== */
.sidebar-column {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-subtle) !important;
    width: 260px !important;
    min-width: 260px !important;
    padding: 8px !important;
    position: fixed !important;
    left: 0 !important;
    top: 0 !important;
    height: 100vh !important;
    z-index: 50 !important;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 2px 0 8px rgba(0, 0, 0, 0.3) !important;
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
    transition: all 0.2s ease !important;
    position: relative !important;
    overflow: hidden !important;
}

button.nav-item::before {
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: -100% !important;
    width: 100% !important;
    height: 100% !important;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent) !important;
    transition: left 0.5s !important;
}

button.nav-item:hover::before {
    left: 100% !important;
}

button.nav-item:hover {
    background: #2a2b32 !important;
    transform: translateX(4px) !important;
}

button.nav-item:active {
    transform: scale(0.98) !important;
}

.profile-section {
    position: absolute !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    padding: 12px !important;
    border-top: 1px solid var(--border-subtle) !important;
    background: linear-gradient(to top, var(--bg-sidebar), transparent) !important;
}

/* ===== BUTTONS ===== */
.toggle-btn, .clear-btn {
    position: fixed !important;
    width: 40px !important;
    height: 40px !important;
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    color: var(--text-secondary) !important;
    cursor: pointer !important;
    z-index: 100 !important;
    font-size: 18px !important;
    transition: all 0.2s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
}

.toggle-btn {
    top: 20px !important;
    left: 276px !important;
}

.toggle-btn.sidebar-closed {
    left: 20px !important;
}

.clear-btn {
    top: 20px !important;
    right: 20px !important;
}

.toggle-btn:hover, .clear-btn:hover {
    background: var(--bg-hover) !important;
    transform: scale(1.05) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
}

.toggle-btn:active, .clear-btn:active {
    transform: scale(0.95) !important;
}

/* ===== MAIN CONTENT ===== */
.main-content {
    margin-left: 260px !important;
    transition: margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
    padding-bottom: 140px !important;
}

.main-content.sidebar-closed {
    margin-left: 0 !important;
}

.main-content.sidebar-closed ~ .input-area,
.sidebar-closed ~ * .input-area {
    left: 0 !important;
}

/* ===== WELCOME SCREEN ===== */
.main-content > div:first-of-type {
    animation: fadeIn 0.5s ease-out !important;
    overflow-y: auto !important;
    padding-top: 80px !important;
}

/* ===== CHATBOT ===== */
.chatbot-wrapper {
    background: var(--bg-main) !important;
    border: none !important;
    overflow-y: auto !important;
    padding-top: 80px !important;
    padding-bottom: 0px !important;
}

.chatbot-wrapper .message {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
    animation: slideIn 0.3s ease-out !important;
}

/* Message hover effect */
.chatbot-wrapper .message:hover {
    background: rgba(255, 255, 255, 0.02) !important;
}

/* Hide Gradio's built-in buttons */
.chatbot-wrapper button,
.chatbot-wrapper .copy-button,
.chatbot-wrapper .delete-button,
.chatbot-wrapper [title="Delete"],
.chatbot-wrapper [title="Copy"] {
    display: none !important;
}

/* ===== TYPING INDICATOR ===== */
.typing-indicator {
    display: flex !important;
    gap: 4px !important;
    padding: 16px 24px !important;
}

.typing-indicator span {
    width: 8px !important;
    height: 8px !important;
    border-radius: 50% !important;
    background: var(--text-muted) !important;
    animation: pulse 1.4s ease-in-out infinite !important;
}

.typing-indicator span:nth-child(2) {
    animation-delay: 0.2s !important;
}

.typing-indicator span:nth-child(3) {
    animation-delay: 0.4s !important;
}

/* ===== INPUT AREA ===== */
.input-area {
    padding: 16px 24px !important;
    background: var(--bg-main) !important;
    border-top: 1px solid var(--border-subtle) !important;
    box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.2) !important;
    position: fixed !important;
    bottom: 0 !important;
    left: 260px !important;
    right: 0 !important;
    z-index: 10 !important;
    transition: left 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.input-area textarea {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    padding: 12px 16px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
}

.input-area textarea:hover {
    border-color: #565869 !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
}

.input-area textarea:focus {
    outline: none !important;
    border-color: var(--accent-green) !important;
    box-shadow: 0 0 0 3px rgba(16, 163, 127, 0.1) !important;
}

.hint-text {
    text-align: center !important;
    font-size: 11px !important;
    color: var(--text-muted) !important;
    margin-top: 8px !important;
    margin-bottom: 0 !important;
    overflow: hidden !important;
    white-space: nowrap !important;
    animation: fadeIn 0.5s ease-out !important;
}

.hint-text::-webkit-scrollbar {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
}

.command-hint {
    background: var(--bg-secondary) !important;
    padding: 4px 8px !important;
    border-radius: 6px !important;
    margin: 0 4px !important;
    font-family: 'SF Mono', Monaco, Consolas, monospace !important;
    display: inline-block !important;
    transition: all 0.2s ease !important;
    border: 1px solid var(--border-subtle) !important;
}

.command-hint:hover {
    background: var(--bg-hover) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 10px !important;
    height: 10px !important;
}

::-webkit-scrollbar-track {
    background: transparent !important;
}

::-webkit-scrollbar-thumb {
    background: #565869 !important;
    border-radius: 5px !important;
    border: 2px solid var(--bg-main) !important;
    transition: background 0.2s ease !important;
}

::-webkit-scrollbar-thumb:hover {
    background: #6e6e80 !important;
}

/* ===== LOADING STATE ===== */
.loading {
    opacity: 0.6 !important;
    pointer-events: none !important;
}

/* ===== SMOOTH TRANSITIONS ===== */
* {
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
    .main-content {
        margin-left: 0 !important;
    }
    
    .sidebar-column {
        z-index: 100 !important;
        box-shadow: 2px 0 16px rgba(0, 0, 0, 0.5) !important;
    }
    
    .toggle-btn {
        left: 12px !important;
    }
    
    .toggle-btn.sidebar-open {
        left: 268px !important;
    }
    
    .input-area {
        padding: 16px !important;
    }
}

/* ===== ACCESSIBILITY ===== */
button:focus-visible {
    outline: 2px solid var(--accent-green) !important;
    outline-offset: 2px !important;
}

textarea:focus-visible {
    outline: none !important;
}

/* ===== POLISH ===== */
.gradio-container {
    animation: fadeIn 0.3s ease-out !important;
}

/* Remove Gradio branding */
.gradio-container .footer {
    display: none !important;
}

/* Clean up default Gradio styles */
.block, .form {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
}
"""


def get_custom_css():
    """Returns the custom CSS string"""
    return CHATGPT_CSS
