import spacy
import networkx as nx
import matplotlib.pyplot as plt
from spacy.matcher import PhraseMatcher

# 加载SpaCy模型
nlp = spacy.load("en_core_web_sm")
# 初始化基因、蛋白质和酶的匹配器
def create_matcher(nlp, gene_list, enzyme_list):
    matcher = PhraseMatcher(nlp.vocab)
    # 将基因和酶的模式添加到匹配器中
    matcher.add("GENE", [nlp(text) for text in gene_list])
    matcher.add("ENZYME", [nlp(text) for text in enzyme_list])
    # 定义互动关系的动词模式
    interaction_verbs = [
        "interacts", "binds", "activates", "inhibits", "regulates",
        "modulates", "promotes", "reduces", "affects", "stimulates", "increases"  # 添加更多动词
    ]
    interaction_patterns = [nlp(text) for text in interaction_verbs]
    for verb in interaction_patterns:
        matcher.add("INTERACTION", [verb])
    return matcher
# 从文件读取基因信息
def read_gene_info(file_path):
    gene_set = set()
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.split(", ")
            for part in parts:
                if "Gene:" in part:
                    gene = part.split(": ")[1].strip()
                    gene_set.add(gene)
    return list(gene_set)


# 提取基因、蛋白质、酶的互动信息，并记录相关句子
def extract_interactions(text, nlp, matcher):
    doc = nlp(text)
    matches = matcher(doc)

    interactions = []
    entities = {}
    interaction_sentences = []  # 用于存储与互动关系相关的句子

    # 记录匹配到的实体
    for match_id, start, end in matches:
        match_text = doc[start:end]
        match_type = nlp.vocab.strings[match_id]

        # 记录基因和酶的匹配
        if match_type == "GENE":
            entities[match_text.text] = "GENE"
        elif match_type == "ENZYME":
            entities[match_text.text] = "ENZYME"
        elif match_type == "INTERACTION":
            verb = match_text.text
            # 记录互动关系，确保前后有基因和酶
            last_gene = None
            last_enzyme = None

            # 查找与动词相关的基因和酶
            for previous_entity in list(entities.keys())[::-1]:  # 反向查找
                if entities[previous_entity] == "GENE":
                    last_gene = previous_entity
                    break

            for next_entity in list(entities.keys()):  # 正向查找
                if entities[next_entity] == "ENZYME":
                    last_enzyme = next_entity
                    break

            # 检查是否找到有效的互动关系
            if last_gene and last_enzyme:
                interactions.append((last_gene, verb, last_enzyme))
                # 找到关系所在的句子
                sentence = doc.text
                # 确定该句子在文档中的位置
                start_char = doc[:start].end_char
                end_char = doc[end].idx
                sentence_start = text.rfind('.', 0, start_char) + 1  # 找到句子开始的位置
                sentence_end = text.find('.', end_char)  # 找到句子结束的位置
                if sentence_end == -1:  # 如果没找到句子结束，直到文本末尾
                    sentence_end = len(text)
                sentence = text[sentence_start:sentence_end].strip()  # 提取句子
                interaction_sentences.append(sentence)  # 保存相关句子

    return interactions, interaction_sentences  # 返回句子


# 构建互动网络
def build_interaction_network(interactions):
    G = nx.DiGraph()
    for entity1, relation, entity2 in interactions:
        G.add_edge(entity1, entity2, label=relation)
    return G


# 可视化互动网络
def visualize_network(G):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue",
            font_size=10, font_weight="bold", font_color="black")

    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, font_color="red", font_size=8,
        label_pos=0.5, bbox=dict(facecolor="white", edgecolor="none", alpha=0.6)
    )

    plt.title("Cotton Fiber Development Interaction Network")
    plt.axis("off")
    plt.show()


# 将互动关系和句子写入文件
def write_results_to_file(interactions, sentences, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        for i, (gene, verb, enzyme) in enumerate(interactions):
            file.write(f"{gene} {verb} {enzyme}\n")
            if i < len(sentences):
                file.write(f"Sentence: {sentences[i]}\n\n")  # 写入相关句子


# 主程序
def main():
    # 读取基因信息
    gene_file_path = "E:/桌面/大学实践数据/大四上/nlp/pythonProject/genename.txt"
    gene_list = read_gene_info(gene_file_path)

    # 读取上传的文本内容
    try:
        with open("E:/桌面/大学实践数据/大四上/nlp/pythonProject/sentresult.txt", "r", encoding="utf-8") as file:
            text = file.read()

        # 定义酶的列表（可以根据需要调整）
        enzyme_list = [
            "PDF2", "KCS4", "ARF5", "ERF", "MYB", "bHLH", "NAC", "WRKY",
            "GST", "SOD", "CAT", "POD", "JAZ1", "JAZ2", "AtLOX4", "AtAOS", "GhAPX1"
        ]

        matcher = create_matcher(nlp, gene_list, enzyme_list)
        interactions, sentences = extract_interactions(text, nlp, matcher)

        # 输出提取的互动信息
        if interactions:
            print("提取的互动关系:")
            for interaction in interactions:
                print(interaction)
        else:
            print("没有提取到互动关系。")

        # 将结果写入文件
        output_file_path = "E:/桌面/大学实践数据/大四上/nlp/pythonProject/extracted_interactions3.txt"
        write_results_to_file(interactions, sentences, output_file_path)

        # 构建和展示基因互动图谱
        G = build_interaction_network(interactions)
        visualize_network(G)

    except FileNotFoundError:
        print("文件未找到，请检查文件路径。")
    except Exception as e:
        print(f"发生错误: {e}")


# 运行主程序
if __name__ == "__main__":
    main()
