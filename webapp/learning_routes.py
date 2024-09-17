from flask import Blueprint, render_template
from py.model import Cour

# Créer le Blueprint pour la section "learning"
learning_bp = Blueprint('learning', __name__, template_folder='templates')

# Routes "learning"
@learning_bp.route('/learning_redirect')
def learning_redirect():
    cours = Cour().query.all()
    return render_template('learning/learning_main.html', lessons=cours)

#route cpp
@learning_bp.route("/learning/cpp")
def learning_cpp():
    return render_template('/learning/cpp/Cpp.html')

@learning_bp.route("/learning/cpp/Lesbases")
def learning_cpp_Lesbases():
    return render_template('/learning/cpp/Lesbases.html')

@learning_bp.route("/learning/cpp/Operateurs")
def learning_cpp_Operateurs():
    return render_template('/learning/cpp/Operateurs.html')

@learning_bp.route("/learning/cpp/Variables")
def learning_cpp_Variables():
    return render_template('/learning/cpp/TypeVariables.html')

@learning_bp.route("/learning/cpp/Structure")
def learning_cpp_Structure():
    return render_template('/learning/cpp/Structure.html')

@learning_bp.route("/learning/cpp/Pointeurs")
def learning_cpp_Pointeurs():
    return render_template('/learning/cpp/Pointeurs.html')

@learning_bp.route("/learning/cpp/Allocation_Dynamique")
def learning_cpp_Allocation_Dynamique():
    return render_template('/learning/cpp/AllocationDynamique.html')

@learning_bp.route("/learning/cpp/Exemple")
def learning_cpp_Exemple():
    return render_template('/learning/cpp/Exemple.html')
#--------------------


#route cmd
@learning_bp.route("/learning/cmd")
def learning_cmd():
    return render_template('/learning/cmd/Cmd.html')
#------------------