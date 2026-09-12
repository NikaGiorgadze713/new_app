import requests
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("GOOGLE_BOOKS_API_KEY")

response = requests.get(
    "https://www.googleapis.com/books/v1/volumes",
    params={"q": "Mistborn Brandon Sanderson", "key": api_key}
)

print(response.json())