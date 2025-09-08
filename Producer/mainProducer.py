from Manager_Producer import Manager
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv()) # load the env vars using the dotenv library

manager = Manager() # create instance of Manager_Producer

if __name__ == '__main__':
    manager.publish_the_jsons() # run the main method