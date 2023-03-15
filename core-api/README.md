### Running the application
    FLASK_APP=crime_radar.py flask run

# Development

### Generate new database update script, in case there have been any changes
    FLASK_APP=app.py flask db migrate

### Updating the database with the new model
    FLASK_APP=app.py flask db upgrade

### Going back one version in the database structure
    FLASK_APP=app.py flask db upgrade

### Running pytest
    pytest
======
### Running the application
    FLASK_APP=crime_radar.py flask run

# Development

### Generate new database update script, in case there have been any changes
    FLASK_APP=app.py flask db migrate

### Updating the database with the new model
    FLASK_APP=app.py flask db upgrade

### Going back one version in the database structure
    FLASK_APP=app.py flask db upgrade

### Running pytest
    pytest
