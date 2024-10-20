import historyeasy, historymedium, historyhard
import sportseasy, sportsmedium, sportshard
import sexedueasy, sexedumedium, sexeduhard
import pyttsx3
from tkinter import *
import random
import threading

engine = pyttsx3.init() 
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[1].id)    
difficulty = ['easy', 'medium', 'hard']
categories = ['sports', 'history', 'sexedu']
score = 0
asked = []
answered = False  # Tracks if the user has answered the current question
# Main window
rt = Tk()
rt.title("quiz-app")

# Global variables for widgets
l1 = None
t_score = None
status = None
easy_bt = None
mid_bt = None
hard_bt = None
extra_bt = None
another = None
highest = None
def load_ini():
    global l1, easy_bt, mid_bt, hard_bt, extra_bt, t_score, status, another

    l1 = Label(rt, text="Choose difficulty level: ")
    l1.grid(row=0, column=0)
    easy_bt = Button(rt, text="easy", fg="white", bg="green", width=7, height=2, command=lambda: load_ques("easy"))
    easy_bt.grid(row=1, column=0)

    mid_bt = Button(rt, text="medium", fg="white", bg="green", width=7, height=2, command=lambda: load_ques("medium"))
    mid_bt.grid(row=2, column=0)

    hard_bt = Button(rt, text="hard", fg="white", bg="green", width=7, height=2, command=lambda: load_ques("hard"))
    hard_bt.grid(row=3, column=0)

    extra_bt = Button(rt, text="", width=1, height=1)
    extra_bt.grid(row=4, column=0)

    t_score = Label(rt, text=f"score: 0")
    t_score.grid(row=1, column=7)

    status = Label(rt, text="")
    status.grid(row=5, column=0)

    quitting = Button(rt, text="quit", fg="white", bg="red", command=exitted)
    quitting.grid(row=7, column=0)

    another = Button(rt, text="Next >>", fg="white", bg="blue", state=DISABLED, command=lambda: load_ques("easy"))
    another.grid(row=7, column=7)
    with open("highscore.txt","r") as f:
        highscore = f.read()
    highest = Label(rt,text=f"highscore: {highscore}")
    highest.grid(row=2,column=7)

def check_correct(answer, correct):
    global score, status, t_score, another, answered

    # Disable all options after the user selects an answer
    disable_buttons()

    if answer == correct:
        score += 1
        status.configure(text="Correct answer", fg="green")
        t_score.configure(text=f"score: {score}")
        answered = True  # Mark as answered
        another.configure(state=NORMAL)  # Enable "Next" button to go to the next question
    else:
        status.configure(text="Incorrect answer, try again", fg="red")
        another.configure(state=DISABLED)
    with open("highscore.txt", "r") as f:
        highscore = int(f.read()) 
    if score > highscore:
        with open("highscore.txt", "w") as f:
            f.write(str(score))
        highest.configure(text=f"highscore: {score}")

def disable_buttons():
    """Disable all option buttons to prevent re-clicking."""
    easy_bt.configure(state=DISABLED)
    mid_bt.configure(state=DISABLED)
    hard_bt.configure(state=DISABLED)
    extra_bt.configure(state=DISABLED)

def enable_buttons():
    """Enable all option buttons for the new question."""
    easy_bt.configure(state=NORMAL)
    mid_bt.configure(state=NORMAL)
    hard_bt.configure(state=NORMAL)
    extra_bt.configure(state=NORMAL)

def exitted():
    global status, another
    status.configure(text=f"You have exited. Final score: {score}", fg="blue")
    another.destroy()

def shuffler():
    return random.choice(categories)

def speak_question(text):
    """Speak the question using TTS in a separate thread."""
    engine.say(text)
    engine.runAndWait()

def load_ques(mode):
    global asked, l1, easy_bt, mid_bt, hard_bt, extra_bt, another, answered
    answered = False 
    another.configure(state=DISABLED)  
    enable_buttons()
    category = shuffler()
    bulk = eval(f"{category}{mode}.quiz_data")
    r_bulk = random.randint(0, 19)
    ques_rep = f"{category}{mode}{r_bulk}"

    if ques_rep not in asked:
        asked.append(ques_rep)
        question_data = bulk[r_bulk]
        l1.configure(text=question_data['question'])
        
        # Run the TTS in a separate thread to avoid blocking the UI
        threading.Thread(target=speak_question, args=(question_data['question'],)).start()

        op_count = len(question_data['options'])

        if op_count == 2:
            easy_bt.configure(text=question_data['options'][0], width=25, height=10, command=lambda: check_correct(question_data['options'][0], question_data['answer']))
            mid_bt.configure(text=question_data['options'][1], width=25, height=10, command=lambda: check_correct(question_data['options'][1], question_data['answer']))
            hard_bt.configure(text="", width=1, height=1, fg="white", bg="white")
            extra_bt.configure(text="", width=1, height=1, fg="white", bg="white")
        else:
            easy_bt.configure(text=question_data['options'][0], width=25, height=10, command=lambda: check_correct(question_data['options'][0], question_data['answer']))
            mid_bt.configure(text=question_data['options'][1], width=25, height=10, command=lambda: check_correct(question_data['options'][1], question_data['answer']))
            hard_bt.configure(text=question_data['options'][2], fg="white", bg="green", width=25, height=10, command=lambda: check_correct(question_data['options'][2], question_data['answer']))
            extra_bt.configure(text=question_data['options'][3], fg="white", bg="green", width=25, height=10, command=lambda: check_correct(question_data['options'][3], question_data['answer']))
    else:
        load_ques(mode)

if __name__ == "__main__":
    load_ini()
    rt.mainloop()
