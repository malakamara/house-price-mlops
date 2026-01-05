#!/bin/bash

RESOURCE_GROUP="rg-mlops-house-price"

echo "=========================================="
echo "Nettoyage des ressources Azure"
echo "=========================================="

read -p "Voulez-vous vraiment supprimer toutes les ressources ? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Opération annulée."
    exit 0
fi

echo "Ressources à supprimer:"
az resource list --resource-group $RESOURCE_GROUP --output table

echo "Suppression en cours..."
az group delete --name $RESOURCE_GROUP --yes --no-wait

echo "Suppression lancée (prend 5-10 minutes)"
echo "Vérifiez sur : https://portal.azure.com"