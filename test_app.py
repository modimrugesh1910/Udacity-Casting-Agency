import unittest
import json
from app import app
from models import db

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client
        self.assistant = {"Authorization": "Bearer assistant"}
        self.director = {"Authorization": "Bearer director"}
        self.producer = {"Authorization": "Bearer producer"}

        with app.app_context():
            db.drop_all()
            db.create_all()

    # Actors - GET
    def test_get_actors_as_assistant_success(self):
        res = self.client().get('/actors', headers=self.assistant)
        self.assertEqual(res.status_code, 200)

    def test_get_actors_no_auth(self):
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 401)

    # Actors - POST
    def test_post_actor_as_director_success(self):
        actor = {"name": "Tom", "age": 40, "gender": "Male"}
        res = self.client().post('/actors', json=actor, headers=self.director)
        self.assertEqual(res.status_code, 201)

    def test_post_actor_missing_field(self):
        actor = {"name": "Tom"}
        res = self.client().post('/actors', json=actor, headers=self.director)
        self.assertEqual(res.status_code, 422)

    # Movies - POST
    def test_post_movie_as_producer_success(self):
        movie = {"title": "Matrix", "release_date": "2025-12-01"}
        res = self.client().post('/movies', json=movie, headers=self.producer)
        self.assertEqual(res.status_code, 201)

    def test_post_movie_as_director_forbidden(self):
        movie = {"title": "Matrix", "release_date": "2025-12-01"}
        res = self.client().post('/movies', json=movie, headers=self.director)
        self.assertEqual(res.status_code, 403)

    # DELETE actor
    def test_delete_actor_as_director_success(self):
        self.client().post('/actors', json={"name": "John", "age": 30, "gender": "Male"}, headers=self.director)
        res = self.client().delete('/actors/1', headers=self.director)
        self.assertEqual(res.status_code, 200)

    def test_delete_actor_not_found(self):
        res = self.client().delete('/actors/99', headers=self.director)
        self.assertEqual(res.status_code, 404)

    # PATCH movie
    def test_patch_movie_as_director_success(self):
        self.client().post('/movies', json={"title": "Inception", "release_date": "2023-10-10"}, headers=self.producer)
        res = self.client().patch('/movies/1', json={"title": "Updated"}, headers=self.director)
        self.assertEqual(res.status_code, 200)

    def test_patch_movie_not_found(self):
        res = self.client().patch('/movies/999', json={"title": "X"}, headers=self.director)
        self.assertEqual(res.status_code, 404)

    # DELETE movie - RBAC
    def test_delete_movie_as_producer_success(self):
        self.client().post('/movies', json={"title": "Tenet", "release_date": "2025-01-01"}, headers=self.producer)
        res = self.client().delete('/movies/1', headers=self.producer)
        self.assertEqual(res.status_code, 200)

    def test_delete_movie_as_assistant_forbidden(self):
        res = self.client().delete('/movies/1', headers=self.assistant)
        self.assertEqual(res.status_code, 403)

if __name__ == "__main__":
    unittest.main()

