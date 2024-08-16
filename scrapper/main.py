import os
from src.scrapper import Scrapper
from src.filter import Filter
from src.compile import Compile

def main():
    # Scrapper().run()

    files: list[str] = os.listdir(path="output/raw")
    for file in files:
        Filter(file_path=f"output/raw/{file}").run()

    Compile().run()

if __name__ == '__main__':
    main()