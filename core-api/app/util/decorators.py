from app.util import exceptions
from datetime import datetime
from functools import wraps

from flask import g, request
from itsdangerous import BadSignature
from app.service import auth_service
from app.service.auditlog_service import AuditLogService


def authentication(f):
    """Verify the token and user information and injects its user data."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            if not token:
                raise exceptions.InvalidToken
            user = auth_service.verify_auth_token(token)
            if user:
                if request.get_json():
                    request.json["tenant_id"] = user.get("tenant_id")
                    request.json["tenant"] = user.get("tenant_id")
                kwargs["user_id"] = user.get('user_id')
                kwargs["scopes"] = user.get('scopes')
                kwargs["tenant_id"] = user.get("tenant_id")
                kwargs['active'] = user.get('active')
                kwargs['email'] = user.get('email')
                kwargs['name'] = user.get('name')
                return f(*args, **kwargs)
            else:
                raise exceptions.InvalidToken
        except BadSignature:
            raise exceptions.InvalidToken
    return decorated_function


def authentication_tenantless(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            hash_ = request.headers.get('Authorization')
            if hash_ is None:
                raise exceptions.InvalidToken
            user = auth_service.verify_auth_token(hash_)
            if user:
                kwargs["user_id"] = user.get('user_id')
                kwargs["scopes"] = user.get('scopes')
                kwargs['email'] = user.get('email')
                kwargs['active'] = user.get('active')
                kwargs['uid'] = user.get('uid')
                kwargs['name'] = user.get('name')
                return f(*args, **kwargs)
            else:
                raise BadSignature
        except BadSignature:
            raise exceptions.InvalidToken
    return decorated_function


def requires_authz(scopes, operator='AND'):
    """Verify if the logged user with valid token has permission to access the resource."""
    def authz(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_scopes = kwargs.get("scopes")
            matched_scopes = [s for s in scopes if s in user_scopes]

            if (operator == 'OR' and len(matched_scopes) == 0) or (operator == 'AND' and len(matched_scopes) != len(scopes)):
                raise exceptions.AccessDenied

            kwargs['matched_scopes'] = " ".join(matched_scopes)
            return f(*args, **kwargs)
        return decorated_function
    return authz


def audit(f):
    """Verify if the operation went well and log to AuditLog table when yes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = str(kwargs.get('user_id', ""))
        tenant_id = str(kwargs.get('tenant_id', ""))
        name = str(kwargs.get('name', ""))

        g.setdefault('audit_data', {
            'data': [],
            'user_id': user_id,
            'tenant_id': tenant_id,
            'user_name': name,
            'ip': request.remote_addr,
            'browser': str(request.user_agent),
            'url': request.full_path,
        })

        response = f(*args, **kwargs)

        # If there is no user_id or there is an error, do not log
        if (
            not user_id
            or (
                "is_json" in dir(response) and response.is_json
                and ('errors' not in response.json or len(response.json['errors']) != 0)
            )
        ):
            return response

        audit_data = g.get('audit_data')

        def compare_equal_attribute_value(attribute_data):
            old = attribute_data['old_value']
            old = old.isoformat(timespec="milliseconds") if type(old) is datetime else old
            new = attribute_data['new_value']
            new = new.isoformat(timespec="milliseconds") if type(new) is datetime else new
            return old != new

        audit_log_data = []

        for entry in audit_data.get('data'):
            if compare_equal_attribute_value(entry):
                audit_log_data.append(entry)

        AuditLogService.log(
            object_type=audit_data.get('object_type'),
            object_name=audit_data.get('object_name'),
            object_id=audit_data.get('object_id'),
            user_id=audit_data.get('user_id'),
            action=audit_data.get('action'),
            url=audit_data.get('url'),
            data=audit_log_data,
            browser=audit_data.get('browser'),
            user_name=audit_data.get('user_name'),
            ip=audit_data.get('ip'),
            tenant_id=audit_data.get('tenant_id')
        )

        return response
    return decorated_function
