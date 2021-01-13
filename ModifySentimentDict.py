import spacy
import pandas as pd


ConnectionWords=["chat","hired","invited","save","saved","volunteered","community","peer","peers","mentor",
"partnership","activities","cohort","ambassadors","connection","connect","connects","connecting","connected","reconnect","reconnected",
"comrades","fellow","bond","engagement","gatherings","outings","dinners","events","meets","met","friend","friendly","engage","children","siblings","caregivers","caregiver","household","comradery","enrolled","compassionate","kindly","traveled","degradation"]

DisconnectionWords=["denied","disowned","disown","deny","discharged","reject","rejected","disqualifies","abuse"
"slapped","overcrowding","overcrowded","punched","dehumanized","lonely","refuse","threatened","fired","isolated","stigma",
"stigmas","biases","barriers","alone","isolation","fired","threatened","divorced","trapped","helpless","homelessness","broken","separated"]

NewColumnsDict={'Connection':ConnectionWords,'Disconnection':DisconnectionWords}

ConnectionPhrases=['kindness from strangers','supportive family','stay with','saved me',
'comfortable socializing','were nice','huge heart','around people','feel heard','support system','peer support',
'community support','support structures','my fellow','my friend','a reading group','attached at the hip',
'a big family','guards down','community service','friends of mine','career opportunities','taking care','work for'
'talking to total strangers','friend for life','close with','help others','my first love','beloved parents'
]

DisconnectionPhrases=['made fun of','nobody hired me','difficulty being with','problems getting close to people',
'turn a blind eye','socializing feels dangerous','treated me like an object','walls were closing in','left behind',
'wholly inadequate','never asked anyone','custody battle','missed the birth','afraid of men','nowhere to go'

]

Challenges=['alcohol','ptsd','depression','suicide','high anxiety','military sexual trauma','mst','popping pills',
'substance use disorder','prescription drugs','opioids','drugs','rock bottom','in pain','homelessness','shelter','shelters'
'medical debts','in crisis','housing assistance','harsh living conditions','panic attack','panic attacks','flashbacks',
'paperwork','pay rent','sexually assaulted','TBI','injury','nightmares','night terrors','scared of myself','dark times',
'sexual harassment','self destruct','re-traumatized','domestic abuse','life insurance','medical discharge','seizure',
'intimate partner abuse','traumatic brain injury','amputated','self-medicate','long days','compulsive behavior','frustration',
'constant care','incarceration','jail','prison','self harm','racism','bad back','knee','hearing','tinnitus','bad back',
'sleep','sleepless nights','lumbar','awake','abusive','debt','trans','LGBT'
]

Renewal=['blessing','forever grateful','new journey','strong mother','strong father','hold my ground','positive life',
'better version of myself','not give up','recovery','healing','a new way','empowerment','success story','success stories',
'proud of myself','resilient','2nd chance','second chance','regain','new passion','tools to cope','work toward the future',
'bigger purpose','i persevered','a new mission']

NewColumnsPhrases={'Connection':ConnectionPhrases,'Disconnection':DisconnectionPhrases,
'Challenges':Challenges,'Renewal':Renewal}



def UpdateDictionary(IndexLookup,dictionaryFill, columname,WordSet):
    Counts=dictionaryFill[columname]
    for s in WordSet:
        #print(s)
        WordIndex=IndexLookup[IndexLookup==s].index[0]
        Counts[WordIndex]=Counts[WordIndex]+1
    dictionaryFill[columname]=Counts
    return dictionaryFill
def ModifyLSATokenScores(NewColumnsDict):
    input_LSA=pd.read_csv("data/TemplateNRCEmotions.csv")
    print(input_LSA.shape)
    OriginalTable=input_LSA.to_dict(orient='series')
    IndexLookup=OriginalTable['English Word']
    terms=set(input_LSA["English Word"].to_list())
    dictionaryFill={}
    NewColumns=[key for key in NewColumnsDict.keys()]
    for c in NewColumns:dictionaryFill[c]=[0 for r in range(input_LSA.shape[0])]### No Word scrore
    for key in NewColumnsDict.keys():
        dictionaryFill=UpdateDictionary(IndexLookup,dictionaryFill,key,terms.intersection(set(NewColumnsDict[key])))
        input_LSA.insert(loc=input_LSA.shape[1],column=key,value=dictionaryFill[key])
    ####Add rows for new words:
    ColNames=list(input_LSA.columns.values)
    WordsToAdd={}
    for ckey in NewColumnsDict.keys():
        NewWords=list(set(NewColumnsDict[ckey])-terms.intersection(set(NewColumnsDict[ckey])))
        EmoDefinitions={}
        for w in NewWords:EmoDefinitions[w]=[ckey]
        for c in ColNames:
            if 'Word' in c:
                WordsToAdd[c]=[key for key in EmoDefinitions.keys()]
                continue
            WordsToAdd[c]=[ int(c in EmoDefinitions[key]) for key in EmoDefinitions.keys() ]
        WordsDF=pd.DataFrame(data=WordsToAdd)
        input_LSA=pd.concat([WordsDF, input_LSA])
        del WordsDF
    input_LSA.to_csv("data/FilledEmotions.csv")
    print(input_LSA.shape)

def BuildMatchPatterns(NewColumnsPhrases):
    ###Write out phrases to a csv to read back for pattern matching
    PhraseDictionary={'pattern':[]}
    for key in NewColumnsPhrases.keys():
        PhraseDictionary['pattern'].extend(NewColumnsPhrases[key])#### Load all words
        PhraseDictionary[key]=[]
    for pattern in PhraseDictionary['pattern']:
            for key in NewColumnsPhrases.keys():PhraseDictionary[key].append(int(pattern in NewColumnsPhrases[key]))
    print(PhraseDictionary)
    outputDF=pd.DataFrame(PhraseDictionary)
    outputDF.to_csv("data/FilledPatternPhrases.csv")

ModifyLSATokenScores(NewColumnsDict)
BuildMatchPatterns(NewColumnsPhrases)
