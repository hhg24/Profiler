import pandas as pd

MAX_SUMMARY_COLUMNS = 3


def _build_chapter_interpretations(
    data: pd.DataFrame,
    chapter_column: str,
    interpretation_column: str | None = None
) -> pd.DataFrame:
    """
    Build one interpretation row per chapter.

    If `interpretation_column` exists, the first non-empty value is used.
    Otherwise a short data-driven summary is generated for each chapter.
    Auto-generated summaries include row count and averages for up to
    the first 3 numeric columns.
    """
    if chapter_column not in data.columns:
        raise ValueError(f"chapter_column '{chapter_column}' was not found in the data.")

    if interpretation_column and interpretation_column in data.columns:
        grouped = (
            data[[chapter_column, interpretation_column]]
            .copy()
            .dropna(subset=[chapter_column])
        )
        grouped[interpretation_column] = (
            grouped[interpretation_column].fillna("").astype(str).str.strip()
        )
        grouped = grouped[grouped[interpretation_column] != ""]
        if not grouped.empty:
            return (
                grouped.groupby(chapter_column, as_index=False)
                .first()
                .rename(columns={chapter_column: "chapter", interpretation_column: "interpretation"})
            )

    rows = []
    numeric_columns = data.select_dtypes(include="number").columns.tolist()
    chapter_data = data.dropna(subset=[chapter_column])

    for chapter, chapter_df in chapter_data.groupby(chapter_column, sort=False):
        summary_parts = [f"Rows: {len(chapter_df)}"]
        for col in numeric_columns[:MAX_SUMMARY_COLUMNS]:
            summary_parts.append(f"{col} avg: {chapter_df[col].mean():.2f}")
        rows.append(
            {
                "chapter": chapter,
                "interpretation": "; ".join(summary_parts),
            }
        )

    return pd.DataFrame(rows, columns=["chapter", "interpretation"])


def write_to_excel(
    data,
    file_name,
    sheet_names=None,
    chapter_column: str | None = None,
    interpretation_column: str | None = None,
    interpretation_sheet_name: str = "Interpretations"
):
    """
    Write a DataFrame or a list of DataFrames to an Excel file with optional sheet names.

    Parameters:
    data (pd.DataFrame or list of pd.DataFrame): The DataFrame(s) to write to the Excel file.
    file_name (str): Name of the output Excel file.
    sheet_names (str or list of str, optional): The name(s) of the sheet(s). If not provided, default names will be used.

    chapter_column (str, optional): Column name that identifies chapter sections.
        If provided (for a single DataFrame input), an interpretation sheet is added.
    interpretation_column (str, optional): Column containing chapter interpretations.
        If not provided or empty, interpretations are auto-generated from chapter data.
    interpretation_sheet_name (str): Name of the interpretation sheet.

    Returns:
    None
    """
    # Define the file path
    file_path = f"./results/{file_name}"
    # Create an Excel writer object
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        if isinstance(data, pd.DataFrame):
            # Handle a single DataFrame
            sheet_name = sheet_names if isinstance(sheet_names, str) else 'Sheet1'
            data.to_excel(writer, sheet_name=sheet_name, index=False)

            if chapter_column:
                interpretation_df = _build_chapter_interpretations(
                    data=data,
                    chapter_column=chapter_column,
                    interpretation_column=interpretation_column,
                )
                interpretation_df.to_excel(
                    writer, sheet_name=interpretation_sheet_name, index=False
                )
        elif isinstance(data, list):
            # Handle a list of DataFrames
            if sheet_names is None:
                # Default sheet names if none are provided
                sheet_names = [f"Sheet{i + 1}" for i in range(len(data))]
            elif not isinstance(sheet_names, list) or len(sheet_names) != len(data):
                raise ValueError("sheet_names must be a list with the same length as the data list.")
            
            for df, sheet_name in zip(data, sheet_names):
                if not isinstance(df, pd.DataFrame):
                    raise ValueError(f"All elements in the data list must be DataFrames.")
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            raise ValueError("Input data must be a DataFrame or a list of DataFrames.")
