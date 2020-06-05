import random
import pronouncing

class Syla:
	vowels = ['a','e','i','o','u','y']
	consonants = ['b','c','d','f','g','h','j','k','l','m','n','p',
	              'q','r','s','t','v','w','x','y','z']
	letters = vowels + consonants
	def count_syl(self,word):
		'''
		counts syllables in a word

		>>> x = Form('arduous')
		>>> x.syl
		3

		>>> y = Form('smuckers')
		>>> y.syl
		2

		>>> y = Form('brr')
		1
		'''
		phone_lst = pronouncing.phones_for_word('fuckers')
		return pronouncing.syllable_count(phone_lst[0])

class Form(Syla):
	speech_dict = {}
	def __init__(self, sentence):
		self.syl = self.parse_sentence(sentence)

	def parse_sentence(self, sentence):
		'''
		parses sentences into syllables and also creates speech_dict

		>>> x = Form('My bitch love do cocaine, ooh')
		>>> x.syl 
		7
		'''
		word, prev_word, syl_count = '', '', 0
		for i in sentence:
			if i is '*':
				return i
			elif i is '(':
				return syl_count
			elif i is '[':
				next = sentence[1]
				if next is 'H' or next is 'C':
					return 'C'
				return 'E'
			i = i.lower()
			if i not in self.letters:
				if word:
					syl_count += self.count_syl(word)
					self.dict_check(word, prev_word)
					word, prev_word = '', word
			else:
				word += i

		if word:
			syl_count += self.count_syl(word)
			self.dict_check(word, prev_word)
			self.dict_check('.', word)
		return syl_count

	def dict_check(self, word, prev_word):
		if prev_word:
			if prev_word in Form.speech_dict:
				if word not in Form.speech_dict[prev_word]:
					Form.speech_dict[prev_word].append(word)
			else:
				Form.speech_dict[prev_word] = [word]

class Block:
	def __init__(self):
		self.form_lst = []
		self.song_form = []
		x = open('gucci.txt','rt', encoding='latin1')
		for line in x:
			line = line.replace("'",'')
			formed = Form(line).syl
			if formed is '*':
				self.form_lst.append(self.song_form)
				self.song_form = []
			elif formed:
				self.song_form.append(formed)
		self.speech_dict = Form.speech_dict
		filtered = filter(lambda x: len(x) > 1, self.form_lst)
		self.form_lst = []
		for x in filtered:
			self.form_lst.append(x)

	def __str__(self):
		print('**********************')
		for i in self.form_lst:
			for b in i:
				print(b)
			print('**********************')
		return ''

x = Block()

class Lyric_Gen(Syla):
	'''
	returns a line of rap
	self.last = last word of line
	'''
	def __init__(self, syl_ceiling, rhyme = ''):
		#optional rhyme argument for last word to rhyme
		self.speech_dict = x.speech_dict
		self.max_syls = syl_ceiling
		self.og_rhyme = rhyme
		self.last = ''
		self.set_syls()

	def set_syls(self):
		#sets the rhyme and the max amount of syllables to be made in the lyric loop
		self.lyric = ''
		if self.og_rhyme:
			self.rhyme = self.rhyme_check(self.og_rhyme)
			self.syl_ceiling = self.max_syls - self.count_syl(self.rhyme)
		else:
			self.rhyme = self.og_rhyme
			self.syl_ceiling = self.max_syls
		self.syllables = 0

	def rand_key(self):
		#yields a random key from self.speech_dict
		return random.choice(list(self.speech_dict.keys()))

	def rand_list(self, word):
		#yields a random word from self.speech_dict[word]
		return random.choice(self.speech_dict[word])

	def lyric_loop(self, word, last):
		#recursive function creates a line w/ correct syllables & rhyme
		if self.syllables >= self.syl_ceiling:
			if self.syllables == self.syl_ceiling:
				self.lyric = self.lyric + ' ' + self.rhyme
				return self.lyric
			return self.restart()
		elif word not in self.speech_dict or word is self.last:
			return self.restart()
		else:
			self.syllables += self.count_syl(word)
			if self.lyric:
				self.lyric = self.lyric + ' ' + word
				self.last = self.rhyme or word
			else:
				self.lyric = word
				self.last = self.rhyme or word
			return self.lyric_loop(self.rand_list(word), word)

	def restart(self):
		#retart lyric loop 
		self.set_syls()
		return self.lyric_loop(self.rand_key(), '')

	def rhyme_check(self, word):
		#selects a random rhyme from word 
		return random.choice(pronouncing.rhymes(word))

y = Lyric_Gen(10, 'bunk')


class Song:
	def __init__(self):
		self.form = random.choice(x.form_lst)
		self.song_lst = []
		self.chorus = []
		self.chorus_made = False
		self.index, self.max_len = 0, len(self.form)
		self.rhyme_count = 0
		self.form_check()

	def form_check(self):
		if self.index >= self.max_len:
			return
		pointer = self.form[self.index]
		if isinstance(pointer, int):
			self.create()
		else:
			if pointer == 'E':
				if self.song_lst:
					self.song_lst.append('')
			else:
				self.index += 1
				self.song_lst.append('')
				return self.chorus_fork()
		self.index += 1
		return self.form_check()

	def create(self):
		syllables = self.form[self.index]
		if not self.rhyme_count:
			flag = True
			while flag:
				lyric_object = Lyric_Gen(syllables)
				lyric_object.restart()
				if pronouncing.rhymes(lyric_object.last):
					flag = False
			self.rhyme_count = 1
		else:
			lyric_object = Lyric_Gen(syllables, self.last)
			lyric_object.restart()
			self.rhyme_count = 0
		self.song_lst.append(lyric_object.lyric)
		self.last = lyric_object.last

	def chorus_fork(self):
		if self.chorus_made:
			return self.chorus_return()
		else:
			return self.make_chorus()

	def make_chorus(self):
		if self.index == self.max_len:
			return 
		elif self.form[self.index] is 'E':
			self.chorus_made = True
			return self.form_check()
		self.create()
		self.chorus.append(self.song_lst[len(self.song_lst) - 1])
		self.index += 1
		return self.make_chorus()

	def chorus_return(self):
		for b in self.chorus:
			self.index += 1
			self.song_lst.append(b)
		return self.form_check()

	def end_check(self):
		if self.index >= self.max_len:
			return True
		return False

	def __repr__(self):
		for x in self.song_lst:
			print(x)
		return ''


def play():
	z = Song()
	print(z)



