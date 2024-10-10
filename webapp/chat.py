from datetime import datetime
import os
from flask import Blueprint, app, redirect, render_template, request, send_from_directory, session, url_for
from werkzeug.utils import secure_filename
from pyfile.config.model import Classe, Message
from extensions import socketio, db  # Importer socketio et db depuis extensions.py
from flask_socketio import send, join_room, leave_room
from decoration import student_required

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
    messages = Message.query.filter_by(id_classe=classe.id).order_by(Message.date.asc()).all()
    return render_template('/class/chat.html', username=username, classe=classe, messages=messages)

# Gérer les messages
@student_required
@socketio.on('message')
def handle_message(msg):
    room = session.get('id_classe')
    username = session.get('username')
    # Filtrer les messages vides
    if not msg.strip():
        return

    # Filtrage des mots interdits
    mots_interdits = ['fdp', 'enculer', 'mot3']
    for mot in mots_interdits:
        if mot in msg.lower():
            send(f'{username}: [Message bloqué]', room=room)
            return

    # Enregistrer le message
    new_message = Message(
        id_classe=session.get('id_classe'),
        content=msg,
        type='text',
        date=datetime.now(),
        sender=session.get('user_id')
    )
    db.session.add(new_message)
    db.session.commit()

    # Envoyer le message à la room
    send(f'{username}: {msg}', room=room)

# Gérer l'envoi de fichiers
@student_required
@chat.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        room = session.get("id_classe")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        send(f'{session["username"]} a envoyé un fichier: {filename}', room=room)
    return '', 204

# Gérer les téléchargements de fichiers
@student_required
@chat.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

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
