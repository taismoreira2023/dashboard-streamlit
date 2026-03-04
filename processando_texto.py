import nltk
from nltk import tokenize
import unidecode

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class text_process:

    def __init__(self):
        self.irrelevant_words = nltk.corpus.stopwords.words('portuguese')
        self.irrelevant_words = [word for word in self.irrelevant_words if word != 'não']


    def processingWhiteSpace(self,df,column):
        processed_sentence = []

        for text in df[column]:
            space_token = tokenize.WhitespaceTokenizer()
            text_token = space_token.tokenize(text)
            new_word = [word for word in text_token if word not in self.irrelevant_words]
            processed_sentence.append(' '.join(new_word))


        return processed_sentence
    

    def stopWordsUnidecode(self, df, column):

        df['processing_Unidecode'] = [unidecode.unidecode(phrase) for phrase in df[column]]
        stopWords_unidecode = [unidecode.unidecode(phrase) for phrase in self.irrelevant_words]
        
        processed_sentence = []

        for text in df['processing_Unidecode']:
            word_punct_tokenizer = tokenize.WordPunctTokenizer()
            text_token = word_punct_tokenizer.tokenize(text)
            new_word = [word for word in text_token if word.isalpha() and word not in stopWords_unidecode]
            processed_sentence.append(' '.join(new_word))

        return processed_sentence

