class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author




book1 = Book("jack", "King von")
book2 = Book("Mistborn", "Brandon Sanderson")

print(book1.title)
print(book1.author)
print(book2.title)
print(book2.author)