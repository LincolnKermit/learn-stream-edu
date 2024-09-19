from functools import wraps
from flask import Blueprint, flash, redirect, render_template, session, url_for
from py.config.model import Matiere, User
from decoration import student_required
# Créer le Blueprint pour la section "learning"
learning_bp = Blueprint('learning', __name__, template_folder='templates')




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