from Manager_Producer import Manager
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

manager = Manager()

if __name__ == '__main__':
    manager.publish_the_jsons()