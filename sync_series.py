from models import Series, BookRelease
from database import SessionLocal
from hardcover_service import get_series_books


def clean_book_list(raw_books):
    junk_words = ["Boxed", "Collection", "Trilogy", "Saga", "Box Set"]
    cleaned = []

    for entry in raw_books:
        title = entry["book"]["title"]
        is_junk = False
        for word in junk_words:
            if word in title:
                is_junk = True
        if not is_junk and entry["position"] is not None:
            cleaned.append(entry)
    return cleaned


def remove_duplicate_positions(cleaned_list):
    seen_positions = []
    final_list = []

    for entry in cleaned_list:
        position = entry["position"]
        if position not in seen_positions:
            seen_positions.append(position)
            final_list.append(entry)
    return final_list


def save_series_to_db(series_name, author, cleaned_books, hardcover_id):
    db = SessionLocal()

    new_series = Series(
        name=series_name, author=author, status="ongoing", hardcover_id=hardcover_id
    )
    db.add(new_series)
    db.commit()
    db.refresh(new_series)

    print("Created series with id:", new_series.id)
    for entry in cleaned_books:
        new_book = BookRelease(
            series_id=new_series.id,
            book_number=entry["position"],
            title=entry["book"]["title"],
        )
        db.add(new_book)

    db.commit()
    print("Saved", len(cleaned_books), "books")

def refresh_series(series_id):
    db = SessionLocal()

    series = db.query(Series).filter(Series.id == series_id).first()
    result = get_series_books(series.hardcover_id)
    raw_list = result["data"]["series_by_pk"]["book_series"]
    cleaned = clean_book_list(raw_list)
    final = remove_duplicate_positions(cleaned)

    added = 0

    for entry in final:
        existing = (db.query(BookRelease).filter(BookRelease.series_id == series_id,BookRelease.book_number == entry["position"],).first())

        if existing is None:
            new_book = BookRelease(
                series_id=series_id,
                book_number=entry["position"],
                title=entry["book"]["title"],
            )
            db.add(new_book)
            added += 1

    db.commit()
    return added


if __name__ == "__main__":
    print("Books added:", refresh_series(1))
