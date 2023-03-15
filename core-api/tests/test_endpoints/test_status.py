import unittest
from app import create_app, db
from app.config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class StatusTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_status_ok(self):
        response = self.app.test_client().get(
            '/api/v1/status'
        )

        assert response.status_code == 200
        assert {'status': 'ok'} == response.get_json()


if __name__ == '__main__':
    unittest.main(verbosity=2)
