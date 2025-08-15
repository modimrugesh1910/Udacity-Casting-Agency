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


# Enable debug
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))