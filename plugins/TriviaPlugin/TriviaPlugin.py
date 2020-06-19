import logging
from collections import defaultdict
import random
from datetime import datetime 
from datetime import timedelta
from time import sleep
import threading
import os
import pandas as pd
import sys
sys.path.insert(0, os.path.dirname(__file__))
from PointsDB import PointsDB

class TriviaPlugin():
	def __init__(self):
		self._dir = os.path.dirname(__file__)
		self._load_questions()

		self._db = PointsDB()

		self._current_ans = None
		self._timeout = None

		self._outbound_messages = []
	
	def _load_questions(self):
		# Load SC Trivia into self._trivia_sc
		folder = os.path.dirname(os.path.abspath(__file__))
		df = pd.read_csv(os.path.join(folder,'questions.csv')).dropna()
		self._questions = []
		for kind, units, unit in df.values:
			self._questions.append({'question': 'What is the [ {} ] for the [ {} ]?'.format(kind, unit), 'answer': str(int(units))})
		for speech, unit in pd.read_csv(os.path.join(folder, 'questions_speech.tsv'),delimiter='\t').dropna().values:
			self._questions.append({'question': '[ UNIT SPEECH ] {}'.format(speech), 'answer': unit})

		for q in self._questions:
			print('{} : {}'.format(q['question'], q['answer']))

	def add_points(self, user) -> int:
		''' Add points for this user and return the new points
		'''
		current_points = self._db.get(user)
		new_points = current_points + 5
		logging.info("Current points: {}".format(current_points))
		logging.info("New points: {}".format(new_points))
		self._db.update(user, new_points)
		return str(new_points)

	def check_for_answer(self, user, msg):
		if msg.strip().lower() == self._current_ans.lower():
			new_points = self.add_points(user)
			self._outbound_messages.append('{} got it ({} total points)! Answer: {}'.format(user, new_points, self._current_ans))				
			self._current_ans = None
			self._timeout = None
			
	def parse(self, user, msg):
		''' Get the incoming messages
		'''	
		# If there is already a question going
		if self._current_ans == None and msg == '!trivia':
			question = random.choice(self._questions)
			self._outbound_messages.append(question['question'])
			self._current_ans = question['answer']
			self._timeout = datetime.now() + timedelta(seconds=30)
			logging.debug("Adding question to queue: {}".format(question['question']))

		if self._current_ans != None:
			self.check_for_answer(user, msg)
		if self._timeout != None and datetime.now() > self._timeout:
			self._outbound_messages.append("Timed out. Answer: {}".format(self._current_ans))
			self._current_ans = None
			self._timeout = None

	def get_outbound(self):
		''' Return the outbound messages
		'''
		if self._timeout != None and datetime.now() > self._timeout:
			self._outbound_messages.append("Timed out. Answer: {}".format(self._current_ans))
			self._current_ans = None
			self._timeout = None

		r = list(self._outbound_messages)
		self._outbound_messages = []
		return r

if __name__ == '__main__':
	t = TriviaPlugin()
		
