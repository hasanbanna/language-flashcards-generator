from language_flashcards import *

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
print("---downloading image files---\n")
generate_context_images(clozed_word_dict['context_images'])
for i in range(len(clozed_word_dict['context_images'])):
  clozed_word_dict['context_images'][i] = "<src href='{}.png'>".format(clozed_word_dict['context_images'][i])
#  generate an audio for the sentence for each clozed word
print("---downloading audio files---\n")
clozed_word_dict['sentence_audio'] = []
clozed_word_dict['sentence_audio'].append('[sound:{}.mp3]'.format(trim_sentence(target_language_sentence, 20)))
generate_speech_from_text('fr-FR', 0.8, target_language_sentence)

clozed_word_dict['word_audio'] = []
for word in get_words(clozed_word_dict['part_of_speech']):
  clozed_word_dict['word_audio'].append('[sound:{}.mp3]'.format(word))
  generate_speech_from_text('fr-FR', 0.8, word)
print('---downloading audio files complete---\n')
for part_of_speech in clozed_word_dict['part_of_speech']:
  # Clozed Sentence
  generate_cloze_deletion(target_language_sentence, part_of_speech['word']))
  # English Translation
  # translate the text into source langauge - i.e French -> English
  print('english: {}'.format(translate_text(part_of_speech['word'], source_langauge)))
  # Part of Speech
  print('{} - {}'.format(part_of_speech['tag'], part_of_speech['gender']))

print(clozed_word_dict)