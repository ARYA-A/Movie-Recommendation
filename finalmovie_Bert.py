import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from nltk import sent_tokenize
from sentence_transformers import SentenceTransformer

df = pd.read_csv("dfmaster.csv")
titlerow=df[['title']]
descrow=df[['desc']]
desc_list = df["desc"].tolist()
movie_list=df["title"].tolist()


def process_bert_similarity(base_document,documents):
    # This will download and load the pretrained model offered by UKPLab.
    model = SentenceTransformer('bert-base-nli-mean-tokens')

    # Although it is not explicitly stated in the official document of sentence transformer, the original BERT is meant for a shorter sentence. We will feed the model by sentences instead of the whole documents.
    sentences = sent_tokenize(base_document)
    base_embeddings_sentences = model.encode(sentences)
    base_embeddings = np.mean(np.array(base_embeddings_sentences), axis=0)

    vectors = []
    for i, document in enumerate(documents):
        sentences = sent_tokenize(document)
        embeddings_sentences = model.encode(sentences)
        embeddings = np.mean(np.array(embeddings_sentences), axis=0)

        vectors.append(embeddings)

        #print("making vector at index:", i)

    scores = cosine_similarity([base_embeddings], vectors).flatten()

    return scores



#get the index of movie in title column
def getrowindex(df,rowstring,searchquery):
    for column in rowstring:
        columnSeriesObj = df[column]
        value = columnSeriesObj.values
        for i in range(0, len(value), 1):
            if searchquery in value[i]:
                indexno = i
    return indexno

#get the movie description that belongs to particular movie
def getcolumnvalue(df,columnname,indexno):
    for column in columnname:
        columnSeriesObj = df[column]
        movievalue = columnSeriesObj.values
        moviedescription = movievalue[indexno]
    print("Movie Description:-", moviedescription)
    return movievalue,moviedescription





def sortthelist(list):
    # sort the list
    sorted_list = sorted(list,reverse=True)
    #print("Score List:-", list)
    #print("Sorted Score List:-", sorted_list)
    return sorted_list

#get the index of first 5 elements excluding the first one(Movie desc user entered)
def getindexlistofsortedlist(score_list,sorted_score_list):
    indexlist = []
    counter = 1
    while True:
        for count, scorevalue in enumerate(score_list):
            if scorevalue == sorted_score_list[counter]:
                indexlist.append(count)
                counter += 1
        if counter > 5:
            break
    ("Score Index List:-", indexlist)
    return indexlist




#Get the value for titile from indexlist
def getrowvaluefortitile(indexlist,titlerow):
    related_movie_list = []
    for column in titlerow:
        columnSeriesObj = df[column]
        value = columnSeriesObj.values
        for i in range(0, 5, 1):
            inx = indexlist[i]
            related_movie_list.append(value[inx])
    print("Related Movie List:-", related_movie_list)
    return related_movie_list

listtemp=["hello","world"]

def listtostring(list):
    string = ','.join([str(elem) for elem in list])
    return string




def output():
    documents = desc_list
    for column in titlerow:
        columnSeriesObj = df[column]
        value = columnSeriesObj.values
        for i in range(0,50, 1):
            movie = value[i]
            print("-----------------------------------------------------------------------------")
            print("Movie Name:-", movie)
            indexno = getrowindex(df, titlerow, value[i])
            movievalue, moviedescription = getcolumnvalue(df, descrow, indexno)
            score_list = process_bert_similarity(moviedescription, documents)
            sorted_score_list = sortthelist(score_list)
            indexlist = getindexlistofsortedlist(score_list, sorted_score_list)
            related_movie_list = getrowvaluefortitile(indexlist, titlerow)
            related_movie_string = listtostring(related_movie_list)
            mapped=zip(related_movie_list,sorted_score_list[1:6])
            #print("sorted_score_list :-", sorted_score_list[1:6])
            mapped_string=listtostring(set(mapped))
            #print(mapped_string)
            df.at[i, 'Related_movie_list'] = mapped_string
            print("-----------------------------------------------------------------------------")
    df.to_csv("dfmaster.csv", index=False)




output()

#Prometheus