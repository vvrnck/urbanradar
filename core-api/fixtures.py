import os
from datetime import datetime
from app import create_app, db
from app.model import Tenant, Section, User, Layer, Scope, Role, RoleScope, UserRoleTenant
from sqlalchemy.exc import IntegrityError

# Create the application instance
app = create_app()

def insert_data():
    with app.app_context():
        # Insert data into Tenant
        tenant_id = 1
        tenant = Tenant(
            id=tenant_id,
            name='Urbanradar',
            city='Urbanradar',
            city_code='UR',
            country='Brazil',
            status=1,
            last_update=datetime.utcnow(),
            creation_date=datetime.utcnow()
        )
        # Check if Tenant already exists
        if not Tenant.query.get(tenant.id):
            db.session.add(tenant)
            db.session.commit()

        # Insert data into Section
        section = Section(
            tenant=1,
            name='Occurencies',
            icon='mdi-layers',
            order=1,
            label={'en': 'Occurencies', 'pt': 'Ocorrências'},
            creation_date=datetime.utcnow(),
            last_update=datetime.utcnow()
        )
        # Check if Section already exists
        if not Section.query.filter_by(name=section.name, tenant=section.tenant).first():
            db.session.add(section)
            db.session.commit()

        # Insert data into User
        users = [
            User(
                uid=os.environ.get("FIREBASE_ADMIN_UID"),
                name='admin',
                email=os.environ.get("FIREBASE_ADMIN_EMAIL"),
                active=True,
                last_update=datetime.utcnow(),
                creation_date=datetime.utcnow()
            )
        ]
        for user in users:
            # Check if User already exists
            existing_user = User.query.filter_by(email=user.email).first() 
            if not existing_user:
                db.session.add(user)
                db.session.commit()

        # Insert data into Layer
        section = Section.query.first()
        layer = Layer(
            name='Ocurrencies',
            tenant=1,
            id_section=section.id,
            selected=False,
            order=1,
            active=True,
            style={
                'colorScale': {
                    'point': {},
                    'polygon': [
                        'hsl(230, 100%, 50%)',
                        'hsl(180, 100%, 50%)',
                        'hsl(120, 100%, 50%)',
                        'hsl(60, 100%, 50%)',
                        'hsl(0, 100%, 50%)'
                    ],
                    'image_overlay': []
                },
                'color': '#FFFFFF',
                'types': [
                    {'name': 'scale', 'value': True, 'icon': 'mdi-palette', 'label': 'scale'},
                    {'name': 'hexagon', 'value': False, 'icon': 'mdi-format-paint', 'label': 'hexagon'},
                    {'name': 'icon', 'value': False, 'icon': 'mdi-star-circle', 'label': 'icon'},
                    {'name': 'marker', 'value': False, 'icon': 'mdi-map-marker', 'label': 'marker'},
                    {'name': 'point', 'value': False, 'icon': 'mdi-brightness-1', 'label': 'point'}
                ],
                'texture': {'value': 'NONE', 'options': ['NONE', 'HORIZONTAL', 'VERTICAL']},
                'extra_props': {
                    'marker': {'image': '', 'icon': 'pin-black.png'},
                    'image_overlay': {},
                    'polygon': {},
                    'point': {},
                    'mobile': True,
                    'type': '!icon'
                }
            },
            editable=True,
            label={'en': 'Occurrencies', 'pt': 'Ocorrências'},
            configurable=True,
            creation_date=datetime.utcnow(),
            last_update=datetime.utcnow()
        )
        # Check if Layer already exists
        if not Layer.query.get(layer.id):
            db.session.add(layer)

        # Insert data into Scope
        scopes = [
            (1, 'View navbar Map Page Option', 'map.view', 'Map Option View'),
            (2, 'View optimization Option', 'optimization.view', 'Optimization Option View'),
            (3, 'View user feedback Option', 'feedback.view', 'User Feedback Option View'),
            (4, 'View helper Option', 'helper.view', 'Helper Option View'),
            (5, 'Select layers in sidebar menu', 'map.layer.view', 'Layers View'),
            (6, 'Select reset button option', 'map.reset.view', 'View Reset Button'),
            (7, 'Select apply button option', 'map.apply.view', 'View Apply Button'),
            (8, 'Select filter options', 'map.filter.view', 'View and Select Filters'),
            (9, 'Select dates options', 'map.date.view', 'View and Select calendar dates'),
            (10, 'Select texture options', 'map.texture.view', 'View and Select different textures'),
            (11, 'Select map types', 'map.type.view', 'View box and Select Map types'),
            (12, 'View Map Captions', 'map.caption.view', 'View Map Captions floating options'),
            (13, 'View Toolbox', 'map.toolbox.view', 'View and use Toolbox'),
            (14, 'View SearchBar', 'map.search.view', 'View and use Searchbar'),
            (15, 'View Controls Pane', 'map.control.view', 'View and use Controls Pane'),
            (16, 'List Users', 'user.list.view', 'List Users and use Filters'),
            (17, 'Create Users', 'user.create', 'Create users in Tenant'),
            (18, 'Delete Users', 'user.delete', 'Delete a user from a Tenant'),
            (19, 'Associate Profiles to Users', 'user.edit', 'Edit a user in Tenant'),
            (20, 'View Reports', 'report.search.view', 'View Reports'),
            (21, 'Edit Status Reports', 'report.status.edit', 'Edit Status Reports'),
            (22, 'View Predictions', 'prediction.list.view', 'View Predictions Reports'),
            (23, 'Search Predictions', 'prediction.search.view', 'Search Predictions Reports'),
            (24, 'Associate Roles to Users and Scopes', 'role.edit', 'Edit a role in Tenant'),
            (25, 'Create Roles', 'role.create', 'Create a role in Tenant'),
            (26, 'Delete Roles', 'role.delete', 'Delete a role in Tenant'),
            (27, 'List Roles', 'role.list.view', 'List roles in Tenant'),
            (28, 'Scope List', 'scope.list.view', 'List scopes in Tenant'),
            (29, 'Management View ', 'management.view', 'Management View'),
            (30, 'Feedback View', 'feedback.view', 'Feedback View'),
            (31, 'Administration View', 'administration.view', 'Administration View'),
            (32, 'Section Create', 'section.create', 'Create Sections in Tenant'),
            (33, 'Section List View', 'section.list.view', 'List Sections in Tenant'),
            (34, 'Section Edit', 'section.edit', 'Edit Sections in Tenant'),
            (35, 'Section Delete', 'section.delete', 'Delete Sections in Tenant'),
            (36, 'Layer Create', 'layer.create', 'Create new Layers in Tenant'),
            (37, 'Layer List View', 'layer.list.view', 'List Layers in Tenant'),
            (38, 'Layer Edit', 'layer.edit', 'Edit Layers in Tenant'),
            (39, 'Layer Delete', 'layer.delete', 'Delete Layers in Tenant')
        ]

        for scope_id, description, key, name in scopes:
            if not Scope.query.get(scope_id):
                db.session.add(Scope(
                    id=scope_id,
                    description=description,
                    key=key,
                    name=name,
                    last_update=datetime.utcnow(),
                    creation_date=datetime.utcnow()
                ))
                db.session.commit()

        # Insert data into Role
        roles = [
            ('Administrators', False, tenant_id),
            ('Users', True, tenant_id)
        ]

        for name, is_default, tenant_id in roles:
            if not Role.query.filter_by(name=name).first():
                db.session.add(Role(
                    name=name,
                    default=is_default,
                    tenant_id=tenant_id
                ))
                db.session.commit()

        # Insert data into RoleScope - making admin have all scopes
        admin_role = Role.query.filter_by(name="Administrators").first()
        for scope_id, name, permission, description in scopes:         
            if not RoleScope.query.filter_by(role_id=admin_role.id, scope_id=scope_id).first():
                db.session.add(RoleScope(
                    role_id=admin_role.id,
                    scope_id=scope_id
                ))
                db.session.commit()

        # Insert data into UserRoleTenant
        user = User.query.first()
        user_role_tenants = [
            (user.id, admin_role.id, 1),
        ]

        for user_id, role_id, tenant_id in user_role_tenants:
            if not UserRoleTenant.query.filter_by(user_id=user_id, role_id=role_id, tenant_id=tenant_id).first():
                db.session.add(UserRoleTenant(
                    user_id=user_id,
                    role_id=role_id,
                    tenant_id=tenant_id
                ))
                
        db.session.commit()

if __name__ == '__main__':
    insert_data()