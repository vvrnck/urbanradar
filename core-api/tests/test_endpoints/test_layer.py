import unittest
from http import HTTPStatus

from app import create_app, db
from app.models import Layer
from app.config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class LayerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_filter(self):
        l1 = Layer(id=1, name='Rouba e Furto', checked=True, origin='SC')
        l2 = Layer(id=2, name='Acidente', checked=True, origin='CT')
        db.session.add_all([l1, l2])

        db.session.commit()

        response = self.app.test_client().get('/api/v1/layer', data={'origin': 'SC'})

        assert response.status_code == HTTPStatus.OK
        assert [{
            'id': 1,
            'checked': True,
            'name': 'Rouba e Furto'
        }] == response.get_json()

    def test_required_fields(self):
        response = self.app.test_client().get('/api/v1/layer')
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


if __name__ == '__main__':
    unittest.main(verbosity=2)
