from pydoc import text
from tkinter import *
from tkinter import messagebox
from turtle import bgcolor
import pandas as pd
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pd.read_csv('./data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pd.read_csv('./data/french_words.csv')
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')

def known():
        to_learn.remove(current_card)
        data = pd.DataFrame(to_learn)
        data.to_csv('./data/words_to_learn.csv', index=False)
        next_word()

def next_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(to_learn)
    canvas.itemconfig(card_title, text='French', fill='black')
    canvas.itemconfig(card_word, text=current_card['French'], fill='black')
    canvas.itemconfig(card_image, image=card_front)
    flip_timer = window.after(3000, flip_card)

def flip_card():
    canvas.itemconfig(card_title, text='English', fill='white')
    canvas.itemconfig(card_word, text=current_card['English'], fill='white')
    canvas.itemconfig(card_image, image=card_back)
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Flash Cards')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file='./images/card_front.png')
card_back = PhotoImage(file='./images/card_back.png')
card_image = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="", font=('Ariel', 40, 'italic'))
card_word = canvas.create_text(400, 260, text='', font=('Ariel', 60, 'bold'))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file='./images/wrong.png')
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_word)
unknown_button.grid(row=1, column=0)

tick_image = PhotoImage(file='./images/right.png')
known_button = Button(image=tick_image, highlightthickness=0, command=known)
known_button.grid(row=1, column=1)

next_word()
window.mainloop()