
# STARLAB

![Alt](https://i.imgur.com/fJxNPJi.png)
>Le menu principal du jeu!
## 1 Coucou!

Bonnnnjour à tous!
Vous n'imaginez même pas la satisfaction que j'ai à cet instant. J'ai commencé le projet en septembre dernier dans le cadre de ce tuto, voulant partager quelque chose de plus 'gros' que ce qui était demandé.

je me suis attaqué à trop gros... Vraiment, travailler aussi longtemps sur un projet (un exercice en plus), c'est extrêmement **démotivant**. J'ai eu des mois à vide où je ne programmais plus du tout, des journées où je pataugeais et ne faisais rien...
Mais bon c'est enfin là et c'est finit!

>Sinon rien à voir mais je viens de découvrir un super logiciel de capture d'écran (*gratuis*), qui reconnait tout seul les zones d'images à capturer et les envoi direct sur un hébergeur d'image, c'est beau, c'est magique [et c'est ici!](http://puush.me/)

Je disais donc... J'ai enfin finis ce projet. J'ai utilisé **Pygame** comme librairie externe pour programmer le jeu en fenêtré, crée les images une à une, et j'avais pour projet de créer les sons aussi, puis je me suis souvenu que mon but premier était *d'apprendre à programmer*, donc pas de sons.

Je sais que ce projet dépasse clairement les directives de l'exercice proposé dans ce tutoriel. J'ai voulu me faire plaisir et vous faire partager quelque chose de différent.
J'espère d'ailleurs que vous prendrez un peu de plaisir à découvrir ce petit jeu. :)

## 2 Les prérequis
![Alt](https://media.giphy.com/media/cALkoAIov3Y9a/giphy.gif)

Alors je commence par les choses qui fâchent, parce que c'est relou, ça ne va pas vous faire plaisir mais mon projet demande quelque prérequis.

### python 3.6+
Ouai bon en même temps, je vis avec mon époque ein. :P
J'aime trop les [f-string](https://www.pydanny.com/python-f-strings-are-fun.html), et c'est une feature de la **3.6**, Voila tout.

J'éspère franchement que vous savez gérer les différentes versions de python sur votre ordinateur parce que moi je galère x1000, et ça change en plus d'un système d'exploitation à l'autre, et d'une console de commande à l'autre.

C'est une des choses les plus **horribles** en python!
J'utilise pour ma part le shell bash de [git for windows](https://gitforwindows.org/), qui simule le shell Bash de linux avec ses mots clé type. Dans ce shell je peux, si j'ai plusieurs versions de python en même temps, demander à lancer le programme avec une version spécifique:
```
py -3.6 nomDuFichier.py
```
Et le mieux c'est de savoir utiliser [pyvenv](https://makina-corpus.com/blog/metier/2015/bien-configurer-son-environnement-de-developpement-python), encore une chose que je ne maîtrise pas mais je vais m'empresser de lire ce lien que je viens de trouver après l'écriture de ce lisez-moi, ça a l'air d'être très bon et concis!

### Pygame
![Alt](https://jeux.developpez.com/tutoriels/Pygame/images/pygame_logo.gif)

Bon là vous ne pourrez pas y échapper, à coup de:
> pip install pygame

Et le tour est joué.

### Moviepy
![Alt](https://zulko.github.io/moviepy/_images/logo.png)
Utilisé pour jouer ma cinématique au lancement du programme.
> pip install moviepy

Ou sinon, vous allez dans:
> /f_roboc/introduction/introduction.py

Et vous verrez dans l'initialisation de la classe la variable ```self._play_movie = True```. Mettez ```False``` à la place et vous n'aurez plus besoin de moviepy.
Vous pouvez toujours voir la cinematique dans le dossier introduction, c'est le fichier ```movie.mp4```.

Pour ceux qui ont installé moviepy, lors du premier lancement de mon jeu un sous-module s'installera, ce sera peut être un peu long mais voila, vous serez prévenu. ^^'

### English please!
![Alt](http://www.splyon.fr/wp-content/uploads/2017/12/i-want-you-to-speak-english-bs-base_1.png)
Je code en anglais, et je documente (*depuis la troisième réécriture de ce jeu*) en anglais! J'ai un petit niveau en anglais donc même pour moi c'est galère, mais faut s'y habituer, le monde de la programmation est un monde anglophone. :/
Vous verrez peut être quelques fautes d'anglais d'ailleurs.
> Si vous avez le courage de lire tous les fichiers de code, vous remarquerez que certains ont une documentation en français. C'est parce que je ne les ai pas retouchés depuis un moment et avant j'écrivais mes docs en français.

---
Si vous avez lu jusqu'ici, vous avez le minimum pour juger mon projet.
Peut être que vous n'aurez pas envie d'installer tout ça, que ça vous énerve de devoir aller aussi loin pour cet exercice. Je vous comprendrais et dans ce cas là, mettez la note que vous voulez, je sais bien que j'ai pris des risques.

## 3 Jouer au jeu

Je ne vais pas m'attarder sur cette partie, mais je vais juste vous dire comment y jouer:

- lancez ```roboc.py```. Une fois dans le menu principal, cliquez sur ```commencer```.
![Alt](https://i.imgur.com/8Oez97b.png)
Vous voila à l'écran de sélection de niveaux. Vous ne pouvez pas sélectionner de niveaux car le serveur n'est pas démarré.
- lancez ```server.py```.
![Alt](https://i.imgur.com/nbKfxbI.png)
Voila, le serveur reçoit en permanence (*tout les dixièmes de secondes*) des messages de notre client.
- notre client a une autre gueule, ont peut sélectionner une map. Les deux disponibles sont les deux même avec des spawners différents (j'en reparlerai dans la partie suivante).![Alt](https://i.imgur.com/8gPNwTg.png)
- Cliquez sur une carte (*la première est mieux, l'autre était pour les testes de collisions de héros, et a donc moins de spawners*).
- Vous voila dans l'écran d'attente!
![Alt](https://i.imgur.com/CnlOlnb.png)
Là vous ne pouvez rien faire de plus pour l'instant.
- Ouvrez un autre client en cliquant sur ```roboc.py```!
![Alt](https://i.imgur.com/8dUjnjT.png)
Magie! le bouton ```rejoindre```est maintenant actif. Vous savez à quoi je pense, bewi allez-y cliquez! :p
![Alt](https://i.imgur.com/HW8yn0V.png)
Beaucoup d'informations ici. Les boutons de gauche n'ont pas été programmés. La boîte de message à droite non plus.
- Vous avez 2 clients différents retournant la même fenêtre. Chaque client possède son propre personnage (*le premier ouvert contrôle l'astronaute, le second contrôle l'alien*).
- Chaque tour se joue en **10 secondes maximum**. Vous voyez la jauge de temps au milieu se remplir petit à petit. Cliquer sur ```Fin du tour```terminera le tour du personnage plus tôt.
- Quand le tour d'un personnage est passé, vous ne pouvez rien faire sur son écran et tout est grisé.
- Lorsque le tour est actif, vous pouvez: **bouger** (3 points de mouvement par personnage par tour), utiliser votre **pouvoir de transformation** (pour changer un bloc en un autre), ou **terminer votre tour plus rapidement** (fin du tour).
- pour bouger, c'est intuitif pointez votre souris vers des cases adjacents au héro.![Alt](https://i.imgur.com/X9Jqdn4.png)
> Les cases bleues sont des cases de mouvement.
- Cliquez sur la case bleu et vous vous déplacerez.
- Pour utiliser votre pouvoir de transformation, cliquez sur le gros bouton rouge à gauche de ```Fin du tour```:
- ![Alt](https://i.imgur.com/gfoA8Fo.png)
> les cases vertes sont les cases que l'ont peut transformer.

- Cliquez ensuite sur une case verte pour lancer l'animation. Cliquez n'importe où ailleurs pour sortir de cette vision, et pouvoir vous déplacer.
-Le but est d'arriver au vaisseau spatial (la sortie!):
![Alt](https://i.imgur.com/5wJkrZj.png)
> Bravo vous êtes trop fort!

Et voila. J'ai pas fait de portes mais j'ai crée des téléporteurs, **finissez votre mouvement dessus** et vous vous téléporterez vers l'autre téléporteur.

![Alt](https://media.giphy.com/media/ui1hpJSyBDWlG/giphy.gif)

## 4 la notation
![Alt](https://www.langtra.be/wp-content/uploads/2017/02/Pr%C3%A9paration-examen-toeic-toefl-690x270.jpg)

Bawey j'ai pas tout fait comme demandé, du coup:
 
 - **Serveur ou client premier**, ça c'est pas important car le jeu demandera quand même le serveur si on veut lancer la partie. A noter que le serveur est très stable, il ne crashera pas si ont quitte un client en cours de jeu, mais il se réinitialisera (merci les blocks de code  ```try: except:```). Pour les clients, c'est si ont quitte le serveur *normalement* il reviennent au menu principal avec un message d'erreur tout beau, mais parfois ils seront bloqués en jeu.
 - pour la **précision de la carte: c'est bon**. Je n'affiche par contre que 5 cartes maximum (*parce que j'allais pas passer ma vie à programmer un truc parfait :D*). Les cartes possèdent certaines règles pour être validés par le jeu (et donc importés). Bon je pense pas que vous allez vous amuser à en créer donc je ne vous les donne pas, mais vous pouvez faire un tour dans le fichier ```maps_importation.py``` dans ```f_roboc/select_level/``` pour vous faire une idée.
 - **placement aléatoire du robot**. J'ai voulu aller plus loin: j'ai crée des zones de placement (spawners en anglais) dans la carte même. Elles sont représentés par des points "```.```". Ensuite le programme choisis de placer les héros en fonction de ces zones.
 - **murer/percer une porte**. Bon là comme vous l'avez vu précédemment, c'est fait.
 - La **gestion du mouvement** est adapté à ce type de jeu, et j'ai limité le déplacement à 3 cases. C'est un choix personnel, pour créer quelque chose de plus équilibré.
 - **la documentation**. Tout est documenté, avec plus ou moins de précisions c'est sure.
 -  **la pertinence des tests**. Hahaha on y vient à ces tests! Déjà lancez cette commande depuis la racine du projet: ``` py -m unittest``` car j'ai tout mis dans un dossier à part et si vous faites pas ça les imports vont ch*** à base d'exceptions. Ensuite j'ai utilisé des threads pour simuler le serveur ou le client, ça m'a beaucoup aidé... Mais à la fin j'utilisais plus souvent [pdb](http://sametmax.com/debugger-en-python-les-bases-de-pdb/) ou des tests manuels. Donc j'ai pas tout testé. Il fallait que je finisse le projet, je ne pouvais pas passer 1 mois de plus dessus. Ceci dit j'ai testé mes modules du dossier ```constants``` et ça, ça m'a été très très utile. Au final même, je sais que j'utiliserai [pytest](http://sametmax.com/se-simplifier-les-tests-python-avec-pytest/) la prochaine fois, en appliquant le [test drivent developpement](https://openclassrooms.com/courses/testez-un-projet-python/decouvrez-le-test-driven-development) que j'aime beaucoup beaucoup!
 - **lisibilité et découpage du projet**. Le projet est archi-découpé vous en conviendrez. La lisibilité n'est pas toujours au top je l'avoue, j'ai fait en sorte d'être le plus claire possible (*j'ai re-factorisé entièrement le projet 2 fois*) mais certaines méthodes sont un peu compliqués.
 - **Ouverture à l'amélioration**. Normalement oui, j'ai bien découpé le projet pour ça.
 
 Voila pour ~~l'autocritique~~ l'explication sur mes choix vis à vis de la notation.

 ![Alt](https://media.giphy.com/media/GCvktC0KFy9l6/giphy.gif)
> Oui j'aime bien les images...

## 4 Le reste

Non là franchement, j'en peux plus d'écrire. Je vous donne le lien sur mon ancien jeu (qui se base sur le premier exercice de ce tutoriel!), où j'explique plus précisément le fonctionnement de pygame. C'est très concis et certainement pas la meilleure explication, mais vous aurez au moins une idée de comment ça marche. La différence de plus est que mon projet est encore plus découpé, avec une vrai arborescence (et qu'il n'y a pas de gestion de la caméra).
[le projet en question](https://github.com/8area8/Mysterious_labyrinth)

et [ce projet sur mon pofil github](https://github.com/8area8/StarLab-v2)

Donc voila, bonne correction. :)

![Alt](https://media.giphy.com/media/yoJC2El7xJkYCadlWE/giphy.gif)

> Written with [StackEdit](https://stackedit.io/).
