# Chatbot using Flan-T5 

This project is a **command-line chatbot** built as part of the ATG Technical Assignment.  
It uses **Hugging Face’s Flan-T5 model** for text generation, with a **sliding window memory** and a **fallback mechanism** to ensure more accurate answers for common factual questions.  

---

## 📌 Features
- Uses Flan-T5-base (google/flan-t5-base) as the primary text generation model.
- Maintains short-term memory (last 3–5 conversation turns) for context.
- Automatically expands follow-up queries (e.g., “And India?” → “What is the capital of India?”).
- Fallback validator ensures correct answers for common factual queries (e.g., capitals).
Provides a simple CLI interface with /exit command to quit.
- Modular structure with separate files:
  - model_loader.py → Loads the Hugging Face model.
  - chat_memory.py → Sliding-window memory management.
  - interface.py → CLI loop, integration, and fallback logic.
---

## 🛠️ Setup

1. Install dependencies:
   ```bash
   pip install transformers
   ```

2. Run the chatbot:
   ```bash
   python interface.py
   ```

---

## 💻 Usage Example
```

Flan-T5 Chatbot started. Type /exit to quit.

User: hii
Bot: Is there anything I can help you with?
User: who are you?
Bot: I’m a Flan-T5 powered chatbot, here to help you..
User: what is the capital of india?
Bot: The capital of India is New Delhi.
User: china?
Bot: The capital of China is Beijing.
User: japan?
Bot: The capital of Japan is Tokyo.
User: germany?
Bot: The capital of Germany is Berlin.
User: /exit
Exiting chatbot. Goodbye!
```

## Demo video


https://github.com/user-attachments/assets/355dddef-6b7c-496d-8f0c-9d7173b8bac5


---

## 📌 Notes
- This chatbot is not fully comprehensive — Flan-T5 is an instruction-based model and may sometimes generate incorrect or fabricated responses.
- The fallback system guarantees factual answers for specific queries, such as capitals, jokes, and identity questions.
- The main goal of this assignment is demonstrating integration, memory management, and a command-line interface.

---

✨ Your Flan-T5 CLI chatbot is now ready to use!
