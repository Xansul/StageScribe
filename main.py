import tkinter
from tkinter.font import NORMAL
from tracemalloc import start
import scribe

def begin(scribe, start_button, end_button):
    #call scribe function
    scribe.begin_record()

    #update button states
    start_button["state"] = tkinter.DISABLED
    end_button["state"] = tkinter.NORMAL

def end(scribe, start_button, end_button):
    #call scribe function
    scribe.end_recording()

    #update button states
    start_button["state"] = tkinter.NORMAL
    end_button["state"] = tkinter.DISABLED

#create scribe object
scribeObject = scribe.scribe()

#setup tkinter window
window = tkinter.Tk()
window.title("StageScribe")

#setup buttons
start_record_button = tkinter.Button(window, text="Begin Recording", command=lambda: begin(scribeObject, start_record_button, end_record_button))
end_record_button = tkinter.Button(window, text="End Recording", command=lambda: end(scribeObject, start_record_button, end_record_button))

start_record_button.pack()
end_record_button.pack()

end_record_button["state"] = tkinter.DISABLED

#setup text box
text = tkinter.Text(window, height=8)
text.pack()

#start window
window.mainloop()