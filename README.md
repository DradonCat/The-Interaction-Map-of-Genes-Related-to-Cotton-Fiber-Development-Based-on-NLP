# The-Interaction-Map-of-Genes-Related-to-Cotton-Fiber-Development-Based-on-NLP
在本项目中我们使用一系列NLP技术从PubMed上提取到有关于棉花纤维生长的相关基因，然后利用相关基因进行了分析。

以下是代码使用步骤：

1.在PubMed上提取相关文献

首先根据linux中下载pubid的pdf文件将需要的相关文献的Pmid提取出来。这是一段linux上的命令，若需要提取其他类型的文献，仅需要在term后将cotton+fiber修改为你想提取的文献的关键词。

curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cotton+fiber&retmax=1000&retstart=0&retmode=xml">pmids_batch_1.xml

然后根据Pmid提取相关的文献摘要和注释。在这一步骤里分别根据cotton.py提取相关摘要和gene.py提取相关注释。需要特别注意的是，在提取注释中，你需要提取什么类型的注释就需要将species_id部分的Chemical修改为你需要提取的注释类型，比如“Gene”等，具体的注释类型可以通过API加pmid链接点进去获取。

2.NER模型获取文献摘要中的基因

在这一步骤中，直接使用NER(1).py即可，需要注意的是加载模型时仅第二个模型生效，另外两个效果很差。

3.通过获取的基因和文献摘要来完成互作图谱。

首先通过sentence.py将获取的文献转换为一句一行的格式，然后通过extract.sh来找出相关基因所在的句子并保存下来，值得注意的是在这一步时是在linux上完成的代码，保留好所在句子后就可以通过map3.py来完成基因互作图谱的构建了。
