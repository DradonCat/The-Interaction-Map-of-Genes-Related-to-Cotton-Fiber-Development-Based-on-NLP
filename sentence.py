import nltk 
from nltk.tokenize import sent_tokenize  
import re

current_line_number = 0 
with open(r'/home/featurize/work/BIONIP/abstracts.txt', 'r', encoding='utf-8') as file:  
    for line in file:  
        current_line_number += 1  
        if len(line)>20:  
            match = re.search(r'Abstract: \[(.*?)\]', line).group(1)
            start_index = match.find("|a|") + 3
            sen = match[start_index:] 
            sentences = sent_tokenize(sen) 
            with open('sentence1.txt', 'a', encoding='utf-8') as file:
                for sentence in sentences:  
                    file.write(sentence + '\n')

#sentences = sent_tokenize(text)  
#print(sentences)
#with open('sentence1.txt', 'a', encoding='utf-8') as file:  
#    for sentence in sentences:  
#        file.write(sentence + '\n')