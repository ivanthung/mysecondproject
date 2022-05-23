from mysecondproject.printstats import print_dataframe
import pandas as pd

def test_random_function():

    d = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data=d)

    result = print_dataframe(df)
    assert isinstance(result, pd.DataFrame)
