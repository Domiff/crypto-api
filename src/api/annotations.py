from datetime import datetime
from typing import Annotated, Literal

from fastapi import Query

ticker_query = Annotated[Literal["btc", "eth"], Query()]
date = Annotated[datetime, Query()]
