from time import time
import matplotlib.pyplot as plt
import pyLDAvis

import tools.mySQL as mysql
from gensim import corpora, models
import pyLDAvis.gensim as ldaVis

def buildCorpus():
    t0=time()
    results = mysql.selectWordToken()
    print('Get data samples :', len(results))
    # 创建语料的词语词典，每个单独的词语都会被赋予一个索引
    data_sample = [doc.split() for doc in results]
    # print(data_sample[0])
    dictionary = corpora.Dictionary(data_sample)
    # print((list(dictionary.items())[:100]))
    # 使用上面的词典，将转换文档列表（语料）变为bow
    doc_bow = [dictionary.doc2bow(doc) for doc in data_sample]

    # print(doc_bow[0])
    print("Get corpus，cost time:  %0.3f s." % (time() - t0))
    return doc_bow,dictionary,data_sample

def findBestParameters():
    corpus,dictionary,data_sample=buildCorpus()
    # passes=10
    chunksizes=[256,512,1024,2048,4096,8192] #
    passes_value=[10,20,30]
    max_topics=15
    time_start=time()
    path='parameters results.txt'
    for passes in passes_value:
        for chunksize in chunksizes:
            print('passes=',passes,' chunksize=',chunksize)

            x = [] # x轴
            coherence_values = []   # 一致性
            model_list = [] # 存储对应主题数量下的lda模型

            with open(path, 'a', encoding='utf-8') as file:
                file.write('passes='+str(passes))
                file.write('  chunksize ='+str(chunksize)+'\n')

            for topic in range(2,max_topics):
                x.append(topic+1)
                print(" Number of Topics= ", topic+1)
                t0 = time()
                lda_model = models.LdaModel(corpus=corpus, num_topics=topic+1, id2word =dictionary,alpha='auto',passes=passes,chunksize=chunksize,random_state=42)
                costed_time=str(time() - t0)
                print('     train model using :',costed_time)
                model_list.append(lda_model)

                # calculate coherence
                coherencemodel = models.CoherenceModel(model=lda_model, texts=data_sample,dictionary=dictionary, coherence='c_v')
                coherence=coherencemodel.get_coherence()
                print('     coherence: ',coherence)
                coherence_values.append(coherence)
                # if coherence is very high,then save model.
                if coherence>0.4:
                    lda_model.save('p{}_c{}_lda_model_numT{}.model'.format(passes,chunksize,str(topic+1)))


                # Store them into txt
                numtopics_store=str('   number of topics = '+str(topic+1)+'\n')
                ctime_store=str('       the costed time = '+str(costed_time)+'\n')
                coherence_store=str('       coherence= '+str(coherence)+'\n')
                with open(path, 'a', encoding='utf-8') as file:
                    file.write(numtopics_store)
                    file.write(ctime_store)
                    file.write(coherence_store)

            print('coherence_values: ',coherence_values)
            # 绘制一致性折线图
            plt.plot(x, coherence_values)
            plt.title("Finding best number of topics:  coherence")
            plt.xlabel("Number of Topics ")
            plt.ylabel("coherence score")
            plt.savefig('p{}_c{}_number_of_topic_with_coherence.jpg'.format(passes,chunksize))
            plt.show()

    # record costed time on training model.
    total_time=time()-time_start
    print('total_time: ',total_time)
    with open(path, 'a', encoding='utf-8') as file:
        file.write('total_time='+str(total_time))

#Make LDAvis
def LDAvis():
    doc_bow,dictionary,data_sample=buildCorpus()
    # TODO: path list!
    pathes=['p10_c512_lda_model_numT5.{}','p10_c512_lda_model_numT6.{}','p10_c1024_lda_model_numT5.{}',
            'p20_c512_lda_model_numT6.{}','p20_c1024_lda_model_numT5.{}','p30_c1024_lda_model_numT5.{}',
            'p30_c512_lda_model_numT6.{}','p20_c1024_lda_model_numT6.{}']
    for path in pathes:
        lda=models.LdaModel.load(path.format('model'))
        print('model load!')
        visulisation=ldaVis.prepare(lda, doc_bow, dictionary)
        pyLDAvis.save_html(visulisation,path.format('html'))
