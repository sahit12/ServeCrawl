from django.shortcuts import render
from .scripts.crawl import crawl_wiki
from .scripts.crawl import relevance_search
from .scripts.crawl import extract
from gensim.summarization.summarizer import summarize
from .scripts.crawl import servenlp

def home(request):
    return render(request, 'crawl/home.html')

def about(request):
    return render(request, 'crawl/about.html', {'title_head' : 'About'})

def wiki_data(request):
    if request.method == 'POST':
        searchword = request.POST['searchword']
        inputTitle = request.POST['inputTitle']
        inputLink = request.POST['inputLink']
        inputArticleSize = request.POST['inputArticleSize']
        inputTotalArticleWords = request.POST['inputTotalArticleWords']
        inputDate = request.POST['inputDate']

        es = relevance_search.RelevantSearch(searchword)
        print(es.check_url_authenticity())
        results = es.extract_relevant(
            title=inputTitle,
            link=inputLink,
            article_size=inputArticleSize,
            total_article_words=inputTotalArticleWords,
            date=inputDate
        )

        return render(request, 'crawl/wiki_data.html', { 'results' : results })
    else:
        return render(request, 'crawl/wiki_data.html')

def extract_summ(request):
    if request.method == "POST":
        sumlink = request.POST["sumlink"]
        p_tags = extract.extract_summary(sumlink)
        joined_p_tags = "".join(p_tags)
        result = summarize(joined_p_tags)

        # Do NLP- find frequency of words
        # tokenize words
        word_tokens = servenlp.ServeNLP.serve_word_token(joined_p_tags, stopwords='yes')
        freq_wa = servenlp.ServeNLP.serve_word_frequency(word_tokens)

        return render(request, 'crawl/summary.html', { 'results' : result, 'frequency' : freq_wa })
    else:
        return render(request, 'crawl/summary.html')