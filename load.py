# load.py
import os

def save_to_csv(df, filename, output_dir="output"):
    """Saves a DataFrame to CSV in the specified directory."""
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    df.to_csv(output_path, index=False)
    print(f"Saved to {output_path}")
