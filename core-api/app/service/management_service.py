from app.model.User import User
from app.model.Role import Role
from app.model.UserRoleTenant import UserRoleTenant
from app.model.Tenant import Tenant
from app.model.Scope import Scope
from app.model.RoleScope import RoleScope
from ext import db


class ManagementService:

    @staticmethod
    def create_user(origin, roles, name, email, uid, active):
        if origin is None:
            raise KeyError("Origin not Provided")
        if name is None:
            raise KeyError("Name not Provided")
        if email is None:
            raise KeyError("Email not Provided")
        if uid is None:
            raise KeyError("Uid not Provided")
        if active is None:
            raise KeyError("Active not Provided")
        user = User(uid, name, email, active)
        db.session.add(user)
        tenant = Tenant.query.filter(Tenant.city_code == origin).first()
        for role in roles:
            user_role = UserRoleTenant(user.id, role["id"], tenant.id)
            db.session.add(user_role)

        db.session.commit()
        user_json = {"id": user.id, "uid": user.uid, "name": user.name}
        return user_json

    @staticmethod
    def list_users(origin):
        if origin is None:
            raise KeyError("Origin not Provided")
        users_db = User.query.join(UserRoleTenant).join(Tenant).filter(Tenant.city_code == origin).all()
        users = []
        for user in users_db:
            users_json = {"id": user.id, "uid": user.uid, "name": user.name}
            users.append(users_json)
        return users

    @staticmethod
    def fetch_user(uid, origin):
        if origin is None:
            raise KeyError("Origin not Provided")
        if uid is None:
            raise KeyError("User not Provided")
        user = User.query.join(UserRoleTenant).join(Role).join(Tenant).add_entity(Role) \
            .filter(Tenant.city_code == origin, User.uid == uid).all()
        user_json = {"uid": uid, "name": user[0].User.name, "roles": []}
        for unit in user:
            role_json = {"id": unit.Role.id, "name": unit.Role.name}
            user_json["roles"].append(role_json)
        return user_json

    @staticmethod
    def edit_user(origin, email, name, active, roles, user_id):
        user = User.query.filter(User.id == user_id).first()
        if email is not None:
            try:
                user.email = email
                db.session.commit()
            except Exception as err:
                db.session.rollback()
                raise KeyError("Email provided in illegal format")
        if name is not None:
            try:
                user.name = name
                db.session.commit()
            except Exception as err:
                db.session.rollback()
                raise KeyError("Name provided in illegal format")

        if active is not None:
            try:
                user.active = active
                db.session.commit()
            except Exception as err:
                db.session.rollback()
                raise KeyError("Active provided in illegal format")

        if roles is not None:
            try:
                UserRoleTenant.query.filter(UserRoleTenant.user_id == user_id).delete()
                tenant = Tenant.query.filter(Tenant.city_code == origin).first()
                for role in roles:
                    role_scope = UserRoleTenant(user_id, role["id"], tenant.id)
                    db.session.add(role_scope)
                db.session.commit()
            except Exception as err:
                db.session.rollback()
                raise KeyError("Roles provided in illegal format")
        user_json = {"uid": user.uid, "name": user.name, "roles": roles, "email": email}
        return user_json

    @staticmethod
    def delete_user(user_id):
        if user_id is None:
            raise KeyError("User not provided")

        user = User.query.filter(User.id == user_id).first()
        db.session.commit()
        UserRoleTenant.query.filter(UserRoleTenant.user_id == user_id).delete()
        db.session.commit()

        return True
    #
    # @staticmethod
    # def list_roles(origin):
    #     if origin is None:
    #         raise KeyError("Origin not Provided")
    #     roles_db = Role.query.join(RoleScopeTenant).join(Tenant).filter(Tenant.city_code == origin).all()
    #     roles = []
    #     for role in roles_db:
    #         roles_json = {"id": role.id, "name": role.name, "default": role.default}
    #         roles.append(roles_json)
    #     return roles
    #
    # @staticmethod
    # def fetch_role(_id, origin):
    #     if origin is None:
    #         raise KeyError("Origin not Provided")
    #     if _id is None:
    #         raise KeyError("Role not Provided")
    #     role_user = Role.query.join(UserRoleTenant).join(User).join(Tenant).add_entity(User) \
    #         .filter(Tenant.city_code == origin, Role.id == _id).all()
    #     role_scopes = Role.query.join(RoleScopeTenant).join(Scope).join(Tenant).add_entity(Scope) \
    #         .filter(Tenant.city_code == origin, Role.id == _id).all()
    #     role_json = {"id": _id, "name": role_scopes[0].Role.name, "users": [], "scopes": []}
    #     for unit in role_user:
    #         user_json = {"uid": unit.User.uid, "name": unit.User.name}
    #         role_json["users"].append(user_json)
    #     for unit in role_scopes:
    #         scopes_json = {"id": unit.Scope.id, "description": unit.Scope.description,
    #                        "key": unit.Scope.key, "name": unit.Scope.name}
    #         role_json["scopes"].append(scopes_json)
    #     return role_json
    #
    # @staticmethod
    # def create_role(origin, scopes, name):
    #     if origin is None:
    #         raise KeyError("Origin not Provided")
    #     if scopes is None:
    #         raise KeyError("Scopes not Provided")
    #     if name is None:
    #         raise KeyError("Name not Provided")
    #     role = Role(name)
    #     db.session.add(role)
    #
    #     # Fetch for Tenant ID
    #     tenant = Tenant.query.filter(Tenant.city_code == origin).first()
    #
    #     # Associate roles into scopes
    #     for scope in scopes:
    #         role_scope = RoleScopeTenant(role.id, scope["id"], tenant.id)
    #         db.session.add(role_scope)
    #     db.session.commit()
    #
    #     role_json = {"id": role.id, "name": role.name, "scopes": scopes}
    #     return role_json
    #
    # @staticmethod
    # def edit_role(tenant_id, scopes, name, role_id):
    #     role = Role.query.filter(Role.id == role_id).first()
    #     if scopes is not None:
    #         try:
    #             RoleScopeTenant.query.filter(RoleScopeTenant.role_id == role_id).delete()
    #             for scope in scopes:
    #                 role_scope = RoleScopeTenant(role.id, scope["id"], tenant_id)
    #                 db.session.add(role_scope)
    #             db.session.commit()
    #         except Exception as err:
    #             db.session.rollback()
    #             raise KeyError("Scopes provided in illegal format")
    #     if name is not None:
    #         role.name = name
    #         db.session.commit()
    #
    #     role_json = {"id": role.id, "name": role.name, "scopes": scopes}
    #     return role_json
    #
    # @staticmethod
    # def delete_role(role_id, tenant_id):
    #     if role_id is None:
    #         raise KeyError("Role not provided")
    #     Role.query.filter(Role.id == role_id).delete()
    #     db.session.commit()
    #     RoleScopeTenant.query.filter(RoleScopeTenant.role_id == role_id).delete()
    #     db.session.commit()
    #
    #     return True

    @staticmethod
    def list_scopes():
        scopes_db = Scope.query.all()
        scopes = []
        for scope in scopes_db:
            scopes_json = {"id": scope.id, "description": scope.description, "key": scope.key, "name": scope.name}
            scopes.append(scopes_json)
        return scopes

    @staticmethod
    def fetch_user_scopes(uid, origin):
        if uid is None:
            raise KeyError("User not Provided")
        user = User.query.join(UserRoleTenant).join(Role). \
            join(Tenant).join(RoleScopeTenant, Role.id == RoleScopeTenant.role_id).join(Scope). \
            add_entity(Role).add_entity(Scope).filter(Tenant.city_code == origin, User.uid == uid).all()
        user_json = {"id": user[0].User.id, "uid": uid, "name": user[0].User.name, "origin": origin,
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

    @staticmethod
    def trade_user_mail_for_uid(email):
        user = User.query.filter(User.email == email).first()
        return user.uid

    @staticmethod
    def fetch_user_by_uid(uid):
        if uid is None:
            raise KeyError("Uid not Provided")
        user = User.query.join(UserRoleTenant).join(Role).join(Tenant).add_entity(Tenant) \
            .filter(User.uid == uid).first()
        user_json = {"uid": user.User.uid, "name": user.User.name, "email": user.User.email,
                     "tenant": user.Tenant.name}
        return user_json
