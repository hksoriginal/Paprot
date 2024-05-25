"""
!!!! For Mistral Zphyre Model !!!!
<|system|>
</s>
<|user|>
{prompt}</s>
<|assistant|>


!!!! For Llama2 model
[INST] <<SYS>>
You are a helpful, respectful and honest assistant. Always answer as helpfully
as possible, while being safe.  Your answers should not include any harmful,
unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure
that your responses are socially unbiased and positive in nature. If a
question does not make any sense, or is not factually coherent, explain
why instead of answering something not correct. If you don't know the
answer to a question, please don't share false information.
<</SYS>>
{prompt}[/INST]

"""

"""<|system|>Using the information contained in the context, 
give a comprehensive answer to the question.
If the answer is contained in the context, also report the source URL.
If the answer cannot be deduced from the context, do not give an answer.</s>
<|user|>
Context:{}
  Question: {{query}}
  </s>
<|assistant|>
"""

PROMPT_TEXTi = '''
<|system|> Use the following pieces of policy to answer briefly question at the 
end. Always be factually correct based on the policy and focus only on 
relevant section of policy. Use the following references for acronyms -> (APL=Advanced Privilege Leave, OPH=Optional Paid Holiday, CL=Contingency Leave, PL=Privilege Leave, RIL -> Reliance Industries Limited)</s>
<|user|> Policy : {context}
Question: {question}</s>
<|assistant|>
'''
PROMPT_TEXT = '''
<|system|>You are an HR Query Resolver.You cannot change Policy at any 
cost.Use the given Policy to answer the asked question precisely.Always be factually correct & concise.</s>
<|user|> Policy : {context} Question: {question}</s>
<|assistant|>
'''

INPUT_VARIABLES = ['context', 'question']

PROMPT_TEXT11 = '''
[INST]<<SYS>> Use the following pieces of policy  to answer question at 
the end.If you don't know the answer, just say that you don't know, don't try to make up an answer.Always be factually correct based on the policy and focus only on relevant section of policy.DO NOT EXPAND THE ACRONYMS!!!<</SYS>>
Use the following references for acronyms -> (APL=Advanced Privilege Leave, 
OPH=Optional Paid Holiday, CL=Contingency Leave, PL=Privilege Leave, RIL -> 
Reliance Industries Limited)
Policy Context : {context}
Question: {question}
Helpful Answer :
[/INST]
'''
