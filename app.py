from flask import Flask,request,render_template
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import os

#calling loading api key
load_dotenv()
app=Flask(__name__)#application start here


#configure api call moderl
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel("gemini-2.5-flash")

df=pd.read_csv("qa_data (1).csv")
#csv to context
context_text= "" 
for _,row in df.iterrows():
    context_text +=f"Q: {row['question']}\nA:{row['answer']}\n\n"

def ask_gemini(query):
    prompt = f"""
You are a Q&A assistant.

Answer ONLY using the context below.
If the answer is not present, say: No relevant Q&A found.

Context:
{context_text}

Question: {query}
"""
    response=model.generate_content(prompt)
    return response.text.strip()
 #route function
@app.route("/",methods=["GET","POST"])
def home():
    answer=""
    if request.method=="POST":
        query=request.form["query"]
        answer=ask_gemini(query)
    return render_template("index.html",answer=answer)

if __name__=="__main__":
    app.run()


#print("Q & A Chat Bot ")
#print("Enter exit get terminate")

#while True:
   # user_input=input("You :")
    #if user_input.lower()=="exit":
     #   print("GoddBye")
        #break
    #answer=ask_gemini(user_input)
    #print(f"{answer}\n")