"""Extensões Flask inicializadas sem depender da app (Application Factory pattern)."""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()
ma: Marshmallow = Marshmallow()
