## Example steps for Azure:
1. `az login`
2. `az account set --subscription "Visual Studio Enterprise"`
3. `az group create --name "myResourceGroup" --location "eastus"`
4. `az storage account create --name hotstarttest --resource-group myResourceGroup --location eastus --sku Standard_LRS --kind StorageV2`
5. `az storage blob service-properties update --account-name hotstarttest --static-website --404-document error.html --index-document index.html`
6. `az storage account show-connection-string --name hotstarttake --resource-group myResourceGroup --output tsv`
7. `az storage blob upload-batch -s build -d '$web' --connection-string "your_connection_string_here"`
8. `az storage account show --name hotstarttest --resource-group myResourceGroup --query "primaryEndpoints.web" --output tsv`

Example steps for AWS:
1. `aws s3api create-bucket --bucket react-app-94bc49c46158ddb2 --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2`
2. `aws s3 sync ../sample-app/dist s3://react-app-94bc49c46158ddb2`
3. 
