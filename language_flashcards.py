# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import six
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-tlang", "--target_language", help="target language")
args = parser.parse_args()

# print (args.target_langauge);


text = "Me voilà installée à Montpellier! J'habite avec une famille très gentille: Jacques et Marie Trapet et leurs enfants, Cecile et Juliette. Je trouve leur maison très belle, mais ils ne sont pas contents et ils cherchent une autre maison à la campagne, avec des chambres individuelles pour les enfants. Nous sommes très occupés ici."

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
            relevant_content.append(token.text.content)
            print (gender[token.part_of_speech.gender], token.text.content)
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

    for entity in entities:
        print('=' * 20)
        print(u'{:<16}: {}'.format('name', entity.name))
        print(u'{:<16}: {}'.format('type', entity_type[entity.type]))
        print(u'{:<16}: {}'.format('metadata', entity.metadata))
        print(u'{:<16}: {}'.format('salience', entity.salience))
        print(u'{:<16}: {}'.format('wikipedia_url',
              entity.metadata.get('wikipedia_url', '-')))

# 1. Input a sentence -> it must be a sentence
# 2. Analyze syntax so I can pick out words from a sentence
# 3. Get images related to the words
# 4. Get pronunciation for the words using text to speech
