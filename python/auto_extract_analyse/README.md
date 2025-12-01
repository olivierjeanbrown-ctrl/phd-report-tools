# Automated Extract and SELECT Tool

This Python tool helps you load multiple CSV datasets, build SQL `SELECT` statements, and create `LEFT JOIN` queries interactively. It also saves the final SQL query to an `/output` folder.

---

## Features

1. **Load CSV datasets**  
   - Prompts you to input the number of datasets to combine.  
   - Loads each CSV from the `/raw` folder into memory.  

2. **Build SQL SELECT statements**  
   - Choose columns to select.  
   - Optionally include `DISTINCT`.  
   - Calculates derived columns (e.g., sums).  

3. **Add LEFT JOINs interactively**  
   - Joins additional tables based on columns you specify.  
   - Validates that columns exist in each table.  

4. **Save SQL query**  
   - Saves the final SQL query to `/output/joined_query.sql`.

---


