#!/bin/bash

# Script de déploiement Azure pour House Price API
# Usage: ./deploy.sh

set -e  # Arrêter en cas d'erreur

# Variables (personnalisez selon vos besoins)
RESOURCE_GROUP="rg-mlops-house-price"
LOCATION="centralus"
CONTAINER_APP_NAME="house-price-api"
CONTAINERAPPS_ENV="env-mlops-house-price"
ACR_NAME="hprmlkamacr"
IMAGE_NAME="house-price-api"
IMAGE_TAG="v1"

echo "=========================================="
echo "Déploiement Azure - House Price API"
echo "=========================================="
echo ""

# Vérifier que Azure CLI est installé
if ! command -v az &> /dev/null; then
    echo "✗ Azure CLI n'est pas installé. Veuillez l'installer depuis https://aka.ms/InstallAzureCLI"
    exit 1
fi
echo "✓ Azure CLI détecté"

# Vérifier la connexion Azure
echo "Vérification de la connexion Azure..."
if ! az account show &> /dev/null; then
    echo "✗ Non connecté à Azure. Connexion en cours..."
    az login
fi
echo "✓ Connecté à Azure"
SUBSCRIPTION_NAME=$(az account show --query name -o tsv)
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
echo "  Abonnement: $SUBSCRIPTION_NAME ($SUBSCRIPTION_ID)"

# Créer le groupe de ressources s'il n'existe pas
echo ""
echo "Vérification du groupe de ressources '$RESOURCE_GROUP'..."
if ! az group show --name $RESOURCE_GROUP &> /dev/null; then
    echo "Création du groupe de ressources..."
    az group create --name $RESOURCE_GROUP --location $LOCATION
    echo "✓ Groupe de ressources créé"
else
    echo "✓ Groupe de ressources existe déjà"
fi

# Créer ACR s'il n'existe pas
echo ""
echo "Vérification d'Azure Container Registry '$ACR_NAME'..."
if ! az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP &> /dev/null; then
    echo "Création d'Azure Container Registry..."
    az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --admin-enabled true
    echo "✓ Azure Container Registry créé"
else
    echo "✓ Azure Container Registry existe déjà"
fi

# Récupérer les identifiants ACR
echo ""
echo "Récupération des identifiants ACR..."
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query "passwords[0].value" -o tsv)
echo "✓ Identifiants ACR récupérés"

# Créer l'environnement Container Apps s'il n'existe pas
echo ""
echo "Vérification de l'environnement Container Apps '$CONTAINERAPPS_ENV'..."
if ! az containerapp env show --name $CONTAINERAPPS_ENV --resource-group $RESOURCE_GROUP &> /dev/null; then
    echo "Création de l'environnement Container Apps..."
    az containerapp env create --name $CONTAINERAPPS_ENV --resource-group $RESOURCE_GROUP --location $LOCATION
    echo "✓ Environnement Container Apps créé"
else
    echo "✓ Environnement Container Apps existe déjà"
fi

# Build et push de l'image Docker
echo ""
echo "Build et push de l'image Docker vers ACR..."
echo "Cela peut prendre quelques minutes..."
az acr build --registry $ACR_NAME --image "$IMAGE_NAME:$IMAGE_TAG" --file Dockerfile .
if [ $? -eq 0 ]; then
    echo "✓ Image Docker buildée et pushée vers ACR"
else
    echo "✗ Échec du build de l'image Docker"
    exit 1
fi

# Créer ou mettre à jour la Container App
echo ""
echo "Vérification de la Container App '$CONTAINER_APP_NAME'..."
if ! az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP &> /dev/null; then
    echo "Création de la Container App..."
    az containerapp create \
        --name $CONTAINER_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --environment $CONTAINERAPPS_ENV \
        --image "$ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG" \
        --registry-server "$ACR_NAME.azurecr.io" \
        --registry-username $ACR_USERNAME \
        --registry-password $ACR_PASSWORD \
        --target-port 8000 \
        --ingress external \
        --cpu 1.0 \
        --memory 2.0Gi
    echo "✓ Container App créée"
else
    echo "Mise à jour de la Container App..."
    az containerapp update \
        --name $CONTAINER_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --image "$ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG"
    echo "✓ Container App mise à jour"
fi

# Récupérer l'URL de l'API
echo ""
echo "Récupération de l'URL de l'API..."
APP_URL=$(az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --query "properties.configuration.ingress.fqdn" -o tsv)

# Afficher le résumé
echo ""
echo "=========================================="
echo "✅ DÉPLOIEMENT RÉUSSI !"
echo "=========================================="
echo ""
echo "URL de l'API: https://$APP_URL"
echo ""
echo "Endpoints disponibles:"
echo "  - Health: https://$APP_URL/health"
echo "  - Docs: https://$APP_URL/docs"
echo "  - Predict: https://$APP_URL/predict"
echo ""
echo "Ressources créées:"
echo "  - Resource Group: $RESOURCE_GROUP"
echo "  - Container Registry: $ACR_NAME.azurecr.io"
echo "  - Container App Environment: $CONTAINERAPPS_ENV"
echo "  - Container App: $CONTAINER_APP_NAME"
echo ""
echo "Pour voir les logs:"
echo "  az containerapp logs show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --follow"
echo ""

# Test optionnel
read -p "Voulez-vous tester l'API maintenant? (O/N): " TEST
if [[ "$TEST" =~ ^[OoYy]$ ]]; then
    echo ""
    echo "Test du health check..."
    if curl -f -s "https://$APP_URL/health" > /dev/null; then
        echo "✓ Health check réussi!"
        curl -s "https://$APP_URL/health" | jq . 2>/dev/null || curl -s "https://$APP_URL/health"
    else
        echo "⚠ Health check échoué. L'API peut mettre quelques minutes à démarrer."
    fi
fi

echo ""
echo "Déploiement terminé!"
