import pandas as pd

urls=['https://www.footballguys.com/rankings/duration/preseason?pos=all&ppr=0', 'https://www.footballguys.com/rankings/duration/preseason?pos=all&ppr=1']

def web_scrape():
    for url in urls:
        rb_df = pd.read_html(url)
        raw_df = rb_df[0].iloc[lambda x: x.index < 112]
        column_list = raw_df.columns.tolist()
        column_list.remove('Footballguys Consensus (all 24 experts)  edit  Rank')
        column_list.remove('Player')
        df = raw_df.drop(columns=column_list)
        df = df.rename(columns={'Footballguys Consensus (all 24 experts)  edit  Rank':'Rank'})
        df = df[df["Rank"].str.contains("Tier") == False]
        df['Player'] = df['Player'].str.rstrip(' ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        print(df)