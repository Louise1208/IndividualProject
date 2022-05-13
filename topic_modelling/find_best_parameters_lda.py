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
    # print(results[0])
    data_sample = [doc.split() for doc in results]

    dictionary = corpora.Dictionary(data_sample)
    doc_bow = [dictionary.doc2bow(doc) for doc in data_sample]

    # print(doc_bow[0])
    print("Get corpus，cost time:  %0.3f s." % (time() - t0))
    return doc_bow, dictionary, data_sample


def findBestParameters():
    # only transcripts
    corpus, dictionary, data_sample = buildCorpus()

    chunksizes = [168,256,512,1024,2048]
    passes_value = [10,20]
    max_topics = 20
    time_start = time()
    path = 'output files/txt files/parameters results.txt'
    for passes in passes_value:
        for chunksize in chunksizes:
            print('passes=', passes, ' chunksize=', chunksize)

            x = []
            coherence_values = []

            with open(path, 'a', encoding='utf-8') as file:
                file.write('passes=' + str(passes))
                file.write('  chunksize =' + str(chunksize) + '\n')

            # range(5, max_topics)
            for topic in range(8, max_topics):
                num_topics = topic + 1

                print(" Number of Topics= ", num_topics)
                t0=time()
                lda_model = models.LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary, alpha='auto',
                                            passes=passes, chunksize=chunksize, random_state=42)
                print('         costed time on build LDA model:',time()-t0)

                print('start calculate coherence')
                # calculate coherence
                coherence_model = models.CoherenceModel(model=lda_model, texts=data_sample, dictionary=dictionary,
                                                        coherence='c_v')
                coherence = coherence_model.get_coherence()
                print('     coherence: ', coherence)
                if coherence <0.44:

                    continue

                x.append(num_topics)
                coherence_values.append(coherence)

            # if coherence is very high,then save model.
                if coherence > 0.49:
                    lda_model.save('p{}_c{}_lda_model_numT{}.model'.format(passes, chunksize, str(num_topics)))

                    # Store them into txt
                numtopics_store = str('   number of topics = ' + str(num_topics) + '\n')
                coherence_store = str('       coherence= ' + str(coherence) + '\n')
                # min_docu_store = str(
                #     '       the topic_id: ' + str(num_d_t.index(min(num_d_t))) + 'n_doc' + str(min(num_d_t)) + '\n')

                with open(path, 'a', encoding='utf-8') as file:
                    file.write(numtopics_store)
                    file.write(coherence_store)
                    # file.write(min_docu_store)

            print('coherence_values: ', coherence_values)
            # line chart
            plt.plot(x, coherence_values)
            plt.title("Line Chart of CS with Different K")
            plt.xlabel("Number of Topics(K) ")
            plt.ylabel("coherence scores(CS) ")
            plt.savefig(
                'output files/line charts/p{}_c{}_number_of_topic_with_coherence.jpg'.format(passes, chunksize))
            plt.show()

    # record costed time on training model.
    total_time = time() - time_start
    print('total_time: ', total_time)
    with open(path, 'a', encoding='utf-8') as file:
        file.write('total_time=' + str(total_time))
    return corpus, dictionary, data_sample

# Make LDAvis
def LDAvis():
    doc_bow, dictionary, data_sample = buildCorpus()
    pathes = [ '{}p10_c512_lda_model_numT7.{}']
    for path in pathes:
        lda = models.LdaModel.load(path.format('', 'model'))
        print('model load!')
        visulisation = ldaVis.prepare(lda, doc_bow, dictionary)
        pyLDAvis.save_html(visulisation, path.format('output files/pyLDAvis visualisation/', 'html'))
