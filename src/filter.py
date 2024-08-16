from typing import Any
from re import Pattern
import re
import json

key: dict[int, str] = {0: "name", 1: "text"}

class Filter():
    def __init__(self, file_path) -> None:
        self.file_path: Any = file_path
        self.filtered_cards: dict = []
        self.card_type: str = ""

    def run(self) -> None:
        """Run the filter
        1. Filter the cards
        """
        self.__set_patterns()
        self.__filter_cards()

    def __set_patterns(self) -> None:
        name = r"(?:^)(.*?)(?= ›)"
        text = r"(?:› )(.*?)(?=$)"

        if "pokemon" in self.file_path:
            name = r"(?:^)(.*?)(?= ·)"
            text = r"(?:· )(.*?)(?=$)"
            self.card_type = "Pokemon"

        elif "trainer" in self.file_path:
            self.card_type = "Trainer"

        elif "energy" in self.file_path:
            self.card_type = "Energy"

        self.pattern: list[Pattern[str]] = [name, text]

    def __find_information(self, card: str) -> dict:
        
        card_information: dict = {}
        for index, pattern in enumerate(iterable=self.pattern):
            match: re.Match[str] | None = re.findall(pattern=pattern, string=card)
            if match:
                card_information[key[index]] = match[0]

        card_information["type"] = self.card_type
        return card_information
    
    def __filter_cards(self) -> None:
        with open(file=self.file_path, mode="r", encoding="utf-8") as file:
            cards: list[str] = file.readlines()
            for card in cards:
                card_information: dict = self.__find_information(card=card)
                if card_information:
                    self.filtered_cards.append(card_information)  
                 
        self.__save_filtered_cards()

    def __save_filtered_cards(self) -> None:
        with open(file=f"output/filtered/filtered_cards_{self.card_type}.json", mode="w", encoding="utf-8") as file:
            json.dump(obj=self.filtered_cards, fp=file, indent=4, ensure_ascii=False)
