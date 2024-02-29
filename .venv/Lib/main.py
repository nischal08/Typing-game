from tkinter import *

CAPITAL_KEYS = {"Shift_L", "Shift_R", "Caps_Lock"}
limit = 2 #Is in seconds
current_time = 0
count = 0
is_capital = False
is_init = True
script = "A computer program can easily produce gibberish, especially if it has been provided with garbage beforehand. This program does something a little different. It takes a block of text as input and works out the proportion of characters within the text according to a chosen order. For example, an order of 2 means the program looks at pairs of letters, an order of 3 means triplets of letters and so on.."


def handle(event):
    global timer
    global count
    global is_init
    global is_capital
    if is_init:
        timer = window.after(1000, update, current_time, limit)
        is_init = False
    if event.keysym in CAPITAL_KEYS:
        # is_capital = True
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
    # is_capital = False


def update(current_time, limit):
    current_time += 1
    global timer
    if current_time < limit:
        timer_text.configure(text=current_time)
        timer = window.after(1000, update, current_time, limit)
    else:
        wpm_text.configure(text=int((count / 5) / (limit/60)))
        # accuracy_text.configure(text=int((/count)*100))
        # timer_text.configure(text="Times Up!",fg="white",bg="red")
        timer_text.configure(text=current_time,fg="white",bg="red")
        window.after_cancel(timer)
        entry.config(state=DISABLED)
        window.unbind(handle)


def restart():
    global timer
    global count
    global is_init
    count = 0
    is_init=True
    entry.config(state="normal")
    entry.delete(0, 'end')
    window.bind("<Key>", handle)
    current_time = 0
    for tag in text.tag_names():
        # print(text.tag_ranges(tag))
        text.tag_remove(tag, "1.0", "end")
    timer_text.configure(text=current_time)
    if timer is not None:
        window.after_cancel(timer)
        timer = None
    # update
    # timer = window.after(1000, update, current_time, limit)
    # timer_text.configure(text='Time:?')
    wpm_text.configure(text="?")


window = Tk(className="Typing Game", )
frame = Frame( window)
frame.pack()

bottomframe = Frame(window,width= 430,)
bottomframe.pack( side = TOP )

window.geometry('600x300')
timer_label = Label(frame,  text="Time Left:", )
timer_text = Label(frame, width=3, text="0", bg="yellow")
wpm_label = Label(frame,  text="WPM:", )
wpm_text = Label(frame,width=3, text="?", bg="blue", fg="white")
accuracy_label = Label(frame,  text="Accuracy:", )
accuracy_text = Label(frame,width=3, text="?", bg="green", fg="white")
restart_btn = Button(bottomframe,text="Restart", command=restart)
text = Text(bottomframe, font=('Arial', 20), height=4)
text.insert(INSERT, script)
text.tag_config("incorrect", foreground="red")
text.tag_config("correct", foreground="green")
# text.config(state = DISABLED)
entry = Entry(bottomframe, font=('Arial', 20), )
text.config(state=DISABLED)
timer_label.pack(side=LEFT,pady=5,padx=2)
timer_text.pack(side=LEFT,pady=5,padx=2)
wpm_label.pack(side=LEFT,pady=5,padx=2)
wpm_text.pack(side=LEFT,pady=5,padx=2)
accuracy_label.pack(side=LEFT,pady=5,padx=2)
accuracy_text.pack(side=LEFT,pady=5,padx=2)
text.pack()
entry.pack(fill='x')
restart_btn.pack(pady=10)

window.bind("<Key>", handle)
window.mainloop()

# TODO: Calculate total correct count
# TODO: Calculate accuracy rate and show in UI
# TODO: Save highscore
# TODO: Web scrape of typing game website to show random new text
