from dotenv import load_dotenv, find_dotenv
from Manager_Consumer import Manager

load_dotenv(find_dotenv())

manager = Manager()

if __name__ == '__main__':
    manager.run()