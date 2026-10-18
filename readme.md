# FactClash

## Overview
`factclash` is python library that functions just before feeding the retrieval information to the LLM for the final call. It recognizes which facts are contradictory to each other and can cause LLM to hallucinate. FactClash comes in the middle it first detects if contradictory facts exist inside the context. Then it would partition the context window into different context window with contradictory facts existing in each one of them plus some supporting for each one from the context window. 

## Data Structure 

FactClash inspects the context window of the LLM. It recieves different formats including (JSON, md, xlsx) then turn it into a list of different context windows for the specified format by the user. 
```Example: 
str -> list[str]
```


## How it helps 
The main three source of contradictions are: 
- Fault recording and human error while documenting a specific task. 
- Change of policy within a company. For instance in a certain timestamp the policy of the company was X but now it turned into Y for some certain conditions 
- Retrieval Error: The retrieval mechanism actually retrieved False information that can potentially cause contradiction with True information that is retrieved. 



