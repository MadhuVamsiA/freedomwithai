
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

***************************************************
# 3. Install the required libraries in python environment
****************************************************

!pip install -q openai 

!pip install Flask

!pip install requests

**********************************************
# 4. Run the .py file
**********************************************
1. Open anconda terminal/prompt on your local and then go to the directory where the chatbot_with_chatgpt_API.py with the below command
   cd "folder path"

   Note: Make sure to activate the environment if you have created any other than base environmnet (conda activate envname)
3. run "python chatbot_with_chatgpt_API.py"
   ![image](https://github.com/MadhuVamsiA/freedomwithai/assets/143532033/1cf0506e-cf51-4dd1-9d63-ee61367b158d)

4. it is going to give us a one url. click on that or copy paste to any browser.
5. It will open a window like below. You can enter prompt and click on get response button to get the response.
   
 ![image](https://github.com/MadhuVamsiA/freedomwithai/assets/143532033/21589b45-1231-476e-b196-f282160e0661)

