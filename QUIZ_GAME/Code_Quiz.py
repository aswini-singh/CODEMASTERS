import random
import tkinter as tk
from tkinter import messagebox

class QuizGame:
    def __init__(self, file_path):
        self.questions = []
        self.score = 0
        self.current_question_index = 0
        self.load_quiz_questions(file_path)

    def load_quiz_questions(self, file_path):
        with open(file_path, "r") as file:
            lines = [line.strip() for line in file.readlines()]
            i = 0
            while i < len(lines):
                question_line = lines[i]
                if question_line.startswith("[FILL]"):
                    question = {"question": question_line[6:], "correct_answer": ""}
                    i += 1
                    while i < len(lines) and not lines[i].startswith("correct_answer: "):
                        i += 1
                    if i < len(lines):
                        question["correct_answer"] = lines[i][15:].strip().lower() 
                        i += 1
                    self.questions.append(question)
                elif question_line.endswith('?'):
                    question = {"question": question_line, "options": [], "correct_answer": ""}
                    i += 1
                    while i < len(lines) and not lines[i].startswith("option: "):
                        question["options"].append(lines[i])
                        i += 1
                    if i < len(lines):
                        question["correct_answer"] = lines[i][8:].strip().lower()  
                        i += 1
                    self.questions.append(question)
                else:
                    i += 1

    def shuffle_questions(self):
        random.shuffle(self.questions)

    def ask_question(self):
        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]
            if "options" in question_data:
                self.ask_multiple_choice_question(question_data)
            else:
                self.ask_fill_in_the_blank_question(question_data)
        else:
            self.display_results()

    def check_answer(self):
        user_answer = self.user_answer_entry.get().strip().lower() 
        correct_answer = self.current_correct_answer  

        if user_answer == correct_answer:
            messagebox.showinfo("Correct!", "Your answer is correct!")
            self.score += 1
        else:
            messagebox.showerror("Wrong!", f"Wrong! The correct answer is '{self.current_correct_answer}'")

        self.current_question_index += 1
        self.clear_widgets()  
        self.ask_question()

    def display_results(self):
        result_message = f"Your score is {self.score}/{len(self.questions)}"
        if self.score == len(self.questions):
            result_message += "\nCongratulations! You answered all questions."
        elif self.score >= len(self.questions) / 2:
            result_message += "\nGood job! You did well."
        else:
            result_message += "\nKeep practicing. You can do better next time."
        CustomMessageBox(self.root, "Quiz completed!",result_message)

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def ask_multiple_choice_question(self, question_data):
        question_text = question_data["question"]
        options = question_data["options"]

        self.clear_widgets() 

        self.question_label = tk.Label(self.root, text=question_text, wraplength=400, padx=20, pady=10, font= ("Helvetica", 18,"bold") ,fg="red")
        self.question_label.pack()

        self.user_answer_entry = None 
        self.current_correct_answer = question_data["correct_answer"]

        for i, option in enumerate(options, start=1):
            tk.Radiobutton(self.root, text=f"{i}. {option}", variable=self.selected_option, value=option).pack()
        custom_font_submit_button = ("Helvetica", 16,"bold")

        self.submit_button = tk.Button(self.root, text="Submit", fg="darkblue",font=("Arial",16,"bold"),command=self.check_answer)
        self.submit_button.pack()

        # Create the user answer entry here
        self.user_answer_entry = tk.Entry(self.root, width=20,fg="purple",font=("Helvetica", 20,"bold"))
        self.user_answer_entry.pack()

    def ask_fill_in_the_blank_question(self, question_data):
        question_text = question_data["question"]

        self.clear_widgets() 

        self.question_label = tk.Label(self.root, text=question_text, wraplength=400, padx=20, pady=10, font=("Helvetica", 18,"bold"),fg="red")
        self.question_label.pack()

        self.user_answer_entry = None  
        self.current_correct_answer = question_data["correct_answer"]

        self.user_answer_entry = tk.Entry(self.root, width=20,fg="purple",font=("Helvetica", 20,"bold"))
        self.user_answer_entry.pack()

        self.submit_button = tk.Button(self.root, text="Submit",fg="darkblue",font=("Arial",16,"bold"), command=self.check_answer)
        self.submit_button.pack()

    def next_question(self):
        self.current_question_index += 1

        if self.current_question_index < len(self.questions):
            self.ask_question()
        else:
            self.display_results()

  
    def start_quiz(self):
        self.shuffle_questions()

        self.root = tk.Tk()
        self.root.title("CodeMasters Quiz Game")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 600  
        window_height = 450  
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.user_answer_entry = None 

        self.selected_option = tk.StringVar()

        self.ask_question()

        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry)):
                widget.config(font=("Helvetica", 20,"bold"))

        self.root.mainloop()

class CustomMessageBox(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x200")
        title_label = tk.Label(self, text=title, padx=50, pady=10, fg="darkred", font=("Helvetica", 20, "bold"))
        title_label.pack()
        tk.Label(self, text=message, padx=50, pady=60,fg="darkgreen",font=("Helvetica", 16,"bold")).pack()
        ok_button = tk.Button(self, text="OK", command=self.destroy,fg="darkblue",font=("Helvetica", 16, "bold"))
        ok_button.pack()

if __name__ == "__main__":
    game = QuizGame("Quiz_Game/question.txt")
    game.start_quiz()
