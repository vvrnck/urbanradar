from firebase_admin import auth
from ext import db
from flask import current_app
from sqlalchemy import func
from app.model.User import User
from app.model.Role import Role
from app.model.Scope import Scope
from app.model.Tenant import Tenant
from app.model.UserRoleTenant import UserRoleTenant
from app.model.RoleScope import RoleScope
from app.service import user_service
from app.model.FeatureCollection import FeatureCollection
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def get_user_tenants(uid) -> tuple:
    user_data = user_service.get_user_by_uid(uid)
    urt = db.session.query(UserRoleTenant.tenant_id, UserRoleTenant.user_id, User.active).join(User,
                                                                                               UserRoleTenant.user_id == User.id).filter(
        User.uid == uid).all()
    if urt:
        tenant_list = [u.tenant_id for u in urt]
        return tenant_list, user_data
    return [], None


def get_user_info_from_firebase(access_token: str) -> dict:
    user_info = auth.verify_id_token(access_token)
    return user_info


def generate_user_token_tenantless(user_id, uid, email, name, active, expires_in=300) -> dict:
    serial = Serializer(current_app.secret_key, expires_in=expires_in)
    scopes = ["profile", "email"]
    auth_token = serial.dumps(
        {
            "user_id": str(user_id),
            "uid": str(uid),
            "email": email,
            "name": name,
            "active": active,
            "scopes": scopes,
        }
    ).decode("ascii")

    token_data = {
        "access_token": auth_token,
        "expires_in": expires_in,
        "scope": scopes,
    }

    return token_data


def generate_user_token(user_id, uid, email, tenant_id, roles, scopes, feature_collections, name, expires_in=3600) -> dict:
    serial = Serializer(current_app.secret_key, expires_in=expires_in)
    auth_token = serial.dumps(
        {
            "user_id": str(user_id),
            "uid": str(uid),
            "email": email,
            "tenant_id": str(tenant_id),
            "role_id": roles,
            "scopes": scopes,
            "name": name
        }
    ).decode("ascii")

    token_data = {
        "access_token": auth_token,
        "expires_in": expires_in,
        "tenant_id": str(tenant_id),
        "scope": scopes,
        "roles": roles,
        "feature_collections": feature_collections
    }

    return token_data


def verify_auth_token(token):
    serial = Serializer(current_app.secret_key)
    data = serial.loads(token)

    return data


def fetch_user_scopes(user_id, tenant_id):
    user = User.query.join(UserRoleTenant).join(Role). \
        join(Tenant).join(RoleScopeTenant, Role.id == RoleScopeTenant.role_id).join(Scope). \
        add_entity(Role).add_entity(Scope).filter(User.id == user_id).filter(Tenant.id == tenant_id).all()
    user_json = {"id": user[0].User.id, "user_id": user_id, "name": user[0].User.name, "tenant_id": tenant_id,
                 "active": user[0].User.active,
                 "email": user[0].User.email, "roles": [], "scopes": []}
    for unit in user:
        role_json = {"id": int(unit.Role.id), "name": unit.Role.name}
        if role_json not in user_json["roles"]:
            user_json["roles"].append(role_json)

    for unit in user:
        scope_json = {"id": unit.Scope.id, "key": unit.Scope.key, "name": unit.Scope.name}
        if scope_json not in user_json["scopes"]:
            user_json["scopes"].append(scope_json)
    return user_json


def get_user_scopes(user_id, tenant_id):
    role_scopes = db.session.query(Role.id, Role.name, func.array_agg(Scope.key).label("scopes")).join(RoleScope,
                                                                                                       RoleScope.role_id == Role.id).join(
        Scope, RoleScope.scope_id == Scope.id).join(UserRoleTenant, UserRoleTenant.role_id == Role.id).filter(
        UserRoleTenant.user_id == user_id).filter(UserRoleTenant.tenant_id == tenant_id).group_by(Role.id).all()
    scopes = []
    roles = []
    for role in role_scopes:
        scopes.extend(role.scopes)
        roles.append(
            {
                "id": role.id,
                "name": role.name
            }
        )
    return scopes, roles


def get_feature_collections_by_tenant(tenant_id):
    feature_collections = db.session.query(FeatureCollection.id, FeatureCollection.name, FeatureCollection.bbox,
                                           FeatureCollection.view).join(Tenant,
                                                                        Tenant.id == FeatureCollection.tenant_id).filter(
        Tenant.id == tenant_id).all()
    feat_cols = []
    for feat_col in feature_collections:
        feat_cols.append(
            {
                "id": feat_col.id,
                "name": feat_col.name,
                "bbox": feat_col.bbox,
                "view": feat_col.view
            }
        )
    return feat_cols
