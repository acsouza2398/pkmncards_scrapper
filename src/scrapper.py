import requests
from bs4 import BeautifulSoup


class scrapper():
    def __init__(self):
        self.query = "trainer"
        # self.query = ["pokemon", "trainer", "energy"]
        self.base_url = ["https://pkmncards.com/?s=type%3A", "&sort=date&ord=auto&display=text"]
        self.cards = []

    def run(self):
        url = self.base_url[0] + self.query + self.base_url[1]
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.cards = soup.find_all('article', class_='type-pkmn_card entry')
        last_page = soup.find('a', title='Last Page (Press L)')
        last_page_number = int(last_page.get_text().split()[-1]) if last_page else 1
        for page in range(2, last_page_number + 1):
            response = requests.get(f"{url}&paged={page}")
            soup = BeautifulSoup(response.content, 'html.parser')
            self.cards.extend(soup.find_all('article', class_='type-pkmn_card entry'))
            break

        self.__save_cards()

    def __save_cards(self):
        with open('pkmn_cards.txt', 'w', encoding="utf-8") as f:
            for card in self.cards:
                f.write(card.get_text().replace('\n', ' '))
                f.write('\n')