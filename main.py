from language_flashcards import *

print ('{}\t\t\t{}'.format('front', 'back'))
print ('{}\t\t\t{}'.format('Je ... leur maison', 'trouve "context_image" "word_audio" "sentence_audio" '))


# Get target language
source_langauge = 'en'
# Get source language
target_language = 'fr-FR'

target_language_text = "Je trouve leur maison très belle, mais ils ne sont pas contents et ils cherchent une autre maison à la campagne, avec des chambres individuelles pour les enfants"

# translate the text into source langauge - i.e French -> English
translated_into_source_text = translate_text(target_language_text, source_langauge)

# Get part of speech from the sentences to be used for clozed deletion
clozed_words_from_pos_data = get_relevant_pos_data_from_text(text)
# Create clozed sentences with the target language text

