from flask import Blueprint, request, jsonify, abort
from models import db, Actor, Movie
from auth import requires_auth

app = Blueprint('routes', __name__)

# Actor Endpoints
@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors():
    actors = Actor.query.all()
    return jsonify({'success': True, 'actors': [a.name for a in actors]})

@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actor():
    data = request.get_json()
    actor = Actor(name=data['name'], age=data['age'], gender=data['gender'])
    db.session.add(actor)
    db.session.commit()
    return jsonify({'success': True, 'actor': actor.name})

@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(id):
    actor = Actor.query.get(id)
    if not actor:
        abort(404)
    data = request.get_json()
    actor.name = data.get('name', actor.name)
    actor.age = data.get('age', actor.age)
    actor.gender = data.get('gender', actor.gender)
    db.session.commit()
    return jsonify({'success': True, 'actor': actor.name})

@app.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(id):
    actor = Actor.query.get(id)
    if not actor:
        abort(404)
    db.session.delete(actor)
    db.session.commit()
    return jsonify({'success': True, 'delete': id})

# Movie Endpoints
@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies():
    movies = Movie.query.all()
    return jsonify({'success': True, 'movies': [m.title for m in movies]})

@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie():
    data = request.get_json()
    movie = Movie(title=data['title'], release_date=data['release_date'])
    db.session.add(movie)
    db.session.commit()
    return jsonify({'success': True, 'movie': movie.title})

@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        abort(404)
    data = request.get_json()
    movie.title = data.get('title', movie.title)
    db.session.commit()
    return jsonify({'success': True, 'movie': movie.title})

@app.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        abort(404)
    db.session.delete(movie)
    db.session.commit()
    return jsonify({'success': True, 'delete': id})
