from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os
import base64


import nltk
from nltk.corpus import stopwords



class Processor:

    def __init__(self):
        self.HostileWordsEncoded = os.getenv('HOSTILE_WORDS_ENCODED')
        self.LessHostileWordsEncoded = os.getenv('LESS_HOSTILE_WORDS_ENCODED')

        self.HostileWordsDecodedAsList = None
        self.LessHostileWordsDecodedAsList = None

        self.PowerOfHostile = 2
        self.PowerOfLessHostile = 1

        self.StopWords = None


    def assign_stopwords(self):
        if self.StopWords is None:
            nltk.download('stopwords', quiet=True)
            self.StopWords = set(stopwords.words('english'))

    def remove_stop_words_from_text(self, text:str) -> list:
        text = text.split()
        return [word for word in text if word not in self.StopWords]

    @staticmethod
    def count_precents_of_bds(counts, clean_text):
        return float(format(counts/len(clean_text), '2f'))

    @staticmethod
    def indicted_text_by_precents(precents):
        if precents <= 0.25:
            return False
        return True

    def threaded_text_by_precents(self, precents):
        if precents <= 0.25:
            return 'none'
        elif precents <= 0.45:
            return 'middle'
        else:
            return 'high'

    def decoded_the_hostile_words(self):
        self.HostileWordsDecodedAsList = self.base64_decoder(self.HostileWordsEncoded).lower().split(',')
        self.LessHostileWordsDecodedAsList = self.base64_decoder(self.LessHostileWordsEncoded).lower().split(',')

    @staticmethod
    def base64_decoder(base64_encoded):
        base64_bytes = base64_encoded.encode("ascii")
        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")
        return sample_string

    def count_power_of_hostile_words_in_text(self, text:str):
        counter = 0
        for word in self.HostileWordsDecodedAsList:
            shows_in_text = text.count(word)
            counter += shows_in_text * self.PowerOfHostile

        for word in self.LessHostileWordsDecodedAsList:
            shows_in_text = text.count(word)
            counter += shows_in_text * self.PowerOfLessHostile

        return counter

# p = Processor()
# p.assign_stopwords()
#
#
# text= "the new cycle moves fast but gaza doesn't disappear when cameras do the blockade is still there and so is the humanitarian crisis exactly i read a report yesterday it said malnutrition is spreading among children that's a war crime in itself meanwhile refugees keep growing in number and displacement means whole communities are erased the protests worldwide are encouraging though from london to new york people chant for a ceasefire and free palestine and linking it back to bds it's about applying pressure where governments fail right liberation isn't easy but the people's resilience is inspiring resistance can be cultural political and global and podcasts like hours just small ripples but ripples matter"
#
# p.decoded_the_hostile_words()
# clean_text = p.remove_stop_words_from_text(text=text)
# counts = p.count_power_of_hostile_words_in_text(text=text)
#
# print(counts/ len(clean_text))
