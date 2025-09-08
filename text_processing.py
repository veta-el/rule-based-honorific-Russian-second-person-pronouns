import random
import os

import pos_classes

#Create part of speech objects in dict format {name: dict of objects}
pos_names = os.listdir('class_objects/')
pos_objects = {}

for pos_name in pos_names:
	name = pos_name [:-4]
	pos_objects [name] = pos_classes.collect_pos_objects (name)

def normalize (phrase):
	letters = list(phrase)
	punctuations_to_replace = list(pos_objects['punctuation'].keys ())
	punctuations_to_replace.remove('-')
	letters = [symbol if symbol not in punctuations_to_replace else ' ' for symbol in letters]
	words_string = ''.join(letters)
	words = words_string.split()
	words.insert (0, pos_objects['punctuation'] ['.']) #Insert starting separator - . 
	return words

def part_of_speech(word, prev_element):
	def get_structure (word, prev_element):
		def root_search (word):
			word_len = len(word)
			return next((pos_objects['root'] [root] for root in pos_objects['root'] if word_len >= len(pos_objects['root'] [root].text_form) and word[:len(pos_objects['root'][root].text_form)] == pos_objects['root'][root].text_form), '-')
		def prefix_search (word):
			word_len = len(word)
			return next((pos_objects['prefix'] [prefix] for prefix in pos_objects['prefix'] if word_len >= len(pos_objects['prefix'] [prefix].text_form) and word[:len(pos_objects['prefix'] [prefix].text_form)] == pos_objects['prefix'] [prefix].text_form), '-')
		def suffix_checker (word):
			for suffix in pos_objects['suffix']:
				current_suffix = word [:len (pos_objects['suffix'] [suffix].text_form)]
				if current_suffix == pos_objects['suffix'] [suffix].text_form:
					return True
			return '-'
		def endings_search (word_without_prefix_roots):
			endings_list = []
			for ending in pos_objects['ending']:
				current_ending = word_without_prefix_roots [-len(pos_objects['ending'] [ending].text_form):]
				if current_ending == pos_objects['ending'] [ending].text_form:
					endings_list.append (pos_objects['ending'] [ending])
			if endings_list:
				max_len = max(len (element.text_form) for element in endings_list) #Select only max len endings
				return [ending for ending in endings_list if len(ending.text_form) == max_len]
			else:
				return '-'
		def suffixes_search (word_without_prefix_roots_endings):
			suffixes_list = []
			for suffix in pos_objects['suffix']:
				current_suffix = word_without_prefix_roots_endings [-len(pos_objects['suffix'] [suffix].text_form):]
				if current_suffix == pos_objects['suffix'] [suffix].text_form:
					suffixes_list.append (pos_objects['suffix'] [suffix])
			if suffixes_list:
				max_len = max(len (element.text_form) for element in suffixes_list) #Select only max len suffixes
				return [suffix for suffix in suffixes_list if len(suffix.text_form) == max_len]
			else:
				return '-'
		def sort_endings_suffixes (current_endings, current_suffixes, prev_element):
			first_suffixes_list = []
			second_suffixes_list = []
			first_endings_list = []
			second_endings_list = []
			#Select suffixes
			if (current_suffixes!='-') and (len(current_suffixes)>1):
				parts = []
				for suffix in current_suffixes: #Find potential part of speech
					parts.append (suffix.part_of_speech)
				parts = list(set(parts))
				if len (parts)>1:
					probabilities = {}
					for part in parts:
						probabilities [part] = [pos_objects['bigram'] [probability].procent for probability in pos_objects['bigram'] if pos_objects['bigram'] [probability].second_to_compare == part and type(prev_element).__name__ == pos_objects['bigram'] [probability].first_to_compare]
					right_part = max(probabilities.keys(), key=lambda k: probabilities[k])
				else:
					right_part = parts [0] #Chosen part of speech
				first_suffixes_list.extend(filter(lambda suffix: suffix.part_of_speech == right_part, current_suffixes)) #Select only chosen part of speech suffixes

				current_index = 0
				while current_index != (len (first_suffixes_list)-1): #Select suffixes based on 'pair randomness' if they are of different type character
					if first_suffixes_list [current_index].type_character==first_suffixes_list [current_index+1].type_character:
						current_pair=[first_suffixes_list [current_index], first_suffixes_list [current_index+1]]
						random_suffix = random.choice (current_pair)
						second_suffixes_list.append (random.choice (current_pair))
						current_pair.remove (random_suffix)
						first_suffixes_list.remove (current_pair [0])
					else:
						second_suffixes_list.append (first_suffixes_list [current_index])
						current_index += 1
				second_suffixes_list.append (first_suffixes_list [current_index])
			else:
				second_suffixes_list = current_suffixes

			#Select endings
			if (current_endings!='-') and (len(current_endings)>1):
				if second_suffixes_list!='-': #If we can use suffix part of speech to select endings
					first_ending_list.extend(filter(lambda ending: ending.part_of_speech == second_suffixes_list[0].part_of_speech, current_endings))
				else:
					current_index = 0
					while current_index != (len (current_endings)-1): #Select endings based on 'pair randomness' if they are of different part of speech
						if current_endings [current_index].part_of_speech != current_endings [current_index+1].part_of_speech:
							current_pair = [current_endings [current_index], current_endings [current_index+1]]
							random_ending = random.choice (current_pair)
							first_endings_list.append (random_ending)
							current_pair.remove (random_ending)
							current_endings.remove (current_pair [0])
						else:
							first_endings_list.append (current_endings [current_index])
							current_index += 1
					first_endings_list.append (current_endings [current_index])

				current_index = 0 #Select endings based on 'pair randomness' if they are of different type character
				if len(first_endings_list) != 0:
					while current_index != (len (first_endings_list)-1):
						if first_endings_list [current_index].type_character==first_endings_list [current_index+1].type_character:
							current_pair = [first_endings_list [current_index], first_endings_list [current_index+1]]
							random_ending = random.choice (current_pair)
							second_endings_list.append (random_ending)
							current_pair.remove (random_ending)
							first_endings_list.remove (current_pair [0])
						else:
							second_endings_list.append (first_endings_list [current_index])
							current_index += 1
					second_endings_list.append (first_endings_list [current_index])
				else:
					second_endings_list = '-'
			else:
				second_endings_list = current_endings
			return second_endings_list, second_suffixes_list

		lower_word = word.lower()
		#Search root and prefixes
		current_root = root_search (lower_word) #Root search
		if current_root == '-': #If root not found
			current_prefix = prefix_search(lower_word) #Search for prefix
			if current_prefix != '-': #Prefix found
				word_without_prefix = lower_word [len(current_prefix.text_form):]
				current_root = root_search (word_without_prefix) #New root search knowing about prefix
				if current_root == '-': #No root found
					second_prefix = prefix_search(word_without_prefix) #Second prefix search
					if second_prefix != '-':
						current_prefix = pos_classes.prefix (current_prefix.text_form + second_prefix.text_form) #Combine two prefixes
						word_without_prefix = lower_word [len(current_prefix.text_form):]
						if word_without_prefix == '': #If by accident root was considered as two prefixes
							current_root = pos_classes.root (lower_word)
						else:
							current_root = root_search (word_without_prefix) #Search a root knowing about two prefixes
							if current_root == '-': #No root found - set word_without_prefix [0] as root
								current_root = pos_classes.root (word_without_prefix [0])
					else: #If no root and no second prefix
						current_root = pos_classes.root (word_without_prefix [0])
			else: #No prefix found - set word_without_prefix [0] as root
				word_without_prefix = lower_word
				current_root = pos_classes.root (word_without_prefix [0])
		else: #If first root search succeed - means no prefix needed
			current_prefix = '-'
			word_without_prefix = lower_word

		#Search second root
		word_without_prefix_roots = word_without_prefix [len (current_root.text_form):]
		if word_without_prefix_roots=='': #If no more morphemes
			current_suffixes = '-'
			current_endings = '-'
		else:
			if (word_without_prefix_roots [0]=='е') or (word_without_prefix_roots [0]=='о'): #Connecting vowels
				if len (word_without_prefix_roots)>=2:
					if suffix_checker (word_without_prefix_roots)=='-': #Check if it is not a suffix but a second root
						current_root.text_form = current_root.text_form+word_without_prefix_roots [0] #Add connecting vowel to the first root
						word_without_conj = word_without_prefix [len(current_root.text_form):] #Remove connecting vowel
						second_root = root_search(word_without_conj) #Search for second root
						if second_root != '-':
							current_root.text_form = current_root.text_form+second_root.text_form
							word_without_prefix_roots = word_without_prefix [len (current_root.text_form):]

			#Search endings and suffixes
			current_endings = endings_search(word_without_prefix_roots)
			if current_endings!= '-':
				word_without_prefix_roots_endings = word_without_prefix_roots [:(len (word_without_prefix_roots)-len (current_endings [0].text_form))] #Remove ending len
			else: #Means no ending but probably some suffixes
				word_without_prefix_roots_endings = word_without_prefix_roots
			current_suffixes = suffixes_search(word_without_prefix_roots_endings)
			if current_suffixes != '-':
				material_for_suffixes = word_without_prefix_roots_endings [:(len (word_without_prefix_roots_endings)- len (current_suffixes [0].text_form))]
				if material_for_suffixes!='': #If there are more suffixes
					second_current_suffixes = suffixes_search(material_for_suffixes)
					if second_current_suffixes != '-':
						current_suffixes = second_current_suffixes + current_suffixes #Add new suffixes
						material_for_suffixes = material_for_suffixes [:(len (material_for_suffixes)- len (second_current_suffixes [len (second_current_suffixes)-1].text_form))]
						if material_for_suffixes != '': #search for third-level suffixes
							third_current_suffixes = suffixes_search(material_for_suffixes)
							if third_current_suffixes!='-':
								current_suffixes = third_current_suffixes + current_suffixes #Add new suffixes
			if (current_suffixes != '-') or (current_endings != '-'):
				current_endings, current_suffixes = sort_endings_suffixes (current_endings, current_suffixes, prev_element) #Select endings and suffixes

		if current_suffixes == '-':
			current_suffixes = [pos_classes.suffix ('-', '-', '-', '-')]
		if current_endings == '-':
			current_endings = [pos_classes.ending ('-', '-', '-', '-')]
		if current_prefix == '-':
			current_prefix = pos_classes.prefix ('-')
		if current_root == '-':
			current_root = pos_classes.root ('-')
		#Define part of speech features
		#Huge block of conditions
		if current_suffixes [0].part_of_speech=='noun':
			if word [0].isupper ():
				name='prop'
			else:
				name='common'
			living = '-'
			for i in current_suffixes+current_endings:
				if i.type_character=='gender':
					gender=i.character
				else:
					gender='m'
			if (word [len (word)-1]=='а') or (word [len (word)-1]=='я'):
				declension='1'
			if gender=='f':
				declension='3'
			else:
				declension='2'
			for i in current_suffixes+current_endings:
				if i.type_character=='number':
					number=i.character
				else:
					number='s'
			for i in current_suffixes+current_endings:
				if i.type_character=='case':
					case=i.character
				else:
					case='im'
			set_suffixes={i.text_form for i in current_suffixes}
			if set_suffixes:
				suf = ''.join(set_suffixes)
			else:
				suf = ''
			set_endings={i.text_form for i in current_endings}
			if set_endings:
				endin = ''.join(set_endings)
			else:
				endin = ''
			role='-'
			return pos_classes.noun (lower_word, name, living, gender, declension, number, case, suf, current_prefix.text_form, endin, current_root.text_form, role)
		if current_suffixes [0].part_of_speech=='adjective':
			for i in current_suffixes+current_endings: #But endings are more preferable for choosing features
				if i.type_character=='typ':
					typ=i.character
				else:
					typ='kach'
			for i in current_suffixes+current_endings:
				if i.type_character=='degree':
					degree=i.character
				else:
					degree='netr'
			for i in current_suffixes+current_endings:
				if i.type_character=='form':
					form=i.character
				else:
					form='full'
			for i in current_suffixes+current_endings:
				if i.type_character=='gender':
					gender=i.character
				else:
					gender='m'
			for i in current_suffixes+current_endings:
				if i.type_character=='number':
					number=i.character
				else:
					number='s'
			for i in current_suffixes+current_endings:
				if i.type_character=='case':
					case=i.character
				else:
					case='im'
			set_suffixes={i.text_form for i in current_suffixes}
			if set_suffixes:
				suf = ''.join(set_suffixes)
			else:
				suf = ''
			set_endings={i.text_form for i in current_endings}
			if set_endings:
				endin = ''.join(set_endings)
			else:
				endin = ''
			role='-'
			return pos_classes.adjective (lower_word, typ, degree, form, gender, number, case, suf, current_prefix.text_form, endin, current_root.text_form, role)
		if current_suffixes [0].part_of_speech=='verb':
			for i in current_suffixes+current_endings:
				if i.type_character=='typ':
					typ=i.character
				else:
					if lower_word [0]=='с':
						typ='s'
					else:
						typ='n'
			transitivity='-'
			for i in current_suffixes:
				if i.text_form=='ся':
					reflex='+'
					break
				else:
					reflex='-'
			declension='-'
			for i in current_suffixes+current_endings:
				if i.type_character=='inclination':
					inclination=i.character
				else:
					inclination='iz'
			for i in current_suffixes+current_endings:
				if i.type_character=='person':
					person=i.character
				else:
					person='3'
			for i in current_suffixes+current_endings:
				if i.type_character=='gender':
					gender=i.character
				else:
					gender='m'
			for i in current_suffixes+current_endings:
				if i.type_character=='number':
					number=i.character
				else:
					number='s'
			for i in current_suffixes+current_endings:
				if i.type_character=='time':
					time=i.character
				else:
					time='n'
			set_suffixes={i.text_form for i in current_suffixes}
			if set_suffixes:
				suf = ''.join(set_suffixes)
			else:
				suf = ''
			set_endings={i.text_form for i in current_endings}
			if set_endings:
				endin = ''.join(set_endings)
			else:
				endin = ''
			role='-'
			return pos_classes.verb (lower_word, typ, transitivity, reflex, declension, inclination, person, gender, number, time, suf, current_prefix.text_form, endin, current_root.text_form, role)
		if current_suffixes [0].part_of_speech=='adverb':
			for i in current_suffixes:
				if i.type_character=='degree':
					degree=i.character
				else:
					degree='netr'
			set_suffixes={i.text_form for i in current_suffixes}
			if set_suffixes:
				suf = ''.join(set_suffixes)
			else:
				suf = ''
			role='-'
			return pos_classes.adverb (lower_word, degree, suf, current_prefix.text_form, current_root.text_form, role)
		if current_suffixes [0].part_of_speech=='participle':
			for i in current_suffixes+current_endings:
				if i.type_character=='passive':
					passive=i.character
				else:
					passive='act'
			for i in current_suffixes:
				if i.text_form=='ся':
					reflex='+'
					break
				else:
					reflex='-'
			for i in current_suffixes+current_endings:
				if i.type_character=='typ':
					typ=i.character
				else:
					if lower_word [0]=='с':
						typ='s'
					else:
						typ='n'
			for i in current_suffixes+current_endings:
				if i.type_character=='time':
					time=i.character
				else:
					time='n'
			for i in current_suffixes+current_endings:
				if i.type_character=='form':
					form=i.character
				else:
					form='full'
			for i in current_suffixes+current_endings:
				if i.type_character=='degree':
					degree=i.character
				else:
					degree='netr'
			for i in current_suffixes+current_endings:
				if i.type_character=='gender':
					gender=i.character
				else:
					gender='m'
			for i in current_suffixes+current_endings:
				if i.type_character=='number':
					number=i.character
				else:
					number='s'
			for i in current_suffixes+current_endings:
				if i.type_character=='case':
					case=i.character
				else:
					case='im'
			set_suffixes={i.text_form for i in current_suffixes}
			if set_suffixes:
				suf = ''.join(set_suffixes)
			else:
				suf = ''
			set_endings={i.text_form for i in current_endings}
			if set_endings:
				endin = ''.join(set_endings)
			else:
				endin = ''
			role='-'
			return pos_classes.participle (lower_word, passive, reflex, typ, time, form, degree, gender, number, case, suf, current_prefix.text_form, endin, current_root.text_form, role)
		if current_suffixes [0].part_of_speech=='participle_d':
			for i in current_suffixes:
				if i.type_character=='typ':
					typ=i.character
				else:
					if lower_word [0]=='с':
						typ='s'
					else:
						typ='n'
			transitivity='-'
			for i in current_suffixes:
				if i.text_form=='ся':
					reflex='+'
					break
				else:
					reflex='-'
			set_suffixes={i.text_form for i in current_suffixes}
			if set_suffixes:
				suf = ''.join(set_suffixes)
			else:
				suf = ''
			role='-'
			return pos_classes.participle_d (lower_word, typ, transitivity, reflex, suf, current_prefix.text_form, current_root.text_form, role)
		else:
			return pos_classes.noun (lower_word, 'common', '-', 'm', '2', 's', 'im', '-', current_prefix.text_form, '-', current_root.text_form, '-')

	lower_word = word.lower()
	pos_objects_to_check = list (pos_objects.keys ())

	pos_objects_to_check.remove ('bigram')
	pos_objects_to_check.remove ('ending')
	pos_objects_to_check.remove ('prefix')
	pos_objects_to_check.remove ('root')
	pos_objects_to_check.remove ('suffix')

	for pos_class in pos_objects_to_check:
		for obj_text_form in pos_objects [pos_class].keys ():
			if lower_word == obj_text_form:
				return pos_objects [pos_class] [obj_text_form]
	return get_structure (word, prev_element)

def role_in_sentence (word):
	#Block of conditions for role in sentence
	if (type (word)==pos_classes.pronoun) and (word.pronoun_type=='prityazh'):
		return 'definition'
	if (type (word)==pos_classes.noun) or (type (word)==pos_classes.pronoun):
		if word.case=='im':
			return 'subject'
		else:
			return 'object'
	if type (word)==pos_classes.verb:
		return 'predicate'
	if (type (word)==pos_classes.adjective) or (type (word)==pos_classes.participle):
		return 'definition'
	if (type (word)==pos_classes.participle_d) or (type (word)==pos_classes.adverb):
		return 'circum_obraz'
	if type (word)==pos_classes.numeral:
		return 'circum_mera'
	if type (word)==pos_classes.interjection:
		return 'interjec'
	if type (word)==pos_classes.filler:
		return 'filler'
	if type (word)==pos_classes.preposition:
		return 'indirect_object'
	if type (word)==pos_classes.conjunction:
		return 'conj'
	if type (word)==pos_classes.particle:
		return 'particle'
	if type (word)==pos_classes.punctuation:
		return 'punctuation'

def elements_to_check (phrase, pronoun_number): #Check what elements should be considered for pronoun context
	to_return=[[],[]]
	for i in range (1, 4):
		if pronoun_number+i<len (phrase):
			if (hasattr(phrase [pronoun_number+i], 'role')) and ((phrase[pronoun_number+i].role) [-6:]=='object'):
				continue
			else:
				to_return [1].append (phrase [pronoun_number+i])
		if pronoun_number-i>=0:
			if (hasattr(phrase [pronoun_number-i], 'role')) and ((phrase[pronoun_number-i].role) [-6:]=='object'):
				continue
			else:
				to_return [0].append (phrase [pronoun_number-i])
	return to_return

def result_func (prev_list, word, next_list, number_in_list): #Get the analysis of pronoun based on its context
	number_list = []
	gender = []
	#Consider attributes of context
	if len(prev_list)!=0:
		for element in prev_list:
			if (hasattr (element, 'number')==True) and (element.number!='-'):
				number_list.append (element.number)
			if (hasattr (element, 'gender')==True) and (element.gender!='-'):
				gender.append (element.gender)
	if len(next_list)!=0:
		for element in next_list:
			if (hasattr (element, 'number')==True) and (element.number!='-'):
				number_list.append (element.number)
			if (hasattr (element, 'gender')==True) and (element.gender!='-'):
				gender.append (element.gender)
	s=0 #Counter for singular
	p=0 #Counter for plural
	f=0 #Counter for feminine
	m=0 #Counter for masculine
	for element in gender:
		if element=='f':
			f += 1
		else:
			m += 1
	if m>=f:
		gender='m'
		if ((word.text_form) [0])=='т':
			return {'index': number_in_list, 'pronoun': word, 'number': 's', 'gender': gender, 'honorific': False} #Index of pronoun, pronoun, number, gender, is honorific
	else:
		gender='f'
		if ((word.text_form) [0])=='т':
			return {'index': number_in_list, 'pronoun': word, 'number': 's', 'gender': gender, 'honorific': False}
	for element in number_list:
		if element=='s':
			s += 1
		else:
			p += 1
	if s>=p:
		return {'index': number_in_list, 'pronoun': word, 'number': 's', 'gender': gender, 'honorific': True}
	else:
		return {'index': number_in_list, 'pronoun': word, 'number': 'p', 'gender': gender, 'honorific': False}