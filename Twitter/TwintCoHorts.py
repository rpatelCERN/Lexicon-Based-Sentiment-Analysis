import twint
import pandas as pd

# Configure
###Global options set to mine the replies to a single post from USArmy: How has serving impacted you?
c = twint.Config()
c.Since="2019-05-24"
c.Until="2019-06-01"
c.To = "USArmy"
c.Count=True
c.Lowercase=True
c.Store_csv=True
c.Show_hashtags=True

SearchTerms=["ptsd", "depression", "anxiety", "sexual", "substance", "VA"]
DropThese=["conversation_id","created_at","date","time","timezone","name","place","language","mentions","photos","replies_count","retweets_count","cashtags","link","retweet","quote_url","video","thumbnail","near","geo","source","user_rt","user_rt_id","retweet_id","reply_to","retweet_date","urls","translate","trans_src","trans_dest"]

for s in SearchTerms:
	c.Search=s
	c.Output=s+"Twint.csv"
	twint.run.Search(c)
	input_df=pd.read_csv(s+"Twint.csv")
	input_df=input_df[input_df.conversation_id==1131682502165315585]
	input_df.drop(labels=DropThese,inplace=True,axis=1)
	print(input_df.head())
	input_df.to_csv(s+'Formatted.csv')

