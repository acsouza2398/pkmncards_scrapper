from typing import Literal
from flask import Flask, request, Response
import json
import pandas as pd
from src.model import model

# source my-venv/bin/activate
# screen -r

app = Flask(import_name=__name__)

@app.route(rule="/")
def hello_world() -> Literal['<p>Hello, World!</p>']:
    return "<p>Hello, World!</p>"

# http://10.103.0.28:2323/query?query=sun
@app.route(rule="/query", methods=['GET'])
def query() -> str:
    """
    Route to query the pokemon entries
    Args:
        query (str): The query

    Returns:
        str: The response data in json format
    """    
    query: str | None = request.args.get(key='query', default=None)
    df: pd.DataFrame = pd.read_parquet("scrapper/output/compiled_pokemon.parquet")
    model_instance: model = model(df=df)
    result: pd.DataFrame = model_instance.get_similar_entries(query=query)
    response = {
        "result": json.dumps(obj=result.to_dict(orient='records'), ensure_ascii=False),
        "number_of_results": len(result),
        "query": query,
        "message": "OK",
    }
    response_data = json.dumps(obj=response, indent=4, ensure_ascii=False)
    return Response(response=response_data, status=200, mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True, port=2323, host='0.0.0.0')