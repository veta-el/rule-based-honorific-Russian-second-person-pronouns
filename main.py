import text_processing
import pos_classes

def main (phrase: str):
	normalized_words = text_processing.normalize (phrase)
	for w in range (1, len(normalized_words)):
		normalized_words [w]=text_processing.part_of_speech (normalized_words [w], normalized_words [w-1])
		normalized_words [w].role=text_processing.role_in_sentence (normalized_words [w])

		if normalized_words [w].role=='object': #Type of object role
			if w>=3:
				for j in range (w-1, w-4, -1):
					if normalized_words [j].role=='indirect_object':
						normalized_words [w].role='indirect_object'
						break
					if normalized_words [j].role=='circum_prich':
						normalized_words [w].role='circum_prich'
						break
					if normalized_words [j].role=='circum_zel':
						normalized_words [w].role='circum_zel'
						break
					else:
						normalized_words [w].role='direct_object'
			else:
				normalized_words [w].role='direct_object'
		if (type(normalized_words [w])==pos_classes.punctuation) and (w!=0): #Finding references - appeals
			appeals=[]
			checker = w-1
			while True:
				if checker == -1:
					break
				if (normalized_words [checker].text_form==',') or (normalized_words [checker].text_form=='.'):
					break
				else:
					appeals.append (checker)
					checker -= 1
			checker = 0
			number_of_objects = 0
			current_object = 0
			for number in appeals:
				if normalized_words [number].role=='definition':
					checker = 1
				if (type(normalized_words [number])==pos_classes.noun) or (type(normalized_words [number])==pos_classes.pronoun):
					number_of_objects += 1
					current_object = number
					checker = 1
				else:
					checker = 0
					break
			if (checker == 1) and (number_of_objects == 1):
				normalized_words [current_object].role='appeal'
		
	normalized_words.pop (0) #Space for searching references for pronouns
	pronouns_result = []
	normalized_words.insert (0, pos_classes.punctuation ('.'))
	normalized_words.insert (0, pos_classes.punctuation ('.'))
	normalized_words.append (pos_classes.punctuation ('.'))
	normalized_words.append (pos_classes.punctuation ('.'))

	for i in range (2, (len(normalized_words)-2)):
		if (type (normalized_words [i])==pos_classes.pronoun) and (normalized_words [i].person=='2'):
			two_lists = text_processing.elements_to_check (normalized_words, i)
			before = two_lists [0]
			after = two_lists [1]
			pronouns_result.append (text_processing.result_func (before, normalized_words [i], after, i-2)) #Get dict with Index of pronoun, pronoun, number, gender, is honorific
	return pronouns_result

if __name__ == '__main__':
	text = 'Вы его друг.'
	result = main (text)
	print (result)