from typing import Any
import pandas as pd
import os
import json

class Compile():
    """Compile the cards
    1. Add the data
    2. Save the data to a parquet file
    """
    def __init__(self) -> None:
        self.file_path: str = "output/pkmn.json"

    def run(self) -> None:      
        with open(file=self.file_path, mode='r', encoding='utf-8') as f:
            data = json.load(f)

        df = pd.DataFrame(list(data.items()), columns=['name', 'description'])
        print(df)

        self.__save_to_parquet(df=df)
    
    def __save_to_parquet(self, df: Any) -> None:
        """
        Save the data to a parquet file
        1. Save the data to a parquet file
        """
        df.to_parquet("output/compiled_pokemon.parquet", engine="pyarrow")