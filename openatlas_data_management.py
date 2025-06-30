# Python script for interacting with OpenAtlas archaeological data management platform

# This script provides a conceptual outline for interacting with an OpenAtlas instance.
# OpenAtlas is an open-source, web-based database system for archaeological and historical data.
# Interaction typically happens via its REST API. You would need to have an OpenAtlas instance running
# and have appropriate API credentials.

import requests
import json

print("OpenAtlas Data Management Script")
print("--------------------------------")

# --- Configuration --- 

# Replace with the URL of your OpenAtlas instance
OPENATLAS_BASE_URL = "http://localhost:5000/api/v1/" # Example: "https://your-openatlas-instance.org/api/v1/"

# Replace with your OpenAtlas API key or credentials
# In a real application, these should be loaded securely (e.g., from environment variables)
API_KEY = "your_api_key" # OpenAtlas often uses API keys for authentication

# --- API Endpoints (Commonly Used) --- 

# You would typically find these in your OpenAtlas instance's API documentation
# Example endpoints (may vary based on your OpenAtlas version and configuration):
ENTITIES_ENDPOINT = f"{OPENATLAS_BASE_URL}entities/"
TYPES_ENDPOINT = f"{OPENATLAS_BASE_URL}types/"

# --- Functions for OpenAtlas Interaction --- 

def get_headers(api_key):
    """
    Returns the common headers for API requests, including the API key.
    """
    return {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json"
    }

def get_entities(api_key, entity_type=None, limit=10):
    """
    Retrieves entities from OpenAtlas.
    """
    headers = get_headers(api_key)
    params = {"limit": limit}
    url = ENTITIES_ENDPOINT

    if entity_type:
        url = f"{ENTITIES_ENDPOINT}?type={entity_type}"

    print(f"Retrieving entities from: {url}")
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving entities: {e}")
        return None

def create_entity(api_key, entity_data):
    """
    Creates a new entity in OpenAtlas.
    `entity_data` should be a dictionary matching the entity's schema.
    """
    headers = get_headers(api_key)
    print("Creating new entity...")
    try:
        response = requests.post(ENTITIES_ENDPOINT, headers=headers, data=json.dumps(entity_data))
        response.raise_for_status()
        print("Entity created successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating entity: {e}")
        return None

# --- Example Usage --- 

if __name__ == "__main__":
    # 1. Example: Get some existing entities
    print("\n--- Fetching Entities ---")
    # To get specific types of entities (e.g., 'site', 'find'), you would specify the entity_type.
    # You might need to query the /types/ endpoint first to see available entity types.
    entities = get_entities(API_KEY, limit=5)
    if entities:
        print("Successfully fetched entities:")
        for ent in entities.get("results", []):
            print(f"  Entity ID: {ent.get("id")}, Type: {ent.get("type").get("name")}, Label: {ent.get("label")}")
    else:
        print("Could not fetch entities.")

    # 2. Example: Create a new entity (conceptual)
    # This part is highly dependent on your OpenAtlas data model and the specific entity type you want to create.
    # You would need to know the `type_id` and the expected `data` structure for that type.
    print("\n--- Creating a New Entity (Conceptual) ---")
    # Example: A very simplified data structure for a hypothetical 'Site' entity
    # Replace 'your_site_type_id' with the actual UUID or ID of your site entity type in OpenAtlas
    # And populate 'new_site_data' with actual property IDs and values from your schema.
    # This is a placeholder and will likely fail if run without a matching OpenAtlas setup.
    # new_site_data = {
    #     "type_id": "<UUID_OR_ID_OF_YOUR_SITE_ENTITY_TYPE>",
    #     "label": "New Archaeological Discovery",
    #     "properties": [
    #         {
    #             "type_id": "<UUID_OR_ID_OF_LOCATION_PROPERTY>",
    #             "value": "POINT (-52.123 -7.456)" # WKT format for geometry
    #         },
    #         {
    #             "type_id": "<UUID_OR_ID_OF_DESCRIPTION_PROPERTY>",
    #             "value": "A newly identified potential settlement area in the Amazon basin."
    #         }
    #     ]
    # }
    # new_entity = create_entity(API_KEY, new_site_data)
    # if new_entity:
    #     print(f"New entity created with ID: {new_entity.get("id")}")
    # else:
    #     print("Failed to create new entity.")

print("\nThis script is a starting point. You will need to consult your specific OpenAtlas instance\"s API documentation for exact endpoints, entity types, and data structures.")
print("Remember to replace placeholder values for URL and API key.")


