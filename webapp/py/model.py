from py.db import db

# Liste des matières prédéfinies
MATIERE_CHOICES = [
    ('physique', 'Physique'),
    ('math', 'Math'),
    ('ir', 'IR'),
    ('culture', 'Culture'),
]

ALTERNANCE_CHOICE = [
    (1, 'Entreprise'),
    (0, 'Cour')
]

class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    text = db.Column(db.String(255), nullable=False)
    matiere = db.Column(db.String(50), nullable=False)  # Champ de matière

    def __repr__(self):
        return f'<Homework {self.date} - {self.text} - {self.matiere}>'


class Cour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    nomCour = db.Column(db.String(255), nullable=False)
    matiere = db.Column(db.String(50), nullable=False)
    mainChemin = db.Column(db.String(200), nullable=False)
    idf = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Cour {self.date} - {self.nomCour} - {self.matiere}>'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    username = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(300), nullable=False)
    lastname = db.Column(db.String(300), nullable=False)
    mail = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    phoneNumber = db.Column(db.String(100), nullable=False)
    right = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User created {self.date} - {self.user_name} - {self.id}>'