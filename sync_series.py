def clean_book_list(raw_books):
    junk_words = ["Boxed", "Collection", "Trilogy", "Saga", "Box Set"]
    cleaned = []

    for entry in raw_books:
        title = entry["book"]["title"]
        is_junk = False
        for word in junk_words:
            if word in title:
                is_junk = True
        if not is_junk:
            cleaned.append(entry)
    return cleaned




from hardcover_service import get_series_books

if __name__ == "__main__":
    result = get_series_books(5452)
    raw_list = result["data"]["series_by_pk"]["book_series"]
    cleaned = clean_book_list(raw_list)
    for item in cleaned:
        print(item["position"], "-", item["book"]["title"])
