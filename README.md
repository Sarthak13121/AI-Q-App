# AI-Q Mastery Lab

AI-Q Mastery Lab is an interactive, cyber-themed diagnostic dashboard and security protocol simulation application. Built with Streamlit, it offers users structured training modules across Cyber-Safety, Prompt Engineering, and IT & Coding, backed by automated evaluation and real-time LLM interaction.

---

## 🚀 Key Modules & Protocol Features

- **Diagnostic Training Protocols**:
  - **Cyber-Safety**: Threat vector analysis including Phishing, Deepfakes, Zero-Days, and network security filters.
  - **Prompt Engineering**: Role-prompting models, Few-Shot learning setups, system prompt overrides, and token constraints.
  - **IT & Coding**: Standard data structures, programming logic, model quantization, and server architectures.
- **Interactive Multi-Level Progression**:
  - Unlocks levels dynamically as the player progresses: **Easy Mode** ➡️ **Medium Mode** ➡️ **Hard Mode**.
  - Requires a minimum score of **7/10** correct answers to clear validation gates and authorize progression.
- **Automated Diploma Generation**:
  - Upon completing Hard-Level protocols, the application dynamically generates a stylized, print-ready digital diploma verifying credentials, complete with verification ID.
- **Neural Sandbox**:
  - An unrestricted Large Language Model terminal integrated directly with Groq (`llama-3.1-8b-instant`), facilitating testing of prompt injections, system instructions, and interactive queries.
- **Global Leaderboard & XP Ledger**:
  - Tracks player progress using a local CSV-based database ledger (`leaderboard.csv`) that displays top security agents.

---

## 🎨 Professional Cyber-UI Aesthetics

- **Glassmorphism Sidebar**: Semi-transparent, blur-filtered navigation hub.
- **Digital Rain Canvas**: Background matrix falling characters canvas effect built with HTML5 and native JS rendering behind Streamlit blocks.
- **Dynamic CSS Transitions**: Smooth, animated transitions, custom interactive level selection grids, and hover-triggered micro-animations.

---

## 📁 Repository Structure

```text
AI-Q-App/
├── .devcontainer/       # Dev Container configurations
├── dot.streamlit/       # Streamlit configurations
├── .env.example         # Template for Groq API Key
├── .gitignore           # Excludes environment files & user progress
├── leaderboard.csv      # CSV-based persistence layer for scores
├── main.py              # Central application logic and Streamlit app
└── requirements.txt      # Core python requirements
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.9 or higher.
- A free API Key from [Groq Console](https://console.groq.com/).

### 1. Clone the Repository
```bash
git clone https://github.com/Sarthak13121/AI-Q-App.git
cd AI-Q-App
```

### 2. Set Up a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Your API Key
You can configure your Groq API key in one of three ways:
1. **Sidebar Input**: When running the app, paste your key directly in the sidebar password box.
2. **Environment File**: Create a `.env` file in the root folder and add:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```
3. **Streamlit Secrets**: Add the key inside `.streamlit/secrets.toml`:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```

### 5. Launch the Command Center
```bash
streamlit run main.py
```
Open your browser and navigate to the local URL (usually `http://localhost:8501`).

---

## 🛡️ License

This project is licensed under the MIT License - see the LICENSE file for details.
