from flask import request
from flask import current_app as app
from application import models, schema
from application.models import db
from flask_restx import Api, Resource, Namespace


api = app.config['api']
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


movies_schema = schema.MovieSchema(many=True)
movie_schema = schema.MovieSchema()

directors_schema = schema.DirectorSchema(many=True)
director_schema = schema.DirectorSchema()

genres_schema = schema.GenreSchema(many=True)
genre_schema = schema.GenreSchema()

# Создаем CBV для обработки GET-запросов
@movie_ns.route('/')
class MoviesView(Resource):
    # Возвращает список всех фильмов
    def get(self):
        movies_query = db.session.query(models.Movie)

        args = request.args

        director_id = args.get('director_id')
        if director_id is not None:
            movies_query = movies_query.filter(models.Movie.director_id == director_id)

        genre_id = args.get('genre_id')
        if genre_id is not None:
            movies_query = movies_query.filter(models.Movie.genre_id == genre_id)

        movies = movies_query.all()

        return movies_schema.dump(movies), 200

    def post(self):
        movie = movie_schema.load(request.json)
        db.session.add(models.Movie(**movie))
        db.session.commit()

        return None, 201

@movie_ns.route('/<int:bid>/')
class MovieView(Resource):
    # Возвращает подробную информацию о фильме
    def get(self, bid):
        movie_by_id = db.session.query(models.Movie).filter(models.Movie.id == bid).first()

        if movie_by_id is None:
            return {}, 404

        return movie_schema.dump(movie_by_id), 200

    def put(self, movie_id):
        updated_rows = db.session.query(models.Movie).filter(models.Movie.id == movie_id).update(request.json)
        if updated_rows != 1:
            return None, 400

        db.session.commit()
        return  None, 204

    def delete(self, movie_id):
        deleted_rows = db.session.query(models.Movie).filter(models.Movie.id == movie_id).delete()
        if deleted_rows != 1:
            return None, 400

        db.session.commit()

        return  None, 200

@director_ns.route('/<int:director_id>/')
class DirectorView(Resource):
    # Возвращает подробную информацию о режиссере
    def get(self, director_id):
        director_by_id = db.session.query(models.Director).filter(models.Director.id == director_id).first()

        if director_by_id is None:
            return {}, 404

        return director_schema.dump(director_by_id), 200

    def put(self, director_id):
        updated_rows = db.session.query(models.Director).filter(models.Director.id == director_id).update(request.json)
        if updated_rows != 1:
            return None, 400

        db.session.commit()
        return  None, 204

    def delete(self, director_id):
        deleted_rows = db.session.query(models.Director).filter(models.Director.id == director_id).delete()
        if deleted_rows != 1:
            return None, 400

        db.session.commit()

        return  None, 200

@director_ns.route('/')
class DirectorView(Resource):
    # Возвращает список всех режиссеров
    def get(self):
        directors = db.session.query(models.Director).all()

        return directors_schema.dump(directors), 200

    def post(self):
        director = director_schema.load(request.json)
        db.session.add(models.Director(**director))
        db.session.commit()

        return None, 201

@genre_ns.route('/<int:genre_id>/')
class DirectorView(Resource):
    # Возвращает информацию о жанре с перечислением списка фильмов по жанру
    def get(self, genre_id):
        genre_by_id = db.session.query(models.Genre).filter(models.Genre.id == genre_id).first()

        if genre_by_id is None:
            return {}, 404

        return genre_schema.dump(genre_by_id), 200

    def put(self, genre_id):
        updated_rows = db.session.query(models.Genre).filter(models.Genre.id == genre_id).update(request.json)
        if updated_rows != 1:
            return None, 400

        db.session.commit()
        return None, 204

    def delete(self, genre_id):
        deleted_rows = db.session.query(models.Genre).filter(models.Genre.id == genre_id).delete()
        if deleted_rows != 1:
            return None, 400

        db.session.commit()

        return None, 200


@genre_ns.route('/')
class GenreView(Resource):
    # Возвращает список всех жанров
    def get(self):
        genres = db.session.query(models.Genre).all()

        return genres_schema.dump(genres), 200

    def post(self):
        genre = genre_schema.load(request.json)
        db.session.add(models.Genre(**genre))
        db.session.commit()

        return None, 201

if __name__ == '__main__':
    app.run(debug=True)