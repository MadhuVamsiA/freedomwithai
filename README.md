************

# Prerequesties

*************

## 1. How to get the OPENAI API Key 

1. go to https://openai.com/ and login with your credntials. If you don't have account signup for the same.
2. Once you login you will be able to see the window like below. Click on the on API.

 ![image](https://github.com/MadhuVamsiA/freedomwithai/assets/143532033/6d36bc98-c48d-49a4-95ef-109a559e727d)
4. Now click on personal and then click on view API keys.
![image](https://github.com/MadhuVamsiA/freedomwithai/assets/143532033/b896a1ca-80b4-4008-8b30-75ee331350f1)
5. Click on create new secret key.
![image](https://github.com/MadhuVamsiA/freedomwithai/assets/143532033/77113c26-7449-4fbc-ae4e-a39629affd1d)
6. You will be able to see the below and give the desired name for key then click on create secret key. Copy the secret key and click on done.
Note: Store the key somewhere as we can't see the key once we created.
![image](https://github.com/MadhuVamsiA/freedomwithai/assets/143532033/6b957853-b058-4f04-b053-83cd18f5e021)
7. Use the above copied secret key in the python code.

******************************
## 2. How to get OPENAI API URL
*******************************

1. Follow the first two steps which are in "how to get the OPEN API Key"
2. Navigate to API references which is on top of page and then navigate to create chat completion which is under chat tab on left side of the page.
3. Copy the highlighted URL and use that in the python code wherever required.

![image](https://github.com/MadhuVamsiA/freedomwithai/assets/143532033/6331182a-93d2-4308-8724-c4f483c8a4c8)

***********************************
## 3. How to get serpAPI 
***********************************

1. Go to https://serpapi.com/ and login with your credntials. If you don't have account signup for the same.
2. On right hand side click on api key tab then will get the api key displayed in the middle of page. Copy that key and use it wherever is required.

   ![image](https://github.com/MadhuVamsiA/freedomwithai/assets/143532033/2e8769f0-f689-465f-8dd2-1d199f9a9ead)


***********************************************************
## 4. How to get the PineCone API Key and Environment Name
***********************************************************
1. Signup on  https://www.pinecone.io/
2. Login to Pinecone
3. Go to the API Keys tab on left side , you can see the details in the middle of page. Copy the API key and enviornment name.
   ![image](https://github.com/MadhuVamsiA/freedomwithai/assets/143532033/4f126110-ca11-47d5-92c1-f75cf542eace)

*****************************************
## 5. How to create index in Pinecone
*****************************************
1. Go to the indexes tab and then you can see the create index option.

![image](https://github.com/MadhuVamsiA/freedomwithai/assets/143532033/7e7c782b-e2a3-4938-b163-fb17c4f2ba01)

![image](https://github.com/MadhuVamsiA/freedomwithai/assets/143532033/0382d7ce-7689-49bd-b1c5-146bf244ce06)

2. Once you click on the create index option , you can see the below window.
3. Choose dimentions, metric and pod type accordingly.

   ![image](https://github.com/MadhuVamsiA/freedomwithai/assets/143532033/60c0d184-00f3-4fb2-b90d-25f3f8f31f45)

   ![image](https://github.com/MadhuVamsiA/freedomwithai/assets/143532033/93730554-d6b9-4ff7-b72d-c22ba4b4ca60)

***************************************************
# 6. Install the required libraries in python environment
****************************************************
!pip install --upgrade langchain openai  -q

!pip install sentence_transformers -q

!pip install unstructured -q

!pip install unstructured[local-inference] -q

!pip install jq

!pip install pinecone-client openai tiktoken langchain

!pip install Flask

!pip install requests

!pip install googlesearch-python
!pip install google-search-results

**********************************************
# 6. Run the .py file
**********************************************
1. Open anconda terminal/prompt on your local and then go to the directory where the chatbotv2_minilm_V2.py with the below command
   cd "folder path"

   Note: Make sure to activate the environment if you have created any other than base environmnet (conda activate envname)
3. run "python ChatBot_V3.py"

![image](https://github.com/MadhuVamsiA/freedomwithai/assets/143532033/fc5e16be-13c0-406d-b487-4394698544ff)


4. it is going to give us a one url. click on that or copy paste to any browser.
5. It will open a window like below. You can enter search query like how we search in google and then entire your quey on that seach page then click on submit. It will give the response..
   
![image](https://github.com/MadhuVamsiA/freedomwithai/assets/143532033/12cb84bb-6364-4dfa-a197-3ee102d31857)



 Note: Keep the index.html file under the templates folder in the same path where .py folder exists.



