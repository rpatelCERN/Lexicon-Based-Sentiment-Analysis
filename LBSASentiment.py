from src import lbsa
import pytextrank
import spacy
from spacy.matcher import PhraseMatcher
from matplotlib import pyplot as plt
import seaborn as sns
import pandas  as pd
import sys
file=sys.argv[1]
op_lexicon = lbsa.get_lexicon('opinion', language='english', source='afinn')###close to what you get with AFINN
sa_lexicon = lbsa.get_lexicon('sa', language='english', source='custom')#### Strange classification


def InitNLPPyTextRank():
    nlpPyRank = spacy.load("en_core_web_sm")
    tr = pytextrank.TextRank()
    # add PyTextRank to the spaCy pipeline
    nlpPyRank.add_pipe(tr.PipelineComponent, name="textrank", last=True)

    return nlpPyRank
def TextRank(doc):
 #doc = nlp(text)
 return doc._.phrases

def LoadMatchPatterns(nlp,matcher):
    patternLibrary=pd.read_csv('data/FilledPatternPhrases.csv')
    PatternDefs=list(patternLibrary.columns.values)
    for i in range(2,len(PatternDefs)):
        ListTerms=(patternLibrary[patternLibrary[PatternDefs[i]]==1].pattern).to_list()
        patterns = [nlp.make_doc(term) for term in ListTerms]
        matcher.add(PatternDefs[i], None, *patterns)
    del patternLibrary
    return matcher

def MatchPatterns(nlp,matcher,doc):
    MatchedCategory=[]
    MatchedPhrases=[]
    for match_id, start, end in matcher(doc):
            MatchedPhrases.append(doc[start:end].text)
            MatchedCategory.append(nlp.vocab.strings[match_id])
    return MatchedCategory,MatchedPhrases

def AnalyzeStory(file):
    f=open(file, 'r')
    lines=f.readlines()
    nlp = spacy.load('en')
    docs=nlp.pipe(lines)
    matcher = PhraseMatcher(nlp.vocab)
    LoadMatchPatterns(nlp,matcher)
    OutputDictionary={'TextParagraph':[],'SentimentScore':[],'MatchedPhrases':[],'Challenge':[],'Renewal':[],
    'anger': [], 'anticipation': [], 'disgust': [], 'fear': [], 'joy': [], 'sadness': [], 'surprise': [],
    'trust': [], 'disconnection': [], 'connection': []}

    for doc in docs:
        if len(doc)==1:continue ###Skip \n
        OutputDictionary['TextParagraph'].append(doc.text)
        SentScore=op_lexicon.process(doc.text)
        SentAnalysis=sa_lexicon.process(doc.text)
        #print(doc.text,SentScore,SentAnalysis)
        OutputDictionary['SentimentScore'].append(SentScore['positive']-SentScore['negative'])
        MatchedCategory,MatchedPhrases=MatchPatterns(nlp,matcher,doc)
        OutputDictionary['MatchedPhrases'].append(" ".join(MatchedPhrases))
        SentAnalysis['disconnection']=SentAnalysis['disconnection']+MatchedCategory.count("Disconnection")
        SentAnalysis['connection']=SentAnalysis['connection']+MatchedCategory.count("Connection")
        OutputDictionary['Challenge'].append(MatchedCategory.count("Challenges"))
        OutputDictionary['Renewal'].append(MatchedCategory.count("Renewal"))

        for key in SentAnalysis.keys():OutputDictionary[key].append(SentAnalysis[key])
            #.append(SentScore['positive']-SentScore['negative'])
    outputDF=pd.DataFrame(OutputDictionary)
    outputDF.to_csv("output/Test.csv")


def AnalyzeTweet(file):
    TweetTL=pd.read_table(file)
    Tweets=TweetTL['tweet'].to_list()
    nlp = spacy.load('en')
    docs=nlp.pipe(Tweets)
    matcher = PhraseMatcher(nlp.vocab)
    LoadMatchPatterns(nlp,matcher)

    OutputDictionary={'TextParagraph':[],'SentimentScore':[],'MatchedPhrases':[],'Challenge':[],'Renewal':[],
        'anger': [], 'anticipation': [], 'disgust': [], 'fear': [], 'joy': [], 'sadness': [], 'surprise': [],
        'trust': [], 'disconnection': [], 'connection': []}

    for doc in docs:
        Sentiment=op_lexicon.process(doc.text)
        SentScore=Sentiment["positive"]-Sentiment["negative"]
        MatchedCategory,MatchedPhrases=MatchPatterns(nlp,matcher,doc)
        if SentScore==0 and len(MatchedPhrases)==0 :continue
        #for match_id, start, end in matcher(doc):print(doc.text,doc[start:end],nlp.vocab.strings[match_id])
        #This doesn't work as well for tweets
        OutputDictionary['TextParagraph'].append(doc.text)
        SentAnalysis=sa_lexicon.process(doc.text)
        OutputDictionary['SentimentScore'].append(SentScore)
        MatchedCategory,MatchedPhrases=MatchPatterns(nlp,matcher,doc)
        OutputDictionary['MatchedPhrases'].append(" ".join(MatchedPhrases))
        SentAnalysis['disconnection']=SentAnalysis['disconnection']+MatchedCategory.count("Disconnection")
        SentAnalysis['connection']=SentAnalysis['connection']+MatchedCategory.count("Connection")
        OutputDictionary['Challenge'].append(MatchedCategory.count("Challenges"))
        OutputDictionary['Renewal'].append(MatchedCategory.count("Renewal"))
        for key in SentAnalysis.keys():OutputDictionary[key].append(SentAnalysis[key])

    outputDF=pd.DataFrame(OutputDictionary)
    outputDF.to_csv("output/Test.csv")
AnalyzeTweet(file)
#AnalyzeStory(file)
