import pandas as pd

CSV_PATH = "../data/Test.csv"

def main():
# Split into smaller chunks
    with pd.read_csv(CSV_PATH, chunksize=10000) as reader:
        for i, chunk in enumerate(reader):
            # Write each chunk to a new CSV file
            chunk.to_csv(f'../data/default/customers_file_{i+1}.csv', index=False)

if __name__ == "__main__":
    main()
