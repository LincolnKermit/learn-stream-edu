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
    (2, 'File'),
    (1, 'Code'),
    (0, 'Normal')
]

class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    text = db.Column(db.String(255), nullable=False)
    matiere = db.Column(db.String(50), nullable=False)  # Champ de matière

    def __repr__(self):
        return f'<Homework {self.date} - {self.text} - {self.matiere}>'


class Matiere(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    id_classe = db.Column(db.Integer, db.ForeignKey('classe.id'), nullable=False)  # Foreign key to the Classe table
    nomMatiere = db.Column(db.String(255), nullable=False)
    mainChemin = db.Column(db.String(200), nullable=False)
    idf = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return f'<Matiere {self.date} - {self.nomMatiere}>'

class Cour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomCour = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    chemin = db.Column(db.String(200), nullable=False)
    id_matiere = db.Column(db.Integer, db.ForeignKey('matiere.id'), nullable=False)
    def __repr__(self):
        return f'<Matiere {self.date} - {self.nomCour}>'


class Classe(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)  # Unique ID for each class
    nomClasse = db.Column(db.String(60), nullable=False)  # Name of the class
    users = db.relationship('User', backref='classe', lazy=True)
    def __repr__(self):
        return f'<Classe {self.nomClasse}>'


class Message(db.Model):
    __bind_key__ = 'messages'
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    id_classe = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(300), nullable=True)
    code = db.Column(db.String(1000), nullable=True)
    file = db.Column(db.String(200), nullable=True)
    type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    sender_id = db.Column(db.Integer, nullable=False)  # Juste un entier, pas de clé étrangère
    def __repr__(self):
        return f'<Message {self.date} - {self.id} - content : {self.content}>'



class User(db.Model):
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


