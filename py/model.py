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
    matiere = db.Column(db.String(30), nullable=False)  # Champ de alternance ou non

    def __repr__(self):
        return f'<Homework {self.date} - {self.text} - {self.matiere}>'
