# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.cloud import texttospeech
from google.cloud import translate

import six
import argparse
from google_images_download import google_images_download

response = google_images_download.googleimagesdownload()

# parser = argparse.ArgumentParser()
# parser.add_argument('-text', "--text", help="input text")
# parser.add_argument("-tlang", "--target_language", help="target language")
# args = parser.parse_args()

# target_language = args.target_language
text = "Je trouve leur maison très belle, mais ils ne sont pas contents et ils cherchent une autre maison à la campagne, avec des chambres individuelles pour les enfants"

"""
For each word create a text to speech pronunciation along with the pronunciation of the sentence aswell as an extra.
"""
def generate_cloze_sentences(sentence, clozed_words):
    cloze_sentences = []
    for word in sentence.split(" "):
        if(word in clozed_words):
            cloze_sentences.append(sentence.replace(word,"{{c1::%s}}"%(word)))
    return cloze_sentences

def get_relevant_pos_from_text(text):
    """Detects syntax in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects syntax in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    tokens = client.analyze_syntax(document).tokens

    # part-of-speech tags from enums.PartOfSpeech.Tag
    pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
               'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')
    relevant_tags = ('ADJ', 'ADV', 'NOUN', 'VERB')

    gender = ('N/A', 'FEMININE','MASCULINE', 'NEUTER')

    relevant_content = []
    for token in tokens:
        if pos_tag[token.part_of_speech.tag] in relevant_tags:
            if(token.part_of_speech.proper == 1): # if proper noun(1) then skip
                continue
            if(token.text.content not in relevant_content):
                relevant_content.append(token.text.content)
            # print (gender[token.part_of_speech.gender], token.text.content)
    return relevant_content

def name_entities_from_text(text):
    """Detects entities in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

    entities_names = []
    for entity in entities:
        if(entity.name not in entities_names):
            entities_names.append(entity.name)
    return entities_names



# fr-FR
def generate_speech_from_text(langauge_code, speaking_rate, filename):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3,
        speaking_rate=speaking_rate)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    with open('audio/'+filename+'.mp3', 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

# print(name_entities_from_text(text))

clozed_words = get_relevant_pos_from_text(text)
# arguments = {"keywords": ','.join(clozed_words), "limit":1, "format":'png'}
# paths = response.download(arguments)
# print(paths)
clozed_sentences = generate_cloze_sentences(text, clozed_words)
# print(clozed_sentences)
for cs in clozed_sentences:
    print(cs)

def translate_text(text, target_language):
    # Instantiates a client
    translate_client = translate.Client()
    target = target_language
    translation = translate_client.translate(text, target_language=target)
    return translation['translatedText']
print(translate_text(text, 'en'));