from time import time
import matplotlib.pyplot as plt
import pyLDAvis

import util.mysql as mysql
from gensim import corpora, models
import pyLDAvis.gensim as ldaVis


def buildCorpus():
    t0 = time()
    results = mysql.selectWordToken()
    print('Get data samples :', len(results))
    docs_words = [doc.split() for doc in results]

    # # build n-grams
    # # build bigrams：
    # bigram = models.Phrases(docs_words, min_count=5,threshold=50) # higher threshold fewer phrases.
    # bigram_mod = models.phrases.Phraser(bigram)
    # data_sample=[bigram_mod[doc] for doc in docs_words]

    # build trigram:
    # trigram = models.Phrases(bigram[docs_words], threshold=100)
    # trigram_mod = models.phrases.Phraser(trigram)
    # data_sample=[trigram_mod[bigram_mod[doc]] for doc in docs_words]

    data_sample=docs_words
    dictionary = corpora.Dictionary(data_sample)
    doc_bow = [dictionary.doc2bow(doc) for doc in data_sample]

    # print(doc_bow[0])
    print("Get corpus，cost time:  %0.3f s." % (time() - t0))
    return doc_bow, dictionary, data_sample


def findBestParameters():
    # only transcripts
    corpus, dictionary, data_sample = buildCorpus()
    # TODO
    chunksizes = [512, 1024,2048, 4096, 8192,16384]
    passes_value = [20,30]
    max_topics = 15
    time_start = time()
    path = 'output files/txt files/parameters results.txt'
    for passes in passes_value:
        for chunksize in chunksizes:
            print('passes=', passes, ' chunksize=', chunksize)

            x = []
            coherence_values = []
            model_list = []

            with open(path, 'a', encoding='utf-8') as file:
                file.write('passes=' + str(passes))
                file.write('  chunksize =' + str(chunksize) + '\n')

            for topic in range(2, max_topics):
                x.append(topic + 1)
                print(" Number of Topics= ", topic + 1)
                t0 = time()
                lda_model = models.LdaModel(corpus=corpus, num_topics=topic + 1, id2word=dictionary, alpha='auto',
                                            passes=passes, chunksize=chunksize, random_state=42)
                costed_time = str(time() - t0)
                print('     train model using :', costed_time)
                model_list.append(lda_model)

                # calculate coherence
                coherence_model = models.CoherenceModel(model=lda_model, texts=data_sample, dictionary=dictionary,
                                                       coherence='c_v')
                coherence = coherence_model.get_coherence()
                print('     coherence: ', coherence)
                coherence_values.append(coherence)
                # if coherence is very high,then save model.

                if coherence > 0.4:
                    lda_model.save('p{}_c{}_lda_model_numT{}.model'.format(passes, chunksize, str(topic + 1)))

                # Store them into txt
                numtopics_store = str('   number of topics = ' + str(topic + 1) + '\n')
                coherence_store = str('       coherence= ' + str(coherence) + '\n')
                ctime_store = str('       the costed time = ' + str(costed_time) + '\n')

                with open(path, 'a', encoding='utf-8') as file:
                    file.write(numtopics_store)
                    file.write(coherence_store)
                    file.write(ctime_store)


            print('coherence_values: ', coherence_values)

            # line chart
            plt.plot(x, coherence_values)
            plt.title("Finding best number of topics:  coherence")
            plt.xlabel("Number of Topics ")
            plt.ylabel("coherence score")
            plt.savefig('output files/0 line charts temp/p{}_c{}_number_of_topic_with_coherence.jpg'.format(passes, chunksize))
            plt.show()

    # record costed time on training model.
    total_time = time() - time_start
    print('total_time: ', total_time)
    with open(path, 'a', encoding='utf-8') as file:
        file.write('total_time=' + str(total_time))


# Make LDAvis
def LDAvis():
    doc_bow, dictionary, data_sample = buildCorpus()
    pathes = [ '{}p10_c1024_lda_model_numT5.{}','{}p20_c1024_lda_model_numT5.{}']
    for path in pathes:
        lda = models.LdaModel.load(path.format('','model'))
        print('model load!')
        visulisation = ldaVis.prepare(lda, doc_bow, dictionary)
        pyLDAvis.save_html(visulisation, path.format('output files/pyLDAvis visualisation/','html'))
