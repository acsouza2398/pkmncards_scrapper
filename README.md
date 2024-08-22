# C5.1. Make an API
Student: Ana Carolina Souza

## Description
This API is a simple API that allows you to get information about pokémons. In every game of the Pokémon series, each monster gets a sentence or two that describes it in the game's encyclopedia called a pokédex. The more games a pokémon appears in, the more descriptions it has. This API allows you to get the pokédex entries of pokémon that match phrases or words that the user provides.

The main use of the API would be to explore and understand more about the lore of the pokémon world through these entries. It can be used by fans of the series, or by people who are just curious about the pokémon world. There are many pokémon, and each one has its own unique description, so there is a lot of content to explore.

## Dataset
The dataset used was obtained through webscraping, using Requests and Beautiful Soup, from the website [Pokémon Database](https://pokemondb.net/). This website contains information about all pokémon from the main series games, such as stats, abilities, and pokédex entries. In order to get the pokédex entries, the API uses the descriptions that are available on the website for each pokemon. The scrapper used to get the data is available in the `scrapper` folder, as well as the resulting dataset `compiled_pokemon.parquet` in the `output` folder.

The dataset contains the name of the pokémon and a description that contains all of the pokédex entries compiled into a single text. The dataset has 1025 lines, one for each pokémon released so far.

### How to use the scrapper
The scrapper is a simple script that uses Requests and Beautiful Soup to get the pokédex entries from the Pokémon Database website. To use the scrapper, you need to have Python installed on your machine.
Install the necessary dependencies by running the following command inside the `scrapper` folder:
```
pip install -r requirements.txt
```

You can run the scrapper by running the following command in the root directory of the project:
```
python scrapper/main.py
```

## About the API
### How to install
Install the necessary dependencies by running the following command:
```
pip install -r requirements.txt
```

### How to run
Run the API by running the following command, in the root directory of the project:
```
python main.py
```
This should start up the API, and you should see a message saying that the API is running in the console.

### How to query
The API has one endpoint, which is `/query`. This endpoint receives a query parameter called `query` that is the phrase or word that the user wants to search for in the pokédex entries. The API will return a list of pokémon and their pokédex entries that are similar to the phrase or word that the user provided, up to 10 results.

The Flask server is hosted on `http://10.103.0.28:2323/`.

### Examples

#### Example 1 - Query that returns 10 results
Request:
```
GET http://10.103.0.28:2323/query?query=sun
```
Response (Shortened for brevity):
```json
{
    'result': [
        {'name': 'larvesta',
        'description': 'This Pokémon was believed to have been born from the sun. When it evolves, its entire body is engulfed in flames. ',
        'score': 0.3096613720027947},
        {'name': 'sunflora',
        'description': 'It converts sunlight into energy. In the darkness after sunset, it closes its petals and becomes still. In the daytime, it rushes about in a hectic manner, but it comes to a complete stop when the sun sets. ',
        'score': 0.25370704345895345},
        {'name': 'solgaleo',
        'description': 'It is said to live in another world. Solgaleo was once known as the Beast That Devours the Sun.',
        'score': 0.23062408727517622},
        {'name': 'volcarona',
        'description': 'When volcanic ash darkened the atmosphere, it is said that Volcarona’s fire provided a replacement for the sun. ',
        'score': 0.22962145834689687},
        {'name': 'helioptile',
        'description': 'They make their home in deserts. They can generate their energy from basking in the sun, so eating food is not a requirement.',
        'score': 0.22481717217325028},
        {'name': 'solrock',
        'description': 'SOLROCK is a new species of POKéMON that is said to have fallen from space. It floats in air and moves silently. In battle, this POKéMON releases intensely bright light. Sunlight is the source of SOLROCK’s power.',
        'score': 0.2074828376007953},
        {'name': 'stonjourner',
        'description': 'It stands in grasslands, watching the sun’s descent from zenith to horizon. This Pokémon has a talent for delivering dynamic kicks.',
        'score': 0.20398634504554483},
        {'name': 'sandile',
        'description': 'They live buried in the sands of the desert. The sun-warmed sands prevent their body temperature from dropping. It moves along below the sand’s surface, except for its nose and eyes. ', 'score': 0.19157121316744447},
        {'name': 'sprigatito',
        'description': 'Its fluffy fur is similar in composition to plants. This Pokémon frequently washes its face to keep it from drying out. The sweet scent its body gives off mesmerizes those around it. The scent grows stronger when this Pokémon is in the sun.',
        'score': 0.18118956538947323},
        {'name': 'vanillite',
        'description': 'The temperature of their breath is -58° F. They create snow crystals and make snow fall in the areas around them. This Pokémon formed from icicles bathed in energy from the morning sun. It sleeps buried in snow.',
        'score': 0.1709084791710776}],
    'number_of_results': 10,
    'query': 'sun',
    'message': 'OK'
}
```

#### Example 2 - Query that returns less than 10 results
Request:
```
GET http://10.103.0.28:2323/query?query=lives%20in%20volcanoes
```

Response (Shortened for brevity):
```json
{
    'result': [
        {'name': 'camerupt',
        'description': 'CAMERUPT has a volcano inside its body. Magma of 18,000 degrees F courses through its body. Occasionally, the humps on this POKéMON’s back erupt, spewing the superheated magma.It lives in the crater of a volcano.',
        'score': 0.33971504773742917},
        {'name': 'pansear',
        'description': 'When it is angered, the temperature of its head tuft reaches 600° F. It uses its tuft to roast berries. This Pokémon lives in caves in volcanoes. The fire within the tuft on its head can reach 600° F. Very intelligent, it roasts berries before eating them.',
        'score': 0.26622127406885154},
        {'name': 'turtonator',
        'description': 'The shell on its back is chemically unstable and explodes violently if struck. The hole in its stomach is its weak point. It lives in volcanoes and eats sulfur and other minerals. Materials from the food it eats form the basis of its explosive shell. Its exploding shell poses a real danger but is sensitive to moisture.',
        'score': 0.12532574046386025},
        {'name': 'larvesta', 'description': 'This Pokémon was believed to have been born from the sun. When it evolves, its entire body is engulfed in flames. The base of volcanoes is where they make their homes. ',
        'score': 0.11479693140676235},
        {'name': 'entei',
        'description': 'Volcanoes erupt when it barks. Unable to restrain its extreme power, it races headlong around the land. A POKéMON that races across the land. It is said that one is born every time a new volcano appears. This brawny POKéMON courses around the earth, spouting flames hotter than a volcano’s magma. ENTEI embodies the passion of magma. This POKéMON is thought to have been born in the eruption of a volcano.',
        'score': 0.11153690992797687}],
    'number_of_results': 5,
    'query': 'lives in volcanoes',
    'message': 'OK'
}
```

#### Example 3 - Query that returns something unusual

Request:
```
GET http://10.103.0.28:2323/query?query=bully
```

Response (Shortened for brevity):
```json
{
    'result': [
        {'name': 'sharpedo',
        'description':'Nicknamed “the bully of the sea,” SHARPEDO is widely feared. Its cruel fangs grow back immediately if they snap off.',
        'score': 0.2681954994034775},
        {'name': 'drampa', 'description': 'This Pokémon is friendly to people and loves children most of all. It comes from deep in the mountains to play with children it likes in town. If a child it has made friends with is bullied, Drampa will find the bully’s house and burn it to the ground. It appears in towns and plays with the children.',
        'score': 0.11439216918030394}],
    'number_of_results': 2,
    'query': 'bully',
    'message': 'OK'
}
```

The result is unusual because the expected result was aggressive pokémon, like sharpedo, but the API returned a pokémon that is friendly and protects children from bullies.