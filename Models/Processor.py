from nltk.corpus import stopwords
import base64
import nltk
import os


class Processor:

    def __init__(self):
        self.HostileWordsEncoded = os.getenv('HOSTILE_WORDS_ENCODED') # holds the base64 encoded hostile words
        self.LessHostileWordsEncoded = os.getenv('LESS_HOSTILE_WORDS_ENCODED') # holds the base64 encoded less hostile words

        self.HostileWordsDecodedAsList = None
        self.LessHostileWordsDecodedAsList = None
        self.StopWords = None

        self.PowerOfHostile = 2 # meaning the strongness of found one word of those
        self.PowerOfLessHostile = 1 # meaning the strongness of found one word of those
        self.PrecentsToIndictMessage = 0.15 # what precents of 'bds' text suppose to hold to be indicted
        self.PrecentToSetMiddleMessage = 0.25 # what precents 'bds' text suppose to hold to be middle
                                              # none <= self.PrecentsToIndictMessage
                                              # self.PrecentsToIndictMessage < middle <= self.PrecentToSetMiddleMessage
                                              # high > self.PrecentToSetMiddleMessage

    # thr main method of the class
    def run(self):
        self.decode_the_hostile_words() # load the decoded text the init vars
        self.assign_stopwords() # load the stopwords to the init var

    # decode and assign the encoded words
    def decode_the_hostile_words(self):
        self.HostileWordsDecodedAsList = self.base64_decoder(self.HostileWordsEncoded).lower().split(',')
        self.LessHostileWordsDecodedAsList = self.base64_decoder(self.LessHostileWordsEncoded).lower().split(',')

    # load the stopwords
    def assign_stopwords(self):
        if self.StopWords is None:
            nltk.download('stopwords', quiet=True)
            self.StopWords = set(stopwords.words('english'))

    # got text and return text without stopwords as list
    def remove_stop_words_from_text(self, text:str) -> list:
        text = text.split()
        return [word for word in text if word not in self.StopWords]

    # count shows of the hostile words in text
    def count_power_of_hostile_words_in_text(self, text:str):
        counter = 0
        for word in self.HostileWordsDecodedAsList:
            shows_in_text = text.count(word)
            counter += shows_in_text * self.PowerOfHostile

        for word in self.LessHostileWordsDecodedAsList:
            shows_in_text = text.count(word)
            counter += shows_in_text * self.PowerOfLessHostile

        return counter

    # calculate the shows divide the length of the text without stopwords
    @staticmethod
    def count_precents_of_bds(counts, clean_text):
        return float(format(counts/len(clean_text), '.2f'))

    # return true or false if the text indicted
    def indicted_text_by_precents(self, precents):
        if precents <= self.PrecentsToIndictMessage:
            return False
        return True

    # return three levels of dangerous based on the precents
    def threaded_text_by_precents(self, precents):
        if precents <= self.PrecentsToIndictMessage:
            return 'none'
        elif precents <= self.PrecentToSetMiddleMessage:
            return 'middle'
        else:
            return 'high'

    # decode base64 encoded items
    @staticmethod
    def base64_decoder(base64_encoded):
        base64_bytes = base64_encoded.encode("ascii")
        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")
        return sample_string
