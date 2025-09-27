pour lancer le projet suivez les étapes suivants dans l'ordre et à la lettre :


1) cloner le dépôt

			----cette méthode est pour ceux qui ont l'appli  GIT sur leur pc ----
	-avant de pouvoir cloner vous devez nécessairement avoir l'application "GiT BASH" sur votre PC  à fin de pouvoir taper les commandes 
	-ouvrez git Bash en tant que administrateur et saisissez la commande suivante "  git clone  https://github.com/jchri-cell/tontine_groupe5.git "
	-en suite chercher dans votre pc l'emplacement du fichier tontine_groupe5
	-vous pouvez voir le chemin d'accès où a été cloner le dossier avec la commande " pwd"
			----- cette méthode est pour ceux qui ne dispose pas de GIT-----
N.B : une autre méthode de cloner le dépôt serait de télécharger le fichier zip , pour ce faire :
 _  parmi les options de la bare de navigation ( je parle dela barre de navigation qui est à l'extrême gauche tout en haut ) il y'a une option "code" cliquer déçus , puis vous allez voir un bouton vert écris déçus "code" vous cliquez une nouvelle fois sur ca et là vous allez voir l'option "downloade zip"


2) une fois le dépôt cloner rendez vous sur MySQL workbench :
	- une fois dans MySQL workbench connectez vous avec votre compte(serveur) comme d'habitude
	- ouvrer une nouvelle page vide puis copier et  executer tout le bloc suivant :

                CREATE DATABASE tontine_groupe5 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
                CREATE USER 'junior1'@'localhost' IDENTIFIED BY 'junior23';
                GRANT ALL PRIVILEGES ON tontine_groupe5.* TO 'junior1'@'localhost';
                FLUSH PRIVILEGES;


3)puis rendez vous dans vs code :

	-chercher l'option "file" dans vs code 
	-puis cliquer sur "open folder" et chercher l'emplacement du fichier tontine_groupe5 (le fichier que vous avez cloner dans le dépôt)
	-puis vous ouvrez le terminal dans vs code et vous saisissez la commande suivante " python manage.py makemigrations "
	- en suite tapez la commande suivante " python manage.py migrate  " 
	-une fois les migrations effectués vous pouvez lancez l'application avec la commande " python manage.py runserver " 

N.B: après avoir fait les migrations , allez dans MySQL workbench et faite un "refresh" afin de voir toute les tables  de la base de donnée
