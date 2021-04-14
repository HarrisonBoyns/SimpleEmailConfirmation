from marshmallow import Schema, fields, INCLUDE, EXCLUDE

# can either set that fields are required in the class as seen below

# or once can import INCLUDE and EXCLUDE directly from marshmallow and use these in the classSchema initialisation
# always try add fields that one is expecting


class BookSchema(Schema):
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    description = fields.Str(required=True)


# this is the database model
class Book:
    def __init__(self, title, author, description):
        super().__init__()
        self.title = title
        self.author = author
        self.description = description


book = Book("Clean Code", "Harrison", "Cheese is a type of meat")

# create a BookSchema --> Think of it as if its a sieve
book_schema = BookSchema(unknown=INCLUDE)

incoming_book_data = {
    "title": "clean code",
    "author": "Harrison",
    "description": "A book about love",
}

book = book_schema.load(incoming_book_data)
#  validates for you if it includes an unknown field
# default deserialisation will tell you an error if you pasd through any unknown fields
print(book)


#  can serialise and deserialise data
# very powerful for us
#  can then create a Book object with :

book = Book(**book)
