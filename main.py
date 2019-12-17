"""Main."""
import csv
import time
import functools
import pandas as pd
from neologger import logger


logger = logger.Logger(__name__)


def timeit(func):
    """Log function execute duration."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_timestamp = time.time()
        result = func(*args, **kwargs)
        logger.info(
            'time cost {duration}'.format(
                duration=time.time() - start_timestamp
            )
        )
        return result

    return wrapper

def read_data():
    """Read data from csv and return pandas dataFrame."""
    with open("./src/classifier_output.csv") as csv_file:
        rows = csv.reader(csv_file)
        headers = next(rows, None)
        arr = []
        for row in rows:
            arr.append(row)
        df = pd.DataFrame(arr, columns = headers)
        return df



@timeit
def main():
    """Main."""
    df = read_data()
    logger.info(df)


if __name__ == "__main__":
    main()
