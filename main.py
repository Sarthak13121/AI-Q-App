import streamlit as st
from groq import Groq
import time
import random
import pandas as pd
import os

# --- 1. SECURE API SETUP ---
def get_api_key():
    try:
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
    return "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"

API_KEY = get_api_key()
client = Groq(api_key=API_KEY)

# --- 2. DATA PERSISTENCE ---
SCORE_FILE = "leaderboard.csv"

def get_leaderboard():
    if not os.path.exists(SCORE_FILE):
        return pd.DataFrame(columns=["Name", "XP", "Rank"])
    return pd.read_csv(SCORE_FILE)

def save_score(name, xp, rank):
    df = get_leaderboard()
    if name in df['Name'].values:
        if xp > df.loc[df['Name'] == name, 'XP'].values[0]:
            df.loc[df['Name'] == name, ['XP', 'Rank']] = [xp, rank]
    else:
        new_row = pd.DataFrame([{"Name": name, "XP": xp, "Rank": rank}])
        df = pd.concat([df, new_row], ignore_index=True)
    df.sort_values(by="XP", ascending=False).to_csv(SCORE_FILE, index=False)

# --- 3. QUESTION ENGINE (90 UNIQUE MCQs) ---
questions_db = {
    "Cyber-Safety": {
        "Easy": [{"q": "Is '123456' a strong password?", "a": "❌ NO", "w": ["✅ YES"], "h": "Commonly hacked."}, {"q": "Click links in unknown emails?", "a": "❌ NO", "w": ["✅ YES"], "h": "Phishing risk."}, {"q": "Can AI ask for your bank PIN?", "a": "❌ REFUSE", "w": ["✅ PROVIDE"], "h": "Privacy first."}, {"q": "Is it okay to share your OTP?", "a": "❌ NEVER", "w": ["✅ SOMETIMES"], "h": "OTPs are for you only."}, {"q": "Public Wi-Fi is safe for banking.", "a": "❌ FALSE", "w": ["✅ TRUE"], "h": "Use a VPN."}, {"q": "Locking your PC is good.", "a": "✅ TRUE", "w": ["❌ FALSE"], "h": "Physical security."}, {"q": "Social media quizzes are safe.", "a": "❌ FALSE", "w": ["✅ TRUE"], "h": "They collect data."}, {"q": "Antivirus software is helpful.", "a": "✅ TRUE", "w": ["❌ FALSE"], "h": "Shields system."}, {"q": "AI can make fake news.", "a": "✅ TRUE", "w": ["❌ FALSE"], "h": "Deepfake risk."}, {"q": "Should you backup data?", "a": "✅ YES", "w": ["❌ NO"], "h": "Safety first."}],
        "Medium": [{"q": "What is 2FA?", "a": "Two-Factor Auth", "w": ["Two-File Access", "Timed Auth"], "h": "Double security."}, {"q": "What is a 'Deepfake'?", "a": "AI Altered Media", "w": ["Old Movie", "Photo Filter"], "h": "Swaps faces/voices."}, {"q": "HTTPS means:", "a": "Encrypted Site", "w": ["Fast Site", "Hidden Site"], "h": "S stands for Secure."}, {"q": "A Firewall blocks:", "a": "Unauth Access", "w": ["All Internet", "Virus only"], "h": "Network filter."}, {"q": "What is Phishing?", "a": "Fraud Emails", "w": ["Fishing Hobby", "Slow Web"], "h": "Scams for data."}, {"q": "Is 'admin/admin' safe?", "a": "❌ NO", "w": ["✅ YES"], "h": "Common default login."}, {"q": "Spyware is Malware.", "a": "✅ TRUE", "w": ["❌ FALSE"], "h": "Tracks user activity."}, {"q": "Cookies can track you.", "a": "✅ TRUE", "w": ["❌ FALSE"], "h": "Used for ads/data."}, {"q": "Ransomware targets:", "a": "Your Files", "w": ["Keyboard", "Mouse"], "h": "Encrypts for money."}, {"q": "Encryption hides data.", "a": "✅ TRUE", "w": ["❌ FALSE"], "h": "Needs a key to read."}],
        "Hard": [{"q": "What is a Zero-Day?", "a": "Unknown Vulnerability", "w": ["Old Bug", "Virus Type", "Software Update"], "h": "No time to patch."}, {"q": "SQL Injection targets:", "a": "Databases", "w": ["CSS Styling", "Network Speed", "HTML Images"], "h": "Manipulates queries."}, {"q": "What is 'Salting'?", "a": "Adding Random Data", "w": ["Cleaning Cache", "Naming Files", "Deleting Logs"], "h": "Protects hashed passwords."}, {"q": "MITM attack stands for:", "a": "Man-in-the-Middle", "w": ["Mouse-in-the-Module", "Main-Internal-Task", "Master-Input-Tool"], "h": "Intercepts traffic."}, {"q": "Social Engineering targets:", "a": "Human Psychology", "w": ["Server RAM", "Cloud Storage", "BIOS"], "h": "Manipulates people."}, {"q": "A Honeypot is a:", "a": "Decoy System", "w": ["Data Backup", "Fast Server", "API Key"], "h": "Traps hackers."}, {"q": "Least Privilege means:", "a": "Minimum Access", "w": ["Maximum Speed", "Full Admin", "No Access"], "h": "Security best practice."}, {"q": "Brute Force is:", "a": "Guessing all keys", "w": ["Physical attack", "Email scam", "Social trick"], "h": "Trying every combo."}, {"q": "VPN hides your:", "a": "IP Address", "w": ["RAM size", "Battery life", "File names"], "h": "Masks identity."}, {"q": "E2EE means:", "a": "Only Sender/Receiver", "w": ["Google can read", "Server reads", "Unsecured"], "h": "End-to-End Encryption."}]
    },
    "Prompt Engineering": {
        "Easy": [{"q": "Is 'Write something' a good prompt?", "a": "❌ NO", "w": ["✅ YES"], "h": "Be specific."}, {"q": "Does AI like context?", "a": "✅ YES", "w": ["❌ NO"], "h": "More info = better."}, {"q": "Can AI write emails?", "a": "✅ YES", "w": ["❌ NO"], "h": "Core strength."}, {"q": "AI is always 100% correct.", "a": "❌ FALSE", "w": ["✅ TRUE"], "h": "Hallucinations happen."}, {"q": "Prompts can be long.", "a": "✅ TRUE", "w": ["❌ FALSE"], "h": "Context is key."}, {"q": "AI remembers forever.", "a": "❌ FALSE", "w": ["✅ TRUE"], "h": "Context window limits."}, {"q": "Creative prompts work.", "a": "✅ TRUE", "w": ["❌ FALSE"], "h": "Tuning style."}, {"q": "AI translates text.", "a": "✅ YES", "w": ["❌ NO"], "h": "Language models."}, {"q": "Should you check AI work?", "a": "✅ ALWAYS", "w": ["❌ NEVER"], "h": "Human in the loop."}, {"q": "AI reads your mind.", "a": "❌ FALSE", "w": ["✅ TRUE"], "h": "Reads text only."}],
        "Medium": [{"q": "What is Role Prompting?", "a": "Setting a Persona", "w": ["Asking Names", "System Reboot"], "h": "Act as a [Role]."}, {"q": "What is Few-Shot?", "a": "Giving Examples", "w": ["Short Prompt", "Fast Answer"], "h": "Learning from patterns."}, {"q": "System Prompt is:", "a": "Global Rules", "w": ["BIOS Message", "User Name"], "h": "Sets AI behavior."}, {"q": "Negative prompts tell AI:", "a": "What to EXCLUDE", "w": ["What to INCLUDE", "To be mean"], "h": "Constraints."}, {"q": "JSON output is:", "a": "Structured", "w": ["Unstructured", "A photo"], "h": "Machine readable data."}, {"q": "Temperature affects:", "a": "Creativity", "w": ["CPU Heat", "Battery"], "h": "Randomness control."}, {"q": "Zero-Shot means:", "a": "No Examples", "w": ["No Prompt", "No Answer"], "h": "Direct instruction."}, {"q": "CoT stands for:", "a": "Chain of Thought", "w": ["Code of Task", "Call of Tech"], "h": "Step-by-step logic."}, {"q": "Is AI context limited?", "a": "✅ YES", "w": ["❌ NO"], "h": "Limit on tokens."}, {"q": "Persona prompts change:", "a": "Tone/Style", "w": ["AI Speed", "Internet"], "h": "Audience tuning."}],
        "Hard": [{"q": "Self-Consistency uses:", "a": "Multiple Paths", "w": ["Single Answer", "No Answer", "A Loop"], "h": "Logic voting."}, {"q": "Prompt Injection is:", "a": "A Security Risk", "w": ["Fast Typing", "A Update", "Model Training"], "h": "Bypassing safety."}, {"q": "RAG uses:", "a": "External Data", "w": ["Just AI Brain", "A Webhook", "A Cookie"], "h": "Retrieval Augmented."}, {"q": "Tokenization affects:", "a": "Cost/Length", "w": ["Colors", "Fonts", "Speed only"], "h": "Context usage."}, {"q": "Meta-prompting is:", "a": "AI writing prompts", "w": ["AI buying food", "AI sleeping", "AI training"], "h": "Recursive logic."}, {"q": "Temperature 0 is:", "a": "Deterministic", "w": ["Random", "Creative", "Fast"], "h": "Fixed output."}, {"q": "CoV is for:", "a": "Fact Checking", "w": ["Emailing", "Coding", "Music"], "h": "Chain of Verification."}, {"q": "ToT is for:", "a": "Complex Logic", "w": ["Drawing", "Singing", "Movies"], "h": "Tree of Thoughts."}, {"q": "AI understands emotion?", "a": "Simulation only", "w": ["Always", "Never", "Real Love"], "h": "Pattern matching."}, {"q": "Prompt templates are for:", "a": "Automation", "w": ["Games", "Deleting", "Photos"], "h": "Standardized inputs."}]
    },
    "IT & Coding": {
        "Easy": [{"q": "Is Python a language?", "a": "✅ YES", "w": ["❌ NO"], "h": "Popular coding lang."}, {"q": "HTML is for:", "a": "Websites", "w": ["Math", "Photos"], "h": "Markup language."}, {"q": "A Bug is an:", "a": "Error", "w": ["Animal", "Feature"], "h": "Logic mistake."}, {"q": "Print() outputs text.", "a": "✅ YES", "w": ["❌ NO"], "h": "Basic function."}, {"q": "Can AI code?", "a": "✅ YES", "w": ["❌ NO"], "h": "Auto-gen code."}, {"q": "GitHub is for:", "a": "Version Control", "w": ["Games", "Chatting"], "h": "Storing code repos."}, {"q": "CSS is for:", "a": "Styling", "w": ["Logic", "Database"], "h": "Look and feel."}, {"q": "SQL is for:", "a": "Databases", "w": ["Emails", "Music"], "h": "Querying data."}, {"q": "RAM is memory.", "a": "✅ TRUE", "w": ["❌ FALSE"], "h": "Short term storage."}, {"q": "Cloud is remote servers.", "a": "✅ TRUE", "w": ["❌ FALSE"], "h": "Other people's PC."}],
        "Medium": [{"q": "What is an API?", "a": "Interface", "w": ["Database", "Hardware"], "h": "Connection point."}, {"q": "JSON uses:", "a": "Key-Value Pairs", "w": ["Binary", "Only Text"], "h": "Data format."}, {"q": "Llama 3 is a:", "a": "Model", "w": ["Animal", "Phone"], "h": "Meta's LLM."}, {"q": "IDE stands for:", "a": "Integrated Dev Env", "w": ["Internal Data", "Instant Env"], "h": "VS Code etc."}, {"q": "Python index starts at:", "a": "0", "w": ["1", "-1"], "h": "Zero-based."}, {"q": "Groq uses:", "a": "LPUs", "w": ["GPUs", "CPUs"], "h": "Hardware acceleration."}, {"q": "Streamlit is for:", "a": "Data Apps", "w": ["Games", "Mobile"], "h": "Python web tool."}, {"q": "Pandas library is for:", "a": "DataFrames", "w": ["Drawing", "Music"], "h": "Analysis tool."}, {"q": "Docker uses:", "a": "Containers", "w": ["Virtual Machines", "Files"], "h": "App isolation."}, {"q": "Git Commit means:", "a": "Saving changes", "w": ["Deleting", "Moving"], "h": "Snapshot."}],
        "Hard": [{"q": "O(log n) is for:", "a": "Binary Search", "w": ["Linear Search", "Bubble Sort", "Quick Sort"], "h": "Splitting data."}, {"q": "Transformers use:", "a": "Attention", "w": ["Loops", "Recursion", "Threads"], "h": "Mechanism for context."}, {"q": "Quantization helps with:", "a": "Size/Speed", "w": ["Colors", "Audio", "Fonts"], "h": "Model compression."}, {"q": "Kernel is part of:", "a": "Operating System", "w": ["Web Browser", "Keyboard", "Mouse"], "h": "Hardware core."}, {"q": "REST uses:", "a": "HTTP Methods", "w": ["Binary code", "Physical cables", "Logic"], "h": "Web communication."}, {"q": "Latency means:", "a": "Delay", "w": ["Speed", "Throughput", "Capacity"], "h": "Time to respond."}, {"q": "Multi-threading is for:", "a": "Concurrency", "w": ["Single task", "Deleting", "Printing"], "h": "Parallel execution."}, {"q": "Web Hook is a:", "a": "Reverse API", "w": ["Fish Hook", "Data Link", "UI Tool"], "h": "Push notification."}, {"q": "Kubernetes is for:", "a": "Orchestration", "w": ["Writing code", "Gaming", "Music"], "h": "Managing containers."}, {"q": "Backpropagation is for:", "a": "Training Neural Nets", "w": ["Backing up files", "Deleting history", "Sorting"], "h": "Adjusting weights."}]
    }
}

# --- 4. SESSION STATE ---
for key in ['xp', 'q_idx', 'shuffled_list', 'messages', 'player_name', 'game_active', 'current_level', 'current_path']:
    if key not in st.session_state: 
        st.session_state[key] = 0 if key in ['xp', 'q_idx'] else "" if key in ['player_name', 'current_level', 'current_path'] else [] if key in ['shuffled_list', 'messages'] else False

if 'unlocked_levels' not in st.session_state: st.session_state.unlocked_levels = ["Easy"]
if 'level_scores' not in st.session_state: st.session_state.level_scores = {"Easy": 0, "Medium": 0, "Hard": 0}
if 'page' not in st.session_state: st.session_state.page = "home"

def start_new_round(data_list, difficulty, path):
    st.session_state.shuffled_list = random.sample(data_list, len(data_list))
    st.session_state.q_idx = 0
    st.session_state.game_active = True
    st.session_state.current_level = difficulty
    st.session_state.current_path = path
    st.session_state.level_scores[difficulty] = 0

# --- 5. CERTIFICATE GENERATOR ---
def show_certificate(name, category):
    colors = {"Cyber-Safety": "#00FFA3", "Prompt Engineering": "#7D4CDB", "IT & Coding": "#FFD700"}
    cert_color = colors.get(category, "#00FFA3")
    cert_id = random.randint(100000, 999999)
    award_date = time.strftime("%d %B, %Y")

    cert_html = f"""
    <div id="printableCertificate" style="border: 8px solid {cert_color}; padding: 40px; text-align: center; background-color: #ffffff; color: #111; border-radius: 10px; font-family: 'Inter', sans-serif; margin: 20px auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        <h1 style="color: {cert_color}; font-size: 3rem; margin: 0;">OFFICIAL DIPLOMA</h1>
        <h3 style="letter-spacing: 5px; color: #555;">AI-Q MASTERY LAB</h3>
        <hr style="border: 1px solid {cert_color}; width: 80%; margin: 20px auto;">
        <p style="font-size: 1.2rem;">This confirms that the following Agent has completed all Hard-Level protocols:</p>
        <h2 style="font-size: 3rem; margin: 10px 0; text-transform: uppercase;">{name}</h2>
        <p style="font-size: 1.2rem;">Category: <b>{category}</b></p>
        <div style="margin-top: 50px; display: flex; justify-content: space-around; font-size: 0.8rem; color: #777;">
            <div>DATE: {award_date}</div>
            <div>VERIFICATION: {cert_id}</div>
            <div>INSTITUTION: INDUS UNIVERSITY</div>
        </div>
    </div>
    """
    st.markdown(cert_html, unsafe_allow_html=True)
    st.balloons()
    
    if st.button("🖨️ PRINT DIPLOMA"):
        st.markdown(f"""<script>var printContents = document.getElementById('printableCertificate').innerHTML; var originalContents = document.body.innerHTML; document.body.innerHTML = printContents; window.print(); document.body.innerHTML = originalContents; window.location.reload();</script>""", unsafe_allow_html=True)

# --- 6. ADVANCED CYBER-UI (CSS & JS) ---
st.set_page_config(page_title="AI-Q Mastery Lab", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@400;700&display=swap');

    /* Global Transitions and Aesthetics */
    * { transition: all 0.2s ease-in-out; }
    
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0f172a 0%, #020617 100%);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar - Glassmorphism */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Professional Headings */
    h1, h2, h3 {
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: -1px;
        background: linear-gradient(to right, #00ffa3, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* High-Performance Buttons */
    .stButton>button {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
        padding: 1rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        background: rgba(59, 130, 246, 0.1) !important;
        border-color: #00ffa3 !important;
        box-shadow: 0 0 20px rgba(0, 255, 163, 0.2);
        transform: translateY(-2px);
    }

    /* Level Selection Grid Styling */
    div[data-testid="column"]:nth-of-type(1) .stButton>button { border-left: 5px solid #10b981 !important; }
    div[data-testid="column"]:nth-of-type(2) .stButton>button { border-left: 5px solid #f59e0b !important; }
    div[data-testid="column"]:nth-of-type(3) .stButton>button { border-left: 5px solid #ef4444 !important; }

    /* Interactive Info Boxes */
    .stInfo {
        background: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 16px !important;
        padding: 25px !important;
    }

    /* Hide Defaults */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    </style>
    
    <canvas id="matrix" style="position:fixed; top:0; left:0; z-index:-1; opacity:0.05;"></canvas>
    <script>
    const canvas = document.getElementById('matrix');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const chars = '01';
    const drops = Array(Math.floor(canvas.width/20)).fill(1);
    function draw() {
        ctx.fillStyle = 'rgba(2, 6, 23, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#00ffa3';
        ctx.font = '15px monospace';
        drops.forEach((y, i) => {
            const text = chars[Math.floor(Math.random() * chars.length)];
            ctx.fillText(text, i * 20, y * 20);
            if (y * 20 > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        });
    }
    setInterval(draw, 50);
    </script>
    """, unsafe_allow_html=True)

# --- 7. ACCESS PORTAL ---
if not st.session_state.player_name:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.title("🛡️ Secure Access Portal")
        st.info("Identity verification required to initialize AI-Q modules.")
        name = st.text_input("AGENT DESIGNATION:", placeholder="Enter your name...")
        if st.button("INITIALIZE SESSION", key="init_gate"):
            if name:
                st.session_state.player_name = name
                st.rerun()
            else: st.error("Verification Error: Name field cannot be null.")
    st.stop()

# --- 8. PLAY LEVEL UI ---
def play_level_ui():
    lvl = st.session_state.current_level
    if st.button("🛑 TERMINATE MISSION", key="abort"): st.session_state.game_active = False; st.rerun()

    if st.session_state.q_idx < len(st.session_state.shuffled_list):
        curr = st.session_state.shuffled_list[st.session_state.q_idx]
        options = [curr['a']] + curr['w'] 
        random.seed(st.session_state.q_idx) 
        random.shuffle(options)

        st.markdown(f"### PROTOCOL: {st.session_state.current_path} | LEVEL: {lvl}")
        st.info(f"**QUERY {st.session_state.q_idx + 1}/10:** \n\n {curr['q']}")
        
        cols = st.columns(len(options))
        for i, option in enumerate(options):
            with cols[i]:
                if st.button(option, key=f"opt_{st.session_state.q_idx}_{i}", use_container_width=True):
                    if option == curr['a']:
                        st.session_state.xp += 50
                        st.session_state.level_scores[lvl] += 1
                        st.session_state.q_idx += 1
                        st.success("Correct Response."); time.sleep(0.4); st.rerun()
                    else:
                        st.session_state.xp -= 20
                        st.session_state.q_idx += 1
                        st.error(f"Logic Error. Hint: {curr['h']}"); time.sleep(0.8); st.rerun()
    else:
        score = st.session_state.level_scores[lvl]
        st.subheader(f"Session Analytics: {score}/10 Correct")
        if score >= 7:
            if lvl == "Hard": show_certificate(st.session_state.player_name, st.session_state.current_path)
            else:
                st.success(f"🔓 {lvl.upper()} PROTOCOL SUCCESSFUL")
                if lvl == "Easy" and "Medium" not in st.session_state.unlocked_levels: st.session_state.unlocked_levels.append("Medium")
                elif lvl == "Medium" and "Hard" not in st.session_state.unlocked_levels: st.session_state.unlocked_levels.append("Hard")
        else: st.warning("Validation Failed. Target Score: 7/10.")
        if st.button("BACK TO HUB"): st.session_state.game_active = False; st.rerun()

# --- 9. SIDEBAR ---
with st.sidebar:
    st.markdown(f"### 🕵️ AGENT ID: \n{st.session_state.player_name.upper()}")
    st.metric("CURRENT XP", f"{st.session_state.xp} PTS")
    save_score(st.session_state.player_name, st.session_state.xp, "Elite")
    st.write("---")
    if st.button("🏠 COMMAND CENTER"): st.session_state.page = "home"; st.session_state.game_active = False; st.rerun()
    if st.button("🔄 REBOOT PROGRESS"): st.session_state.unlocked_levels = ["Easy"]; st.session_state.xp = 0; st.rerun()
    st.write("---")
    st.subheader("🏆 GLOBAL LEADERBOARD")
    st.table(get_leaderboard().head(5))

# --- 10. MAIN NAVIGATION ---
if st.session_state.page == "home":
    st.title("👾 AI-Q MASTERY HUB")
    st.write("Choose your engagement module:")
    c1, c2 = st.columns(2)
    with c1:
        st.info("### 🎮 ACTIVE MISSIONS \n Timed logic and safety benchmarks.")
        if st.button("INITIALIZE MISSION HUB", key="nav_play"): st.session_state.page = "play"; st.rerun()
    with c2:
        st.info("### 🧪 NEURAL SANDBOX \n Unrestricted Large Language Model access.")
        if st.button("INITIALIZE SANDBOX", key="nav_sand"): st.session_state.page = "sandbox"; st.rerun()

elif st.session_state.page == "play":
    st.title("🛰️ MISSION CONTROL")
    if not st.session_state.game_active:
        cat = st.selectbox("CHOOSE KNOWLEDGE PATH:", list(questions_db.keys()))
        l1, l2, l3 = st.columns(3)
        with l1:
            if st.button("🟢 EASY MODE", key="lvl_e"): start_new_round(questions_db[cat]["Easy"], "Easy", cat); st.rerun()
        with l2:
            lock_m = "Medium" not in st.session_state.unlocked_levels
            label_m = "🟡 MEDIUM MODE" if not lock_m else "🔒 LOCKED"
            if st.button(label_m, disabled=lock_m, key="lvl_m"): start_new_round(questions_db[cat]["Medium"], "Medium", cat); st.rerun()
        with l3:
            lock_h = "Hard" not in st.session_state.unlocked_levels
            label_h = "🔴 HARD MODE" if not lock_h else "🔒 LOCKED"
            if st.button(label_h, disabled=lock_h, key="lvl_h"): start_new_round(questions_db[cat]["Hard"], "Hard", cat); st.rerun()
    else: play_level_ui()

elif st.session_state.page == "sandbox":
    st.title("🧪 NEURAL SANDBOX")
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    if p := st.chat_input("Inject prompt..."):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        res = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": p}])
        st.session_state.messages.append({"role": "assistant", "content": res.choices[0].message.content}); st.rerun()