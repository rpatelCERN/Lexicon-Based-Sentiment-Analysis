import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:bluenote@localhost:5432/TwintPTSD')

input_df=pd.read_table("SubstanceAbuse.csv")
DropThese=["conversation_id","created_at","date","time","timezone","name","place","language","mentions","photos","replies_count","retweets_count","cashtags","link","retweet","quote_url","video","thumbnail","near","geo","source","user_rt","user_rt_id","retweet_id","reply_to","retweet_date","urls","translate","trans_src","trans_dest"]
input_df.drop(labels=DropThese,inplace=True,axis=1)
print(input_df.head())


input_df.to_csv('SubstanceAbuseFormatted.csv')
#input_df.to_sql('SubstanceAbuse', con=engine, if_exists='replace')

#print(engine.execute("SELECT * FROM SubstanceAbuse").fetchall())
