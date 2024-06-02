from flask import Flask
from flask_login import LoginManager
from app.models import db
from flask_migrate import Migrate # type: ignore
#from flask_sqlalchemy import SQLAlchemy


#db = SQLAlchemy()
migrate=Migrate()
login_manager = LoginManager()


# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(host='0.0.0.0', debug=True, port=port)

def create_app(settings_module):
    app = Flask(__name__)
    app.config.from_object(settings_module)
    
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    login_manager.login_view = "signin"
    
    #BluePrints
    from app.admin import admin_bp
    from app.auth import auth_bp
    
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.debug=True
    return app
