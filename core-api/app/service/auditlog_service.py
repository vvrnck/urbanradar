from app.model.AuditLog import AuditLog
from ext import db
from typing import List
from app.serializer.audit import AuditResponseList


class AuditLogService:

    @staticmethod
    def log_event_with_token(user, request, duration):
        # Criar AuditLog Object
        audit_log = AuditLog()

        audit_log.user_uid = user['uid']
        audit_log.user_name = user['name']
        audit_log.tenant = user['tenant_id']
        audit_log.url = request.url
        audit_log.action = request.path
        audit_log.browser = str(request.user_agent)
        audit_log.ip = request.remote_addr
        audit_log.duration = str(duration)

        db.session.add(audit_log)
        db.session.commit()

        return audit_log

    @staticmethod
    def log(tenant_id, object_type: str, object_name: str, object_id: str, user_id: str, action: str, url: str, data: list = None,
            browser: str = None, ip: str = None, user_name: str = None, autocommit=True):
        """Given user, object, action and url, register them on audit log table"""

        if data is None:
            data = []

        audit = AuditLog(object_type, object_name, object_id, user_id, action, url, data, browser, ip, user_name, tenant_id)
        if autocommit:
            db.session.add(audit)
            db.session.commit()

        return audit

    def get_audit_by_type_and_id(self, object_id: int, object_type: str) -> List[dict]:
        audit_list = db.session.query(AuditLog).filter(AuditLog.object_id == object_id).filter(AuditLog.object_type == object_type).all()
        audit_resp = [AuditResponseList.from_orm(audit).dict() for audit in audit_list]
        return audit_resp
