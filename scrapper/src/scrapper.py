import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import time
import json


class Scrapper():
    """Scrapper class to scrap the pokemon cards from pkmncards.com
    1. query: str -> The query to search for
    2. base_url: list[str] -> The base url to make a request
    3. cards: list -> The list of cards to store the cards
    4. run() -> Run the scrapper
    5. __make_request(url: str) -> Make a request to the url and return the soup object
    6. __save_cards() -> Save the cards to a file
    """
    def __init__(self) -> None:
        self.query: str = "/pokedex/bulbasaur"
        self.base_url: str = "https://pokemondb.net"
        self.pokemon = {}

    def run(self) -> None:
        """Run the scrapper
        1. Loop through the queries
        2. Set the query
        3. Run the scrapper
        """
        c = 0
        while self.query != None or c < 5:
            print(f"Scraping {self.query}")
            self.__scrap()      
            time.sleep(10)
            c += 1
            if c % 5 == 0:
                break

        self.__save_pokemon()  

    def __scrap(self) -> None:
        """Run the scrapper
        1. Make a request to the first page
        2. Get the last page number
        3. Loop through the pages and get the cards
        4. Save the cards to a file
        """
        url: str = self.base_url + self.query
        print(url)
        soup: BeautifulSoup = self.__make_request(url=url)
        descriptions = soup.find_all(name='td', class_='cell-med-text')
        descriptions = ' '.join([description.get_text() for description in descriptions])

        self.pokemon[self.query.replace("/pokedex/", "")] = descriptions

        self.query: str = self.__get_next(soup=soup)

    def __get_next(self, soup: BeautifulSoup) -> str:

        next_query: Tag = soup.find(name='a', class_='entity-nav-next')
        return next_query['href'] if next_query else None

    def __make_request(self, url: str) -> BeautifulSoup:
        """Make a request to the url and return the soup object
        1. url: str -> The url to make a request
        2. response: requests.Response -> The response object
        3. return: BeautifulSoup -> The soup object
        """
        response: requests.Response = requests.get(url=url)
        return BeautifulSoup(markup=response.content, features='html.parser')

    def __save_pokemon(self) -> None:
        """Save the pokemon to a file
        1. Open a file in write mode
        2. Loop through the cards and write the text to the file
        """
        with open(file=f'output/pkmn.json', mode='w', encoding="utf-8") as f:
            json.dump(self.pokemon, f, ensure_ascii=False, indent=4)