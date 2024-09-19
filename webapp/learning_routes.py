from functools import wraps
from flask import Blueprint, flash, redirect, render_template, session, url_for
from py.config.model import Matiere, User

# Créer le Blueprint pour la section "learning"
learning_bp = Blueprint('learning', __name__, template_folder='templates')


def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("Vous devez être connecté pour accéder à cette page.")
            return redirect(url_for('users.login'))
        
        user = User.query.filter_by(username=session['username']).first()
        if user.right == 'admin':
            return f(*args, **kwargs)

        if not user or user.right != 'student':
            flash("Vous n'avez pas les autorisations nécessaires pour accéder à cette page.")
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function

# Routes "learning"
@learning_bp.route('/learning_redirect')
@student_required
def learning_redirect():
    matiere = Matiere().query.all()
    return render_template('learning/learning_main.html', matieres=matiere)

#route cpp
@learning_bp.route("/learning/cpp")
@student_required
def learning_cpp():
    return render_template('/learning/cpp/Cpp.html')

@learning_bp.route("/learning/cpp/Lesbases")
@student_required
def learning_cpp_Lesbases():
    return render_template('/learning/cpp/Lesbases.html')

@learning_bp.route("/learning/cpp/Operateurs")
@student_required
def learning_cpp_Operateurs():
    return render_template('/learning/cpp/Operateurs.html')

@learning_bp.route("/learning/cpp/Variables")
@student_required
def learning_cpp_Variables():
    return render_template('/learning/cpp/TypeVariables.html')

@learning_bp.route("/learning/cpp/Structure")
@student_required
def learning_cpp_Structure():
    return render_template('/learning/cpp/Structure.html')

@learning_bp.route("/learning/cpp/Pointeurs")
@student_required
def learning_cpp_Pointeurs():
    return render_template('/learning/cpp/Pointeurs.html')

@learning_bp.route("/learning/cpp/Allocation_Dynamique")
@student_required
def learning_cpp_Allocation_Dynamique():
    return render_template('/learning/cpp/AllocationDynamique.html')

@learning_bp.route("/learning/cpp/Exemple")
@student_required
def learning_cpp_Exemple():
    return render_template('/learning/cpp/Exemple.html')
#--------------------


#route cmd
@learning_bp.route("/learning/cmd")
def learning_cmd():
    return render_template('/learning/cmd/Cmd.html')
#------------------

#route physique
@learning_bp.route("/learning/physique")
def learning_mesurage():
    return render_template('/learning/physique/Mesurage.html')
#------------------