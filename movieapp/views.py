from django.shortcuts import render,redirect
from movieapp.forms import MovieForm,MoviereviewForm
from movieapp.models import Movie,Moviereview
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews,stopwords
import string
def extract_features(word_list):
    #adding punctuation to the list of words to be removed
    #'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'   ==>string.punctuation
    
    remove_list=list(string.punctuation)

    #adding stopwords to remove list
    #['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours',
    #'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself',
    #'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those',
    #'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a',
    #'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
    #'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
    #'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
    #'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
    #'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't",
    #'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
    #'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren',
    #"weren't", 'won', "won't", 'wouldn', "wouldn't"]

    stopwordsnew=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours',
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself',
    'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those',
    'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a',
    'an', 'the', 'and', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
    'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
    'over', 'under', 'again', 'further', 'then', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
    'more', 'most', 'other', 'some', 'such','own', 'same', 'so', 'than','s', 't', 'd', 'll','o', 'm', 're', 've']
    for sw in stopwordsnew:
        remove_list.append(sw)
    cleaned={}
    for word in word_list:
        if word not in remove_list:
            cleaned[word.lower()]=True
    return cleaned
def predictsentiment(st):
    positive_fileids = movie_reviews.fileids('pos')

    
    #print(type(positive_fileids),"positive",positive_fileids[:5])
    #output  <class 'list'> positive ['pos/cv000_29590.txt', 'pos/cv001_18431.txt', 'pos/cv002_15918.txt', 'pos/cv003_11664.txt', 'pos/cv004_11636.txt']
    #Returns a list of file names in neg dir
    
    negative_fileids = movie_reviews.fileids('neg')
    

    #===> movie_reviews.words(fileids='pos/cv000_29590.txt') returns the list of words in that file
    
    features_positive = [(extract_features(movie_reviews.words(fileids=[f])),'Positive') for f in positive_fileids]
    #print("positive features",features_positive[:1][:1])
    features_negative = [(extract_features(movie_reviews.words(fileids=[f])),'Negative') for f in negative_fileids]
    #print("negative features",features_negative[:1][:1])

    
    threshold_factor=0.8
    threshold_positive= int(threshold_factor * len(features_positive))
    threshold_negative= int(threshold_factor * len(features_negative))
    features_train = features_positive[:threshold_positive]+features_negative[:threshold_negative]
    #features_train one data==> [({'book':True},'Positive')]
    #print("features train",features_train[:1])
    features_test = features_positive[threshold_positive:]+features_negative[threshold_negative:]
    #print("\nNumber of training datapoints:", len(features_train))
    #print("Number of test datapoints:", len(features_test))
    classifier = NaiveBayesClassifier.train(features_train)
    #print("\nAccuracy of the classifier:", nltk.classify.util.accuracy(classifier, features_test))
    #print("\nPredictions:")
    #print("Enter review")
    #st=input()
    #print("\nReview:", st)
    probdist = classifier.prob_classify(extract_features(st.split()))
    pred_sentiment = probdist.max()
    #print("Predicted sentiment:", pred_sentiment)
    #print("Probability:", round(probdist.prob(pred_sentiment), 2))
    return pred_sentiment


 
def sentiment_scores(sentence): 
    sid_obj = SentimentIntensityAnalyzer() 
    sentiment_dict = sid_obj.polarity_scores(sentence) 
  
    # decide sentiment as positive, negative and neutral 
    if sentiment_dict['compound'] >= 0.05 : 
        return "Positive"
  
    elif sentiment_dict['compound'] <= - 0.05 : 
        return "Negative"
  
    else : 
        return "Neutral"

# Create your views here.
def movieadd(request):
    if(request.method=="POST"):
        form=MovieForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect("/showmovie")
            except:
                pass
    else:
        form=MovieForm()
    return render(request,"takemovie.html",{'form':form})
def showmovie(request):
    movies=Movie.objects.all()
    return render(request,"showmovie.html",{'movies':movies})
def delmovie(request,id):
    movie=Movie.objects.get(id=id)
    movie.delete()
    return redirect("/showmovie")
def editmovie(request,id):
    movies=Movie.objects.get(id=id)
    return render(request,"editmovie.html",{'movies':movies})
def updatemovie(request,id):
    movies=Movie.objects.get(id=id)
    form=MovieForm(request.POST,instance=movies)
    if(form.is_valid()):
        form.save()
        return redirect("/showmovie")
    return render(request,"editmovie.html",{'movies':movies})
def reviewadd(request,id):
    movieid=id
    if(request.method=="POST"):
        print("in first if")
        form=MoviereviewForm(request.POST)
        if(form.is_valid()):
            try:
                print("second if")
                temp=form.save(commit=False)
                print("saved")
                temp.movieid=id
                print("movieid")
                temp.sentinaive=predictsentiment(temp.review)
                print("naive",temp.sentivader)
                temp.sentivader=sentiment_scores(temp.review)
                print("vader",temp.sentinaive,"naive",temp.sentivader)
                temp.save()
                return redirect("/showreview/"+str(id))
            except:
                pass
    else:
        print("inelse")
        form=MoviereviewForm()
    return render(request,"takereview.html",{'form':form,'movieid':id})
def showreview(request,id):
    print("id=",id,type(id))
    #try:
    reviews=Moviereview.objects.filter(movieid=id)
    print("in showreview try",reviews)
    return render(request,"showreview.html",{'reviews':reviews,'movieid':id})
    #except:
    #    print("in except of show")
    #   return redirect("/reviewadd/"+str(id))
def delreview(request,id,movieid):
    review=Moviereview.objects.get(id=id)
    ###check with review.movieid
    review.delete()
    return redirect("/showreview/"+str(movieid))
def editreview(request,id):
    reviews=Moviereview.objects.get(id=id)
    return render(request,"editreview.html",{'reviews':reviews})
def updatereview(request,id):
    reviews=Moviereview.objects.get(id=id)
    tempid=reviews.movieid
    tempsenti=reviews.sentivader
    form=MoviereviewForm(request.POST,instance=reviews)
    if(form.is_valid()):
        temp=form.save(commit=False)
        temp.movieid=tempid
        temp.sentinaive=predictsentiment(form.cleaned_data['review'])
        temp.sentivader=sentiment_scores(form.cleaned_data['review'])
        temp.save()
        return redirect("/showreview/"+str(tempid))
    return render(request,"editreview.html",{'reviews':reviews})
def showgraph(request,id):
    poscount=Moviereview.objects.filter(movieid=id,sentivader="Positive").count()
    negcount=Moviereview.objects.filter(movieid=id,sentivader="Negative").count()
    return render(request,"showgraph.html",{'poscount':poscount,'negcount':negcount})



