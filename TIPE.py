#Il est conseillé, pour la comprehension de l'utilité de chaque fonction, de lire en parallèle le fichier descriptif_code_TIPE.pdf


import networkx as nx
import random as rd
import matplotlib.pyplot as plt
import math

            ##                       ##
            ## PARTIE CHEMINS CONNUS ##
            ##                       ##

## PARTIE DESSIN
def generateDicoPosition(longueur,largeur):
    dico={}
    for i in range(largeur):
        for j in range(longueur):
            dico[(i,j)]=(i,j)
    return(dico)
    
def dessine(graphe,longueur,largeur):
    nx.draw_networkx(graphe,generateDicoPosition(longueur,largeur))
    plt.show()

def dessine_noname(graphe,longueur,largeur):
    nx.draw(graphe,generateDicoPosition(longueur,largeur))
    plt.show()

## PARTIE GENERATION CHEMIN CONNU
def generate(longueur,largeur,probarete,fonctionpoids,parampoids):
    graph=nx.Graph()
    #Création des noeuds
    for i in range(largeur):
        for j in range(longueur):
            graph.add_node((i,j))
    #Création des aretes
    for i in range(largeur):
        for j in range(longueur):
            if i!=(largeur-1) and rd.random()>1-probarete:
                graph.add_edge((i,j),(i+1,j),weight=fonctionpoids((i,j),(i+1,j),graph,parampoids))
            if j!=(longueur-1) and rd.random()>1-probarete:
                graph.add_edge((i,j),(i,j+1),weight=fonctionpoids((i,j),(i,j+1),graph,parampoids))
    return(graph)
    
def generateConnexe(longueur,largeur,probarete,limite,fonctionpoids,parampoids):
    i=0
    g=generate(longueur,largeur,probarete,fonctionpoids,parampoids)
    while not(nx.is_connected(g)) and i<limite:
        i+=1
        g=generate(longueur,largeur,probarete,fonctionpoids,parampoids)
    if nx.is_connected(g):
        return g
    else:
        raise nx.ExceededMaxIterations('Pas de graphe connexe généré avant '+str(limite)+' itérations')
    return

def generateSensUnique(longueur,largeur,probarete,probsensunique,fonctionpoids,parampoids):
    graph=nx.DiGraph()
    #Création des noeuds
    for i in range(largeur):
        for j in range(longueur):
            graph.add_node((i,j))
    #Création des aretes
    for i in range(largeur):
        for j in range(longueur):
            if i!=(largeur-1) and rd.random()>1-probarete:  #Arete ?
                if rd.random()>1-probsensunique:                #Arete à sens unqiue ?
                    if rd.random()>0.5:                             #Sens de l'arete à sens unique ?
                        graph.add_edge((i,j),(i+1,j),weight=fonctionpoids((i,j),(i+1,j),graph,parampoids))
                    else:
                        graph.add_edge((i+1,j),(i,j),weight=fonctionpoids((i+1,j),(i,j),graph,parampoids))
                else:
                    graph.add_edge((i,j),(i+1,j),weight=fonctionpoids((i,j),(i+1,j),graph,parampoids))
                    graph.add_edge((i+1,j),(i,j),weight=fonctionpoids((i+1,j),(i,j),graph,parampoids))
            if j!=(longueur-1) and rd.random()>1-probarete:
                if rd.random()>1-probsensunique:
                    if rd.random()>0.5:
                        graph.add_edge((i,j),(i,j+1),weight=fonctionpoids((i,j),(i,j+1),graph,parampoids))
                    else:
                        graph.add_edge((i,j+1),(i,j),weight=fonctionpoids((i,j+1),(i,j),graph,parampoids))
                else:
                    graph.add_edge((i,j),(i,j+1),weight=fonctionpoids((i,j),(i,j+1),graph,parampoids))
                    graph.add_edge((i,j+1),(i,j),weight=fonctionpoids((i,j+1),(i,j),graph,parampoids))
    return(graph)
    
def generateConnexeSensUnique(longueur,largeur,probarete,probsensunique,limite,fonctionpoids,parampoids):
    i=0
    g=generateSensUnique(longueur,largeur,probarete,probsensunique,fonctionpoids,parampoids)
    while not(nx.is_strongly_connected(g)) and i<limite:
        i+=1
        g=generateSensUnique(longueur,largeur,probarete,probsensunique,fonctionpoids,parampoids)
    if nx.is_strongly_connected(g):
        return g
    else:
        raise nx.ExceededMaxIterations('Pas de graphe fortement connexe généré avant '+str(limite)+' itérations')

## PARTIE RESULTATS CONNEXITE
def propconnex(n,longueur,largeur,probArete):
    compteur=0
    for i in range(n):
        g=generate(longueur,largeur,probArete,constante,1)
        if nx.is_connected(g):
            compteur+=1
    return compteur/n
def resultats_connexite_taille(nbEssais,probArete,i):
    y=[]
    for taille in range(5,51):
        y+=[propconnex(nbEssais,taille,taille,probArete)]
        print(i,taille)
    return(y)
    
def resultats_connexite(nbEssais):
    x=range(5,51)
    for i in range(1,10):
        probArete=1-(0.05*i)
        y=resultats_connexite_taille(nbEssais,probArete,i)
        plt.plot(x,y)
    plt.show()
        
## PARTIE PROBA
def constante(depart,arrive,graph,parametre):
    return parametre
    
def uniforme(depart,arrive,graph,parametre):
    inf,sup=parametre
    return rd.randint(inf,sup)
    
## PARTIE INTERCEPTION CHEMINS CONNUS
def temoin_connus(graph,chemin,cop):
    #Calcul du temps que va mettre le mobile a rejoindre chacun des noeuds de son chemin
    tempsCible=[0]
    for i in range(1,len(chemin)):
        tempsCible+=[tempsCible[-1]+graph[chemin[i-1]][chemin[i]]['weight']]
    
    #Calcul du meilleur point d'interception
    tempsIntercepteur=0
    CheminArrive=nx.shortest_path(graph,source=cop,target=chemin[-1],weight='weight')
    for i in range(len(CheminArrive)-1):
        tempsIntercepteur+=graph[CheminArrive[i]][CheminArrive[i+1]]['weight']
    i=1
    while i<(len(chemin)+1) and tempsIntercepteur+graph[chemin[-i]][chemin[-(i+1)]]['weight']<=tempsCible[-(i+1)]: #Tant qu'on peut rebrousser chemin sans rencontrer la cible, on continue
        tempsIntercepteur+=graph[chemin[-i]][chemin[-(i+1)]]['weight']
        i+=1
    return (chemin[-i],max(tempsIntercepteur,tempsCible[-i]))

def dijkstraAdapte(graph,chemin,cop):
    d={} #Initialisation de l'algorithme classique
    sommets=list(graph.nodes)
    for n in sommets:
        d[n]=math.inf
    d[cop]=0
        
    #Calcul du temps que va mettre le mobile a rejoindre chacun des noeuds de son chemin
    tempsMobile=[0]
    for i in range(1,len(chemin)):
        tempsMobile+=[tempsMobile[-1]+graph[chemin[i-1]][chemin[i]]['weight']]
    
    def mini_distance(sommets):
        min=math.inf
        for n in sommets:
            if d[n]<min:
                min=d[n]
                s=n
        return s
    
    def maj_distance(s1,s2):
        if d[s2]>d[s1]+graph[s1][s2]['weight']:
            d[s2]=d[s1]+graph[s1][s2]['weight']
    
    noeudsAParcourir=len(chemin) #Nombre de noeud dont on a pas encore le temps minimum pour les rejoindre
    interceptionPotentielle=[] #Liste de noeud où l'interception est possible
    while noeudsAParcourir>1 and sommets!=[]: #Tant que tous les noeuds du chemin n'ont pas leure distance minimum, il faut continuer
        s=mini_distance(sommets)
        sommets.remove(s)
        for i in range(len(chemin)):
            if s==chemin[i]: #Si on étudie un noeud du chemin, c'est qu'on a trouve le temps minimum pour l'atteindre
                noeudsAParcourir-=1 #Donc on enlève 1 au nombre de noeuds dont on a pas le temps minimum
                if tempsMobile[i]>=d[chemin[i]]:
                    interceptionPotentielle+=[(chemin[i],tempsMobile[i])] #On l'ajoute à la liste des noeuds d'interception si on peut intercepter en ce noeud
        for n in list(nx.neighbors(graph,s)):
            maj_distance(s,n)
    #On ajoute le dernier noeud du chemin à la liste des noeuds d'interception
    interceptionPotentielle+=[(chemin[-1],max(tempsMobile[-1],d[chemin[-1]]))]
    
    #On trouve le meilleur noeuds d'interception
    tempsmin=math.inf
    for c in interceptionPotentielle:
        noeud,temps=c
        if temps<tempsmin:
            noeudmin=noeud
            tempsmin=temps
    return (noeudmin,tempsmin) #La version pour trouver le chemin n'est pas beaucoup plus compliquée

## PARTIE RESULTAT INTERCEPTION CONNU
def generateurChemin(graph,longueur,largeur,tailleChemin):
    chemin=[(rd.randint(0,longueur-1),rd.randint(0,largeur-1))]
    for i in range(tailleChemin-1):
        possibilite=list(nx.neighbors(graph,chemin[-1]))
        chemin+=[possibilite[rd.randint(0,len(possibilite)-1)]]
    return chemin

def generateurPosition(graph,longueur,largeur):
    return (rd.randint(0,longueur-1),rd.randint(0,largeur-1))

def temps_intercept_moyen(n,longueur,largeur,probArete,fonctionPoids,paramPoids,tailleChemin):
    tempsDijkstra=0
    tempsTemoin=0
    for i in range(n):
        g=generateConnexe(longueur,largeur,probArete,math.inf,fonctionPoids,paramPoids)
        chemin=generateurChemin(g,longueur,largeur,tailleChemin)
        cop=generateurPosition(g,longueur,largeur)
        a,tempsARajouter=temoin_connus(g,chemin,cop)
        tempsTemoin+=tempsARajouter
        a,tempsARajouter=dijkstraAdapte(g,chemin,cop)
        tempsDijkstra+=tempsARajouter
    return(tempsTemoin/n,tempsDijkstra/n)

def resultats_interception_connu_taille(nbEssais,probArete,i):
    temoin=[]
    dijkstra=[]
    for taille in range(5,21):
        print(i,taille)
        temoinAAjouter,dijkstraAAjouter=temps_intercept_moyen(nbEssais,taille,taille,probArete,constante,1,taille)
        temoin+=[temoinAAjouter]
        dijkstra+=[dijkstraAAjouter]
    return(temoin,dijkstra)

def resultat_interception_connu(nbEssais):
    x=range(5,21)
    for i in range(1,6):
        probArete=1-(0.05*i)
        temoin,dijkstra=resultats_interception_connu_taille(nbEssais,probArete,i)
        plt.plot(x,temoin,'o')
        plt.plot(x,dijkstra)
    plt.show()

            ##                         ##
            ## PARTIE CHEMINS INCONNUS ##
            ##                         ##

##PARTIE DESSIN
def racinesNieme(n):
    d={}
    for i in range(n):
        d[i]=(math.cos(2*i*math.pi/n),math.sin(2*i*math.pi/n))
    return d

def dessineGPE(graphe,n):
    nx.draw_networkx(graphe,racinesNieme(n))
    plt.show()

def dessineGPE_noname(graphe,n):
    nx.draw(graphe,racinesNieme(n))
    plt.show()

##PARTIE GENERATEUR CHEMIN INCONNU
def generateurGPEC(n,fct_probArete):
    graph=nx.Graph()
    #Création des noeuds
    for i in range(n):
        graph.add_node(i)
    #Création des aretes du contour
    graph.add_edge(n-1,0)
    for i in range(n-1):
        graph.add_edge(i,i+1)
    
    #Création des aretes interieures
    voisinsPossibles=[] #Liste des listes des voisins avec les-quels le noeud peut " créer une arête
    for i in range(n):
        voisinsPossibles+=[[k for k in range(i+2,i+math.ceil(n/2))]]
    for s1 in range(n):
        for s2 in voisinsPossibles[s1]:
            if rd.random()>1-fct_probArete(s1,s2):
                graph.add_edge(s1,s2%n)
                if s2>=n:
                    for int in range(s1+1,s2): #On retire les possibilités de liaison des noeuds enfermés "à l'interieur" avec ceux "à l'exterieur" de l'arête
                        for ext in range(s2%n+1,s1):
                            if ext in voisinsPossibles[int%n]:
                                voisinsPossibles[int%n].remove(ext) #On retire les possibilités de liaison des noeuds enfermés "à l'interieur" avec ceux "à l'exterieur" de l'arête
                            if ext+n in voisinsPossibles[int%n]:
                                voisinsPossibles[int%n].remove(ext+n)
                            if int%n in voisinsPossibles[ext]:
                                voisinsPossibles[ext].remove(int%n) #Et inversement...
                            if int in voisinsPossibles[ext]:
                                voisinsPossibles[ext].remove(int)
                else:
                    for int in range(s1+1,s2):
                        for ext in range(s2+1,s1+n):
                            if ext%n in voisinsPossibles[int]:
                                voisinsPossibles[int].remove(ext%n)
                            if ext in voisinsPossibles[int]:
                                voisinsPossibles[int].remove(ext) 
                            if int in voisinsPossibles[ext%n]:
                                voisinsPossibles[ext%n].remove(int)
                            if int+n in voisinsPossibles[ext%n]:
                                voisinsPossibles[ext%n].remove(int+n)
                print(voisinsPossibles)
    return(graph)

##PARTIE PROBA
def demiInverseLongeur(i,j):
    return 1/(2*(j-i-1))
