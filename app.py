from flask import Flask
# Remova a importação local do SQLAlchemy aqui, já que você está usando a instância de `database.py`
from database import db
from routes import api_blueprint  # Certifique-se de que este import está correto com base na localização do seu arquivo routes.py
from dotenv import dotenv_values

config = dotenv_values(".env")


def create_app():
#banco postgre publicado:
#url= jdbc:postgresql://silly.db.elephantsql.com:5432/rzojbgsw
#database:rzojbgsw
#password:pyyo3P8_lMOtxwYzJsP234BUYx4ovBs4
    #

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config["LOCAL_DATABASE_URI"] #'postgresql://rzojbgsw:pyyo3P8_lMOtxwYzJsP234BUYx4ovBs4@silly.db.elephantsql.com:5432/rzojbgsw'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Remova a linha onde você tinha `db = SQLAlchemy(app)`
    
    db.init_app(app)
    
    with app.app_context():
        # Importações dentro do contexto da aplicação para evitar importações circulares
        app.register_blueprint(api_blueprint, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
