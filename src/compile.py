from typing import Any
import pandas as pd
import os
import json

class Compile():
    def __init__(self) -> None:
        self.data: list = []

    def run(self) -> Any:
        self.__add_data()
        df:any = pd.concat(objs=self.data, axis=0)
        self.__save_to_parquet(df=df)

    def __add_data(self) -> None:
        for file in os.listdir(path="output/filtered"):
            with open(file=f"output/filtered/{file}", mode="r", encoding="utf-8") as f:
                data: Any = json.load(fp=f)
                self.data.append(pd.DataFrame(data=data))
    
    def __save_to_parquet(self, df: Any) -> None:
        df.to_parquet("output/compiled_cards.parquet", engine="pyarrow")