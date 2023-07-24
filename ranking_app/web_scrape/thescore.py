import pandas as pd

urls = ['https://www.thescore.com/news/2563170', 'https://www.thescore.com/news/2563174', 'https://www.thescore.com/news/2541042']

def web_scrape():
    for url in urls:    
        rb_df = pd.read_html(urls[0])
        df = rb_df[0].iloc[lambda x: x.index < 100]
        df = df.drop(columns=["Team", "Pos."])
        df = df.rename(columns={"Player":"player_name", "Rank":"rank"})
        print(df)