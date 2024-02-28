from tkinter import *

SHIFT_KEYS = {"Shift_L", "Shift_R"}
limit = 5
current_time = 0
print_time = "0"
count = 0
wpm = "?"
is_capital = False
is_init = True
script = "A computer program can easily produce gibberish - especially if it has been provided with garbage beforehand. This program does something a little different. It takes a block of text as input and works out the proportion of characters within the text according to a chosen order. For example, an order of 2 means the program looks at pairs of letters, an order of 3 means triplets of letters and so on. The software can regurgitate random text that is controlled by the proportion of characters. The results can be quite surprising."


def handle(event):
    global timer
    global count
    global is_init
    global is_capital
    if is_init:
        timer = window.after(1000, update, current_time, limit)
        is_init = False
    if event.keysym in SHIFT_KEYS:
        is_capital = True
        return None
    key_pressed = event.keysym.upper() if is_capital else event.keysym
    print(key_pressed)
    if count == 0 and key_pressed == "BackSpace":
        return;
    if count > 0 and key_pressed == "BackSpace":
        count -= 1
        text.tag_remove("incorrect", "1." + f"{count}", )
        text.tag_remove("correct", "1." + f"{count}", )

    elif script[count] != key_pressed:
        text.tag_add("incorrect", "1." + f"{count}", )
        count += 1

    else:
        text.tag_add("correct", "1." + f"{count}", )
        count += 1
    is_capital = False


def update(current_time, limit):
    current_time += 1
    print_time = str(current_time)
    global timer
    if current_time <= limit:
        timer_text.configure(text="Time: " + print_time)
        timer = window.after(1000, update, current_time, limit)
    else:
        wpm = str((count / 5) / 0.5)
        wpm_text.configure(text="WPM: " + wpm)
        window.after_cancel(timer)
        entry.config(state=DISABLED)
        window.unbind(handle)


def restart():
    global timer
    global count
    count = 0
    entry.config(state="normal")
    entry.delete(0, 'end')
    window.bind("<Key>", handle)
    current_time = 0
    for tag in text.tag_names():
        text.tag_remove(tag, "1.0", "end")
    print_time = str(current_time)
    timer_text.configure(text="Time: " + print_time)
    if timer is not None:
        window.after_cancel(timer)
        timer = None
    # update
    timer = window.after(1000, update, current_time, limit)
    # timer_text.configure(text='Time:?')
    wpm = "?"


window = Tk(className="Typing Game", )
window.geometry('600x300')
timer_text = Label(window, text="Time: " + print_time, bg="yellow")
wpm_text = Label(window, text="WPM: " + wpm, bg="blue", fg="white")
restart_btn = Button(text="Restart", command=restart)
# timer = window.after(1000, update, current_time, limit)
text = Text(window, font=('Arial', 20), height=4)
text.insert(INSERT, script)
text.tag_config("incorrect", foreground="red")
text.tag_config("correct", foreground="green")
# text.config(state = DISABLED)
entry = Entry(window, font=('Arial', 20), )
text.config(state=DISABLED)
timer_text.pack()
wpm_text.pack()
text.pack()
entry.pack(fill='x')
restart_btn.pack(pady=10)

window.bind("<Key>", handle)
window.mainloop()

# TODO: Calculate accuracy rate and show in UI
# TODO: Save highscore
