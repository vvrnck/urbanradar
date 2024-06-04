from app.model.Role import Role
from app.model.RoleScope import RoleScope
from app.model.Scope import Scope
from app.model.User import User
from app.model.UserRoleTenant import UserRoleTenant
from app.serializer.role import RolePatch, RoleCreate, RoleList
from app.serializer.user import UserPatch, UserCreate
from ext import db
from typing import List
from app.util.exceptions import EntityNotFound


def get_role_by_id(role_id, tenant_id):
    role = db.session.query(Role).filter(Role.id == role_id).filter(Role.tenant_id == tenant_id).first()
    if role:
        return role
    raise EntityNotFound


def edit_role(role_id: str, role_data: RolePatch) -> Role:
    tenant_id = role_data.tenant_id
    role = get_role_by_id(role_id, tenant_id)
    for key in role_data.dict(exclude_unset=True):
        if key != "scopes":
            role.__setattr__(key, role_data.__getattribute__(key))
        else:
            scopes = role_data.scopes
            role.scopes.clear()
            for scope in scopes:
                rs = RoleScope(scope.id)
                role.scopes.append(rs)
    db.session.commit()
    return role


def delete_role(role_id: str, tenant_id: str) -> Role:
    role = get_role_by_id(role_id, tenant_id)
    db.session.delete(role)
    db.session.commit()
    return role


def list_roles(tenant_id: str) -> List[Role]:
    roles = db.session.query(Role).filter(Role.tenant_id == tenant_id).all()
    return roles


def create_role(role_data: RoleCreate) -> Role:
    role = Role(**role_data.dict())
    scope_list = []
    for scope in role_data.scopes:
        rs = RoleScope(scope.id)
        scope_list.append(rs)
    role.scopes.extend(scope_list)
    db.session.add(role)
    db.session.commit()
    return role


def get_user_by_id(user_id: int, tenant_id: int) -> User:
    user = db.session.query(User).filter(User.id == user_id).join(UserRoleTenant, UserRoleTenant.user_id == User.id).filter(UserRoleTenant.tenant_id == tenant_id).first()
    if not user:
        raise EntityNotFound
    return user


def get_user_by_uid(uid: str) -> User:
    user = db.session.query(User).filter(User.uid == uid).first()
    if not user:
        raise EntityNotFound
    return user


def get_user_by_id_with_roles(user_id: int, tenant_id: int) -> (User, List[Role]):
    user = get_user_by_id(user_id, tenant_id)
    roles = db.session.query(Role).join(UserRoleTenant, Role.id == UserRoleTenant.role_id).filter(Role.tenant_id == tenant_id).filter(UserRoleTenant.user_id == user_id).all()
    return user, roles


def delete_user_by_id(user_id: int, tenant_id: int) -> User:
    user = get_user_by_id(user_id, tenant_id)
    db.session.delete(user)
    db.session.commit()
    return user


def list_users(tenant_id: int) -> List[User]:
    users = db.session.query(User).join(UserRoleTenant, UserRoleTenant.user_id == User.id).filter(UserRoleTenant.tenant_id == tenant_id).all()
    return users


def edit_user(user_id: int, user_data: UserPatch) -> User:
    tenant_id = user_data.tenant_id
    user = get_user_by_id(user_id, tenant_id)
    for key in user_data.dict(exclude_unset=True):
        if key != "roles":
            user.__setattr__(key, user_data.__getattribute__(key))
        else:
            roles = user_data.roles
            db.session.query(UserRoleTenant).filter(UserRoleTenant.tenant_id == tenant_id).filter(UserRoleTenant.user_id == user_id).delete()
            urt_list = []
            for role in roles:
                urt = UserRoleTenant(user_id, role.id, tenant_id)
                urt_list.append(urt)
            db.session.add_all(urt_list)
    db.session.commit()
    return user


def create_user(user_data: UserCreate) -> (User, RoleList):
    user = User(**user_data.dict())
    roles = user_data.roles
    for role in roles:
        urt = UserRoleTenant(role_id=role.id, tenant_id=user_data.tenant_id)
        user.user_role_tenant.append(urt)
    db.session.add(user)
    db.session.commit()
    return user, roles


def list_scopes() -> List[Scope]:
    scopes = db.session.query(Scope).all()
    return scopes
