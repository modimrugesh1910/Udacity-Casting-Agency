import unittest
import json
from app import create_app
from models import db

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.assistant = {"Authorization": "Bearer assistant"}
        self.director = {"Authorization": "Bearer director"}
        self.producer = {"Authorization": "Bearer producer"}
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def test_get_actors_as_assistant(self):
        res = self.client().get('/actors', headers=self.assistant)
        self.assertEqual(res.status_code, 200)

    def test_post_actor_as_director(self):
        actor = {"name": "Tom", "age": 40, "gender": "Male"}
        res = self.client().post('/actors', json=actor, headers=self.director)
        self.assertEqual(res.status_code, 200)

    def test_post_movie_as_producer(self):
        movie = {"title": "Matrix", "release_date": "2025-12-01"}
        res = self.client().post('/movies', json=movie, headers=self.producer)
        self.assertEqual(res.status_code, 200)

    def test_post_movie_as_director_forbidden(self):
        movie = {"title": "Matrix", "release_date": "2025-12-01"}
        res = self.client().post('/movies', json=movie, headers=self.director)
        self.assertEqual(res.status_code, 403)

    def test_delete_actor_as_director(self):
        self.client().post('/actors', json={"name": "Tom", "age": 30, "gender": "Male"}, headers=self.director)
        res = self.client().delete('/actors/1', headers=self.director)
        self.assertEqual(res.status_code, 200)

    def test_patch_movie_as_director(self):
        self.client().post('/movies', json={"title": "Inception", "release_date": "2023-10-10"}, headers=self.producer)
        res = self.client().patch('/movies/1', json={"title": "Inception Updated"}, headers=self.director)
        self.assertEqual(res.status_code, 200)

    def test_delete_movie_as_assistant_forbidden(self):
        res = self.client().delete('/movies/1', headers=self.assistant)
        self.assertEqual(res.status_code, 403)

if __name__ == "__main__":
    unittest.main()
