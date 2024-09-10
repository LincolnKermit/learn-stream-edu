document.addEventListener('DOMContentLoaded', function() {
    const terminalOutput = document.getElementById('output');
    const commandInput = document.getElementById('command-input');

    // Simuler un système de fichiers (reset à chaque reload)
    let fileSystem = {
        '/': {
            type: 'dir',
            content: {
                'file1.txt': { type: 'file', content: 'Contenu du fichier 1' },
                'file2.txt': { type: 'file', content: 'Contenu du fichier 2' },
                'hiddenfile': { type: 'file', content: 'Fichier caché', hidden: true },
                'folder1': { type: 'dir', content: {} }
            }
        }
    };

    let currentDirectory = '/';  // Répertoire actuel

    const commands = {
        ls: function(options) {
            const dir = getCurrentDirectory();
            if (!dir) {
                return "Erreur : répertoire introuvable.";
            }
            let output = '';
            const files = Object.keys(dir.content);

            files.forEach(file => {
                if (dir.content[file].hidden && !options.includes('-a')) {
                    // Ne pas afficher les fichiers cachés sauf si '-a' est utilisé
                    return;
                }
                output += file + (dir.content[file].type === 'dir' ? '/' : '') + '\n';
            });

            if (!output) {
                output = 'Aucun fichier ou répertoire.';
            }
            return output.trim();
        },
        pwd: function() {
            return currentDirectory;
        },
        cd: function(options) {
            if (options.length === 0) {
                return "Erreur : chemin manquant pour la commande 'cd'.";
            }

            const targetDir = options[0];

            if (targetDir === '..') {
                // Remonter d'un niveau si possible
                if (currentDirectory !== '/') {
                    currentDirectory = currentDirectory.substring(0, currentDirectory.lastIndexOf('/')) || '/';
                }
                return currentDirectory;
            } else if (targetDir === '/') {
                currentDirectory = '/';
                return currentDirectory;
            } else {
                const newDir = getCurrentDirectory().content[targetDir];
                if (newDir && newDir.type === 'dir') {
                    currentDirectory += (currentDirectory === '/' ? '' : '/') + targetDir;
                    return currentDirectory;
                } else {
                    return `Erreur : répertoire '${targetDir}' introuvable.`;
                }
            }
        },
        mkdir: function(options) {
            if (options.length === 0) {
                return "Erreur : nom du répertoire manquant pour 'mkdir'.";
            }

            const dirName = options[0];
            const currentDir = getCurrentDirectory();

            if (currentDir.content[dirName]) {
                return `Erreur : un fichier ou répertoire nommé '${dirName}' existe déjà.`;
            }

            currentDir.content[dirName] = { type: 'dir', content: {} };
            return `Répertoire '${dirName}' créé.`;
        },
        rm: function(options) {
            if (options.length === 0) {
                return "Erreur : nom du fichier ou répertoire manquant pour 'rm'.";
            }

            const target = options[0];
            const currentDir = getCurrentDirectory();

            if (!currentDir.content[target]) {
                return `Erreur : fichier ou répertoire '${target}' introuvable.`;
            }

            delete currentDir.content[target];
            return `Fichier ou répertoire '${target}' supprimé.`;
        },
        echo: function(options) {
            return options.join(' ');
        },
        help: function(options) {
            const availableCommands = "Commandes disponibles : ls, pwd, cd, mkdir, rm, echo, cat.";
            if (options.length === 0) {
                return "Utilisation : /help [command]. " + availableCommands;
            }
            const cmd = options[0];
            if (commands[cmd]) {
                return `${cmd}: ${commands[cmd].description || 'Aucune description disponible.'}`;
            } else {
                return `Commande inconnue : ${cmd}. ${availableCommands}`;
            }
        },
        cat: function(options) {
            if (options.length === 0) {
                return "Erreur : fichier manquant pour 'cat'.";
            }

            const fileName = options[0];
            const file = getCurrentDirectory().content[fileName];

            if (file && file.type === 'file') {
                return file.content;
            } else {
                return `Erreur : fichier '${fileName}' introuvable.`;
            }
        },
        '>': function(output, fileName) {
            // Rediriger la sortie vers un fichier
            getCurrentDirectory().content[fileName] = { type: 'file', content: output };
            return `Sortie redirigée vers ${fileName}`;
        }
    };

    // Ajouter des descriptions aux commandes
    commands.ls.description = "Liste les fichiers et répertoires. Options : -a (affiche tous les fichiers), -l (détails).";
    commands.pwd.description = "Affiche le répertoire de travail actuel.";
    commands.cd.description = "Change de répertoire.";
    commands.mkdir.description = "Crée un nouveau répertoire.";
    commands.rm.description = "Supprime des fichiers ou répertoires. Option : -r (suppression récursive).";
    commands.echo.description = "Affiche un texte dans le terminal.";
    commands.cat.description = "Affiche le contenu d'un fichier.";

    commandInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            const input = commandInput.value.trim();
            processCommand(input);
            commandInput.value = '';  // Clear the input
        }
    });

    function processCommand(input) {
        if (input.includes('&&')) {
            // Gestion des commandes multiples avec &&
            const cmds = input.split('&&').map(cmd => cmd.trim());
            let success = true;
            cmds.forEach(cmd => {
                if (success) {
                    const result = executeCommand(cmd);
                    if (result.includes('Erreur')) {
                        success = false;
                    }
                    addOutput(result);
                }
            });
        } else if (input.includes('>')) {
            // Gestion de la redirection de sortie >
            const parts = input.split('>');
            const cmd = parts[0].trim();
            const fileName = parts[1].trim();
            const output = executeCommand(cmd);
            addOutput(commands['>'](output, fileName));
        } else {
            // Commande unique
            addOutput(executeCommand(input));
        }
    }

    function executeCommand(input) {
        const parts = input.split(' ');
        const command = parts[0];
        const options = parts.slice(1);  // Options de la commande

        if (command.startsWith('/help')) {
            return commands.help(options);
        } else if (commands[command]) {
            return commands[command](options);
        } else {
            return `${command}: commande non trouvée.`;
        }
    }

    function getCurrentDirectory() {
        const pathParts = currentDirectory.split('/').filter(Boolean);
        let dir = fileSystem['/'];

        pathParts.forEach(part => {
            if (dir.content[part] && dir.content[part].type === 'dir') {
                dir = dir.content[part];
            } else {
                dir = null;
            }
        });

        return dir;
    }

    function addOutput(text) {
        const newLine = document.createElement('div');
        newLine.textContent = `user@bts-ciel-eb:~$ ${text}`;
        terminalOutput.appendChild(newLine);
        terminalOutput.scrollTop = terminalOutput.scrollHeight;  // Scroll to bottom
    }
});
