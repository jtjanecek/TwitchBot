# Trivia Plugin
# Author: John Janecek
# Created 3/21/2016

from collections import defaultdict
import random
from time import sleep
import threading



class TriviaPlugin():
    def __init__(self):
        self._num_questions_left = 0
        self._questions = []
        self._trivia_sc = []
        self._trivia_gen = []
        self._blanks = []
        self._point_dict = defaultdict(int)
        self._trivia_type = "gen"
        
        self._load_into_memory()
    
    
    # ==========================================================================
    #                     Private Methods    
    # ==========================================================================

    
    
    def _load_into_memory(self):
        # Load SC Trivia into self._trivia_sc
        f = open("sctrivia.txt")
        lines = f.read().splitlines()
        f.close()
        for line in lines:
            self._trivia_sc.append(line.split("|"))
        
        # Load General Trivia into self._trivia_gen
        of = open("trivia.txt")
        lines = of.read().splitlines()
        of.close()
        for line in lines:
            self._trivia_gen.append(line.split("|"))
            
        # Load the user points into memory
        f1 = open("points.txt")
        lines = f1.read().splitlines()
        f1.close()
        for line in lines:
            temp = line.split("|")
            self._point_dict[temp[0]] = int(temp[1])
        

    def _do_trivia_game(self):
        # Called to start the Trivia game ( only 1 question )
        #   Sends the question through mybot and starts the threads
        #   to get the answer and read the messages.
        
        sleep(2)
        self._mybot.send_msg(self._questions[0][0])
        
        self._blanks = []
        self._initialize_blanks()
        
        self._lock = threading.Lock()
        self._thread_stop = threading.Event()
        blank_thread = threading.Thread(target = self._time_blanks)
        check_thread = threading.Thread(target = self._check_answer)    
        blank_thread.start()
        check_thread.start()
        blank_thread.join()
        check_thread.join()
    
    def _time_blanks(self):
        # Sets a 5 second timer. After the 5 seconds elapses, as soon  
        #   as a chatter types something, it will display the 
        #   hint as blanks with an extra letter filled in
        while(not self._thread_stop.is_set()):
            sleep(5)
            self._lock.acquire()
            if (self._thread_stop.is_set()):
                self._lock.release()
                break;
            if "".join(self._blanks).lower() == self._questions[0][1].lower():
                self._thread_stop.set()
                self._lock.release()
                break;
            else:
                self._fill_blank()
                if "".join(self._blanks).lower() == self._questions[0][1].lower():
                    self._thread_stop.set()
                    self._lock.release()
                    self._mybot.send_msg("Nobody got it... " + "".join(self._blanks))
                    break;
                else:
                    self._mybot.send_msg(" ".join(self._blanks))
    
            self._lock.release()
            
       
    def _check_answer(self):
        # Thread function that constantly checks whether the 
        #    incoming messages in chat are the answer to the question.
        #    If they are, then _declare_winner() and break both threads.
        while(not self._thread_stop.is_set()):
            self._lock.acquire()
            if "".join(self._blanks).lower() == self._questions[0][1].lower():
                self._thread_stop.set()
                self._mybot.send_msg("Nobody got it...")
                self._lock.release()
                break
            else:
                usr_msg = self._mybot.get_user_and_message()
                answer = usr_msg[1]
                if answer.lower() == self._questions[0][1].lower():
                    self._declare_winner(usr_msg[0])
                    self._thread_stop.set()
                    self._lock.release()
                    break
            self._lock.release()
            sleep(1)
        
        
    def _initialize_blanks(self) -> None:
        # Sets up blanks with number of characters as there are in the answer
        for character in self._questions[0][1]:
            if character == " ":    
                self._blanks.append("-")
            else: self._blanks.append("_")
            
            
    def _fill_blank(self) -> None:
        # Fills in one character in the HINT
        while(True):
            index = int(random.random() * len(self._questions[0][1]))
            if self._blanks[index] == "_":
                self._blanks[index] = self._questions[0][1][index].upper()
                return;
    
        
    def _declare_winner(self , winner: str) -> None:
        # Sends a winner message and updates the points in memory
        self._point_dict[winner] += 5
        message = winner + " is the winner! "
        message += "Awarded 5 Trivia Points. "
        message += "Current points: " + str(self._point_dict[winner])
        self._mybot.send_msg(message)
        
        
    # ==========================================================================
    #                      Methods Needed for every plugin    
    # ==========================================================================

    
    def __str__(self) -> str:
        # Used for "commands" command
        return "trivia"
        
    def start(self, mybot) -> None:
        self._mybot = mybot
        # Called to start 3 questions of trivia
        
        self._num_questions_left = 3
        del self._questions[:] # Delete current leftover questions
    
        # Start sc trivia
        random.seed();
        if self._trivia_type == "sc":
            sz = len(self._trivia_sc)
            for i in range(3):
                self._questions.append(self._trivia_sc[int(random.random()*sz)])
        # Start General trivia
        else:
            sz = len(self._trivia_gen)
            for i in range(3):
                self._questions.append(self._trivia_gen[int(random.random()*sz)])
    
        # Ask each individual question
        self._mybot.send_msg(" Starting 3 Questions of Trivia...")
        for i in range(3): 
            self._do_trivia_game()
            del self._questions[0]  # Delete the question that was just asked.
            self._num_questions_left -= 1
            
    def triggered(self, username, message, command_char) -> bool:
        # Returns whether this plugin is triggered by the username / message
        if message[0] != command_char:
            return False
        if message[1:7] == "trivia":
            if len(message) > 7 and message[8:] == "sc":
                self._trivia_type = "sc"   
            else:
                self._trivia_type = "gen"
            return True    
        return False
    
    def unload_memory(self) -> None:
        # Writes memory points back to the file
        of = open("points.txt","w")
        for item in self._point_dict.items():
            of.write(item[0] + "|" + str(item[1]) + "\n")
        
        
