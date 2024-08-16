import requests
from bs4 import BeautifulSoup, NavigableString, Tag


class scrapper():
    """Scrapper class to scrap the pokemon cards from pkmncards.com
    1. query: str -> The query to search for
    2. base_url: list[str] -> The base url to make a request
    3. cards: list -> The list of cards to store the cards
    4. run() -> Run the scrapper
    5. __make_request(url: str) -> Make a request to the url and return the soup object
    6. __save_cards() -> Save the cards to a file
    """
    def __init__(self) -> None:
        self.query: str = ""
        self.queries: list[str] = ["pokemon", "trainer", "energy"]
        self.base_url: list[str] = ["https://pkmncards.com/?s=type%3A", "&sort=date&ord=auto&display=text"]
        self.cards: list = []

    def run(self) -> None:
        """Run the scrapper
        1. Loop through the queries
        2. Set the query
        3. Run the scrapper
        """
        for query in self.queries:
            print(f"Scraping {query} cards...")
            self.query = query
            self.__scrap()        

    def __scrap(self) -> None:
        """Run the scrapper
        1. Make a request to the first page
        2. Get the last page number
        3. Loop through the pages and get the cards
        4. Save the cards to a file
        """
        url: str = self.base_url[0] + self.query + self.base_url[1]
        soup: BeautifulSoup = self.__make_request(url=url)
        self.cards = soup.find_all(name='article', class_='type-pkmn_card entry')

        last_page_number: int = self.__get_page_number(soup=soup)

        if last_page_number > 1:
            self.__iterate_pages(last_page_number=last_page_number)

        self.__save_cards()

    def __iterate_pages(self, last_page_number: int) -> None:
        """Iterate through the pages and get the cards
        1. last_page_number: int -> The last page number
        2. Loop through the pages and get the cards
        """
        for page in range(2, last_page_number + 1):
            print(f"Scraping page {page} of {last_page_number}...")
            url: str = f"{self.base_url[0]}{self.query}{self.base_url[1]}&paged={page}"
            soup: BeautifulSoup = self.__make_request(url=url)
            self.cards.extend(soup.find_all(name='article', class_='type-pkmn_card entry'))
            break

    def __get_page_number(self, soup: BeautifulSoup) -> int:
        """Get the last page number
        1. soup: BeautifulSoup -> The soup object
        2. last_page: Tag | NavigableString | None -> The last page tag
        3. last_page_number: int -> The last page number
        4. return: int -> The last page number
        """
        last_page: Tag | NavigableString | None = soup.find(name='a', title='Last Page (Press L)')
        return int(last_page.get_text().split()[-1]) if last_page else 1

    def __make_request(self, url: str) -> BeautifulSoup:
        """Make a request to the url and return the soup object
        1. url: str -> The url to make a request
        2. response: requests.Response -> The response object
        3. return: BeautifulSoup -> The soup object
        """
        response: requests.Response = requests.get(url=url)
        return BeautifulSoup(markup=response.content, features='html.parser')

    def __save_cards(self) -> None:
        """Save the cards to a file
        1. Open a file in write mode
        2. Loop through the cards and write the text to the file
        """
        with open(file=f'output/raw/pkmn_cards_{self.query}.txt', mode='w', encoding="utf-8") as f:
            for card in self.cards:
                f.write(card.get_text().replace('\n', ' '))
                f.write('\n')