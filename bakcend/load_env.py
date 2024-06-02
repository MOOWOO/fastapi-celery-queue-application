import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Print all environment variables in a format suitable for export
for key, value in os.environ.items():
    if key != "PATH":  # Exclude PATH for safety
        print(f'export {key}="{value}"')
