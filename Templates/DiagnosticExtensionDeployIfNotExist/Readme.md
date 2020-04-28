# VMExtensionDeployIfNotExists for Windows
1. definition
    ```
    az policy definition create --name swuDeployWindowsVMExtension --display-name "Deploy VM Diagnostic Extension if not exists for Windows" --rules Policy/DiagnosticExtensionDeployIfNotExist/VMExtensionDeployIfNotExists.windows.json --params Policy/DiagnosticExtensionDeployIfNotExist/VMExtensionDeployIfNotExists.params.json
    ```
1. assignment
    - Doable through CLI, but for now just manual assignment since it pretty straight forward step
        - In portal, policy tab, find the policy definition and click on assign
        - In The parameter tab fill in the storage account resource ID, i.e. `/subscriptions/{subscription ID}/resourceGroups/{resource group name}/providers/Microsoft.Storage/storageAccounts/{storage account name}`

# VMExtensionDeployIfNotExists for Linux
1. definition
    ```
    az policy definition create --name deployLinuxVMExtension --display-name "Deploy VM Diagnostic Extension if not exists for Linux" --rules Policy/DiagnosticExtensionDeployIfNotExist/VMExtensionDeployIfNotExists.linux.json --params Policy/DiagnosticExtensionDeployIfNotExist/VMExtensionDeployIfNotExists.params.json
    ```
1. assignment
    - Doable through CLI, but for now just manual assignment since it pretty straight forward step
        - In portal, policy tab, find the policy definition and click on assign
        - In The parameter tab fill in the storage account resource ID, i.e. `/subscriptions/{subscription ID}/resourceGroups/{resource group name}/providers/Microsoft.Storage/storageAccounts/{storage account name}`
