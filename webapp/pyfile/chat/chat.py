from datetime import datetime
import os
from flask import Blueprint, redirect, render_template, request, send_file, send_from_directory, session, current_app, url_for
from werkzeug.utils import secure_filename
from pyfile.config.model import Classe, Message, User, TYPE
from extensions import socketio, app  # Importer socketio et db depuis extensions.py
from flask_socketio import send, join_room, leave_room
from decoration import student_required
from pyfile.db import db
from pyfile.chat.moderation import testAll
from pathlib import Path

chat = Blueprint('chat', __name__, template_folder='templates')

# Page du chat
@student_required
@chat.route('/chat_room', methods=['GET', 'POST'])
def chat_room():
    username = session.get('username')
    classe = Classe.query.get(session.get('id_classe'))
    if not username or not classe:
        return redirect(url_for('index'))
    
    # Charger les messages de la classe
    messages = Message.query.filter_by(id_classe=classe.id).order_by(Message.date.desc()).limit(30).all()
    files = Message.query.filter_by(id_classe=classe.id, type=2).order_by(Message.date.desc()).limit(30).all()
    files.reverse()
    return render_template('/class/chat.html', username=username, classe=classe, messages=messages, files=files)

@student_required
@chat.route('/upload_message', methods=['POST'])
def upload_message():
    msg = request.form.get('message', '').strip()
    file = request.files.get('file')
    user = User.query.filter_by(username=session.get('username')).first()
    room = session.get('id_classe')

    # Vérifier si le message est vide et qu'il n'y a pas de fichier
    if not msg and not file:
        return "Message ou fichier manquant", 400

    # Cas où seul un message est envoyé
    if msg and not file:
        # Vérification du contenu du message avec la fonction testAll
        if testAll(msg) == '[bloqué]':
            socketio.send(f'{session.get("username")}: [Message bloqué]', room=room)
            return '', 204

        # Créer un nouvel objet Message et l'ajouter à la base de données
        new_message = Message(
            id_classe=user.id_classe,
            content=msg,
            type=0,  # TYPE[0] pour les messages texte
            date=datetime.now(),
            sender_id=user.id,
            sender_username=user.username
        )
        db.session.add(new_message)
        db.session.commit()

        # Envoyer le message à la room via SocketIO
        socketio.send(f'{user.username}: {msg}', room=room)
        return '', 204

    # Cas où un fichier est joint
    if file:
        class_directory = os.path.join('classe', str(user.id_classe), 'uploads')
        Path(class_directory).mkdir(parents=True, exist_ok=True)

        filename = secure_filename(file.filename)
        filepath = os.path.join(class_directory, filename)

        # Sauvegarder le fichier sur le disque
        file.save(filepath)

        # Enregistrer le message avec fichier
        new_message = Message(
            id_classe=user.id_classe,
            content=(msg + " " + file.filename) if msg else file.filename,
            type=2,  # Assurez-vous que '2' correspond au type 'File'
            fileName=filename,
            filepath=filepath,
            date=datetime.now(),
            sender_id=user.id,
            sender_username=user.username
        )
        db.session.add(new_message)
        db.session.commit()

        # Envoyer un message à la room via SocketIO
        socketio.send(f'{user.username} a envoyé un fichier: {filename}', room=room)
        return '', 204


#------------ Upload et dowload file from chat ------------

# Gérer les téléchargements de fichiers
@student_required
@chat.route('/files/<filename>')
def uploaded_file(filename):
    user = User.query.filter_by(username=session.get('username')).first()

    if not user:
        return "Utilisateur non trouvé", 400

    if not secure_filename(filename):
        return "Fichier non trouvé", 404
    print(" \n\n\n"+ filename)
    return send_file(secure_filename(filename))

#-------------------------------------------------

#------------ entré sortie de la room ------------
# Gérer l'entrée dans la room 
@student_required
@socketio.on('join')
def on_join(data):
    username = session.get('username')
    room = session.get('id_classe')
    join_room(room)
    send(f'{username} a rejoint la room.', room=room)

# Gérer la sortie de la room
@student_required
@socketio.on('leave')
def on_leave(data):
    username = session.get('username')
    room = session.get('id_classe')
    leave_room(room)
    send(f'{username} a quitté la room.', room=room)
#-------------------------------------------------
