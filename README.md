# LEGO

## Considerations
* Tried to locate Swagger or OpenAPI schemas at conventional locations
* Inspected HTTP response headers for clues
* Flatten the list to contain quantity per (design ID, color). Since the combination of design ID and color are unique, it can be stored as dictionary keys. Dictionary items can be inserted and queried in constant time.