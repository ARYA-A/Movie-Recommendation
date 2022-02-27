import pandas as pd


df = pd.read_csv("dfmaster.csv")
titlerow=df[['title']]
descrow=df[['desc']]




#searchquery=input("Enter the search Query:-")#movie name
def cosine_distance_countvectorizer_method(s1, s2):
    # sentences to list
    allsentences = [s1, s2]
    # packages
    from sklearn.feature_extraction.text import CountVectorizer
    from scipy.spatial import distance
    # text to vector
    vectorizer = CountVectorizer()
    all_sentences_to_vector = vectorizer.fit_transform(allsentences)
    text_to_vector_v1 = all_sentences_to_vector.toarray()[1].tolist()
    text_to_vector_v2 = all_sentences_to_vector.toarray()[0].tolist()
    # distance of similarity
    cosine = distance.cosine(text_to_vector_v1, text_to_vector_v2)
    percentage=round((1 - cosine) * 100, 2)
    #print('Similarity of two sentences are equal to ',percentage, '%')
    return cosine,percentage

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


def getthemoviescoresfordescription(movievalue,moviedescription):
    temp_score = ""
    temp_percentage = ""
    score_list = []
    # iterate over column 'desc' and pass the:- 'moviedescription' and iterated 'desc value' to cosine function
    for i in range(0, len(movievalue), 1):
        temp_score, temp_percentage = cosine_distance_countvectorizer_method(moviedescription, movievalue[i])
        score_list.append(temp_score)
    return score_list


def sortthelist(list):
    # sort the list
    sorted_list = sorted(list,reverse=True)
    print("Score List:-", list)
    print("Sorted Score List:-", sorted_list)
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
    for column in titlerow:
        columnSeriesObj = df[column]
        value = columnSeriesObj.values
        for i in range(0,len(value), 1):
            movie = value[i]
            print("-----------------------------------------------------------------------------")
            print("Movie Name:-", movie)
            indexno = getrowindex(df, titlerow, value[i])
            movievalue, moviedescription = getcolumnvalue(df, descrow, indexno)
            score_list = getthemoviescoresfordescription(movievalue, moviedescription)
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