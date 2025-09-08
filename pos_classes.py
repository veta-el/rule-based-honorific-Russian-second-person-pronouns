import pandas as pd

#Morpheme classes
class root:
	def __init__ (self, text_form):
		self.text_form=text_form

class prefix:
	def __init__ (self, text_form):
		self.text_form=text_form

class suffix:
	def __init__ (self, text_form, part_of_speech, type_character, character):
		self.text_form=text_form
		self.part_of_speech=part_of_speech
		self.type_character=type_character
		self.character=character

class ending:
	def __init__ (self, text_form, part_of_speech, type_character, character):
		self.text_form=text_form
		self.part_of_speech=part_of_speech
		self.type_character=type_character
		self.character=character

#Part of speech/token classes
class punctuation:
	def __init__ (self, text_form):
		self.text_form=text_form
		self.role='punctuation'
		self.root=text_form

class noun:
	def __init__ (self, text_form, name, living, gender, declension, number, case, suffix, prefix, ending, root, role):
		self.text_form=text_form
		self.name=name
		self.living=living
		self.gender=gender
		self.declension=declension
		self.number=number
		self.case=case
		self.suffix=suffix
		self.prefix=prefix
		self.ending=ending
		self.root=root
		self.role=role

class adjective:
	def __init__ (self, text_form, adj_type, degree, form, gender, number, case, suffix, prefix, ending, root, role):
		self.text_form=text_form
		self.adj_type=adj_type
		self.degree=degree
		self.form=form
		self.gender=gender
		self.number=number
		self.case=case
		self.suffix=suffix
		self.prefix=prefix
		self.ending=ending
		self.root=root
		self.role=role

class numeral:
	def __init__ (self, text_form, num_type, gender, number, case, suffix, prefix, ending, root, role):
		self.text_form=text_form
		self.num_type=num_type
		self.gender=gender
		self.number=number
		self.case=case
		self.suffix=suffix
		self.prefix=prefix
		self.ending=ending
		self.root=root
		self.role='-'

class pronoun:
	def __init__ (self, text_form, pronoun_type, person, case, number, gender, suffix, prefix, ending, root, role):
		self.text_form=text_form
		self.pronoun_type=pronoun_type
		self.person=person
		self.gender=gender
		self.number=number
		self.case=case
		self.suffix=suffix
		self.prefix=prefix
		self.ending=ending
		self.root=root
		self.role='-'

class verb:
	def __init__ (self, text_form, verb_type, transitivity, reflex, declension, inclination, person, gender, number, tense, suffix, prefix, ending, root, role):
		self.text_form=text_form
		self.verb_type=verb_type
		self.transitivity=transitivity
		self.reflex=reflex
		self.declension=declension
		self.inclination=inclination
		self.person=person
		self.gender=gender
		self.number=number
		self.tense=tense
		self.suffix=suffix
		self.prefix=prefix
		self.ending=ending
		self.root=root
		self.role=role

class adverb:
	def __init__ (self, text_form, degree, suffix, prefix, root, role):
		self.text_form=text_form
		self.degree=degree
		self.suffix=suffix
		self.prefix=prefix
		self.root=root
		self.role=role

class participle:
	def __init__ (self, text_form, passive, reflex, particip_type, tense, form, degree, gender, number, case, suffix, prefix, ending, root, role):
		self.text_form=text_form
		self.passive=passive
		self.reflex=reflex
		self.particip_type=particip_type
		self.tense=tense
		self.form=form
		self.degree=degree
		self.gender=gender
		self.number=number
		self.case=case
		self.suffix=suffix
		self.prefix=prefix
		self.ending=ending
		self.root=root
		self.role=role

class participle_d:
	def __init__ (self, text_form, particip_d_type, transitivity, reflex, suffix, prefix, root, role):
		self.text_form=text_form
		self.particip_d_type=particip_d_type
		self.transitivity=transitivity
		self.reflex=reflex
		self.suffix=suffix
		self.prefix=prefix
		self.root=root
		self.role=role

class preposition:
	def __init__ (self, text_form, role):
		self.text_form=text_form
		self.role='-'
		self.root=text_form

class conjunction:
	def __init__ (self, text_form, conj_type, role):
		self.text_form=text_form
		self.conj_type=conj_type
		self.role='-'
		self.root=text_form

class particle:
	def __init__ (self, text_form, role):
		self.text_form=text_form
		self.role='-'
		self.root=text_form

class interjection:
	def __init__ (self, text_form, role):
		self.text_form=text_form
		self.role='-'
		self.root=text_form

class filler:
	def __init__ (self, text_form, role):
		self.text_form=text_form
		self.role='-'
		self.root=text_form

class bigram:
	def __init__ (self, first_to_compare, second_to_compare, procent):
		self.first_to_compare=first_to_compare
		self.second_to_compare=second_to_compare
		self.procent=procent

CLASS_OBJECTS_PATH = 'class_objects/'

def collect_pos_objects (class_name):
	#Read data file
	try:
		data = pd.read_csv (CLASS_OBJECTS_PATH+class_name+'.csv')
	except FileNotFoundError:
		print ('No such file')
		return False

	#Create objects
	class_dict = globals()[class_name]
	list_attributes = list(data.columns)
	objects = {}

	for obj_id in range (0, data.shape [0]):
		attributes = []
		for attr in list_attributes:
			attributes.append (data.at [obj_id, attr])
		try:
			obj = class_dict(*attributes)
		except TypeError:
			attributes.append ('-')
			obj = class_dict(*attributes)
		try:
			objects [obj.text_form] = obj
		except AttributeError:
			objects [class_name+str(obj_id)] = obj

	return objects #Return a dict of objects