from dotenv import load_dotenv, find_dotenv
from Manager_Consumer import Manager

load_dotenv(find_dotenv()) # load the env vars using the dotenv library

manager = Manager() # create instance of Manager_Consumer

if __name__ == '__main__':
    manager.run() # run the main method