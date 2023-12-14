# Data exports and imports

## Exports:
1. Go to MySQL Workbench and search for your results to export
    For all results: 
    ```
    USE spotify;
    SELECT * FROM tracks;
    SELECT * FROM artists;
    SELECT * FROM genres;
    SELECT * FROM artistToGenre;
    SELECT * FROM trackToGenre;
    ```
2. Export each table to JSON with the naming convention as follows:
    1. The beginning of the filename must be the table name in the camelcase
    2. The table name must be followed by a period "."
3. Save it in the same directory as import.py 


## Imports:
1. Navigate to the directory of import.py in the terminal
2. Run the script:
```
py import.py
```
3. Verify completion of import in the MySQL Workbench
