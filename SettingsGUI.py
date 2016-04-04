import tkinter


class SettingsGUI():
    def __init__(self, current_settings: dict):
        self._root = tkinter.Tk()
        self._settings = current_settings
    
        self._nick_label = tkinter.Label(self._root,text = ("Bot nickname [default: " + self._settings["nick"] + "]"))
        self._nick_label.grid(row = 1, column = 1, sticky ="W")
        self._nick_entry = tkinter.Entry(self._root)
        self._nick_entry.grid(row = 1,column = 2)
        
        self._oauth_label = tkinter.Label(self._root,text = ("Bot oauth [default: " + self._settings["oauth"] + "]"))
        self._oauth_label.grid(row = 2, column = 1, sticky ="W")
        self._oauth_entry = tkinter.Entry(self._root)
        self._oauth_entry.grid(row = 2,column = 2)    
        
        self._command_char_label = tkinter.Label(self._root,text = ("Bot command character [default: " + self._settings["command_char"] + "]"))
        self._command_char_label.grid(row = 3, column = 1, sticky ="W")
        self._command_char_entry = tkinter.Entry(self._root)
        self._command_char_entry.grid(row = 3,column = 2)     
        
        self._stream_label = tkinter.Label(self._root,text = ("Stream for bot to join [default: " + self._settings["stream"] + "]"))
        self._stream_label.grid(row = 4, column = 1, sticky ="W")
        self._stream_entry = tkinter.Entry(self._root)
        self._stream_entry.grid(row = 4,column = 2)    


        self._join_button = tkinter.Button(self._root,text = "Join Stream", command = self._join_stream)
        self._join_button.grid(row = 5, column = 2, sticky = "E")
                
        


    def main_routine(self) -> dict:
        self._root.mainloop()
        return self._settings

    def _join_stream(self):
        if self._nick_entry.get() != "":
            self._settings["nick"] = self._nick_entry.get()
        if self._oauth_entry.get() != "":
            self._settings["oauth"] = self._oauth_entry.get()
        if self._command_char_entry.get() != "":
            self._settings["command_char"] = self._command_char_entry.get()
        if self._stream_entry.get() != "":
            self._settings["stream"] = self._stream_entry.get()        
        
        self._root.destroy()

