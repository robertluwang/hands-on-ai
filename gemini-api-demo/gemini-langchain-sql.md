# Chat with SQL using Gemini+Langchain

- Reading an SQL database can be challenging
- Accurate prompts enable Gemini models to generate answers based on the data
- The Gemini API allows you to retrieve necessary information by chatting with an SQL database

Here is demo how to chat with SQL using Gemini API and Langchain data framework.

## Installation


```python
!pip install -U -q google-generativeai langchain langchain-community langchain-google-genai
```


```python
import sqlite3

from langchain.chains import create_sql_query_chain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough

import google.generativeai as genai
from IPython.display import Markdown
```

## Setup API key

Place below line to .env under current folder, 

GOOGLE_API_KEY=xxx


```python
import os

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
```

## Set up sample db

1. **Load the California Housing Dataset:** Load the dataset from sklearn.datasets and extract it into a DataFrame.



```python
from sklearn.datasets import fetch_california_housing

california_housing_bunch = fetch_california_housing(as_frame=True)
california_housing_df = california_housing_bunch.frame
```

2. **Connect to local SQLite db:** 


```python
conn = sqlite3.connect("house.db")

# Write the DataFrame to a SQL table named 'housing'.
california_housing_df.to_sql("housing", conn, index=False)
```




    20640




```python
# Create an SQLDatabase object
db = SQLDatabase.from_uri("sqlite:///house.db")
```

## Question to query
Asking the LLM to generate queries.



```python
# you can see what information is available
Markdown(db.get_table_info())
```





CREATE TABLE housing (
	"MedInc" REAL, 
	"HouseAge" REAL, 
	"AveRooms" REAL, 
	"AveBedrms" REAL, 
	"Population" REAL, 
	"AveOccup" REAL, 
	"Latitude" REAL, 
	"Longitude" REAL, 
	"MedHouseVal" REAL
)

/*
3 rows from housing table:
MedInc	HouseAge	AveRooms	AveBedrms	Population	AveOccup	Latitude	Longitude	MedHouseVal
8.3252	41.0	6.984126984126984	1.0238095238095237	322.0	2.5555555555555554	37.88	-122.23	4.526
8.3014	21.0	6.238137082601054	0.9718804920913884	2401.0	2.109841827768014	37.86	-122.22	3.585
7.2574	52.0	8.288135593220339	1.073446327683616	496.0	2.8022598870056497	37.85	-122.24	3.521
*/




```python
# Define query chain
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)
write_query_chain = create_sql_query_chain(llm, db)
```

The `create_sql_query_chain` provides default prompts for various types of SQL including Oracle, Google SQL, MySQL and more, it is suitable for our task. 


```python
Markdown(write_query_chain.get_prompts()[0].template)
```




You are a SQLite expert. Given an input question, first create a syntactically correct SQLite query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per SQLite. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use date('now') function to get the current date, if the question involves "today".

Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

Only use the following tables:
{table_info}

Question: {input}




```python
response = write_query_chain.invoke({"question": "What is the total population?"})
response
```




    'Question: What is the total population?\nSQLQuery: SELECT SUM("Population") FROM housing'




```python
db.run('SELECT SUM("Population") FROM housing')
```




    '[(29421840.0,)]'



Great! The SQL query is correct, but it needs proper formatting before it can be executed directly by the database.


## Validate the query


```python
validate_prompt = PromptTemplate(
    input_variables=["not_formatted_query"],
    template="""You are going to receive a text that contains a SQL query. Extract that query.
    Make sure that it is a valid SQL command that can be passed directly to the Database.
    Avoid using Markdown for this task.
    Text: {not_formatted_query}"""
)
```


```python
validate_chain = write_query_chain | validate_prompt | llm | StrOutputParser()
validate_chain.invoke({"question": "What is the total population?"})
```




    'SELECT SUM("Population") FROM housing \n'



## Automatic querying
Let's automate the process of querying the database using *QuerySQLDataBaseTool*. This tool can receive text from previous parts of the chain, execute the query, and return the answer.



```python
execute_query = QuerySQLDataBaseTool(db=db)
execute_chain = validate_chain | execute_query
execute_chain.invoke({"question": "What is the total population?"})
```




    '[(29421840.0,)]'



## Generate answer
You are almost done!

To enhance our output, you'll use LLM not only to get the number but to get properly formatted and natural language response.


```python
answer_prompt = PromptTemplate.from_template(
    """You are going to receive a original user question, generated SQL query, and result of said query. You should use this information to answer the original question. Use only information provided to you.

Original Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

answer_chain = (
    RunnablePassthrough.assign(query=validate_chain).assign(
        result=itemgetter("query") | execute_query
    )
    | answer_prompt | llm | StrOutputParser()
)

answer_chain.invoke({"question": "What is the total population?"})
```




    'The total population is 29,421,840. \n'



## Conclusion

Chatting with an SQL database using the Gemini API and Langchain framework streamlines the process of querying complex datasets. This approach leverages the capabilities of large language models to generate precise SQL queries from natural language prompts, simplifying database interactions. By integrating these tools, users can efficiently retrieve and analyze data without extensive SQL knowledge, making data-driven decision-making more accessible. This demonstration showcases the potential of combining advanced AI models with robust data frameworks to enhance database querying, providing a powerful tool for users across various fields.


```python

```
