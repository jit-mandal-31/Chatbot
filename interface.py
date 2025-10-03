from model_loader import load_model
from chat_memory import ChatMemory


class Chatbot:
    def __init__(self):
        self.chatbot = load_model()
        self.memory = ChatMemory(window_size=3)

    def fallback(self, user_input: str, bot_reply: str = "") -> str:
        """
        Fallback/validation:
        - Provides factual answers for known questions (capitals, jokes, identity).
        - Validates Flan-T5 responses against correct data.
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

        # Validate country-capital responses
        for country, capital in capitals.items():
            if country in text:
                if not bot_reply or capital.lower() not in bot_reply.lower():
                    return f"The capital of {country.capitalize()} is {capital}."
                return bot_reply

        # Simple fallbacks
        if "joke" in text:
            return "Why don’t skeletons fight each other? They don’t have the guts!"
        if "who are you" in text:
            return "I’m a Flan-T5 powered chatbot, here to help you.."
        if not bot_reply:
            return "Sorry, I don’t know the answer."

        return bot_reply

    def expand_query(self, user_input: str) -> str:
        """
        Expands follow-up queries like 'and India?' into full questions using
        the last user input from memory as context.
        """
        text = user_input.strip().lower()
        if text.startswith("and"):
            # Look for the last user question
            prev_user_inputs = [
                msg for msg in self.memory.history if msg.startswith("User:")
            ]
            if prev_user_inputs:
                last_question = prev_user_inputs[-1].replace("User:", "").strip().lower()
                if "capital" in last_question:
                    country = text.replace("and", "").strip(" ?")
                    return f"What is the capital of {country.capitalize()}?"
        return user_input

    def get_response(self, user_input: str) -> str:
        # Expand follow-up queries
        expanded_input = self.expand_query(user_input)
        self.memory.add("User", expanded_input)

        # Build Flan-T5 instruction prompt
        conversation = self.memory.get_context()
        instruction = (
            "You are a factual chatbot. Use the conversation history to answer "
            "the latest user question clearly and correctly.\n\n"
            f"Conversation so far:\n{conversation}\n\nBot:"
        )

        # Generate response using only max_new_tokens (avoid warning)
        response = self.chatbot(
            instruction,
            max_new_tokens=128,  # ✅ only this
            do_sample=True,
            top_p=0.9,
            temperature=0.7
        )[0]["generated_text"].strip()

        # Extract bot reply
        bot_reply = response.split("Bot:")[-1].strip()

        # Apply fallback/validation
        bot_reply = self.fallback(expanded_input, bot_reply)
        self.memory.add("Bot", bot_reply)

        return bot_reply


def run_chat():
    bot = Chatbot()
    print("Flan-T5 Chatbot started. Type /exit to quit.\n")

    while True:
        user_input = input("User: ").strip()
        if user_input.lower() == "/exit":
            print("Exiting chatbot. Goodbye!")
            break

        bot_reply = bot.get_response(user_input)
        print("Bot:", bot_reply)


if __name__ == "__main__":
    run_chat()
