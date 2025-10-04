from model_loader import load_model
from chat_memory import ChatMemory
import re


class Chatbot:
    def __init__(self):
        self.chatbot = load_model()
        self.memory = ChatMemory(window_size=3)

    def fallback(self, user_input: str, bot_reply: str = "") -> str:
        """
        Fallback/validation function:
        - Expands known facts (capitals, jokes, identity).
        - Validates Flan-T5 answers against correct data.
        """
        text = user_input.lower()
        capitals = {
            "france": "Paris",
            "italy": "Rome",
            "india": "New Delhi",
            "germany": "Berlin",
            "denmark": "Copenhagen",
            "netherlands": "Amsterdam",
            "belgium": "Brussels",
            "switzerland": "Bern",
            "china": "Beijing",
            "japan": "Tokyo",
            "pakistan": "Islamabad",
            "bangladesh": "Dhaka",
        }

        # ✅ Validate country-capital answers
        for country, capital in capitals.items():
            if country in text:
                if not bot_reply or capital.lower() not in bot_reply.lower():
                    return f"The capital of {country.capitalize()} is {capital}."
                return bot_reply

        # ✅ Simple fallbacks
        if "joke" in text:
            return "Why don’t skeletons fight each other? They don’t have the guts!"
        if "who are you" in text:
            return "I’m a Flan-T5 powered chatbot, here to help you.."
        if not bot_reply:
            return "Sorry, I don’t know the answer to that."

        return bot_reply

    def expand_query(self, user_input: str) -> str:
        """
        Expand follow-up queries like 'and India?' into full questions.
        Uses last user question as context.
        """
        text = user_input.strip().lower()

        if text.startswith("and"):
            prev_user_inputs = [msg for msg in self.memory.history if msg.startswith("User:")]
            if prev_user_inputs:
                last_question = prev_user_inputs[-1].replace("User:", "").strip().lower()
                if "capital" in last_question:
                    country = text.replace("and", "").strip(" ?")
                    return f"What is the capital of {country.capitalize()}?"
        return user_input

    def get_response(self, user_input: str) -> str:
     
        expanded_input = self.expand_query(user_input)

        self.memory.add("User", expanded_input)

       
        conversation = self.memory.get_context()
        instruction = (
            "You are a factual chatbot. Use the conversation history to answer "
            "the latest user question clearly and correctly.\n\n"
            f"Conversation so far:\n{conversation}\n\nBot:"
        )

        response = self.chatbot(
            instruction,
            max_length=128,
            do_sample=True,
            top_p=0.9,
            temperature=0.7
        )[0]["generated_text"].strip()

        bot_reply = response.split("Bot:")[-1].strip()

        # ✅ Apply fallback/validation
        bot_reply = self.fallback(expanded_input, bot_reply)

        # Save reply
        self.memory.add("Bot", bot_reply)
        return bot_reply


def run_chat():
    bot = Chatbot()
    print("Flan-T5 Chatbot started. Type /exit to quit.\n")

    while True:
        user_input = input("User: ")
        if user_input.strip().lower() == "/exit":
            print("Exiting chatbot. Goodbye!")
            break

        bot_reply = bot.get_response(user_input)
        print("Bot:", bot_reply)


if __name__ == "__main__":
    run_chat()
