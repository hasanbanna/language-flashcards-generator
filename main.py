from language_flashcards import *

# Assumptions
# Each word is unique
# Each word is processed in order
# TODO: change source / taget language naming confusing
# TODO: google_images_download library should allow the image_name to be the same as the keyword

# Get target language
source_langauge = 'en'
# Get source language
target_language = 'fr-FR'

target_language_sentence = "Je trouve leur maison très belle, mais ils ne sont pas contents et ils cherchent une autre maison à la campagne, avec des chambres individuelles pour les enfants"

# Get part of speech from the sentences to be used for clozed deletion
clozed_word_dict = get_relevant_pos_data_from_text(target_language_sentence)

# Get named entities from the sentence
clozed_word_dict['context_images'] = name_entities_from_sentence(target_language_sentence)
# for each entity generate a contextual image
print("---downloading image files---")
generate_context_images(clozed_word_dict['context_images'])
#  generate an audio for the sentence for each clozed word
# print("---downloading audio files---")
# clozed_word_dict['sentence_audio'] = []
# clozed_word_dict['sentence_audio'].append('[sound:{}.mp3]'.format(trim_sentence(target_language_sentence, 20)))
# generate_speech_from_text('fr-FR', 0.8, target_language_sentence)

# clozed_word_dict['word_audio'] = []
# for word in get_words(clozed_word_dict['part_of_speech']):
#   clozed_word_dict['word_audio'].append('[sound:{}.mp3]'.format(word))
#   generate_speech_from_text('fr-FR', 0.8, word)
print('---downloading audio files complete---')
# # for cloze_word in clozed_word_dict:
#   # Clozed Sentence
#   # print(generate_cloze_deletion(target_language_sentence, cloze_word['word']))
#   # Context Image

#   # Word Audio
#   # Sentence Audio

#   # English Translation
#   # translate the text into source langauge - i.e French -> English
#   # print('english: {}'.format(translate_text(cloze_word['word'], source_langauge)))
#   # Part of Speech
#   # print('{} - {}'.format(cloze_word['tag'], cloze_word['gender']))

print(clozed_word_dict)