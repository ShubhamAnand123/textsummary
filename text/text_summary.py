import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
text=""" The Churel, also spelled as Charail, Churreyl, Chudail, Chudel, Chuṛail, Cuḍail or Cuḍel (Hindi: चुड़ैल, Urdu: چڑیل) is a mythical or legendary creature resembling a woman, which may be a demoniacal revenant said to occur in South Asia and Southeast Asia, particularly popular in India, Bangladesh, Nepal and Pakistan. The churel is typically described as "the ghost of an unpurified living thing", but because she is often said to latch on to trees, she is also called a tree-spirit.[1] According to some legends, a woman who dies during childbirth or pregnancy or from suffering at the hands of her in-laws will come back as a revenant churel for revenge, 
particularly targeting the males in her family.The churel is mostly described as extremely ugly and hideous but is able to shape-shift and disguise herself as a beautiful woman to lure men into the woods or mountains where she either kills them or sucks up their life-force or virility, turning them into old men. Their feet are believed to be turned the other way around, so the toes face the direction of their back.
There are many folk remedies and folkloric sayings that elaborate on how to get rid of revenant and ghostly churels, and a number measures that supposedly prevent churels from coming to life. The family of a woman who dies a traumatic, tragic, or unnatural death might perform special rituals fearing that the victimised woman might return as a churel. The corpses of suspected churels are also buried in a particular method and posture so as to prevent her from returning.
The churel is known as the Pichal Peri in the Punjab region of India and Pakistan, Petni/Shakchunni in the Bengal region, and Pontianak in Malaysia and Indonesia. The word "churel" is also often used colloquially or mistakenly for a witch in India and Pakistan.[2] She has also remained prevalent in modern-day literature, cinema, television, and radio and many references to her activities and is still sighted in rural regions in South-East Asia.[3]"""
def summarizer(rawdocs):
    stopwords=list(STOP_WORDS)
    #print(stopwords)
    nlp=spacy.load("en_core_web_sm")
    doc=nlp(rawdocs)
    #print(doc)
    tokens =[token.text for token in doc]
    #print(tokens)
    word_freq={}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text]=1
            else:
                word_freq[word.text]+=1
    #print(word_freq)
    max_freq=max(word_freq.values())
    #print(max_freq)
    for word in word_freq.keys():
        word_freq[word]=word_freq[word]/max_freq
    #print(word_freq)

    sent_tokens = [sent for sent in doc.sents]
    #print(sent_tokens)
    sent_score={}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_score.keys():
                    sent_score[sent]=word_freq[word.text]
                else:
                    sent_score[sent]+=word_freq[word.text]

    #print(sent_score)
    select_len= int(len(sent_tokens)*0.2)
    #print(select_len)
    summary = nlargest(select_len,sent_score,key=sent_score.get)
    #print(summary)
    final_summary=[word.text for word in summary]
    summary=' '.join(final_summary)
   # print(text)
    #print(summary)
    #print("orignal length",len(text.split(' ')))
    #print("new length ",len(summary.split()))
    return summary,doc,len(rawdocs.split(' ')),len(summary.split())

