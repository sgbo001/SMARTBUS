from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'c2063081' # Must be replaced by your <storage_account_name>
    account_key = 'H25Y8tmCnZFNVvOSYzkuNlCGAFwqEt+nFiZXbeD9l3KUF95b3OU1e8mrBZhMGjaG8UO3UyEe/ktT+AStFrdNEQ==' 
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'c2063081' 
    account_key = 'H25Y8tmCnZFNVvOSYzkuNlCGAFwqEt+nFiZXbeD9l3KUF95b3OU1e8mrBZhMGjaG8UO3UyEe/ktT+AStFrdNEQ==' 
    azure_container = 'static'
    expiration_secs = None