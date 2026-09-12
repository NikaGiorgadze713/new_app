import requests
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("HARDCOVER_API_KEY")



query = """
query {
  series_by_pk(id: 5452) {
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
    json={"query": query},
    headers={"Authorization": f"Bearer {api_key}"}
)


print(response.json())

