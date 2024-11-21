import xml.etree.ElementTree as ET  
import requests  
import os  
  
def parse_pmids_from_xml(xml_file):  
    """  
    解析XML文件并提取PMID列表  
    """  
    with open(xml_file, 'r') as file:  
      pmids = [line.strip() for line in file]  
    return pmids  
  
# PubTator API端点  
api_url = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/pubtator?pmids="
  
# 存储摘要的文件名  
output_file = 'genename.txt'  
i=0
xml_file = "/home/featurize/work/BIONIP/pmids.xml"
pmids=parse_pmids_from_xml(xml_file)
# 打开输出文件  
with open(output_file, 'a', encoding='utf-8') as out_file:  
    for pmid in pmids:  
        # 发送请求获取摘要  
        response = requests.get(api_url + pmid)  
        # 检查请求是否成功  
        if response.status_code == 200:  
            # 解析响应内容（这里假设响应内容是制表符分隔的，且第一行是标题行）  
            lines = response.text.strip().split('\n')  
            # 假设第二行是摘要行（具体取决于PubTator的输出格式，可能需要调整）  
            for line in lines:  
        # 分割每行数据  
                parts = line.split('\t')  # 或者使用.split('\t')如果数据是用制表符分隔的  
        # 检查是否有足够的数据部分（根据您的数据格式）  
                if len(parts) > 1:  
                    if "Chemical" in parts:   
                        species_id = parts[parts.index("Chemical") + 1]  # 获取物种名称  
                # 可能还有其他字段，比如物种的ID或其他相关信息  
                        species = parts[parts.index("Chemical") - 1]  # 假设物种ID在"Species"之前  
                # 注意：这里的索引操作是基于您的数据格式的，如果格式不同，需要相应调整  
                # 打印或存储提取的信息  
                        out_file.write(f"PMID: {pmid}, Species: {species}, Species ID: {species_id}\n")
            print("one artical has search over in ",i)
            i=i+1
        else:  
            print(f"Failed to retrieve abstract for PMID: {pmid}, status code: {response.status_code}")


