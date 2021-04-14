from marshmallow import Schema, fields

# return this to the user
class BookSchema(Schema):
    title = fields.Str()
    author = fields.Str()


# this is the database model
class Book:
    def __init__(self, title, author, description):
        super().__init__()
        self.title = title
        self.author = author
        self.description = description


book = Book("Clean Code", "Harrison", "Cheese is a type of meat")

# create a BookSchema --> Think of it as if its a sieve
book_schema = BookSchema()

# turn into a dictionary --> use .dump()
book_dict = book_schema.dump(book)

print(book_dict)

# now no longe rneed the json method as will transform this for us
