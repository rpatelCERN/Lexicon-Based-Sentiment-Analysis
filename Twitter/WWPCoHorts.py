import twint
import pandas as pd

# Configure
###Global options set to mine the replies to a single post from USArmy: How has serving impacted you?
c = twint.Config()
c.Username = "wwp"
c.Count=True
c.Lowercase=True
c.Store_csv=True
c.Show_hashtags=True

SearchTerms=["homeless", "injury", "ptsd", "mst", "substance", "caregiver"]
DropThese=["conversation_id","created_at","date","time","timezone","name","place","language","mentions","photos","replies_count","retweets_count","cashtags","link","retweet","quote_url","video","thumbnail","near","geo","source","user_rt","user_rt_id","retweet_id","reply_to","retweet_date","translate","trans_src","trans_dest"]

for s in SearchTerms:
	c.Search=s
	c.Output=s+"TwintWWP.csv"
	twint.run.Search(c)
	input_df=pd.read_csv(s+"TwintWWP.csv")
	input_df.drop(labels=DropThese,inplace=True,axis=1)
	print(input_df.head())
	input_df.to_csv(s+'Formatted.csv')

