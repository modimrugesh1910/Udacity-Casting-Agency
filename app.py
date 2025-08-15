from flask import Flask, jsonify
from models import setup_db
from auth import AuthError

# Create the app first
app = Flask(__name__)

# Set up the database
setup_db(app)

# Define error handler AFTER app is defined
@app.errorhandler(AuthError)
def handle_auth_error(e):
    return jsonify({
        "success": False,
        "error": e.status_code,
        "message": e.error['description']
    }), e.status_code

# Define a root route for testing
@app.route('/')
def index():
    return jsonify({"message": "Casting Agency API running"})


app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

@app.route("/actors", methods=["GET"])
@requires_auth("get:actors")
def get_actors():
    return jsonify({"actors": [actor.format() for actor in Actor.query.all()]}), 200

@app.route("/movies", methods=["GET"])
@requires_auth("get:movies")
def get_movies():
    return jsonify({"movies": [movie.format() for movie in Movie.query.all()]}), 200

@app.route("/actors", methods=["POST"])
@requires_auth("post:actors")
def post_actor():
    data = request.get_json()
    try:
        actor = Actor(name=data["name"], age=data["age"], gender=data["gender"])
        actor.insert()
        return jsonify({"actor": actor.format()}), 201
    except:
        abort(422)

@app.route("/movies", methods=["POST"])
@requires_auth("post:movies")
def post_movie():
    data = request.get_json()
    try:
        movie = Movie(title=data["title"], release_date=data["release_date"])
        movie.insert()
        return jsonify({"movie": movie.format()}), 201
    except:
        abort(422)

@app.route("/actors/<int:actor_id>", methods=["PATCH"])
@requires_auth("patch:actors")
def patch_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if not actor:
        abort(404)
    data = request.get_json()
    actor.name = data.get("name", actor.name)
    actor.age = data.get("age", actor.age)
    actor.gender = data.get("gender", actor.gender)
    actor.update()
    return jsonify({"actor": actor.format()}), 200

@app.route("/movies/<int:movie_id>", methods=["PATCH"])
@requires_auth("patch:movies")
def patch_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404)
    data = request.get_json()
    movie.title = data.get("title", movie.title)
    movie.release_date = data.get("release_date", movie.release_date)
    movie.update()
    return jsonify({"movie": movie.format()}), 200

@app.route("/actors/<int:actor_id>", methods=["DELETE"])
@requires_auth("delete:actors")
def delete_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if not actor:
        abort(404)
    actor.delete()
    return jsonify({"deleted": actor_id}), 200

@app.route("/movies/<int:movie_id>", methods=["DELETE"])
@requires_auth("delete:movies")
def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404)
    movie.delete()
    return jsonify({"deleted": movie_id}), 200

@app.errorhandler(403)
def forbidden(error):
    return jsonify({"success": False, "error": 403, "message": "Forbidden"}), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": 404, "message": "Not found"}), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "Unprocessable"}), 422


# Enable debug
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))