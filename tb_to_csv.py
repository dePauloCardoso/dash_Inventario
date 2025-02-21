import pandas as pd

# Define the full path to your Excel file
input_path = r"C:\Users\paulocardoso\OneDrive - ARCO Educacao\Área de Trabalho\ARCO\estoqueSAE\inventario\celulaInventario\1-comparacao\baseComparacao.xlsx" # Adjust this to your actual path
output_path = r"C:\Users\paulocardoso\OneDrive - ARCO Educacao\Área de Trabalho\Docs_Paulo\Paulo\Pessoal\Python\dashInventory\data\acuracidade.csv"  # Adjust where you want to save the CSV

# Load the Excel file
df = pd.read_excel(input_path, sheet_name="acuracidade")  # Change the sheet name if needed

# Save as CSV
df.to_csv(output_path, index=False)  # Set index=False to exclude row numbers

print(f"CSV file saved at: {output_path}")
