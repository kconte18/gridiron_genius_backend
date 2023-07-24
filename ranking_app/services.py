import numpy as np
import pandas as pd

from .web_scrape import cbs, fantasypros, fftoday, footballguys, thescore

def web_scrap_to_db():
    try:
        fantasypros.web_scrape
    except:
        return "Nope"
    # obj = rb_df.head()