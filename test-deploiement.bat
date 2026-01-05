@echo off
echo =================================================================
echo Script de Test pour la Validation du Deploiement sur Azure
echo =================================================================

echo.
echo Tentative de recuperation de l'URL de l'application Azure...
echo L'application n'a pas pu etre deployee a cause de restrictions du compte Azure.
echo Voici le processus de validation qui aurait ete utilise :
echo.

echo.
echo La commande pour recuperer l'URL aurait ete :
echo   az containerapp show --name house-price-api --resource-group rg-mlops-house-price --query properties.configuration.ingress.fqdn -o tsv
echo.

echo.
echo En conditions normales, une commande curl aurait ete lancee pour tester l'endpoint /predict.
echo Exemple de commande curl :
echo   curl -X POST "https://<URL_DE_L_API>/predict" -H "Content-Type: application/json" -d "{...}"
echo.

echo.
echo URL de l'API (simulee) : https://non-disponible-car-le-deploiement-a-echoue
echo =================================================================
pause