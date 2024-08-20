from typing import Literal
from flask import Flask, request, Response
import json
import pandas as pd
from src.model import model

app = Flask(import_name=__name__)

@app.route(rule="/")
def hello_world() -> Literal['<p>Hello, World!</p>']:
    return "<p>Hello, World!</p>"

# http://127.0.0.1:5000/query?query=axew
@app.route(rule="/query", methods=['GET'])
def query() -> str:
    query: str | None = request.args.get(key='query', default=None)
    df: pd.DataFrame = pd.read_parquet("scrapper/output/compiled_cards.parquet")
    model_instance: model = model(df=df)
    result: pd.DataFrame = model_instance.get_similar_cards(query=query)
    response = {
        "result": json.dumps(obj=result.to_dict(orient='records'), ensure_ascii=False),
        "number_of_results": len(result),
        "query": query,
        "message": "OK",
    }
    response_data = json.dumps(obj=response, indent=4, ensure_ascii=False)
    return Response(response=response_data, status=200, mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True)