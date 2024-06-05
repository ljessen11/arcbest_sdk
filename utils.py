from datetime import datetime
import pprint


pp = pprint.PrettyPrinter(indent=4)

def bool_to_str(x: bool | None) -> str:
    return 'Y' if x else 'N'


def get_current_date_as_tuple() -> tuple:
    now = datetime.now()
    return (now.day, now.month, now.year)
