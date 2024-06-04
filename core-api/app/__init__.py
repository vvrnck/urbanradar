import os
import json
from firebase_admin import credentials
from app.api import (audit_api, auth_api, layer_api, feature_api, field_api, tenant_api, section_api, error_handler, endpoints, role_api, user_api, scope_api)
from flask import Flask
from pydantic import ValidationError
from flask.logging import default_handler
import firebase_admin
from app.config import Config
from app.util.exceptions import AbroadException
from ext import cors, db, migrate, compress
from google.cloud import secretmanager
from app import model
from app import logger


def create_app(conf=Config):
    app = Flask(__name__)
    app.config.from_object(conf)

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    app.config["COMPRESS_MIN_SIZE"] = 1024 * 1024
    app.config["COMPRESS_MIMETYPES"] = ["application/json"]
    app.config["COMPRESS_ALGORITHM"] = "gzip"
    
    compress.init_app(app)

    # client = secretmanager.SecretManagerServiceClient()
    # secret_manager_name = f"projects/{os.environ.get('PROJECT_ID')}/secrets/{os.environ.get('SECRET_ID')}/versions/latest"
    # response = client.access_secret_version(request={"name": secret_manager_name})
    # payload = json.loads(response.payload.data.decode("UTF-8"))
    # cred = credentials.Certificate(payload)
    service_account = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    cred = credentials.Certificate(service_account)

    firebase_admin.initialize_app(cred)

    app.logger.removeHandler(default_handler)

    app.register_blueprint(endpoints.api_bp, url_prefix='/api/v1')
    app.register_blueprint(tenant_api.tenant_bp, url_prefix='/api/v1/tenant')
    app.register_blueprint(layer_api.layer_bp, url_prefix='/api/v1/layer')
    app.register_blueprint(section_api.section_bp, url_prefix='/api/v1/section')
    app.register_blueprint(feature_api.feature_bp, url_prefix='/api/v1/feature')
    app.register_blueprint(auth_api.auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(field_api.field_bp, url_prefix='/api/v1/field')
    app.register_blueprint(audit_api.audit_bp, url_prefix='/api/v1/audit')
    app.register_blueprint(role_api.role_bp, url_prefix='/api/v1/role')
    app.register_blueprint(user_api.user_bp, url_prefix='/api/v1/user')
    app.register_blueprint(scope_api.scope_bp, url_prefix='/api/v1/scope')
    app.register_error_handler(Exception, error_handler.handle_all_else)
    app.register_error_handler(AbroadException, error_handler.handle_abroad_excp)
    app.register_error_handler(ValidationError, error_handler.handle_validation_err)

    return app
