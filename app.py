from app import app

@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == "__main__":
    from app.database.db import db
    from app.ma import ma
    ma.init_app(app)
    db.init_app(app)
    app.run(debug=True)
