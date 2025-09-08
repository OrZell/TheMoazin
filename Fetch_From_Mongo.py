from DALs.MongoDB_DAL import MongoDB_DAL
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
import speech_recognition as sr

r = sr.Recognizer()

class Fetcher:

    def __init__(self):
        self.MongoDAL = MongoDB_DAL()

    def fetch_the_podcat_by(self, id) -> gridfs.synchronous.grid_file.GridOut:
        fs = self.MongoDAL.get_fs()
        fi = fs.find_one({'file_id': id})
        return fi
        # af = sr.AudioFile(fi)
        # with af as file:
        #     data = r.record(file)
        #     MyText = r.recognize_google(data)
        #     # MyText = MyText.lower()
        #     print(MyText)



f = Fetcher()
print(type(f.fetch_the_podcat_by('d748e16d75e8e067922c259f36f0950f')))