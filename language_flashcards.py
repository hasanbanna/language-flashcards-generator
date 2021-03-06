# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.cloud import texttospeech
# from google.cloud import translate

# import six
# Might use argparse to create command line tool
# target_language = args.target_language

def generate_cloze_deletion(sentence, word):
    return sentence.replace(word,"{{c1::%s}}"%(word), 1)

def get_relevant_pos_data_from_text(text):
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

    relevant_content = {'part_of_speech': []}
    for token in tokens:
        pos_data = {}
        if pos_tag[token.part_of_speech.tag] in relevant_tags:
            if(token.part_of_speech.proper == 1): # if proper noun(1) then skip
                continue
            if(token.text.content not in relevant_content):
                pos_data['gender'] = gender[token.part_of_speech.gender]
                pos_data['tag'] = pos_tag[token.part_of_speech.tag]
                pos_data['word'] = token.text.content
                relevant_content['part_of_speech'].append(pos_data)
    return relevant_content

def name_entities_from_sentence(text):
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
def generate_speech_from_text(lang, speaking_rate, txt):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=txt)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code=lang,
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3,
        speaking_rate=speaking_rate)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    if(len(txt) >= 10):
        txt = trim_sentence(txt, 10)
    with open('{}.mp3'.format(txt), 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)

def get_words(words_dict):
    words = []
    for pos_data in words_dict:
        words.append(pos_data['word'])
    return words

def translate_text(text, target_language):
    # Instantiates a client
    translate_client = translate.Client()
    target = target_language
    translation = translate_client.translate(text, target_language=target)
    return translation['translatedText']

def generate_context_images(context_words):
    from google_images_download import google_images_download
    response = google_images_download.googleimagesdownload()
    arguments = {
        "keywords":','.join(context_words),
        "limit":1,
        "format": "png",
        "size": "medium",
        "no_numbering": True,
        "type": "photo",
        "no_directory": True}
    response.download(arguments)   #passing the arguments to the function
    print ('---downloading images complete---')

# Translate the target language to source language
def translate_text(text, target_language):
    # Instantiates a client
    translate_client = translate.Client()
    target = target_language
    translation = translate_client.translate(text, target_language=target)
    return translation['translatedText']

def trim_sentence(sentence, length):
    return (sentence.replace(' ', '-')[:length] + '..._sent').lower()
