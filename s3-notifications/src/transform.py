import pandas as pd
from src._types import Data


def transform_data(data: Data) -> pd.DataFrame:
    rows = []
    for task in data['tasks']:
        for result in task['result']:
            row = {
                'keyword': result['keyword'],
                'location_code': result['location_code'],
                'language_code': result['language_code'],
                'competition': result['competition'],
                'competition_index': result['competition_index'],
                'search_volume': result['search_volume'],
                'low_top_of_page_bid': result['low_top_of_page_bid'],
                'high_top_of_page_bid': result['high_top_of_page_bid'],
                'cpc': result['cpc']
            }
            rows.append(row)
    return pd.DataFrame(rows)
