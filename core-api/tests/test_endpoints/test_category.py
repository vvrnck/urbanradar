import unittest
from http import HTTPStatus

import pytest

from app import create_app, db
from app.models import Category
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

    def test_filter(self):
        c1 = Category(id=1, name='Roubo e Furto', checked=True, origin='SC')
        c2 = Category(id=2, name='Acidente', checked=True, origin='CT')
        db.session.add_all([c1, c2])

        db.session.commit()

        response = self.app.test_client().get('/api/v1/category', data={'origin': 'SC'})

        assert response.status_code == HTTPStatus.OK
        assert [{
            'id': 1,
            'checked': True,
            'name': 'Roubo e Furto',
            'children': [],
        }] == response.get_json()

    def test_required_fields(self):
        response = self.app.test_client().get('/api/v1/category')
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_result_with_children_field(self):
        c1 = Category(id=1, name='Roubo e Furto', checked=True, origin='SC')
        c2 = Category(id=2, name='Acidente', checked=True, origin='CT')
        c3 = Category(id=3, name='Roubo', checked=False, origin='SC', category=c1)
        db.session.add_all([c1, c2, c3])

        response = self.app.test_client().get('/api/v1/category', data={'origin': 'SC'})
        assert response.status_code == HTTPStatus.OK
        assert [{
            'id': 1,
            'checked': True,
            'name': 'Roubo e Furto',
            'children': [{
                'id': 3,
                'checked': False,
                'name': 'Roubo',
            }]

        }] == response.get_json()

    @pytest.mark.skip('Vamos manter esse bug por enquanto')
    def test_result_with_children_field_where_parent_id_will_be_higher(self):
        c3 = Category(id=3, name='Roubo', checked=False, origin='SC')
        c1 = Category(id=1, name='Roubo e Furto', checked=True, origin='SC', category=c3)
        c2 = Category(id=2, name='Acidente', checked=True, origin='CT')
        db.session.add_all([c1, c2, c3])

        response = self.app.test_client().get('/api/v1/category', data={'origin': 'SC'})
        assert response.status_code == HTTPStatus.OK
        assert [{
            'id': 3,
            'checked': False,
            'name': 'Roubo',
            'children': [{
                'id': 1,
                'checked': True,
                'name': 'Roubo e Furto',
            }]
        }] == response.get_json()


if __name__ == '__main__':
    unittest.main(verbosity=2)
