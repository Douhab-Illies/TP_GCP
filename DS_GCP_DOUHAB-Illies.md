# Reponse au quesitons



## Création d'un Service Account :
    1. Aller dans la console GCP → IAM & Admin → Service Accounts.
    2. Cliquer sur "Créer un service account", lui donner un nom.
    3. Définir les rôles nécessaires (principe du moindre privilège).
    4. Générer une clé JSON uniquement si nécessaire et la stocker en sécurité (éviter de l’exposer dans un repo).
    5. Activer la rotation régulière des clés et supprimer celles inutilisées.

## Création d'un Bucket :
    1. Aller dans la console GCP → Cloud Storage → Buckets → "Créer un bucket".
    2. Choisir un nom unique, la localisation (régionale/multi-régionale pour la performance).
    3. Définir la classe de stockage
    4. Configurer la politique de sécurite pour éviter des suppressions accidentelles.
    5. Activer le chiffrement si besoins

## Gestion des droits (IAM) :
IAM permet de contrôler qui a accès à quelles ressources.
Exemple : Pour restreindre l'accès à un bucket critique :
    • Aller sur IAM, ajouter un utilisateur spécifique avec le rôle Storage Object Viewer au lieu de Storage Admin.

## Configuration de la facturation :
    1. Aller dans la console GCP → Facturation → Lier un compte de facturation.
    2. Configurer des budgets et des alertes pour éviter les dépassements.
    3. Activer la facturation détaillée 
    4. Utiliser des quotas pour éviter une consommation excessive des ressources.


## Regle de Vie :
       « Merci Monsieur, Au revois, Bonne journée »



## GITHUB PROJECT :

https://github.com/Douhab-Illies/TP_GCP




## information 


L'application peut se déployer en cicd, la création d'un SA, bucket, et le run sont automatisé grace au pipline github et au terraform, 
le cloud build est aussi automatiser seulement grace au github pipline


Le compte github a le secret json



## Lien du Bucket : 

https://console.cloud.google.com/storage/browser/sto-illies-terr-cicd?hl=fr&inv=1&invt=AbqxNg&project=python-flask-443908


## L'application

L'application tourne sur un docker :

```Dockerfile
FROM python:3.10-slim

COPY . /opt/app
WORKDIR /opt/app

RUN pip3 install --no-cache-dir -r requirements.txt

ENV BUCKET=$BUCKET

EXPOSE 8080
CMD ["python3", "/opt/app/app_chemin.py"]
```

l'applciation tourne bien sur le cloud et répuère les information apres /app/ :

```Python3
from flask import Flask

app = Flask(__name__)

@app.route('/app/<name>')
def hello(name):
    return f'Hello {name}!'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
```



## Lien de l'application :

voici le lien de l'application 

https://cloud-run-app-jjnfm7mdya-ez.a.run.app/

pour faire un test :
https://cloud-run-app-jjnfm7mdya-ez.a.run.app/app/test

la page devrai afficher  :

```txt
Hello test!
```



## Les comptes 

Le compte sebastien.wachter.ext@univ-lille.fr peut voir toutes les informations du projet sans rien modifier

Et le compte  cicd-swa@notes-on-cloud-swa.iam.gserviceaccount.com peut ecrire et lires sur les buckets
