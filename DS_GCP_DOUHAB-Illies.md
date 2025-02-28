Création d'un Service Account :
    1. Aller dans la console GCP → IAM & Admin → Service Accounts.
    2. Cliquer sur "Créer un service account", lui donner un nom.
    3. Définir les rôles nécessaires (principe du moindre privilège).
    4. Générer une clé JSON uniquement si nécessaire et la stocker en sécurité (éviter de l’exposer dans un repo).
    5. Activer la rotation régulière des clés et supprimer celles inutilisées.
Création d'un Bucket :
    1. Aller dans la console GCP → Cloud Storage → Buckets → "Créer un bucket".
    2. Choisir un nom unique, la localisation (régionale/multi-régionale pour la performance).
    3. Définir la classe de stockage (Standard, Nearline, Coldline, Archive selon la fréquence d’accès).
    4. Configurer la politique de rétention pour éviter des suppressions accidentelles.
    5. Activer le chiffrement et limiter les accès via IAM pour renforcer la sécurité.
Gestion des droits (IAM) :
IAM permet de contrôler qui a accès à quelles ressources.
Exemple : Pour restreindre l'accès à un bucket critique :
    • Aller sur IAM, ajouter un utilisateur spécifique avec le rôle Storage Object Viewer au lieu de Storage Admin.
    • Utiliser les Conditions IAM pour restreindre l’accès à certaines heures ou adresses IP.
Configuration de la facturation :
    1. Aller dans la console GCP → Facturation → Lier un compte de facturation.
    2. Configurer des budgets et des alertes pour éviter les dépassements.
    3. Activer la facturation détaillée et surveiller les dépenses avec Cost Explorer.
    4. Utiliser des quotas pour éviter une consommation excessive des ressources.

Regle de Vie :
       « Au revois, Bonne journée »
