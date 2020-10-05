from bs4 import BeautifulSoup
import requests
import sys


class Translator:
	def __init__(self):
		self.languages = (
			'Arabic', 'German', 'English', 'Spanish', 'French',
			'Hebrew', 'Japanese', 'Dutch', 'Polish', 'Portuguese',
			'Romanian', 'Russian', 'Turkish'
		)
		args = tuple(arg.title() for arg in sys.argv)
		self.lang_src = args[1] if len(args) > 2 else ''
		self.lang_tgt = tuple(args[2:-1]) if len(args) > 2 else ()
		if len(args) > 2 and (args[2] == 'All' or len(args) == 3):
			self.lang_tgt = tuple(lang for lang in self.languages if lang not in (self.lang_src))
		self.word = args[-1] if len(args) > 2 else ''
		self.response = ''
		self.translations = ()
		self.examples_src, self.examples_tgt = (), ()
		self.examples_paired = (())
		self.url = 'https://context.reverso.net/translation'
		self.output_file = ''

	def main(self):
		if len(sys.argv) == 1:
			self.welcome_message()
		self.request_translation()
		self.display_results()
		
	def welcome_message(self):
		print("Hello! I am Tan the Translator. I currently support:")
		for i, lang in enumerate(self.languages):
			print(f'{i+1}. {self.languages[i]}')
			
		option_lang_src = input('Select language to translate from:\n> ')
		self.lang_src = self.languages[int(option_lang_src)-1]
		option_lang_tgt = input("Select language to translate to ('0' for all languages):\n> ")
		self.lang_tgt = (self.languages[int(option_lang_tgt)-1],) if option_lang_tgt != '0' \
			else (lang for lang in self.languages if lang not in (self.lang_src))
		self.word = input('Type the word you want to translate:\n> ')
			
	def request_translation(self):
		self.output_file = open(self.word.lower() + '.txt', 'w+')

		for lang in self.lang_tgt:
			url = self.url + f'/{self.lang_src.lower()}-{lang.lower()}/{self.word.lower()}'
			self.response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

			if self.response:
				soup = BeautifulSoup(self.response.content, 'html.parser')
				self.translations = tuple(transl.get_text(strip=True) for transl
									 in soup.select('#translations-content > .translation')[:5])
				self.examples_src = tuple(example.get_text(strip=True) for example
									 in soup.select('#examples-content > .example > .src')[:5])
				self.examples_tgt = tuple(example.get_text(strip=True) for example
									 in soup.select('#examples-content > .example > .trg')[:5])
				self.examples_paired = tuple((src, tgt) for src, tgt in zip(self.examples_src, self.examples_tgt))

			self.print_to_file(lang)
			
	def print_to_file(self, lang):
		self.output_file.write(f'{lang} Translations\n\n')
		self.output_file.writelines('\n'.join(self.translations))
		self.output_file.write(f'\n\n{lang} Examples\n\n')
		self.output_file.write('\n\n'.join(tuple(f'{src}\n{tgt}' for (src, tgt) in self.examples_paired)))
		self.output_file.write('\n\n\n')
			
	def display_results(self):
		self.output_file.seek(0)
		print('\n' + self.output_file.read())
		self.output_file.close()


if __name__ == '__main__':
	translator = Translator()
	translator.main()
