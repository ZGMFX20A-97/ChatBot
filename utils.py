from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain

#AI処理プロセスの定義
def get_chat_response(prompt, memory, openai_api_key):
    #llmモデルの定義
    model = ChatOpenAI(model="gpt-3.5-turbo", api_key=openai_api_key)

    #外部からメモリーを受け取り、Conversationのチェインを定義
    chain = ConversationChain(llm=model, memory=memory)
    
    #chainのinvoke関数で処理を実行し、パラメーターとしてユーザーの入力(prompt)を渡す
    response = chain.invoke({"input": prompt})

    return response["response"]
