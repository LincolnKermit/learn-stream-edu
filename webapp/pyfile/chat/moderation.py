
bloquer = [
    'fdp', 'enculer', 'enculer', 'nazi', 'zizi', 'enculé', 'salope', 'connard', 'conasse',
    'batard', 'pute', 'tarlouze', 'abruti', 'couillon', 'débile',
    'idiot', 'imbécile', 'crétin', 'enfoiré', 'sacréconnard', 'pédé', 'filsdepute',
    'salaud', 'ordure', 'salo', 'taré', 'chien', 'branleur', 'branleuse',
    'clochard', 'imbecil', 'crétin', 'vieuxcon', 'racaille', 'salepute', 'tapette',
    'cocu', 'satané', 'chiotte', 'con', 'nul', 'dégénéré', 'enculédenazi', 'saloch',
    'sousmerde', 'malade', 'goujat', 'truie', 'pédale', 'connarde', 'pauvrecon',
    'crevure', 'grosporcdégueulasse', 'grosconnard', 'raclure', 'povtype', 'filsdemerde'
]

def testAll(msg):
    msg = remove_char_special(msg)
    msg = remove_space_between(msg)
    msg = remove_number(msg)
    if detect_prohibited_word(msg):
        return "[bloqué]"    
    return msg



def detect_prohibited_word(msg):
    # Vérifier si le message sans espace contient un mot interdit
    for mot in bloquer:
        if mot in msg:
            return True  # Si un mot interdit est trouvé, renvoyer "[bloqué]"

    return False # Sinon renvoyer le message original


def remove_space_between(word):
    """remove space between all letter
    Args:
        word (string): string to remove space 

    Returns:
        _type_: _description_
    """
    new_word = ""
    for letter in word:
        if letter != ' ':
            new_word += letter
    word = new_word
    return word


def remove_char_special(word):
    """
    Supprime les caractères spéciaux d'une chaîne de caractères, tels que '_', '-', '*', '=', etc.

    Args:
        word (str): La chaîne de caractères d'entrée.

    Returns:
        str: La chaîne de caractères sans les caractères spéciaux spécifiés.
    """
    new_word = ""
    special_chars = ['_', '-', '*', '=', '#', '@', '!', '$', '%', '^', '&', '(', ')', '{', '}', '[', ']', '|', '\\', '/', ':', ';', '"', "'", '<', '>', ',', '.', '?', '+']

    for letter in word:
        if letter not in special_chars:
            new_word += letter

    return new_word

def remove_consecutive_duplicates(msg):
    """
    Supprime les caractères consécutifs qui sont des doublons ou des triplons dans une chaîne de caractères.

    Args:
        msg (str): La chaîne d'entrée contenant potentiellement des doublons consécutifs.

    Returns:
        str: La chaîne après avoir supprimé les doublons consécutifs.
    """
    if not msg:
        return msg

    result = msg[0]  # Commence avec le premier caractère
    count = 1  # Compte l'occurrence des caractères consécutifs

    for i in range(1, len(msg)):
        if msg[i] == msg[i - 1]:  # Vérifie si le caractère courant est égal au précédent
            count += 1
        else:
            count = 1  # Réinitialise le compte si le caractère change

        if count < 3:  # N'ajoute que si le caractère n'a pas été répété 3 fois ou plus
            result += msg[i]

    return result

def remove_number(word):
    """Remove all numberr

    Args:
        word (String): word which u wants to delete remove number

    Returns:
        String : word with no numbers 
    """
    new_word = ""
    number = ['0', '1', '2', '3', '4', '5', '6', '7', '9']

    for letter in word:
        if letter not in number:
            new_word += letter

    return new_word


def custom_split(string):
    words = []      # Liste pour stocker les mots
    current_word = ""  # Chaîne temporaire pour accumuler un mot

    for char in string:
        if char != ' ':  # Si le caractère n'est pas un espace
            current_word += char  # Ajouter le caractère au mot en cours
        else:
            if current_word:  # Si on a un mot en cours (pour éviter les espaces multiples)
                words.append(current_word)  # Ajouter le mot à la liste
                current_word = ""  # Réinitialiser le mot en cours
    
    if current_word:  # Ajouter le dernier mot s'il existe
        words.append(current_word)

    return words


def special_in(substring, string):
    """
    Vérifie si une sous-chaîne (substring) est présente dans une chaîne principale (string), 
    en parcourant la chaîne principale caractère par caractère et en comparant les sous-chaînes de même longueur.

    Args:
        substring (str): La sous-chaîne à rechercher dans la chaîne principale.
        string (str): La chaîne principale dans laquelle rechercher la sous-chaîne.

    Returns:
        bool: Retourne True si la sous-chaîne est trouvée dans la chaîne principale, sinon False.

    Exemple:
        >>> special_in("abc", "xyzabcdef")
        True
        >>> special_in("ghi", "xyzabcdef")
        False
    """
    len_sub = len(substring)
    len_str = len(string)

    # Parcourir la chaîne principale pour vérifier la présence du sous-mot
    for i in range(len_str - len_sub + 1):
        if string[i:i + len_sub] == substring:  
            return True
    return False