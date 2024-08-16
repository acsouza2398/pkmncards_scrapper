from typing import Any
from re import Pattern
import re
import json

key: dict[int, str] = {0: "name", 1: "type", 2: "text", 3: "set_origin", 4: "set_origin", 5: "set_number"}

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
        if "pokemon" in self.file_path:
            self.pattern = re.compile(pattern=r"pokemon")
            self.card_type = "pokemon"
        elif "trainer" in self.file_path:
            self.pattern = re.compile(pattern=r"trainer")
            self.card_type = "trainer"
        elif "energy" in self.file_path:
            self.pattern = re.compile(pattern=r"energy")
            name = r"(?:^)(.*?)(?=›)"
            type = r"(?:›) (\w* \w*)(?=)"
            text = r"(?:› \w* \w* )(.*?)(?=  .* ›)"
            set_origin_basic = r"(?:Basic Energy )(.*?)(?= ›)"
            set_origin_special = r"(?:  )(.*?)(?= ›)"
            set_number = r"(?:› #)(.*?)(?=$)"
            self.pattern: list[Pattern[str]] = [re.compile(pattern=name), re.compile(pattern=type), re.compile(pattern=text), re.compile(pattern=set_origin_basic), re.compile(pattern=set_origin_special), re.compile(pattern=set_number)]
            self.card_type = "energy"

    def __find_information(self, card: str) -> dict:
        
        card_information: dict = {}
        for index, pattern in enumerate(iterable=self.pattern):
            match: re.Match[str] | None = re.findall(pattern=pattern, string=card)
            if match:
                card_information[key[index]] = match[0]
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
