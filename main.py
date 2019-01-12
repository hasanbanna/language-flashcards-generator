from language_flashcards import *
import csv
# Get target language
source_langauge = 'en'
# Get source language
target_language = 'fr-FR'

# add file error handling

csv_file = ''

try:
    with open('input.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for target_language_sentence in csv_reader:
            target_language_sentence = target_language_sentence[0]

            # Get part of speech from the sentences to be used for clozed deletion
            clozed_word_dict = get_relevant_pos_data_from_text(
                target_language_sentence)
            # Get named entities from the sentence
            clozed_word_dict['context_images'] = name_entities_from_sentence(
                target_language_sentence)
            # for each entity generate a contextual image
            print("---downloading image files---\n")
            generate_context_images(clozed_word_dict['context_images'])
            for i in range(len(clozed_word_dict['context_images'])):
                clozed_word_dict['context_images'][i] = "<img src='{}.png'>".format(
                    clozed_word_dict['context_images'][i])
                #  generate an audio for the sentence for each clozed word
                print("---downloading audio files---\n")

                clozed_word_dict['sentence_audio'] = []
                clozed_word_dict['sentence_audio'].append(
                    '[sound:{}.mp3]'.format(trim_sentence(target_language_sentence, 20)))
                generate_speech_from_text(
                    'fr-FR', 0.8, target_language_sentence)

                clozed_word_dict['word_audio'] = []
                for word in get_words(clozed_word_dict['part_of_speech']):
                    clozed_word_dict['word_audio'].append(
                        '[sound:{}.mp3]'.format(word))
                    generate_speech_from_text('fr-FR', 0.8, word)

                print('---downloading audio files complete---\n')

                word_audio_count = 0
                for part_of_speech in clozed_word_dict['part_of_speech']:
                    csv_row = ''
                    # Clozed Sentence
                    csv_row += generate_cloze_deletion(target_language_sentence,
                                                       part_of_speech['word'])
                    # English Translation
                    # translate the text into source langauge - i.e French -> English
                    csv_row += ', {}'.format(translate_text(
                        part_of_speech['word'].lower(), source_langauge))
                    # Part of Speech
                    csv_row += ', {} - {}'.format(
                        part_of_speech['tag'], part_of_speech['gender'])
                    # Word audio file name
                    csv_row += ', {}'.format(
                        clozed_word_dict['word_audio'][word_audio_count])
                    word_audio_count = word_audio_count + 1
                    # Sentence audio file name
                    csv_row += ', {}'.format(
                        clozed_word_dict['sentence_audio'][0])
                    csv_row += ', {}'.format(' '.join(map(str,
                                                          clozed_word_dict['context_images'])))
                    csv_file += csv_row + '\n'
except IOError:
    print("Error: input.csv file does not appear to exist.")

# create output.csv
print(csv_file)

