import pandas as pd

from .. import helpers
from ..data import rankings_sources

sources = rankings_sources.thescore_sources

def web_scrape(players_dict):
    for source in sources:    
        rb_df = pd.read_html(source['url'])
        if(source['position_ranking_type'] == 'OVERALL'):
            df = rb_df[0].iloc[lambda x: x.index < 100]
            df = df.drop(columns=["Pos."])
        elif(source['position_ranking_type'] == 'QB'):
            df = rb_df[0].iloc[lambda x: x.index < 32]
        elif(source['position_ranking_type'] == 'RB'):
            df = rb_df[0].iloc[lambda x: x.index < 50]
        elif(source['position_ranking_type'] == 'WR'):
            df = rb_df[0].iloc[lambda x: x.index < 50]
        elif(source['position_ranking_type'] == 'TE'):
            df = rb_df[0].iloc[lambda x: x.index < 40]
        df = df.drop(columns=["Team"])
        # df = df.rename(columns={"Player":"Player", "Rank":"rank"})
        df = df.reindex(columns=['Player', 'Rank'])

        source['df_list'] = helpers.swap_name_with_id(df, players_dict)
    return sources