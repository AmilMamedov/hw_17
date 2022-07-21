

from marshmallow import Schema, fields


# Напишем сериализацию модели Movie
class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Int()
    genre_id = fields.Int()
    director_id = fields.Int()


# Напишем сериализацию модели Director
class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

# Напишем сериализацию модели Genre
class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()