# 🏠 House Price Prediction - Projet MLOps

## 📋 Vue d'ensemble

Ce projet est une application MLOps complète pour la prédiction du prix des maisons utilisant un modèle de **Random Forest Regressor**. Le projet implémente un pipeline end-to-end allant de la préparation des données, à l'entraînement du modèle, jusqu'au déploiement sur Azure Container Apps avec monitoring et détection de drift.




## 🎯 Objectif

Créer et déployer un modèle de Machine Learning pour prédire le prix des maisons à partir de caractéristiques telles que :
- **GrLivArea** : Surface habitable (sq ft)
- **BedroomAbvGr** : Nombre de chambres
- **FullBath** : Nombre de salles de bain complètes
- **YearBuilt** : Année de construction
- **TotalBsmtSF** : Surface du sous-sol (sq ft)




## 🏗️ Architecture du Projet

```
house_price_mlops/
│
├── 📁 data/                          # Données du projet
│   ├── house_prices.csv              # Données brutes originales
│   └── house_prices_clean.csv        # Données nettoyées (output de prepare_data.py)
│
├── 📁 app/                           # Application FastAPI
│   ├── __init__.py
│   ├── main.py                       # Point d'entrée FastAPI avec endpoints
│   ├── models.py                     # Modèles Pydantic pour validation
│   ├── utils.py                      # Fonctions utilitaires
│   └── drift_detect.py               # Module de détection de drift (KS-test)
│
├── 📁 model/                         # Modèles entraînés
│   └── house_price_model.pkl         # Modèle Random Forest sauvegardé
│
├── 📁 tests/                         # Tests automatisés
│   └── test_api.py                   # Tests pytest pour l'API
│
├── 📁 .github/                       # CI/CD GitHub Actions
│   └── workflows/
│       └── ci-cd.yml                 # Pipeline CI/CD complet
│
├── 📁 mlruns/                        # MLflow tracking (généré automatiquement)
│
├── 📄 prepare_data.py                # Script de préparation des données
├── 📄 train_model.py                 # Script d'entraînement avec MLflow
├── 📄 drift_data_gen.py              # Générateur de données pour test de drift
│
├── 📄 Dockerfile                     # Configuration Docker
├── 📄 .dockerignore                  # Fichiers exclus du build Docker
├── 📄 requirements.txt               # Dépendances Python
│
├── 📄 deploy.sh                      # Script de déploiement Azure (PowerShell)
├── 📄 test-deploiement.bat           # Script de test du déploiement
├── 📄 cleanup.sh                     # Script de nettoyage des ressources Azure
│
├── 📄 .gitignore                     # Fichiers ignorés par Git
└── 📄 README.md                      # Documentation (ce fichier)
```

## 🔄 Workflow MLOps

### 1. **Préparation des Données** (`prepare_data.py`)
- Charge les données depuis `data/house_prices.csv`
- Renomme les colonnes (suppression des espaces)
- Nettoie les valeurs manquantes
- Sauvegarde dans `data/house_prices_clean.csv`

### 2. **Entraînement du Modèle** (`train_model.py`)
- Utilise **MLflow** pour le tracking des expériences
- Divise les données (80% train / 20% test)
- Entraîne un **RandomForestRegressor** avec :
  - `n_estimators`: 100
  - `max_depth`: 10
  - `min_samples_split`: 5
- Calcule les métriques (RMSE, R², MSE)
- Génère des visualisations :
  - `prediction_vs_actual.png` : Prédictions vs valeurs réelles
  - `feature_importance.png` : Importance des features
- Enregistre le modèle dans MLflow et localement (`model/house_price_model.pkl`)

### 3. **API FastAPI** (`app/main.py`)
- **Endpoints disponibles** :
  - `GET /` : Page d'accueil de l'API
  - `GET /health` : Health check (vérifie que le modèle est chargé)
  - `POST /predict` : Prédiction de prix (accepte JSON avec les features)
  - `POST /drift/check` : Détection de drift entre données de référence et production
- **Monitoring** : Intégration avec Azure Application Insights
- **CORS** : Activé pour toutes les origines
- **Documentation** : Auto-générée sur `/docs` (Swagger UI) et `/redoc`

### 4. **Détection de Drift** (`app/drift_detect.py`)
- Utilise le **test de Kolmogorov-Smirnov** (KS-test)
- Compare les distributions des features entre :
  - Données de référence : `data/house_prices_clean.csv`
  - Données de production : `data/production_data.csv`
- Génère des rapports JSON dans `drift_reports/`
- Définit un seuil de détection (par défaut : p-value < 0.05)

### 5. **Containerisation** (`Dockerfile`)
- Image de base : `python:3.9-slim`
- Expose le port **8000**
- Installe les dépendances depuis `requirements.txt`
- Lance l'application avec `uvicorn`

### 6. **CI/CD** (`.github/workflows/ci-cd.yml`)
Pipeline GitHub Actions en 2 jobs :

**Job 1 : Test**
- Installation de Python 3.9
- Installation des dépendances
- Exécution des tests pytest avec couverture de code

**Job 2 : Build & Deploy** (uniquement sur branche `main`)
- Connexion à Azure
- Build de l'image Docker
- Push vers Azure Container Registry (ACR)
- Déploiement sur Azure Container Apps
- Vérification du health check

### 7. **Déploiement Azure**
- **Service** : Azure Container Apps
- **Registry** : Azure Container Registry (ACR)
- **Ressource Group** : `rg-mlops-house-price`
- **Location** : `centralus`
- **Ingress** : Externe (URL publique)

## 📊 Stack Technologique

### Backend & ML
- **Python 3.9**
- **FastAPI** 0.104.1 : Framework web asynchrone
- **Scikit-learn** 1.3.2 : Machine Learning
- **MLflow** 2.8.1 : Tracking et gestion des modèles
- **Pandas** 2.1.3 : Manipulation de données
- **NumPy** 1.26.2 : Calculs numériques
- **Joblib** 1.3.2 : Sauvegarde/chargement de modèles
- **Pydantic** 2.5.0 : Validation de données

### Monitoring & Observabilité
- **Azure Application Insights** : Logging et monitoring
- **OpenCensus** : Export de logs vers Azure

### Testing
- **Pytest** 7.4.3 : Framework de tests
- **Pytest-cov** 4.1.0 : Couverture de code
- **Httpx** 0.25.2 : Client HTTP pour tests

### DevOps
- **Docker** : Containerisation
- **GitHub Actions** : CI/CD
- **Azure CLI** : Déploiement cloud

## 🚀 Utilisation

### 1. Préparation des données
```bash
python prepare_data.py
```

### 2. Entraînement du modèle
```bash
python train_model.py
```

### 3. Lancer l'API localement
```bash
uvicorn app.main:app --reload
```
Accéder à la documentation : http://localhost:8000/docs

### 4. Faire une prédiction
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "GrLivArea": 1500.0,
    "BedroomAbvGr": 3,
    "FullBath": 2,
    "YearBuilt": 2000,
    "TotalBsmtSF": 800.0
  }'
```

### 5. Test de drift
```bash
# Générer des données de production avec drift
python drift_data_gen.py

# Vérifier le drift via l'API
curl -X POST "http://localhost:8000/drift/check?threshold=0.05"
```

### 6. Tests automatisés
```bash
pytest tests/ -v --cov=app
```

### 7. Build Docker
```bash
docker build -t house-price-api .
docker run -p 8000:8000 house-price-api
```

## 📈 Métriques du Modèle

Le modèle Random Forest calcule :
- **RMSE** (Root Mean Squared Error) : Erreur quadratique moyenne
- **R²** (Coefficient de détermination) : Qualité de l'ajustement (0-1)
- **MSE** (Mean Squared Error) : Erreur quadratique moyenne

## 🔍 Monitoring & Observabilité

- **Application Insights** : Logs structurés avec dimensions personnalisées
- **Health Check** : Endpoint `/health` pour vérifier l'état du service
- **Drift Detection** : Surveillance continue de la distribution des données
- **MLflow UI** : Visualisation des expériences ML (`mlflow ui --port 5000`)

## 🔐 Configuration

Variables d'environnement :
- `MODEL_PATH` : Chemin vers le modèle (défaut : `model/house_price_model.pkl`)
- `APPLICATIONINSIGHTS_CONNECTION_STRING` : Chaîne de connexion Azure Application Insights

## 📝 Structure des Données

### Input (Prédiction)
```json
{
  "GrLivArea": 1500.0,
  "BedroomAbvGr": 3,
  "FullBath": 2,
  "YearBuilt": 2000,
  "TotalBsmtSF": 800.0
}
```

### Output (Prédiction)
```json
{
  "predicted_price": 185234.56,
  "price_range": "Medium"
}
```

Price ranges :
- **Low** : < $100,000
- **Medium** : $100,000 - $200,000
- **High** : $200,000 - $300,000
- **Very High** : ≥ $300,000

## 🔄 Pipeline CI/CD

1. **Commit/Push** → Déclenche le workflow GitHub Actions
2. **Tests** → Exécution des tests pytest
3. **Build** → Construction de l'image Docker
4. **Push ACR** → Envoi vers Azure Container Registry
5. **Deploy** → Déploiement sur Azure Container Apps
6. **Verify** → Vérification du health check

## 🛠️ Scripts Utilitaires

- `deploy.ps1` : Script PowerShell complet pour déploiement Azure (Windows)
- `deploy.sh` : Script Bash pour déploiement Azure (Linux/Mac)
- `test-deploiement.bat` : Test du déploiement
- `cleanup.sh` : Nettoyage des ressources Azure
- `drift_data_gen.py` : Génération de données pour test de drift

## 📚 Documentation API

Une fois l'API lancée, accéder à :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

---

## 🧪 Guide Complet : Tests, Déploiement et CI/CD

### 📋 Prérequis

Avant de commencer, assurez-vous d'avoir :
- Python 3.9+ installé
- Git installé
- Docker installé (pour la containerisation)
- Azure CLI installé (pour le déploiement Azure)
- Compte Azure avec un abonnement actif
- Compte GitHub (pour CI/CD)

```bash
# Vérifier les installations
python --version
git --version
docker --version
az --version
```

---

### 🔧 Partie 1 : Tests Locaux

#### 1.1 Configuration de l'Environnement

```bash
# Cloner le repository (si nécessaire)
git clone <votre-repo-url>
cd house_price_mlops

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows (PowerShell)
venv\Scripts\Activate.ps1
# Sur Linux/Mac
source venv/bin/activate

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt
```

#### 1.2 Test de la Préparation des Données

```bash
# Vérifier que le fichier source existe
# Placez votre fichier house_prices.csv dans le dossier data/

# Exécuter le script de préparation
python prepare_data.py

# Vérifier que le fichier nettoyé a été créé
# Le fichier data/house_prices_clean.csv doit exister
```

**Résultat attendu** :
- Affiche le nombre de lignes avant/après nettoyage
- Crée `data/house_prices_clean.csv`
- Affiche le prix moyen des maisons

#### 1.3 Test de l'Entraînement du Modèle

```bash
# Exécuter l'entraînement
python train_model.py

# Vérifier les résultats
# - Le modèle doit être sauvegardé dans model/house_price_model.pkl
# - Les graphiques doivent être générés (prediction_vs_actual.png, feature_importance.png)
# - Les métriques doivent s'afficher (RMSE, R²)
```

**Résultat attendu** :
```
RÉSULTATS DE L'ENTRAÎNEMENT
==================================================
RMSE : $XXXXX.XX
R²   : 0.XXXX
==================================================
```

**Vérifier MLflow** :
```bash
# Lancer MLflow UI pour voir les expériences
mlflow ui --port 5000
# Ouvrir http://localhost:5000 dans votre navigateur
```

#### 1.4 Test de l'API Locale

```bash
# Lancer l'API en mode développement
uvicorn app.main:app --reload --port 8000

# Dans un autre terminal, tester les endpoints
```

**Test 1 : Health Check**
```bash
# Windows PowerShell
Invoke-WebRequest -Uri http://localhost:8000/health -Method GET

# Linux/Mac ou Git Bash
curl http://localhost:8000/health
```

**Test 2 : Page d'accueil**
```bash
curl http://localhost:8000/
```

**Test 3 : Prédiction (POST)**
```bash
# Windows PowerShell
$body = @{
    GrLivArea = 1500.0
    BedroomAbvGr = 3
    FullBath = 2
    YearBuilt = 2000
    TotalBsmtSF = 800.0
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:8000/predict -Method POST -Body $body -ContentType "application/json"

# Linux/Mac ou Git Bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "GrLivArea": 1500.0,
    "BedroomAbvGr": 3,
    "FullBath": 2,
    "YearBuilt": 2000,
    "TotalBsmtSF": 800.0
  }'
```

**Test 4 : Test de Drift**
```bash
# D'abord, générer des données de production avec drift
python drift_data_gen.py

# Ensuite, tester la détection de drift
curl -X POST "http://localhost:8000/drift/check?threshold=0.05"
```

**Test 5 : Documentation Swagger**
- Ouvrir http://localhost:8000/docs dans votre navigateur
- Tester les endpoints directement depuis l'interface Swagger

#### 1.5 Tests Unitaires avec Pytest

```bash
# Exécuter tous les tests
pytest tests/ -v

# Avec couverture de code
pytest tests/ -v --cov=app --cov-report=term --cov-report=html

# Ouvrir le rapport de couverture HTML
# Le fichier htmlcov/index.html sera généré
```

**Résultat attendu** :
- Tous les tests doivent passer (✓)
- La couverture de code doit être affichée

---

### 🐳 Partie 2 : Tests avec Docker

#### 2.1 Build de l'Image Docker

```bash
# Vérifier que le modèle est présent
# Le fichier model/house_price_model.pkl doit exister

# Build de l'image
docker build -t house-price-api:local .

# Vérifier que l'image a été créée
docker images | grep house-price-api
```

#### 2.2 Test du Container Docker

```bash
# Lancer le container
docker run -d -p 8000:8000 --name house-price-test house-price-api:local

# Vérifier que le container tourne
docker ps

# Tester l'API
curl http://localhost:8000/health

# Voir les logs
docker logs house-price-test

# Arrêter et supprimer le container
docker stop house-price-test
docker rm house-price-test
```

---

### ☁️ Partie 3 : Déploiement sur Azure

#### 3.1 Configuration Azure CLI

```bash
# Se connecter à Azure
az login

# Vérifier l'abonnement actif
az account show

# Si plusieurs abonnements, sélectionner le bon
az account list --output table
az account set --subscription "VOTRE-SUBSCRIPTION-ID"

# Vérifier que vous êtes connecté
az account show
```

#### 3.2 Création des Ressources Azure

**Option A : Création manuelle (recommandé pour la première fois)**

```bash
# Variables (personnalisez selon vos besoins)
RESOURCE_GROUP="rg-mlops-house-price"
LOCATION="centralus"  # ou "francecentral", "westeurope", etc.
ACR_NAME="hprmlkamacr"  # Doit être unique globalement (minuscules et chiffres uniquement)
CONTAINER_APP_NAME="house-price-api"
CONTAINERAPPS_ENV="env-mlops-house-price"

# Créer le groupe de ressources
az group create --name $RESOURCE_GROUP --location $LOCATION

# Créer Azure Container Registry (ACR)
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true

# Récupérer les identifiants ACR
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query passwords[0].value -o tsv)

echo "ACR Username: $ACR_USERNAME"
echo "ACR Password: $ACR_PASSWORD"
# ⚠️ NOTEZ CES IDENTIFIANTS - Vous en aurez besoin pour GitHub Actions

# Créer l'environnement Container Apps
az containerapp env create \
  --name $CONTAINERAPPS_ENV \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

# Build et push de l'image Docker vers ACR
az acr build \
  --registry $ACR_NAME \
  --image house-price-api:v1 \
  --file Dockerfile .

# Créer la Container App
az containerapp create \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINERAPPS_ENV \
  --image $ACR_NAME.azurecr.io/house-price-api:v1 \
  --registry-server $ACR_NAME.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --target-port 8000 \
  --ingress external \
  --cpu 1.0 \
  --memory 2.0Gi

# Récupérer l'URL de l'API
APP_URL=$(az containerapp show \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn -o tsv)

echo "=========================================="
echo "✅ DÉPLOIEMENT RÉUSSI !"
echo "Votre API est disponible à :"
echo "https://$APP_URL"
echo "=========================================="

# Tester l'API déployée
curl https://$APP_URL/health
```

**Option B : Utiliser le script deploy.sh (PowerShell)**

```powershell
# Modifier les variables dans deploy.sh selon vos besoins
# Puis exécuter :
.\deploy.sh
```

#### 3.3 Configuration d'Application Insights (Optionnel mais Recommandé)

```bash
# Créer une ressource Application Insights
az monitor app-insights component create \
  --app house-price-api-insights \
  --location $LOCATION \
  --resource-group $RESOURCE_GROUP

# Récupérer la connection string
APPINSIGHTS_CONN=$(az monitor app-insights component show \
  --app house-price-api-insights \
  --resource-group $RESOURCE_GROUP \
  --query connectionString -o tsv)

# Mettre à jour la Container App avec la variable d'environnement
az containerapp update \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --set-env-vars "APPLICATIONINSIGHTS_CONNECTION_STRING=$APPINSIGHTS_CONN"
```

#### 3.4 Vérification du Déploiement

```bash
# Vérifier le statut de la Container App
az containerapp show \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "{Status:properties.provisioningState,URL:properties.configuration.ingress.fqdn}"

# Voir les logs
az containerapp logs show \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --follow

# Tester les endpoints
APP_URL=$(az containerapp show \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn -o tsv)

# Health check
curl https://$APP_URL/health

# Test de prédiction
curl -X POST "https://$APP_URL/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "GrLivArea": 1500.0,
    "BedroomAbvGr": 3,
    "FullBath": 2,
    "YearBuilt": 2000,
    "TotalBsmtSF": 800.0
  }'
```

#### 3.5 Mise à Jour du Déploiement

Pour mettre à jour l'application après des modifications :

```bash
# 1. Rebuild l'image
az acr build \
  --registry $ACR_NAME \
  --image house-price-api:v2 \
  --file Dockerfile .

# 2. Mettre à jour la Container App
az containerapp update \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --image $ACR_NAME.azurecr.io/house-price-api:v2
```

---

### 🔄 Partie 4 : Configuration CI/CD avec GitHub Actions

#### 4.1 Préparation des Secrets GitHub

Avant de configurer CI/CD, vous devez créer les secrets dans votre repository GitHub :

1. **Aller dans votre repository GitHub** → Settings → Secrets and variables → Actions

2. **Créer un Service Principal Azure** (pour AZURE_CREDENTIALS) :

```bash
# Remplacer SUBSCRIPTION_ID, RESOURCE_GROUP par vos valeurs
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
RESOURCE_GROUP="rg-mlops-house-price"

# Créer le service principal
az ad sp create-for-rbac \
  --name "github-actions-mlops" \
  --role contributor \
  --scopes /subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP \
  --sdk-auth

# ⚠️ COPIEZ LA SORTIE JSON COMPLÈTE - C'est votre secret AZURE_CREDENTIALS
```

3. **Ajouter les Secrets dans GitHub** :

   - **AZURE_CREDENTIALS** : La sortie JSON complète de la commande ci-dessus
   - **ACR_USERNAME** : Le nom d'utilisateur ACR (généralement le nom de votre ACR)
   - **ACR_PASSWORD** : Le mot de passe ACR (récupéré avec `az acr credential show`)

```bash
# Récupérer les identifiants ACR si vous ne les avez pas
az acr credential show \
  --name $ACR_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "{username:username,password:passwords[0].value}"
```

#### 4.2 Configuration dans GitHub

1. **Aller dans votre repository** → Settings → Secrets and variables → Actions
2. **Cliquer sur "New repository secret"**
3. **Ajouter les 3 secrets** :
   - Name: `AZURE_CREDENTIALS`, Value: `{...JSON complet...}`
   - Name: `ACR_USERNAME`, Value: `votre-acr-name`
   - Name: `ACR_PASSWORD`, Value: `votre-acr-password`

#### 4.3 Ajuster le Workflow CI/CD

Le fichier `.github/workflows/ci-cd.yml` est déjà configuré, mais vérifiez que :

1. **Le nom de l'ACR est correct** dans la variable `ACR_NAME`
   - Le workflow utilise : `houseprice$(echo ${{ github.repository_owner }} | tr '[:upper:]' '[:lower:]' | tr -cd '[:alnum:]')`
   - Si votre ACR a un nom différent, modifiez la ligne 11 du workflow

2. **Le resource group correspond** à celui que vous avez créé

3. **Le nom de la Container App correspond**

#### 4.4 Tester le Pipeline CI/CD

1. **Pousser du code sur la branche main** :

```bash
# Faire une modification mineure (par exemple, ajouter un commentaire)
# Puis commit et push
git add .
git commit -m "Test CI/CD pipeline"
git push origin main
```

2. **Vérifier l'exécution du workflow** :
   - Aller dans votre repository GitHub
   - Cliquer sur l'onglet "Actions"
   - Vous devriez voir le workflow "CI/CD Pipeline" s'exécuter

3. **Surveiller les étapes** :
   - ✓ Test : Les tests pytest doivent passer
   - ✓ Build and push : L'image Docker doit être construite et poussée vers ACR
   - ✓ Deploy : La Container App doit être mise à jour
   - ✓ Verify : Le health check doit réussir

#### 4.5 Vérification du Déploiement Automatique

```bash
# Après le déploiement, vérifier la nouvelle version
az containerapp show \
  --name house-price-api \
  --resource-group rg-mlops-house-price \
  --query "{Image:properties.template.containers[0].image,Revision:properties.latestRevisionName}"

# Tester l'API
APP_URL=$(az containerapp show \
  --name house-price-api \
  --resource-group rg-mlops-house-price \
  --query properties.configuration.ingress.fqdn -o tsv)

curl https://$APP_URL/health
```

---

### 🧹 Nettoyage des Ressources

#### Option 1 : Supprimer uniquement la Container App

```bash
az containerapp delete \
  --name house-price-api \
  --resource-group rg-mlops-house-price
```

#### Option 2 : Supprimer tout le groupe de ressources (ATTENTION : suppression définitive)

```bash
# Utiliser le script cleanup.sh
bash cleanup.sh

# Ou manuellement
az group delete --name rg-mlops-house-price --yes --no-wait
```

---

### ✅ Checklist de Vérification

Avant de considérer le projet comme prêt :

- [ ] Tests locaux passent (pytest)
- [ ] Préparation des données fonctionne
- [ ] Entraînement génère un modèle valide
- [ ] API locale répond correctement
- [ ] Tests Docker passent
- [ ] Image Docker build sans erreur
- [ ] Azure CLI configuré et connecté
- [ ] Ressources Azure créées
- [ ] Déploiement Azure réussi
- [ ] API déployée accessible via HTTPS
- [ ] Secrets GitHub configurés
- [ ] Workflow CI/CD exécuté avec succès
- [ ] Déploiement automatique fonctionne

---

### 🐛 Dépannage Courant

**Problème : Le modèle n'est pas trouvé lors du déploiement**
- Solution : Vérifier que `model/house_price_model.pkl` est présent et pas dans `.dockerignore`

**Problème : Erreur de permissions Azure**
- Solution : Vérifier que le Service Principal a les bonnes permissions (contributor sur le resource group)

**Problème : L'image Docker ne se push pas vers ACR**
- Solution : Vérifier que ACR_USERNAME et ACR_PASSWORD sont corrects dans GitHub Secrets

**Problème : Les tests échouent dans CI/CD**
- Solution : Vérifier que tous les tests passent localement avec `pytest tests/ -v`

**Problème : L'API retourne 503 après déploiement**
- Solution : Vérifier les logs avec `az containerapp logs show --name house-price-api --resource-group rg-mlops-house-price --follow`

---

## 🔄 Prochaines Améliorations Possibles

- [ ] Ajout d'authentification (API keys, OAuth)
- [ ] Cache des prédictions (Redis)
- [ ] Versionning des modèles (MLflow Model Registry)
- [ ] Alertes automatiques en cas de drift
- [ ] A/B testing de modèles
- [ ] Batch prediction endpoint
- [ ] Métriques de performance en temps réel
- [ ] Dashboard de monitoring (Grafana)

## 📄 Licence

Ce projet est un exemple éducatif de projet MLOps.

## 👤 Auteur

Projet de déploiement de modèle MLOps - House Price Prediction
