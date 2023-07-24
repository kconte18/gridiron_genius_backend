import numpy as np
import pandas as pd

from .web_scrape import cbs, fantasypros, fftoday, footballguys, thescore

def web_scrap_to_db():
    try:
        rankings = fantasypros.web_scrape()
        return rankings[0]['df']
    except:
        return "Nope"
    # obj = rb_df.head()