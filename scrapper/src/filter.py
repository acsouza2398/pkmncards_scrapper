from typing import Any
from re import Pattern
import re
import json

key: dict[int, str] = {0: "name", 1: "text"}
key_energy: dict[str, str] = {"{G}": "Grass", "{R}": "Fire", "{W}": "Water", "{L}": "Lightning", "{F}": "Fighting", "{P}": "Psychic", "{D}": "Darkness", "{M}": "Metal", "{C}": "Colorless", "{N}": "Dragon", "{Y}": "Fairy"}

class Filter():
    """Filter the cards
    1. Set the patterns
    2. Filter the cards
    3. Find the information
    4. Save the filtered cards
    """    
    def __init__(self, file_path) -> None:
        self.file_path: Any = file_path
        self.filtered_cards: dict = []
        self.card_type: str = ""

    def run(self) -> None:
        """Run the filter
        1. Set the patterns
        2. Filter the cards
        """
        self.__set_patterns()
        self.__filter_cards()

    def __replace_match(self, match) -> str:
        """
        Replace the match with the key_energy

        Args:
            match (str): The match to replace

        Returns:
            str: The replaced match
        """        
        matched_text: Any = match.group(0)
        return key_energy.get(matched_text, matched_text)

    def __set_patterns(self) -> None:
        """
        Set the patterns
        1. Set the name pattern
        2. Set the text pattern
        3. Set the card type
        4. Set the pattern
        """        
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
        """
        Find the information
        1. Loop through the patterns
        2. Find the match
        3. Set the card information
        4. Return the card information

        Args:
            card (str): The card to find the information

        Returns:
            dict: The card information extracted
        """        
        card_information: dict = {}
        for index, pattern in enumerate(iterable=self.pattern):
            match: re.Match[str] | None = re.findall(pattern=pattern, string=card)
            if match:
                card_information[key[index]] = re.sub(pattern=r"\{[GRWLFPDMNCY]\}", repl=self.__replace_match, string=match[0])

        card_information["type"] = self.card_type
        return card_information
    
    def __filter_cards(self) -> None:
        """Filter the cards
        1. Open the file
        2. Loop through the cards
        3. Find the information
        4. Save the filtered cards
        """
        with open(file=self.file_path, mode="r", encoding="utf-8") as file:
            cards: list[str] = file.readlines()
            for card in cards:
                card_information: dict = self.__find_information(card=card)
                if card_information:
                    self.filtered_cards.append(card_information)  
                 
        self.__save_filtered_cards()

    def __save_filtered_cards(self) -> None:
        """Save the filtered cards
        1. Save the filtered cards to a file
        """
        with open(file=f"output/filtered/filtered_cards_{self.card_type}.json", mode="w", encoding="utf-8") as file:
            json.dump(obj=self.filtered_cards, fp=file, indent=4, ensure_ascii=False)
