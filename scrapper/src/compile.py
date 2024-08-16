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
        self.data: list = []

    def run(self) -> None:
        """
        Run the compiler
        1. Add the data
        2. Save the data to a parquet file
        """        
        self.__add_data()
        df:any = pd.concat(objs=self.data, axis=0)
        self.__save_to_parquet(df=df)

    def __add_data(self) -> None:
        """
        Add the data
        1. Loop through the files
        2. Open the file
        3. Load the data
        4. Append the data
        """
        for file in os.listdir(path="output/filtered"):
            with open(file=f"output/filtered/{file}", mode="r", encoding="utf-8") as f:
                data: Any = json.load(fp=f)
                self.data.append(pd.DataFrame(data=data))
    
    def __save_to_parquet(self, df: Any) -> None:
        """
        Save the data to a parquet file
        1. Save the data to a parquet file
        """
        df.to_parquet("output/compiled_cards.parquet", engine="pyarrow")