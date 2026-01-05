# deploy_fixed.ps1
# Permet d'afficher les erreurs et d'arrêter le script en cas de problème
 $ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Green
Write-Host "DÉBUT DU DÉPLOIEMENT SUR AZURE (VERSION CORRIGÉE)" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# VARIABLES MODIFIÉES
 $RESOURCE_GROUP = "rg-mlops-house-price"
# UTILISATION D'UNE RÉGION DIFFÉRENTE (francecentral)
 $LOCATION = "francecentral" 
# Nom de l'ACR plus court pour éviter les problèmes
 $ACR_NAME = "hpricemlk$(Get-Random -Maximum 9999)"
 $CONTAINER_APP_NAME = "house-price-api"
 $CONTAINERAPPS_ENV = "env-mlops-house-price"
 $IMAGE_NAME = "house-price-api"
 $IMAGE_TAG = "v1"
 $TARGET_PORT = 8000

Write-Host "Variables configurées :"
Write-Host "  - Resource Group: $RESOURCE_GROUP"
Write-Host "  - Location: $LOCATION"
Write-Host "  - ACR Name: $ACR_NAME"
Write-Host "  - Container App: $CONTAINER_APP_NAME"
Write-Host ""

# Installation correcte de l'extension containerapp
Write-Host "Installation de l'extension containerapp..."
try {
    az extension add --name containerapp --upgrade -y
    Write-Host "Extension containerapp installée avec succès." -ForegroundColor Green
} catch {
    Write-Host "Erreur lors de l'installation de l'extension: $_" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Enregistrement des providers
Write-Host "Enregistrement des providers Azure..."
az provider register --namespace Microsoft.ContainerRegistry --wait
az provider register --namespace Microsoft.App --wait
az provider register --namespace Microsoft.Web --wait
az provider register --namespace Microsoft.OperationalInsights --wait
Write-Host "Providers enregistrés."
Write-Host ""

# Création du groupe de ressources
Write-Host "Création du groupe de ressources: $RESOURCE_GROUP dans la région $LOCATION..."
try {
    az group create -n $RESOURCE_GROUP -l $LOCATION
    Write-Host "Groupe de ressources créé avec succès." -ForegroundColor Green
} catch {
    Write-Host "Erreur lors de la création du groupe de ressources: $_" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Création ACR
Write-Host "Création du Container Registry (ACR): $ACR_NAME..."
try {
    az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --admin-enabled true --location $LOCATION
    Write-Host "ACR créé avec succès." -ForegroundColor Green
} catch {
    Write-Host "Erreur lors de la création de l'ACR: $_" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Connexion au ACR
Write-Host "Connexion à l'ACR..."
az acr login --name $ACR_NAME
Write-Host "Connecté à l'ACR."
Write-Host ""

# Récupération des informations de l'ACR
 $ACR_LOGIN_SERVER = az acr show --name $ACR_NAME --query loginServer -o tsv
 $ACR_USER = az acr credential show -n $ACR_NAME --query username -o tsv
 $ACR_PASS = az acr credential show -n $ACR_NAME --query "passwords[0].value" -o tsv
 $IMAGE = "$ACR_LOGIN_SERVER/$IMAGE_NAME`:$IMAGE_TAG"

Write-Host "Informations de l'ACR :"
Write-Host "  - Login Server: $ACR_LOGIN_SERVER"
Write-Host "  - Image: $IMAGE"
Write-Host ""

# Tag et push de l'image
Write-Host "Tag de l'image Docker existante..."
docker tag $IMAGE_NAME`:$IMAGE_TAG $IMAGE
docker tag $IMAGE_NAME`:$IMAGE_TAG "$ACR_LOGIN_SERVER/$IMAGE_NAME`:latest

Write-Host "Push de l'image vers l'ACR..."
docker push $IMAGE
docker push "$ACR_LOGIN_SERVER/$IMAGE_NAME`:latest
Write-Host "Image poussée avec succès."
Write-Host ""

# Création Log Analytics
 $LAW_NAME = "law-mlops-house-price-$(Get-Date -Format yyyyMMddHHmmss)"
Write-Host "Création de l'espace de travail Log Analytics: $LAW_NAME..."
az monitor log-analytics workspace create -g $RESOURCE_GROUP -n $LAW_NAME -l $LOCATION
Start-Sleep -Seconds 15

 $LAW_ID = az monitor log-analytics workspace show --resource-group $RESOURCE_GROUP --workspace-name $LAW_NAME --query customerId -o tsv
 $LAW_KEY = az monitor log-analytics workspace get-shared-keys --resource-group $RESOURCE_GROUP --workspace-name $LAW_NAME --query primarySharedKey -o tsv
Write-Host "Log Analytics créé."
Write-Host ""

# Création Container Apps Environment
Write-Host "Création de l'environnement Container Apps: $CONTAINERAPPS_ENV..."
az containerapp env create -n $CONTAINERAPPS_ENV -g $RESOURCE_GROUP -l $LOCATION --logs-workspace-id $LAW_ID --logs-workspace-key $LAW_KEY
Write-Host "Environnement créé."
Write-Host ""

# Déploiement Container App
Write-Host "Déploiement de la Container App: $CONTAINER_APP_NAME..."
az containerapp create -n $CONTAINER_APP_NAME -g $RESOURCE_GROUP --environment $CONTAINERAPPS_ENV --image $IMAGE --ingress external --target-port $TARGET_PORT --registry-server $ACR_LOGIN_SERVER --registry-username $ACR_USER --registry-password $ACR_PASS --min-replicas 1 --max-replicas 1
Write-Host "Container App déployée."
Write-Host ""

# URL de l'application
 $APP_URL = az containerapp show -n $CONTAINER_APP_NAME -g $RESOURCE_GROUP --query properties.configuration.ingress.fqdn -o tsv

Write-Host "========================================" -ForegroundColor Green
Write-Host "DÉPLOIEMENT RÉUSSI !" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "ACR      : $ACR_NAME"
Write-Host "Resource Group: $RESOURCE_GROUP"
Write-Host ""
Write-Host "URLs de l'application :"
Write-Host "  API      : https://$APP_URL" -ForegroundColor Yellow
Write-Host "  Health   : https://$APP_URL/health" -ForegroundColor Yellow
Write-Host "  Docs     : https://$APP_URL/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "Pour supprimer toutes les ressources, exécutez le script cleanup.ps1" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Green