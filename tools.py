import pandas as pd
from smolagents import tool, Tool


@tool
def get_xlsx_summary(file_path: str) -> str:
    """ Returns the summary of the xlsx file.

    Args:
        file_path (str): path to the xlsx file
    
    Returns:
        str: header of the dataframe (columns and first rows)
    """
    df = pd.read_excel(file_path)
    return df.head().to_string()


if __name__ == '__main__':
    csv_summary = get_xlsx_summary(rf"files_for_tasks\7bd855d8-463d-4ed5-93ca-5fe35145f733.xlsx")
    print(csv_summary)
