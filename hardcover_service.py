

import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("HARDCOVER_API_KEY")


def search_series(name):
    query = """
    query SearchSeries($name: String!) {
      search(query: $name, query_type: "series") {
        results
      }
    }
    """
    response = requests.post(
        "https://api.hardcover.app/v1/graphql",
        json={"query": query, "variables": {"name": name}},
        headers={"Authorization": f"Bearer {api_key}"}
    )
    return response.json()


def get_series_books(series_id):

    query = """
        query GetSeriesBooks($id: Int!) {
           series_by_pk(id: $id) {
             name
             book_series(
               order_by: {position: asc}
               where: {book: {default_physical_edition: {language_id: {_eq: 1}}}}
             ) {
               position
               book {
                 title
               }
             }
            }
        }
        """

    response = requests.post(
        "https://api.hardcover.app/v1/graphql",
        json={"query": query, "variables": {"id": series_id}},
        headers={"Authorization": f"Bearer {api_key}"}
    )

    return response.json()


if __name__ == "__main__":
  print(get_series_books(5452))
