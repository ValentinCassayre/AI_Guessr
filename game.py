import ollama
import re

model_name = 'deepseek-r1:1.5b'

class AIGuessr:
    def __init__(self, model=model_name, num_answers=7):
        self.model = model
        self.num_answers = num_answers
    
    def chat(self, prompt, model=model_name):
        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        output = response["message"]["content"]

        return output 

    def generate_answers(self, question):
        prompt = f"""
        You are playing a game called 'AIGuessr' Your task is to generate the {self.num_answers} most common or popular answers to the following question, ranked in order from most common (1) to least common ({self.num_answers}). The answers should be based on general knowledge, cultural trends, and common associations.

        Question: {question}

        Please format your response as a ranked list:
        1. [Most common answer]
        2. [Second most common answer]
        ...
        {self.num_answers}. [{self.num_answers}th most common answer]
        """

        output = self.chat(prompt)

        return self.extract_answers(output)

    def extract_answers(self, text):
        matches = re.findall(r"\d+\.\s(.+)", text)

        return matches[:self.num_answers] if len(matches) >= self.num_answers else matches

    def play(self):
        print("Welcome to AIGuessr!")
        print("I'll give you questions, and you'll try to guess the top answers that I will predict.")
        print("Let's begin!\n")
        question = input("\nEnter a question for the game: ")
        correct_answers = self.generate_answers(question)

        if not correct_answers:
            print("Couldn't generate answers. Try a different question.")
            return

        guessed_answers = set()
        score = 0

        print(f"\nTry to guess the {self.num_answers} answers! Type 'quit' to give up.")

        while len(guessed_answers) < self.num_answers:
            guess = input("\nYour guess: ").strip().lower()

            if guess == "quit":
                break

            if guess in guessed_answers:
                print("You already guessed that!")
                continue

            if any(guess in ans.lower() for ans in correct_answers): # TODO better checking system : e.g. use the llm
                guessed_answers.add(guess)
                score += 1
                print(f"Correct! {self.num_answers - len(guessed_answers)} more to go.")
            else:
                print("Wrong guess.")

        print("\nGame Over! Here were the top answers:")
        for i, ans in enumerate(correct_answers, start=1):
            print(f"{i}. {ans}")

        print(f"\nYour score: {score}/self.num_answers")


game = AIGuessr(model=model_name, num_answers=5)
game.play()

