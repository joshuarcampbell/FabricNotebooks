import requests
import sempy.fabric as fabric
from notebookutils import mssparkutils

# Get the current workspace ID dynamically
workspaceId = fabric.get_workspace_id()
print(f"Current Workspace ID: {workspaceId}")

# Get authentication token
token = mssparkutils.credentials.getToken("https://api.fabric.microsoft.com")

# Headers for API calls
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Step 1: List all mirrored databases in the workspace
listUrl = f"https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/mirroredDatabases"

try:
    response = requests.get(listUrl, headers=headers)
    response.raise_for_status()
    
    mirroredDatabases = response.json().get("value", [])
    
    if not mirroredDatabases:
        print("No mirrored databases found in this workspace.")
    else:
        print(f"\nFound {len(mirroredDatabases)} mirrored database(s)")
        print("-" * 60)
        
        # Step 2: Resume replication for each mirrored database
        for db in mirroredDatabases:
            dbId = db["id"]
            dbName = db["displayName"]
            
            print(f"\nResuming replication for: {dbName}")
            print(f"  Database ID: {dbId}")
            
            # Call startMirroring API
            startUrl = f"https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/mirroredDatabases/{dbId}/startMirroring"
            
            try:
                startResponse = requests.post(startUrl, headers=headers)
                
                if startResponse.status_code == 200:
                    print(f"  ✓ Successfully resumed replication")
                elif startResponse.status_code == 202:
                    print(f"  ✓ Replication start request accepted (processing)")
                else:
                    print(f"  ✗ Error: {startResponse.status_code}")
                    print(f"  Response: {startResponse.text}")
                    
            except Exception as e:
                print(f"  ✗ Failed to resume: {str(e)}")
        
        print("\n" + "=" * 60)
        print("Replication resume operation completed for all databases")
        
except Exception as e:
    print(f"Error listing mirrored databases: {str(e)}")

