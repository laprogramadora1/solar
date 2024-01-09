from app import create_app
#from util.db import db
#from flask_sqlalchemy import SQLAlchemy

app = create_app()

if __name__ == '__main__':    
    app.run(debug=True, host="0.0.0.0")