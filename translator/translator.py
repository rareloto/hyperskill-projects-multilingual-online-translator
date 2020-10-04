from bs4 import BeautifulSoup
import requests


class Translator:
	def __init__(self):
		self.languages = (
			'Arabic', 'German', 'English', 'Spanish', 'French',
			'Hebrew', 'Japanese', 'Dutch', 'Polish', 'Portuguese',
			'Romanian', 'Russian', 'Turkish'
		)
		self.lang_src, self.lang_tgt = '', ()
		self.word = ''
		self.response = ''
		self.translations = ()
		self.examples_src, self.examples_tgt = (), ()
		self.examples_paired = (())
		self.url = 'https://context.reverso.net/translation'
		self.output_file = ''

	def main(self):
		# Print welcome message
		print("Hello! I am Tan the Translator. I currently support:")
		for i, lang in enumerate(self.languages):
			print(f'{i+1}. {self.languages[i]}')
			
		option_lang_src = input('Select language to translate from:\n> ')
		self.lang_src = self.languages[int(option_lang_src)-1]
		option_lang_tgt = input("Select language to translate to ('0' for all languages):\n> ")
		self.lang_tgt = [self.languages[int(option_lang_tgt)-1]] if option_lang_tgt != '0' \
			else [lang for lang in self.languages if lang not in [self.lang_src]]
		self.word = input('Type the word you want to translate:\n> ')
		
		self.request_translation()
		self.display_results()
			
	def request_translation(self):
		self.output_file = open(self.word + '.txt', 'w+')

		for lang in self.lang_tgt:
			url = self.url + f'/{self.lang_src.lower()}-{lang.lower()}/{self.word}'
			self.response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
			# print('200 OK' if self.response else f'{self.response.status_code} NOT OK')

			if self.response:
				soup = BeautifulSoup(self.response.content, 'html.parser')
				self.translations = (transl.get_text(strip=True) for transl
									 in soup.select('#translations-content > .translation')[:5])
				self.examples_src = (example.get_text(strip=True) for example
									 in soup.select('#examples-content > .example > .src')[:5])
				self.examples_tgt = (example.get_text(strip=True) for example
									 in soup.select('#examples-content > .example > .trg')[:5])
				self.examples_paired = ((src, tgt) for src, tgt in zip(self.examples_src, self.examples_tgt))
			
			self.print_to_file(lang)
			
	def print_to_file(self, lang):
		self.output_file.write(f'{lang} Translations\n\n')
		self.output_file.writelines('\n'.join(self.translations))
		self.output_file.write(f'\n\n{lang} Examples\n\n')
		self.output_file.write('\n\n'.join((f'{src}\n{tgt}' for (src, tgt) in self.examples_paired)))
		self.output_file.write('\n\n\n')
			
	def display_results(self):
		self.output_file.seek(0)
		print('\n' + self.output_file.read())
		self.output_file.close()


if __name__ == '__main__':
	translator = Translator()
	translator.main()
