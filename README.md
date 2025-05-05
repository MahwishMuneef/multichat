# 🤖 Multi-Model Chat Assistant

A powerful, extensible chatbot built with **Gemini (Google)**, **OpenAI**, and **DeepSeek** APIs — all inside an interactive **Streamlit** UI. Users can chat with different LLMs, save conversations to Google Docs, and more.

---

## ✨ Features

- 🔄 Chat with Gemini (Google Generative AI)
- 🧠 Upcoming: Chat with OpenAI (GPT-4/3.5) and DeepSeek
- 💬 Streamlit-based UI for a smooth chat experience
- 💾 Save full chat history to Google Docs
- 🧹 Clear chat memory with one click
- 🔐 API key management via `.env`

---


## 🚀 Getting Started

### 1. Clone the Repository

bash
git clone https://github.com/your-username/multimodel-chatbot.git
cd multimodel-chatbot




## Create a Virtual Environment

python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

##Install Dependencies

pip install -r requirements.txt


##Add Environment Variables

GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here
DEEPSEEK_API_KEY=your_deepseek_key_here


##Run the App
streamlit run app.py