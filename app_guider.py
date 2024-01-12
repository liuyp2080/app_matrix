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
    st.sidebar.header('💡问答提示')
    st.sidebar.subheader('📫APP地址')
    st.sidebar.write('目前收录教学类和类APP，通过询问地址可以对APP进行使用，比如，决策去曲线分析APP的地址。其它的APP还有保序回归APP、食管癌远处转移APP')
    st.sidebar.divider()
    st.sidebar.subheader('📚机器学习知识类')
    st.sidebar.write('目前并没有大面积收集机器学习的知识，而是收录了一些独特的经验和体会，比如，DCA分析的注意事项等')
    
    st.title("📱医学预测模型矩阵") 
    st.write('''
                医学预测模型的作用是通过大数据拟合模型来判断或者预测临床事件的发生，对标的是临床上各种的评估量表，
                其实，研究表明，医学预测模型的准确度已经超过了很多的量表，却没有进行临床应用，其原因是因为临床预测模型还没有找到合适的形式进入临床，
                并且有一定的伦理方面的顾虑，比如，使用机器进行诊断，一旦出现误诊误治，责任不容易厘清。相信不久的将来，临床预测模型将会在临床上广泛的使用。\n
                **问答的知识来源是百度千帆大模型中自建的知识库，通过丰富知识库可以更新问答的内容。
                ''')
    st.divider()
    st.subheader('📜目前收录的APP:')
    col1,col2,col3=st.columns(3)
    with col1:
        st.write("🌟保序回归演示")
    with col2:
        st.write("🌟决策曲线分析演示")
    with col3:
        st.write("🩺食管癌远处转移诊断")
    st.divider()
    #导航机器人
    st.subheader('🤖导航机器人')
    api_key=st.secrets["API_key"]
    secret_key=st.secrets["secret_key"]
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "你好！我收藏我很多的医学APP，你可以问我索要APP的地址进行体验；我还有许多构建APP的体会，你在网络上没有找得到的可以问我哦"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        #prompt
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        #answer
        response = main(prompt,api_key,secret_key)
        msg = json.loads(response)
        answer = msg["result"]
        st.session_state.messages.append(msg)#后台necessary，role 和content
        st.chat_message("assistant").write(answer)#展示
