from language_flashcards import *

# Assumptions
# Each word is unique
# Each word is processed in order

print ('{}\t\t\t{}'.format('front', 'back'))
print ('{}\t\t\t{}'.format('Je ... leur maison', 'trouve "context_image" "word_audio" "sentence_audio" '))

# Get target language
source_langauge = 'en'
# Get source language
target_language = 'fr-FR'

target_language_sentence = "Je trouve leur maison très belle, mais ils ne sont pas contents et ils cherchent une autre maison à la campagne, avec des chambres individuelles pour les enfants"

# translate the text into source langauge - i.e French -> English
translated_into_source_text = translate_text(target_language_sentence, source_langauge)

# Get part of speech from the sentences to be used for clozed deletion
clozed_words_from_pos_data = get_relevant_pos_data_from_text(target_language_sentence)

# Create clozed sentences with the target language text
clozed_sentences = generate_cloze_deletion(target_language_sentence, clozed_words)

# Get named entities from the sentence
named_entities = name_entities_from_sentence(target_language_sentence)

# for each entity generate a contextual image
print("---Generating image files---")
named_entities_images = generate_images(named_entities)

#  generate an audio for the sentence for each clozed word
print("---Generating audio files---")
generate_speech_from_text('fr-FR', 0.8, target_language_sentence, target_language_sentence)
for word in get_words(clozed_words):
  generate_speech_from_text('fr-FR', 0.8, word, word)

# Clozed Sentence	Context Image Word Audio Sentence Audio English Translation Part of Speech