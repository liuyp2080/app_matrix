import streamlit as st
import requests
import json
#百度云OCR API的访问地址
def get_access_token(api_key,secret_key):

    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}".format(api_key,secret_key)
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

def main(prompt,api_key,secret_key):
    '''
    url=https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/plugin/uxcb3ay3596p4xig/
    '''
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/plugin/uxcb3ay3596p4xig/?access_token=" + get_access_token(api_key,secret_key)
    
    payload = json.dumps({
        "query": prompt,
        "plugins":["uuid-zhishiku"],
        "verbose":False
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    return response.text
    


if __name__ == '__main__':
    st.sidebar.header('❤️‍🔥欢迎关注')
    st.sidebar.image('media_code.jpg',width=200)
    
    st.sidebar.header('💡问答提示')
    st.sidebar.subheader('📫APP地址')
    st.sidebar.write('通过询问地址可以对APP进行访问（APP名+地址），比如，决策去曲线分析APP地址。')
    st.sidebar.divider()
    st.sidebar.subheader('📚机器学习知识类')
    st.sidebar.write('知识库内收录了一些独特的经验和体会，包括：医学预测模型矩阵计划？DCA分析的注意事项？预测模型+临床检查的筛查策略？局部评价介绍？XXAPP简介？医学预测模型APP制作规范？')
    st.sidebar.divider()
    st.sidebar.header('⚙️涉及技术')
    st.sidebar.write("问答机器人导航使用百度千帆大模型中自建知识库；python语言APP使用steamlit构建；R语言APP使用shiny构建；临床预测模型使用R或python语言构建") 
    
    st.title("📱医学预测模型矩阵") 
    st.write('''
                医学预测模型的作用是通过大数据拟合模型来判断或者预测临床事件的发生，对标的是临床上各种的评估量表，
                其实，研究表明，医学预测模型的准确度已经超过了很多的量表，却没有进行临床应用，其原因是因为临床预测模型还没有找到合适的形式进入临床，
                并且有一定的伦理方面的顾虑，比如，使用机器进行诊断，一旦出现误诊误治，责任不容易厘清。相信不久的将来，临床预测模型将会在临床上广泛的使用。\n
                
                ''')
    st.subheader('📜收录的APP')
    with st.expander('🎓教学类 ⚕️实用类',expanded=True):
        col1,col2,col3=st.columns(3)
        with col1:
            st.write("🎓保序回归演示")
        with col2:
            st.write("🎓决策曲线分析演示")
        with col3:
            st.write("⚕️食管癌远处转移诊断")
    
    #导航机器人
    st.subheader('🤖导航机器人')
    api_key=st.secrets["API_key"]
    secret_key=st.secrets["secret_key"]
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "你好！我收藏我很多的医学APP，你可以问我索要APP的地址进行体验；我还有许多构建APP的体会，你在网络上没有找得到的可以问我哦"}]
    # for msg in st.session_state["messages"]:
    #     st.chat_message(msg["role"]).write(msg["content"])  
    #
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
    # Display the prior chat messages
    print(st.session_state.messages)    
    for message in st.session_state.messages: 
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = main(prompt,api_key,secret_key)
                msg = json.loads(response)
                answer = msg["result"]
                st.session_state.messages.append({'role':'assistant','content':answer})#后台necessary，role 和content
                st.write(answer)#展

     