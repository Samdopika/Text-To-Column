import pandas as pd

def text_to_columns(file_path, column_name, delimiter):
    # Read Excel file
    df = pd.read_excel(file_path)

    # Check if the column exists in the DataFrame
    if column_name not in df.columns:
        print(f"Column '{column_name}' not found in the Excel sheet.")
        return

    # Split the selected column by the delimiter
    df_split = df[column_name].str.split(delimiter, expand=True)

    # Rename the split columns and add them to the original DataFrame
    for i in range(df_split.shape[1]):
        new_col_base_name = f"{column_name}_{i + 1}"
        new_col_name = new_col_base_name
        counter = 1
        while new_col_name in df.columns:
            new_col_name = f"{new_col_base_name}_{counter}"
            counter += 1
        df[new_col_name] = df_split[i]

    # Remove the original column
    df.drop(column_name, axis=1, inplace=True)

    # Save the modified DataFrame to a new Excel file
    output_file = file_path.replace(".xlsx", "_modified.xlsx")
    df.to_excel(output_file, index=False)
    print(f"Modified Excel sheet saved as: {output_file}")

if __name__ == "__main__":
    # Input file path
    file_path = input("Enter the path to the Excel file: ")

    # Input column name
    column_name = input("Enter the name of the column to apply Text-to-Column: ")

    # Input delimiter
    delimiter = input("Enter the delimiter to use for splitting the column: ")

    # Process the Excel file
    text_to_columns(file_path, column_name, delimiter)
