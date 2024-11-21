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
output_file = 'abstracts.txt'  
i=1312
xml_file = "/home/featurize/work/BIONIP/pmids.xml"
pmids=parse_pmids_from_xml(xml_file)
# 打开输出文件  
with open(output_file, 'a', encoding='utf-8') as out_file:  
    for pmid in pmids[1312:]:  
        # 发送请求获取摘要  
        response = requests.get(api_url + pmid)  
        # 检查请求是否成功  
        if response.status_code == 200:  
            # 解析响应内容（这里假设响应内容是制表符分隔的，且第一行是标题行）  
            lines = response.text.strip().split('\n')  
            # 假设第二行是摘要行（具体取决于PubTator的输出格式，可能需要调整）  
            if lines:  
                # 假设摘要位于某个特定的行（这里需要根据你的实际响应格式来调整）  
                # 例如，如果摘要位于第二行，并且是以制表符分隔的字段中的第二个字段  
                # 你需要确保这一行确实包含至少两个制表符分隔的字段  
                abstract_line= lines[1] 
                # 这里可能需要根据实际的输出格式进行调整  
                fields = abstract_line.split('\t')  
                #if len(fields) > 1:  
                #abstract = fields[1]  # 提取摘要字段  
                    # 写入输出文件  
                out_file.write(f"PMID: {pmid}\nAbstract: {fields}\n\n")
                print('One Abstract has been saved in ',i)  
                i=i+1
                #else:  
                    #print(f"Warning: No abstract field found for PMID {pmid} in line: {abstract_line}")  
            else:  
                print(f"Warning: Empty response for PMID {pmid}")  
        else:  
            print(f"Failed to retrieve abstract for PMID: {pmid}, status code: {response.status_code}")


