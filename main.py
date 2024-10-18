from tkinter import *
import random

import pandas
import pandas as pd


BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
try:
    data = pd.read_csv("data/french_words.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient = "records")
else:
    to_learn = data.to_dict(orient="records")

# ---------------------------- NEXT WORD ------------------------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill = "black")
    canvas.itemconfig(card_text, text=current_card["French"], fill = "black")
    canvas.itemconfig(card_bg, image = card_front_image)
    flip_timer=window.after(2000, func=flip_card)

# ---------------------------- SHOW ANSWER ------------------------------- #

def flip_card():
    canvas.itemconfig(card_title, text = "English", fill = "white")
    canvas.itemconfig(card_text, text = current_card["English"], fill = "white")
    canvas.itemconfig(card_bg, image = card_back_image)

# ---------------------------- REMOVE KNOWN WORDS ------------------------------- #
def is_known():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index = False)
    next_card()

#---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx = 50, pady = 50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func = flip_card)

canvas = Canvas(width = 800, height= 526)
card_front_image = PhotoImage(file= "images/card_front.png")
card_back_image = PhotoImage(file= "images/card_back.png")

card_bg = canvas.create_image(400, 263, image= card_front_image)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness = 0)
card_title = canvas.create_text(400, 150, text = "call function next card",font= ("Ariel", 40, "italic"))
card_text = canvas.create_text(400, 263, text = "call function next card",font= ("Ariel", 60, "bold"))

canvas.grid(row = 0, column = 0, columnspan = 2)

right_img = PhotoImage(file= "images/right.png")
right_button = Button(image= right_img, highlightthickness=0, command = is_known)
right_button.grid(row= 1, column = 1)

wrong_img = PhotoImage(file= "images/wrong.png")
wrong_button = Button(image= wrong_img, highlightthickness=0, command = next_card)
wrong_button.grid(row= 1, column = 0)

# title_label = Label(text = "Title")
# title_label.pack(x= 400, y=150)
next_card()
window.mainloop()