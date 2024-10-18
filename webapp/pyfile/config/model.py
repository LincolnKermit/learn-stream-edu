from enum import Enum
from pyfile.db import db

# Liste des matières prédéfinies
MATIERE_CHOICES = [
    ('physique', 'Physique'),
    ('math', 'Math'),
    ('ir', 'IR'),
    ('culture', 'Culture'),
]

ALTERNANCE_CHOICE = [
    (1, 'Entreprise'),
    (0, 'Cours')
]

TYPE = [
    (3, 'Image'),  # Nouveau type ajouté
    (2, 'File'),
    (1, 'Code'),
    (0, 'Text')
]

class Homework(db.Model):
    __bind_key__ = 'bts'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    text = db.Column(db.String(255), nullable=False)
    matiere = db.Column(db.String(50), nullable=False)  # Champ de matière

    def __repr__(self):
        return f'<Homework {self.date} - {self.text} - {self.matiere}>'

#-------------------- model Learning (matiere cour) -----------------
class Matiere(db.Model):
    __bind_key__ = 'bts'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    id_classe = db.Column(db.Integer, db.ForeignKey('classe.id'), nullable=False)
    nomMatiere = db.Column(db.String(255), nullable=False)
    mainChemin = db.Column(db.String(200), nullable=False)
    def __repr__(self):
        return f'<Matiere {self.date} - {self.nomMatiere}>'

class Cour(db.Model):
    __bind_key__ = 'bts'
    id = db.Column(db.Integer, primary_key=True)
    nomCour = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    chemin = db.Column(db.String(200), nullable=False)
    id_matiere = db.Column(db.Integer, db.ForeignKey('matiere.id'), nullable=False)
    def __repr__(self):
        return f'<Matiere {self.date} - {self.nomCour}>'
#--------------------        -----------------

class Classe(db.Model):
    __bind_key__ = 'bts'
    __tablename__ = 'classe'
    id = db.Column(db.Integer, primary_key=True, nullable=False)  # Unique ID for each class
    nomClasse = db.Column(db.String(60), nullable=False)  # Name of the class
    users = db.relationship('User', backref='classe', lazy=True)
    def __repr__(self):
        return f'<Classe {self.nomClasse} - {self.id}>'


class Message(db.Model):
    __bind_key__ = 'messages'
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id_classe = db.Column(db.Integer,  nullable=False)
    content = db.Column(db.String(300), nullable=True)
    code = db.Column(db.String(500), nullable=True)
    fileName = db.Column(db.String(60), nullable=True)
    filepath = db.Column(db.String(200), nullable=True)
    type = db.Column(db.Integer, nullable=False)  # Nouveau type ajouté
    date = db.Column(db.Date, nullable=False)
    sender_id = db.Column(db.Integer, nullable=False)  # Juste un entier, pas de clé étrangère
    sender_username = db.Column(db.String(255), nullable=True)
    def __repr__(self):
        return f'<Message {self.date} - {self.id} - type: {self.type} - content: {self.content}>'



class User(db.Model):
    __bind_key__ = 'bts'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    id_classe = db.Column(db.Integer, db.ForeignKey('classe.id'), nullable=False)  # Foreign key to the Classe table
    username = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(300), nullable=False)
    lastname = db.Column(db.String(300), nullable=False)
    mail = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(400), nullable=False)
    phoneNumber = db.Column(db.String(100), nullable=False)
    right = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username} ({self.firstname} {self.lastname})>'


