import unittest
from datetime import datetime
from http import HTTPStatus

from app import create_app, db
from app.models import Category, Layer, Feature, Properties
from app.config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class CategoryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_endpoint(self):
        origin = 'SC'
        c1 = Category(id=1, name='Roubo e Furto', checked=True, origin=origin)
        l1 = Layer(id=1, name='Rouba e Furto', checked=True, origin=origin)
        f1 = Feature(id=1, layer=l1, origin=origin, code='123', geo='456', geo_txt='789')
        p1 = Properties(id=1, feature=f1, category=c1, origin=origin, value=50,
                        dt_filter=datetime(2020, 1, 1))
        p2 = Properties(id=2, feature=f1, category=c1, origin=origin, value=50,
                        dt_filter=datetime(2020, 1, 1))

        db.session.add_all([c1, l1, f1, p1, p2])
        db.session.commit()

        response = self.app.test_client().get('/api/v1/features', data={'origin': 'SC'})

        assert response.status_code == HTTPStatus.OK
        assert [{
            'id': 1,
            'checked': True,
            'name': 'Roubo e Furto',
            'children': [],
        }] == response.get_json()


if __name__ == '__main__':
    unittest.main(verbosity=2)
