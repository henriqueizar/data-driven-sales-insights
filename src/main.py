from processing import load_data, clean_data


def main():
    path = "data/sales.xlsx"
    if not path:
        print("Error: File path is empty.")
        return

    df = load_data(path)
    print("Raw Data:")
    print(df, "\n")

    df_cleaned = clean_data(df)
    print("Cleaned Data:")
    print(df_cleaned)


if __name__ == "__main__":
    main()