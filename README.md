# HMM-Decoder

The idea is to code a simple Viterbi decoder for an HMM POS Tagger.  
I have written a decoder for a statistical POS Tagger to find the best sequence, given the encoder. 
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Input sentence and its POS tag genrated by HMM decoding

Sentence: "This was caused by shortages in personal protecting equipment"
POS for above sentence 
This:------- 'DT'
was:-------- 'VBD'
caused:----- 'VBN'
by:--------- 'IN'
shortages:-- 'NNS'
in:--------- 'IN'
personal:--- 'JJ'
protecting:- 'VBG'
equipment:-- 'NN'

============================================================================================================

Approach to Read the encoding file:

I read the given encoding file (hmmmodel.txt) using regex. I checked the sections headings (“Outgoing Count:”, 
“Transition Probability:”, “Emission Probability:”) then depending on section I applied appropriate regex to 
extract the encoding probabilities.

I normalized the transition probabilities so that sum of all transition probabilities from any state/tag will 
sum up to 1 and similarly I normalized the emission probabilities to make sure emission probability for any state/tag 
will sum up to 1.

Also I did validation for tag count.

============================================================================================================

How to run the Program:

thier is varailbe "cmd_prmt" which is set to 'Y' assuming that we are ruuning the program from command prompt. 
If wea are running it from Jupyter Notebook or any other editor we need to change this vairable to 'N' so that 
program will prompt to take input file at run time.

This program needs encoding file (hmmmodel.txt) which has all the tags and transition and emission probabilities 
Either we need to keep this file in appropriate directory where we are running this program or need to change our
current working directory path appropriatly
os.chdir("D:\\Arvin\ArtInt\\IIIT PGSSP\\2019-20 Spring\\Assignments\Assignemnt-2\\Corpus")

This Program needs a input file (we need pass this file name as run parameter) which will have a sentence for which 
we need to genrate POS tags. My Program will genrate the output (pos tags for sentence) and show it in on the screen.




