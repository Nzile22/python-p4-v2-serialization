import pytest
from app import app, db, Pet

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {'message': 'Welcome to the pet directory!'}

def test_pet_by_id(client):
    pet = Pet(name='Fido', species='dog')
    db.session.add(pet)
    db.session.commit()
    
    response = client.get('/pets/1')
    assert response.status_code == 200
    assert response.json['name'] == 'Fido'

def test_pet_not_found(client):
    response = client.get('/pets/999')
    assert response.status_code == 404
    assert response.json == {'message': 'Pet 999 not found.'}

def test_pet_by_species(client):
    pet1 = Pet(name='Fido', species='dog')
    pet2 = Pet(name='Whiskers', species='cat')
    db.session.add(pet1)
    db.session.add(pet2)
    db.session.commit()
    
    response = client.get('/species/dog')
    assert response.status_code == 200
    assert response.json['count'] == 1
    assert response.json['pets'][0]['name'] == 'Fido'
