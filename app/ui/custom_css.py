"""
Custom CSS for ChatGPT-style interface
Clean, organized, single-source-of-truth styling
"""

CHATGPT_CSS = """
/* ============================================================================
   THEME VARIABLES
   ============================================================================ */
:root {
    --bg-main: #212121;
    --bg-sidebar: #171717;
    --bg-secondary: #2f2f2f;
    --text-primary: #ececf1;
    --text-secondary: #c5c5d2;
    --text-muted: #8e8ea0;
    --border-subtle: #3e3e3e;
    --accent-green: #10a37f;
    --accent-hover: #0d8c6e;
}

/* ============================================================================
   GLOBAL STYLES
   ============================================================================ */
body, .gradio-container {
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
}

.gradio-container {
    max-width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* ============================================================================
   EMAIL GATE (Landing Page)
   ============================================================================ */
#email-gate {
    max-width: 500px !important;
    margin: 60px auto !important;
    padding: 50px !important;
    background: var(--bg-secondary) !important;
    border-radius: 16px !important;
    border: 1px solid var(--border-subtle) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4) !important;
}

.hero-avatar {
    display: block !important;
    margin: 0 auto 12px auto !important;
    width: 88px !important;
    height: 88px !important;
    border-radius: 50% !important;
    box-shadow: 0 6px 24px rgba(0,0,0,0.35) !important;
    border: 2px solid rgba(255,255,255,0.08) !important;
    object-fit: cover !important;

}

/* ============================================================================
   MAIN CONTAINER
   ============================================================================ */
#main-container {
    height: calc(100vh - 60px) !important;
    max-width: 100% !important;
    margin: 0 !important;
    overflow: hidden !important;
}

/* ============================================================================
   SIDEBAR
   ============================================================================ */
#sidebar {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-subtle) !important;
    height: 100% !important;
    width: 280px !important;
    display: grid !important;
    grid-template-rows: auto 1fr auto !important;
}

/* Sidebar Header */
.sidebar-header {
    padding: 24px 20px !important;
    border-bottom: 1px solid var(--border-subtle) !important;
}

.sidebar-header h2 {
    font-size: 19px !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    margin: 0 !important;
    letter-spacing: 0.3px !important;
}

/* Sidebar Scrollable Content */
#sidebar-scroll-content {
    overflow-y: auto !important;
    padding: 16px 18px 6px 18px !important;
}

.sidebar-text {
    font-size: 13px !important;
    line-height: 1.7 !important;
    color: var(--text-secondary) !important;
}

.sidebar-text h3 {
    font-size: 11px !important;
    font-weight: 700 !important;
    color: var(--accent-green) !important;
    margin: 24px 0 12px 0 !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}

.sidebar-text code {
    background: rgba(16, 163, 127, 0.15) !important;
    padding: 3px 8px !important;
    border-radius: 6px !important;
    color: var(--accent-green) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    white-space: nowrap !important;
    border: 1px solid rgba(16, 163, 127, 0.2) !important;
}

.sidebar-text em {
    color: var(--text-muted) !important;
    font-style: italic !important;
    display: block !important;
    margin-top: 8px !important;
    padding: 12px !important;
    background: rgba(16, 163, 127, 0.05) !important;
    border-left: 3px solid var(--accent-green) !important;
    border-radius: 4px !important;
    font-size: 12px !important;
    line-height: 1.6 !important;
}

/* Sidebar Footer (Credits + User) */
#sidebar-footer {
    border-top: 1px solid var(--border-subtle) !important;
    padding: 12px 14px !important;
    background: linear-gradient(180deg, #161616, #121212) !important;
}

#credit-display {
    background: var(--accent-green) !important;
    color: white !important;
    padding: 10px 12px !important;
    border-radius: 999px !important;
    text-align: center !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    margin: 0 0 10px 0 !important;
    box-shadow: 0 6px 18px rgba(16,163,127,0.25) !important;
}

.user-info {
    display: grid !important;
    grid-template-columns: 36px 1fr !important;
    align-items: center !important;
    gap: 10px !important;
    padding: 10px 12px !important;
    background: var(--bg-secondary) !important;
    border-radius: 12px !important;
    border: 1px solid #2a2a2a !important;
}

.user-avatar {
    width: 36px !important;
    height: 36px !important;
    border-radius: 50% !important;
}

.user-name {
    font-size: 13px !important;
    color: var(--text-primary) !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    line-height: 1 !important;
}

/* ============================================================================
   CHAT AREA
   ============================================================================ */
#chat-column {
    display: flex !important;
    flex-direction: column !important;
    height: 100% !important;
    padding: 0 20px !important;
}

/* Chat Header (with Clear button) */
#chat-header {
    padding: 8px 4px !important;
    display: flex !important;
    justify-content: flex-end !important;
    align-items: center !important;
    flex-shrink: 0 !important;
}

#clear-button {
    width: auto !important;
    min-width: 96px !important;
    background: transparent !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--accent-green) !important;
    border-radius: 999px !important;
    padding: 6px 14px !important;
    font-size: 13px !important;
    cursor: pointer !important;
    line-height: 1 !important;
    box-shadow: none !important;
    margin-left: auto !important;
}

#clear-button:hover {
    background: rgba(16,163,127,0.08) !important;
    color: var(--accent-green) !important;
}

/* ============================================================================
   CHATBOT COMPONENT (CRITICAL: Remove All Double Layers)
   ============================================================================ */

/* Main chatbot container */
#main-chatbot {
    flex: 1 !important;
    overflow-y: auto !important;
    padding:8px !important;
}

/* ===========================================
   STEP 1: Neutralize ALL Gradio Inner Layers
   =========================================== */
#main-chatbot .message,
#main-chatbot .message *:not(img):not(code):not(pre):not(a) {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

/* Remove pseudo-elements that create extra borders */
#main-chatbot .message::before,
#main-chatbot .message::after,
#main-chatbot .message *::before,
#main-chatbot .message *::after {
    content: none !important;
    display: none !important;
}

/* ===========================================
   STEP 2: Style the OUTER Message Container ONLY
   =========================================== */
#main-chatbot .message {
    background: linear-gradient(180deg, rgba(47,47,47,0.7) 0%, rgba(37,37,37,0.7) 100%) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    padding: 12px 14px !important;
    margin: 8px 0 !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
}

/* Accent borders for user vs assistant */
#main-chatbot .message.user {
    border-left: 3px solid var(--accent-green) !important;
}

#main-chatbot .message.bot,
#main-chatbot .message.assistant {
    border-left: 3px solid #6ea8fe !important;
}

/* ===========================================
   STEP 3: Avatar Styling (No Extra Borders)
   =========================================== */
#main-chatbot .avatar-container {
    width: 45px !important; 
    height: 45px !important;
    flex-shrink: 0 !important;
    margin-right: 12px !important;
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

#main-chatbot .avatar-container img {
    width: 45px !important;
    height: 45px !important;
    border-radius: 50% !important;
    object-fit: cover !important;
    border: none !important;
    box-shadow: none !important;
}

/* ===========================================
   STEP 4: Message Content Styling
   =========================================== */
#main-chatbot .message-content {
    flex: 1 !important;
}

#main-chatbot .message p {
    color: var(--text-secondary) !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
    margin: 0 0 8px 0 !important;
}

#main-chatbot .message p:last-child {
    margin-bottom: 0 !important;
}

#main-chatbot .message code {
    background: rgba(16,163,127,0.15) !important;
    color: #b9ffea !important;
    border: 1px solid rgba(16,163,127,0.25) !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
    font-size: 13px !important;
}

#main-chatbot .message a {
    color: var(--accent-green) !important;
    text-decoration: none !important;
}

#main-chatbot .message a:hover {
    text-decoration: underline !important;
}

/* ===========================================
   STEP 5: Delete Button Styling
   =========================================== */
#main-chatbot .icon-button,
#main-chatbot button[aria-label="Delete"] {
    width: 28px !important;
    height: 28px !important;
    min-width: 28px !important;
    min-height: 28px !important;
    border-radius: 8px !important;
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    opacity: 0.5 !important;
    transition: all 0.2s ease !important;
}

#main-chatbot .message:hover .icon-button,
#main-chatbot .message:hover button[aria-label="Delete"] {
    opacity: 1 !important;
    background: rgba(239, 68, 68, 0.1) !important;
    border-color: #ef4444 !important;
}

/* ============================================================================
   INPUT AREA
   ============================================================================ */
#input-row {
    max-width: 900px !important;
    margin: 16px auto 10px auto !important;
    flex-shrink: 0 !important;
}

#message-input {
    background-color: var(--bg-sidebar) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: var(--text-primary) !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
    font-size: 15px !important;
}

#message-input:focus {
    border-color: var(--accent-green) !important;
    box-shadow: 0 0 0 3px rgba(16,163,127,0.15) !important;
    outline: none !important;
}

#send-button {
    background: var(--accent-green) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 26px !important;
    font-weight: 600 !important;
    box-shadow: 0 8px 18px rgba(16,163,127,0.28) !important;
}

#send-button:hover {
    background: var(--accent-hover) !important;
}

/* ============================================================================
   SUGGESTED QUESTIONS
   ============================================================================ */
#suggested-row {
    max-width: 900px !important;
    margin: 10px auto 20px auto !important;
    flex-shrink: 0 !important;
}

#suggested-row button {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 999px !important;
    padding: 8px 14px !important;
    font-size: 12px !important;
    color: var(--text-secondary) !important;
}

#suggested-row button:hover {
    background: rgba(16,163,127,0.12) !important;
    border-color: var(--accent-green) !important;
    color: var(--accent-green) !important;
}

/* ============================================================================
   FORM INPUTS
   ============================================================================ */
input[type="text"],
input[type="email"],
textarea {
    background-color: var(--bg-sidebar) !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
    padding: 12px !important;
}

input:focus,
textarea:focus {
    border-color: var(--accent-green) !important;
    box-shadow: 0 0 0 3px rgba(16,163,127,0.1) !important;
    outline: none !important;
}

label {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
}

button {
    transition: all 0.2s ease !important;
}

/* ============================================================================
   MARKDOWN GLOBAL STYLES
   ============================================================================ */
.markdown {
    color: var(--text-primary) !important;
}

.markdown p {
    color: var(--text-secondary) !important;
    line-height: 1.6 !important;
}

.markdown code {
    background: var(--bg-sidebar) !important;
    color: var(--accent-green) !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
}

.markdown a {
    color: var(--accent-green) !important;
}

/* ============================================================================
   SCROLLBAR
   ============================================================================ */
::-webkit-scrollbar {
    width: 6px !important;
}

::-webkit-scrollbar-track {
    background: var(--bg-sidebar) !important;
}

::-webkit-scrollbar-thumb {
    background: #4a4a4a !important;
    border-radius: 3px !important;
}

::-webkit-scrollbar-thumb:hover {
    background: #5a5a5a !important;
}

/* ============================================================================
   MOBILE RESPONSIVE
   ============================================================================ */
@media (max-width: 1024px) {
    #sidebar {
        display: none !important;
    }
    
    #main-container {
        padding: 10px !important;
    }
}
"""
