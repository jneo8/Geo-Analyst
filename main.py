"""Main."""
from pkg.osm_parser.pbf_parser import pbf_parser
import time
import functools
import logging


logger = logging.getLogger(__name__)


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


@timeit
def main():
    """Main."""
    pbf_parser(
        "/home/jameslin/ghtinc-Porject/Geo-Analyst/src/taiwan-latest.osm.pbf"
    )


if __name__ == "__main__":
    main()
