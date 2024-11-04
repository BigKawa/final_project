import pandas as pd


def first_clean(dataframe):
    """
    This function is used to clean the given dataframe by setting the index as fiscalDateEnding,
    and filling NaN values with 0. It is used to clean the balance sheet and cash flow data of
    Microsoft.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        The dataframe to be cleaned.

    Returns
    -------
    pandas.DataFrame
        The cleaned dataframe.
    """
    dataframe.columns = dataframe.iloc[0]
    dataframe = dataframe[2:]
    dataframe.set_index("fiscalDateEnding", inplace=True)  # Set the index as fiscalDateEnding
    dataframe = dataframe.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)  # Fill NaN with 0
    return dataframe
