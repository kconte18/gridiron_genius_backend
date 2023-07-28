import pandas as pd

from ..data import rankings_sources
from .. import helpers

sources = rankings_sources.footballguys_sources

def web_scrape(players_dict):
    for source in sources:
        rb_df = pd.read_html(source['url'])
        raw_df = rb_df[0].iloc[lambda x: x.index < 112]
        column_list = raw_df.columns.tolist()
        
        rank_column_value = column_list[0]
        column_list.remove(rank_column_value)
        column_list.remove('Player')
        df = raw_df.drop(columns=column_list)
        df = df.rename(columns={rank_column_value:'Rank'})
        df = df[df["Rank"].str.contains("Tier") == False]
        df['Player'] = df['Player'].str.rstrip(' ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        df = df.reindex(columns=['Player', 'Rank'])
        
        source['df_list'] = helpers.swap_name_with_id(df, players_dict)
    return sources