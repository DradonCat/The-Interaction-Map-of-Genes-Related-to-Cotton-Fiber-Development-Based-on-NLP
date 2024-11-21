import spacy
from collections import Counter
from itertools import combinations

# 加载SciSpacy的生物领域NER模型
#nlp = spacy.load("en_core_sci_sm")  # 确保安装并使用正确的SciSpacy模型
nlp = spacy.load("en_ner_bionlp13cg_md")  # 切换到专门识别基因的模型
#nlp = spacy.load("en_ner_craft_md")

nlp.max_length = 3000000  # 根据文本大小设定足够大的值

# 读取文献内容
with open(r'E:\桌面\大学实践数据\大四上\nlp\短文\abstracts.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# 处理文本，提取命名实体
doc = nlp(text)

# 检查实体提取情况（调试部分）
print("提取到的实体信息：")
for ent in doc.ents:
    print(f'Text: {ent.text}, Label: {ent.label_}')

# 提取基因相关的命名实体
genes = [ent.text for ent in doc.ents if ent.label_ == "GENE_OR_GENE_PRODUCT"]

# 检查是否成功提取基因
if not genes:
    print("没有提取到任何基因实体。")
else:
    print(f"提取到的基因数量：{len(genes)}")

# 统计基因出现频率
gene_freq = Counter(genes)

# 找出基因的共现关系
co_occurrence = Counter()
for sentence in doc.sents:
    sentence_genes = [ent.text for ent in sentence.ents if ent.label_ == "GENE_OR_GENE_PRODUCT"]
    for pair in combinations(sentence_genes, 2):  # 找出成对出现的基因
        co_occurrence[pair] += 1

# 保存基因出现频率和共现关系
with open(r'E:\桌面\大学实践数据\大四上\nlp\短文\gene_frequency2.txt', 'w', encoding='utf-8') as f:
    for gene, freq in gene_freq.items():
        f.write(f'{gene}: {freq}\n')

with open(r'E:\桌面\大学实践数据\大四上\nlp\短文\gene_cooccurrence2.txt', 'w', encoding='utf-8') as f:
    for (gene1, gene2), count in co_occurrence.items():
        f.write(f'{gene1} - {gene2}: {count}\n')

print("基因频率和共现关系已保存。")
