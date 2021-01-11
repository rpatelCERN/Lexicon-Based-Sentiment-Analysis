from src import lbsa
op_lexicon = lbsa.get_lexicon('opinion', language='english', source='afinn')###close to what you get with AFINN
sa_lexicon = lbsa.get_lexicon('sa', language='english', source='custom')#### Strange classification


f=open("../twint/AngiePeacockSexualAssault.txt", 'r')
lines=f.readlines()
for i in range(len(lines)):print (lines[i],op_lexicon.process(lines[i]),sa_lexicon.process(lines[i]))
