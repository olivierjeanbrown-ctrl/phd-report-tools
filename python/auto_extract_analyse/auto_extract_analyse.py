# auto_extract_analyse
# Takes input table, identifies relevant variables, builds a basic SQL script

import pandas as pd
import os

print("Welcome to the Automated Extract and Analyse Tool. Make sure you have SQL and R.\n")


def number_tables():
    #First, we need to identify how many tables will be registered.
    while True:
        try:
            #Request the number of tables in a user input prompt:    
            n_tables = int(input("How many datasets do you need to aggregate into a single table?\n"))
            break
        #Troubleshoot if not an integer:
        except ValueError:
            print("\nInvalid input. Please enter a valid integer.\n")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}\n")
                
    print(f"\nOK. Preparing script for {n_tables} datasets...")
    return n_tables

def source_exctration(n_tables):
    dfs = {}  # dictionary to store DataFrames with table names as keys
    
    #Loop source identifying prompts for each table
    for item in range(0,n_tables):
        #First, we need to identify the dataset source:
        while True:
            try:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                dataset_source = input(f"Enter CSV prefix for dataset {item+1}:\n").strip()
                filename = dataset_source + ".csv"
                filepath = os.path.join(base_dir, "raw", filename)
                
                print("Loading:", filepath, "\n\n")
                df = pd.read_csv(filepath)
                dfs[dataset_source] = df  # save with prefix as key
                break
            except FileNotFoundError:
                print("File not found. Please check the prefix and try again.\n")
            except Exception as e:
                print(f"\nAn unexpected error occurred: {e}\n")       
    return dfs

def build_sql_select(dfs_dict):
    """
    Build a basic SQL SELECT statement interactively from the first DataFrame in dfs_dict.
    """
    print(f"Now we will build a basic SQL SELECT statement from the FIRST dataset you input...\n")
    
    # Get first table
    first_table = next(iter(dfs_dict))
    df = dfs_dict[first_table]

    # Ask if DISTINCT is needed
    distinct_input = input(f"Do you want DISTINCT values? (y/n) [default n]: ").strip().lower()
    distinct = "DISTINCT " if distinct_input == "y" else ""
    if distinct_input == "y":
        print(f"The first column name you input will appear after DISTINCT.")
    # Ask which columns to include with validation
    while True:
        cols_input = input(f"Enter columns to select separated by commas (or leave blank for all):\n").strip()
        columns = cols_input.replace(" ", "").split(",") if cols_input else ["*"]
    
        # Validate columns
        if columns != ["*"]:
            invalid_cols = [col for col in columns if col not in df.columns]
            if invalid_cols:
                print(f"\nError: The following columns do not exist in the table: {', '.join(invalid_cols)}. Please try again.\n")
                continue
    
        cols_str = ", ".join(columns) if columns != ["*"] else "*"
        break
    
    cols_str = ", ".join(columns) if columns != ["*"] else "*"

    # Build SQL
    sql = f"SELECT {distinct}{cols_str} FROM {first_table};"
    return sql

def build_sql_join(dfs_dict, sql_select):
    """
    Appends LEFT JOIN statements to an existing SQL SELECT based on subsequent tables in dfs_dict.
    """
    
    tables = list(dfs_dict.keys())
    base_table = tables[0]
    sql = sql_select.rstrip(";") # remove trailing semicolon to append joins

    for join_table in tables[1:]:
        while True:
            try:
                base_col = input(f"Enter the column from '{base_table}' to join on {join_table}:\n").strip()

                if base_col not in dfs_dict[base_table].columns:
                    print(f"Column '{base_col}' not in {base_table}. Try again.\n")
                    continue
                join_col = input(f"Enter the matching column from '{join_table}':\n").strip()
                if join_col not in dfs_dict[join_table].columns:
                    print(f"Column '{join_col}' not in {join_table}. Try again.\n")
                    continue

                sql += f"\nLEFT JOIN {join_table} \n\tON {base_table}.{base_col} = {join_table}.{join_col}"
                break
            except Exception as e:
                print(f"Unexpected error: {e}. Try again.\n")
    
    sql += ";"
    return sql





n_tables = number_tables()
dfs_dict = source_exctration(n_tables)
sql_select = build_sql_select(dfs_dict)
sql_joined = sql_select
print("\n", sql_select)


if n_tables > 1:
    sql_joined = build_sql_join(dfs_dict, sql_select)
    print("\n", sql_joined)


# Make sure the output folder exists
base_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(base_dir, "output")
os.makedirs(output_dir, exist_ok=True)  # creates folder if it doesn't exist

# Define the output file path
output_file = os.path.join(output_dir, "joined_query.sql")

# Save the SQL string
with open(output_file, "w") as f:
    f.write(sql_joined)

print(f"SQL saved to {output_file}")


