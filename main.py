import streamlit as st
from utils import get_chat_response
from langchain.memory import ConversationBufferMemory
from openai import AuthenticationError

#アプリのタイトルを定義
st.title("チャットボット")

#API Keyを入力するためのサイドバー
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Keyを入力してください",type="password")
    st.markdown("[Open AI API Keyを取得する](https://platform.openai.com/account/)")


if "memory" not in st.session_state:
    #ユーザーとAIの会話の履歴を初期化し、後ほどget_chat_response関数に渡す
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    #sessionに会話の履歴を置く容器がない場合初期化する
    st.session_state["messages"] = [{"role": "ai","content": "こちらチャットボットです。何か手伝えることがありますでしょうか。"}]

#双方送ったメッセージをセッションに保存されたmessageリストから取り出して画面に表示する
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

#ユーザーの入力を受け取る変数を用意
prompt = st.chat_input()

#もし入力があった場合
if prompt:
    if not openai_api_key:
        st.info("OpenAI API Keyを入力してください")
        st.stop()
    
    #ユーザーの入力内容をmessageリストに保存する
    st.session_state["messages"].append({"role": "human","content": prompt})
    #入力した内容を画面へ書き出す
    st.chat_message("human").write(prompt)

    try:
        #返答考える途中はスピナーと文言を表示させる
        with st.spinner("AIが返答中です、少々お待ちを。。。"):
            response = get_chat_response(prompt,st.session_state["memory"],openai_api_key)
        msg = {"role": "ai","content": response}

        #AIが返したメッセージをメッセージリストに保存し、画面へ書き出す
        st.session_state["messages"].append(msg)
        st.chat_message("ai").write(response)

    except(AuthenticationError):
        st.info("正しいAPI Keyを入力してください")
        st.stop()
    



