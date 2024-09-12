import os
from datetime import datetime
from app import create_app, db
from app.model import Tenant, Section, User, Layer, Scope, Role, RoleScope, UserRoleTenant, FeatureCollection
from sqlalchemy.exc import IntegrityError
from insert_geojson_grid import insert_feature_mesh

def insert_tenant(tenant_id):
    if not Tenant.query.get(tenant_id):
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
        db.session.add(tenant)
        db.session.commit()

def insert_section(tenant_id):
    section = Section(
        tenant=tenant_id,
        name='Occurencies',
        icon='mdi-layers',
        order=1,
        label={'en': 'Occurencies', 'pt': 'Ocorrências'},
        creation_date=datetime.utcnow(),
        last_update=datetime.utcnow()
    )
    if not Section.query.filter_by(name=section.name, tenant=section.tenant).first():
        db.session.add(section)
        db.session.commit()

def insert_users():
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
        existing_user = User.query.filter_by(email=user.email).first() 
        if not existing_user:
            db.session.add(user)
            db.session.commit()

def insert_layer(tenant_id):
    section = Section.query.first()
    layer = Layer(
        name='Ocurrencies',
        tenant=tenant_id,
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
    if not Layer.query.filter_by(name="Ocurrencies").first():
        db.session.add(layer)
        db.session.commit()

def insert_feature_collection(tenant_id):
    feat_col_name = "FeatureCollection - 1"
    feature_collection = FeatureCollection(
        name=feat_col_name,
        active=True,
        bbox="",  # calculate on grid mesh
        bucket_url="",  # figure this out
        tenant_id=tenant_id,
        view=""
    )
    if not FeatureCollection.query.filter_by(name=feat_col_name).first():
        db.session.add(feature_collection)
        db.session.commit()

def insert_scopes():
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

def insert_roles(tenant_id):
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

def insert_role_scopes():
    admin_role = Role.query.filter_by(name="Administrators").first()
    scopes = Scope.query.all()

    for scope in scopes:
        if not RoleScope.query.filter_by(role_id=admin_role.id, scope_id=scope.id).first():
            db.session.add(RoleScope(
                role_id=admin_role.id,
                scope_id=scope.id
            ))
    db.session.commit()

def insert_user_role_tenants(tenant_id):
    user = User.query.first()
    admin_role = Role.query.filter_by(name="Administrators").first()
    user_role_tenants = [
        (user.id, admin_role.id, tenant_id)
    ]

    for user_id, role_id, tenant_id in user_role_tenants:
        if not UserRoleTenant.query.filter_by(user_id=user_id, role_id=role_id, tenant_id=tenant_id).first():
            db.session.add(UserRoleTenant(
                user_id=user_id,
                role_id=role_id,
                tenant_id=tenant_id
            ))
    db.session.commit()

# insert features from grid mesh
def insert_features(tenant_id):
    file_name = "grid.json"
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    if not os.path.isfile(file_path):
        print(f"Error: File {file_path} does not exist.")
        return

    layer = Layer.query.first()
    feature_collection = FeatureCollection.query.first()
    insert_feature_mesh(file_path, layer.id, tenant_id, feature_collection.id, "")



def insert_data():
    # create the application instance
    app = create_app()
    with app.app_context():
        try:
            tenant_id = 1
            insert_tenant(tenant_id=tenant_id)
            insert_section(tenant_id=tenant_id)
            insert_users()
            insert_layer(tenant_id=tenant_id)
            insert_feature_collection(tenant_id=tenant_id)
            insert_scopes()
            insert_roles(tenant_id=tenant_id)
            insert_role_scopes()
            insert_user_role_tenants(tenant_id=tenant_id)
            insert_features(tenant_id=tenant_id)
            

        except IntegrityError as e:
            db.session.rollback()
            print(f"IntegrityError: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    insert_data()
    