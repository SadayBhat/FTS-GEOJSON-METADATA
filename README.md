# Full-Text_search-on-GEOJSON


## What it Does

This project enables users to search for geospatial features—like roads or railway stations—based or geographic coordinates. It returns relevant spatial data with metadata such as category, type, and proximity.

Examples:
- “proposed roads near Devanahalli”

---

## How it Works

1. **Full Text Search**  
   The Full-Text Search (FTS) functionality in this project utilizes PostgreSQL's tsvector and plainto_tsquery functions to perform efficient keyword-based searching on the properties field of geospatial features, allowing for fast and accurate location-based searches with natural language queries
   
2. **Fuzzy Search Fallback**  
   If no exact location match is found, it searches by similarity on feature names.

3. **API Built with FastAPI**  
   Fast, interactive, and validates data using Pydantic models.

---
