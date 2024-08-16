import os
from src.scrapper import Scrapper
from src.filter import Filter

def main():
    # Scrapper().run()

    files: list[str] = os.listdir(path="output/raw")
    for file in files:
        Filter(file_path=f"output/raw/{file}").run()
        break

if __name__ == '__main__':
    main()