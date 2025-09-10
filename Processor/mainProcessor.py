from dotenv import load_dotenv, find_dotenv
from Manager_Processor import Manager

load_dotenv(find_dotenv()) # load the env vars using the dotenv library

manager = Manager() # create instance of Manager_STT

if __name__ == '__main__':
    manager.run() # run the main method

