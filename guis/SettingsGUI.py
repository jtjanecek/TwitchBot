import tkinter


class SettingsGUI():
    def __init__(self, current_settings: dict, current_plugins: list):
        self._root = tkinter.Tk()
        self._settings = current_settings
        self._plugins = current_plugins

        self._title_label = tkinter.Label(self._root, text = "Welcome to MyBot!" ,font=("Helvetica", 16))
        self._title_label.grid(row = 1, column = 1, sticky = "N", columnspan = 2)

        self._description = tkinter.Label(self._root, text = "Leave fields below blank to use defaults specified in defaults.txt (shown in brackets)")
        self._description.grid(row = 2, column = 1, sticky = "N", columnspan = 2)

        self._nick_label = tkinter.Label(self._root, text = ("Bot nickname [default: " + self._settings["nick"] + "]"))
        self._nick_label.grid(row = 4, column = 1, sticky ="W")
        self._nick_entry = tkinter.Entry(self._root)
        self._nick_entry.grid(row = 4,column = 2)
        
        self._oauth_label = tkinter.Label(self._root,text = ("Bot oauth [default: " + self._settings["oauth"] + "]"))
        self._oauth_label.grid(row = 5, column = 1, sticky ="W")
        self._oauth_entry = tkinter.Entry(self._root)
        self._oauth_entry.grid(row = 5,column = 2)    
        
        self._command_char_label = tkinter.Label(self._root,text = ("Bot command character [default: " + self._settings["command_char"] + "]"))
        self._command_char_label.grid(row = 6, column = 1, sticky ="W")
        self._command_char_entry = tkinter.Entry(self._root)
        self._command_char_entry.grid(row = 6,column = 2)     
        
        self._stream_label = tkinter.Label(self._root,text = ("Stream for bot to join [default: " + self._settings["stream"] + "]"))
        self._stream_label.grid(row = 7, column = 1, sticky ="W")
        self._stream_entry = tkinter.Entry(self._root)
        self._stream_entry.grid(row = 7,column = 2)    

        current_index = 9
        if current_plugins != []:
            self._plugins_label = tkinter.Label(self._root, text = ("Check the Plugins you want to use"))
            self._plugins_label.grid(row = 8, column = 1)
            for i in range(len(current_plugins)):
                exec("self._var" + str(i) + " = tkinter.IntVar()")	
                exec("self._check" + str(i) + " = tkinter.Checkbutton(self._root,text = \"" + (self._plugins[i].name()) + "\", variable = " + "self._var" + str(i) + ")")	
                exec("self._check" + str(i) + ".grid(row = " + str(current_index) + ",column = 1)")
                current_index += 1



        self._join_button = tkinter.Button(self._root,text = "Join Stream", command = self._join_stream)
        self._join_button.grid(row = 100, column = 2, sticky = "E")
                
        


    def main_routine(self) -> dict:
        self._root.mainloop()
        return (self._settings, self._plugins)

    def _join_stream(self):
        if self._nick_entry.get() != "":
            self._settings["nick"] = self._nick_entry.get()
        if self._oauth_entry.get() != "":
            self._settings["oauth"] = self._oauth_entry.get()
        if self._command_char_entry.get() != "":
            self._settings["command_char"] = self._command_char_entry.get()
        if self._stream_entry.get() != "":
            self._settings["stream"] = self._stream_entry.get()        
        
        if self._plugins != []:
            plugins_to_delete = []
            for i in range(len(self._plugins)):
                value = eval("self._var" + str(i) + ".get()")
                if value == 0:
                     plugins_to_delete.append(self._plugins[i].name())
            self._plugins = [plug for plug in self._plugins if plug.name() not in plugins_to_delete]

        self._root.destroy()

