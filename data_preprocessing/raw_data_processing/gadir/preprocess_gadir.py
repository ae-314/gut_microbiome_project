import pandas as pd
import os

def preprocess_gadir(input_csv: str, output_csv: str = None):
    """
    Preprocess the Gadir metadata CSV file to create a binary classification dataset.
    
    Parameters:
    -----------
    input_csv : str
        Path to the input CSV file (gadir_metadata.csv)
    output_csv : str, optional
        Path to the output CSV file. If None, defaults to 'gadir_preprocessed.csv'
        in the same directory as input_csv.
    
    Returns:
    --------
    pd.DataFrame
        The preprocessed dataframe with Run and label columns
    """
    # Load the dataset
    df = pd.read_csv(input_csv)
    
    # Filter for human samples only (exclude any non-human samples like mice)
    # Check both HOST and Organism columns to ensure we only have human samples
    if 'HOST' in df.columns:
        df = df[df['HOST'].str.contains('Homo sapiens', case=False, na=False)]
    if 'Organism' in df.columns:
        df = df[df['Organism'].str.contains('human', case=False, na=False)]
    
    # Filter out Unclear/unclear samples (case-insensitive)
    df = df[~df['Group'].str.lower().isin(['unclear'])]
    
    # Map Group values to binary labels
    label_mapping = {
        'FoodAllergy': 1,
        'Control': 0,
        'ControlHiRisk': 0
    }
    
    df['label'] = df['Group'].map(label_mapping)
    
    # Select only Run and label columns
    df_preprocessed = df[['Run', 'label']].copy()
    
    # Ensure proper data types
    df_preprocessed['Run'] = df_preprocessed['Run'].astype(str)
    df_preprocessed['label'] = df_preprocessed['label'].astype(int)
    
    # Set output path if not provided
    if output_csv is None:
        input_dir = os.path.dirname(input_csv)
        output_csv = os.path.join(input_dir, 'gadir_preprocessed.csv')
    
    # Save to CSV
    df_preprocessed.to_csv(output_csv, index=False)
    
    # Verify no missing values and warn if found
    missing_runs = df_preprocessed['Run'].isna().sum()
    missing_labels = df_preprocessed['label'].isna().sum()
    if missing_runs > 0 or missing_labels > 0:
        print(f"Warning: Found missing values!")
        print(f"  Missing Run IDs: {missing_runs}")
        print(f"  Missing labels: {missing_labels}")
    
    return df_preprocessed

if __name__ == "__main__":
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'gadir_metadata.csv')
    
    # Run preprocessing
    preprocess_gadir(input_file)

