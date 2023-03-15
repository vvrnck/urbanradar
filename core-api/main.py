from app import app, db
from app.model.Feature import Feature


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Feature': Feature}


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
