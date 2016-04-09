from tkinter import *
import threading
from time import sleep


class BotGUI():
    def __init__(self):
        self._root = Tk()
        self._root.wm_title("BotGUI")
        self._alive = True

        self._text = Text(self._root, bg="black", fg="white")
        self._text.pack()
        
        self._exit_button = Button(self._root, text = "EXIT STREAM", command = self.exit_stream)
        self._exit_button.pack()
        
        self._queue = []
        self._lock = threading.Lock()
        
    def exit_stream(self):
        self._alive = False

    def display(self):
        while(self._alive):
            sleep(.05)
            self._lock.acquire()
            for msg in self._queue:
                self._text.insert(END,msg)
                self._text.see(END)
            self._queue = []
            self._lock.release()
        
    def main_routine(self):
        t = threading.Thread(target = self.display)
        t.daemon = True
        t.start()
        self._root.mainloop()


    def show(self, msg, sep = "\n"):
        self._lock.acquire()
        self._queue.append( str(msg) + sep )
        self._lock.release()
        
    def is_alive(self) -> bool:
        return self._alive
        
    def destroy(self):
        self._root.destroy()
