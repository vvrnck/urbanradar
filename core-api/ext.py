from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_compress import Compress

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
compress = Compress()
