
# coding: utf-8

# In[1]:


import os
import re
from collections import defaultdict, Counter

import sys


# In[4]:


cmd_prmt = 'Y'  # set it to Y if you are running it from command line

#O = input("Provide the word for which you are looking for different sences:")
#O = O.split()                      # O: list of observations
#T = len(O)

if cmd_prmt =='Y':
    input_file_name = sys.argv[1]
else:
    os.chdir("D:\\Arvin\ArtInt\\IIIT PGSSP\\2019-20 Spring\\Assignments\Assignemnt-2\\Corpus") 
    input_file_name = input("Provide the name on input file having the file which needs to tag")

i_file = open(input_file_name,"r")
input_file = i_file.readlines()
i_file.close()

O = []                # O: list of observations
for i in range (len(input_file)):
    O.extend(input_file[i].split())
T=len(O)    
#print(T,'\n',O)    
print (sys.argv)


# In[5]:


N = 0                                                  # Number of states or numebr of tags
Q = []                                                 # list of N states/tags
t_prob = defaultdict(lambda: defaultdict(lambda: 0))   # transition probabilities + Pai(initial probabilities with begin)
e_prob = defaultdict(lambda: defaultdict(lambda: 0))   # emission_probabilities
tag_w_cnt = defaultdict(lambda: 0)                     # number of words emission from any tag, it will be use in validation


## RE to fetch the different data from given file- Start
colon_re = re.compile(" : ")

tg_t1_re = re.compile(".+(?= - )")
tg_t2_re = re.compile("(?<= - ).+(?= : )")    
t_prob_re = re.compile("(?<= : ).+")
#NNP - NNP : 0.38802513

w_e_re = re.compile("(?<=P \().+(?=\|)")
tg_e_re = re.compile("(?<=\|).+(?=\))")    
e_prob_re = re.compile("(?<=\) = ).+")
#P (Pierre|NNP) = 0.00013713
## RE to fetch the different data from given file-End


# In[6]:


file = open('hmmmodel.txt',"r")
encd_file = file.readlines()
file.close()

def word_count_in_tag (str):
    tag_w = re.split(colon_re, str)
    return tag_w[0], tag_w[1]

def transition (str):
    tag1 = re.findall(tg_t1_re,str)[0]
    str =  re.sub(tg_t1_re,'a',str)
    tag2 = re.findall(tg_t2_re,str)[0]
    str =  re.sub(tg_t2_re,'b',str)    
    prob = float(re.findall(t_prob_re,str)[0])
    return tag1, tag2, prob

def emission (str):
    w = re.findall(w_e_re,str)[0]
    str = re.sub(w_e_re,'b',str)
    tag = re.findall(tg_e_re,str)[0]
    str = re.sub(tg_e_re,'a',str)
    prob = float(re.findall(e_prob_re,str)[0])
    return tag, w, prob


file_section = 'tag_count'
for i in range (len(encd_file)):
    
    if encd_file[i][0:12] == 'No. of tags:':
        N = int(encd_file[i][13:])
        
    if encd_file[i][0:5] == 'Tags:':
        tags_str = encd_file[i][6:]
        Q = tags_str.split('\t')
                
    if file_section == 'word_count_in_tag':
        if encd_file[i][0:15] != 'Outgoing Count:' and encd_file[i][0:23] != 'Transition Probability:' and encd_file[i][0:21] != 'Emission Probability:':
            if re.search(colon_re, encd_file[i]) != None:
                tg,wc = word_count_in_tag(encd_file[i])
                tag_w_cnt[tg] = int(wc)
                #print(tg,wc)

    if file_section == 'transition':
        if encd_file[i][0:15] != 'Outgoing Count:' and encd_file[i][0:23] != 'Transition Probability:' and encd_file[i][0:21] != 'Emission Probability:':        
            if re.search(tg_t1_re,encd_file[i]) != None:
                tag1, tag2, t_p = transition (encd_file[i])
                #print ('AG Transition: ',tag1, tag2, t_p)
                t_prob[tag1][tag2]=t_p
    
    if file_section == 'emission':
        if encd_file[i][0:15] != 'Outgoing Count:' and encd_file[i][0:23] != 'Transition Probability:' and encd_file[i][0:21] != 'Emission Probability:':        
            if re.search(w_e_re,encd_file[i]) != None:
                tag, w, e_p = emission (encd_file[i])
                #print ('AG Emmission: ',tag, w, e_p)
                e_prob[tag][w]=e_p

        
    if encd_file[i][0:15] == 'Outgoing Count:':
        file_section = 'word_count_in_tag'
        
    if encd_file[i][0:23] == 'Transition Probability:':
        file_section = 'transition'
        
    if encd_file[i][0:21] == 'Emission Probability:':
        file_section = 'emission'
    


# In[7]:


def data_validation_and_normalization(N, Q, t_prob, e_prob, tag_w_cnt):
    if len(Q) != N:
        print("Tag counts given in file is not matching with actual tags present in file")
    else:
        N = len(Q)
    
    # normalisation of emission probabillities:
    for tag in list(e_prob.keys()):
        tag_prob=0
        w_count = 0
        for word in list (e_prob[tag].keys()):
            tag_prob = tag_prob + e_prob[tag][word]
            w_count +=1
        #if w_count != tag_w_cnt[tag]:
            #print ("For tag ", tag, "count of word is given as ",tag_w_cnt[tag], " however actaul word transmission probabilities are: ", w_count)
        #print(tag, tag_prob)  
        for word in list (e_prob[tag].keys()):
            e_prob[tag][word] = e_prob[tag][word]/tag_prob

    # normalisation of transition probabillities:
    for tag1 in list(t_prob.keys()):
        tag1_prob=0
        for tag2 in list (t_prob[tag1].keys()):
            tag1_prob = tag1_prob + t_prob[tag1][tag2]
        #print(tag1, tag1_prob)  
        for tag2 in list (t_prob[tag1].keys()):
            t_prob[tag1][tag2] = t_prob[tag1][tag2]/tag1_prob
    return N, t_prob, e_prob
            
            
N, t_prob, e_prob = data_validation_and_normalization(N, Q, t_prob, e_prob, tag_w_cnt)     


# In[8]:


viterbi = defaultdict(lambda: defaultdict(lambda: 0))   # emission_probabilities
v_path = defaultdict(lambda: defaultdict(lambda: ''))   # emission_probabilities

#N      - Number of states or numebr of tags
#T      - Number of word in string to decode
#Q      - list of N states/tags
#O      - given input observations for decoding
#t_prob - transition probabilities + Pai(initial probabilities with begin)
#e_prob - emission_probabilities


for tag in Q:
    viterbi[0][tag] = t_prob['Begin'][tag] * e_prob[tag][O[0]]
    v_path[0][tag] = 'Begin'

for t in range (1,T):
    
    for tag in Q:
        max_v = 0
        for tag_old in Q:            
            temp_v = viterbi[(t-1)][tag_old] * t_prob[tag_old][tag] * e_prob[tag][O[t]]
            if temp_v > max_v:
                max_v = temp_v
                viterbi[t][tag] = temp_v
                v_path[t][tag] = tag_old

max_v = 0
v_last_tag = ''
viterbi_prob = 0

for tag_old in Q:
    temp_v = viterbi[(T-1)][tag_old]
    if temp_v > max_v:
        max_v = temp_v
        viterbi_prob = temp_v
        v_last_tag = tag_old
        
      


# In[9]:


#storing tag sequece
tag_back_track = []

tag_temp = v_last_tag
tag_back_track.append(tag_temp)
for i in range (1,T):
    t = T-i
    tag_temp = v_path[t][tag_temp]
    tag_back_track.append(tag_temp)

S = []

for i in range (T):
    S.append(tag_back_track[T-i-1])
    
print ('Probability of tags: ', viterbi_prob)    
#print ('Tag sequence is: ', S)
print ('POS tag sequence for sentence',O, 'is as below:')

for i in range (T):
    print (O[i],': ', S[i])

