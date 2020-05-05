TRANSLATE = '1'
NEW_WORD = '2'
DELETE_WORD = '3'
QUIT = '4'


def get_user_word() -> str:
	"""
	Asks for a word from user and return it
	:return: user input
	"""
	return input('word: ').strip()


def find_word(dictionary: dict, word: str) -> str:
	"""
	Finds a given word in a given dictionary, otherwise prints inductive message
	:param dictionary: dictionary to look for the word
	:param word: word to search in the dictionary
	:return: word translation if word exists, otherwise return None
	"""
	if word in dictionary:
		return dictionary[word]
	print(f"no records found for the word '{word}'")


def translate(dictionary: dict):
	"""
	Gets a word from the user and prints it's translation if exits
	:param dictionary: languages dictionary
	:return: None
	"""
	word = get_user_word()
	translation = find_word(dictionary, word)
	if translation:
		print(f"The translation of the word '{word}' is {translation}")


def new_word(dictionary):
	"""
	Gets a word from the user and it's translation and adds it to the given dictionary
	:param dictionary: languages dictionary
	:return:None
	"""
	word = get_user_word()
	if word in dictionary:
		if input(f"word '{word}' is already in dictionary with the translation '{dictionary[word]}'\n"
		      f"do you want to change translation? [y/n default is n] \n") != 'y':
			return
	tran = input('tran: ').strip()

	dictionary[word] = tran


def delete_word(dictionary):
	"""
	Gets a word from the user and removes it from the given dictionary
	:param dictionary: languages dictionary
	:return: None
	"""
	word = get_user_word()
	if find_word(dictionary, word):
		del dictionary[word]
		print(f"word '{word}' deleted successfully.")


def main():
	dictionary = {}
	user_choice_function = {
		TRANSLATE: translate,
		NEW_WORD: new_word,
		DELETE_WORD: delete_word
	}

	user_input = None
	while user_input != QUIT:
		if user_input in user_choice_function:
			user_choice_function[user_input](dictionary)

		user_input = input('What to do? (1. translate / 2. enter a new word / 3. delete a word / 4. quit)\n').strip()

	print('goodbye...')


if __name__ == '__main__':
	main()
