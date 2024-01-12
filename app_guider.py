import streamlit as st
import requests
import json
#百度云OCR API的访问地址
def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    api_key='GH9o78q9PoemsgbhgbRxSV8a'
    secret_key='eNVOYQZ0d1bxZz2o9WrzmYgxLXTL4g4B'
    """
    # api_key='GH9o78q9PoemsgbhgbRxSV8a'
    # secret_key='eNVOYQZ0d1bxZz2o9WrzmYgxLXTL4g4B'
    
        
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}".format(api_key,secret_key)
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

def main(prompt):
    '''
    url=https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/plugin/uxcb3ay3596p4xig/
    '''
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/plugin/uxcb3ay3596p4xig/?access_token=" + get_access_token()
    
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
    st.title("📱医学预测模型矩阵") 
    st.header('介绍') 
    st.write('''
             医学预测模型的作用是通过大数据拟合模型来判断或者预测临床事件的发生，对标的是临床上各种的评估量表，
             其实，研究表明，医学预测模型的准确度已经超过了很多的量表，却没有进行临床应用，其原因是因为临床预测模型还没有找到合适的形式进入临床，
             并且有一定的伦理方面的顾虑，比如，使用机器进行诊断，一旦出现误诊误治，责任不容易厘清。相信不久的将来，临床预测模型将会在临床上广泛的使用。\n
             目前，医学预测模型最主要的应用形式就是网页应用，本APP致力于收录各个领域的医学预测模型APP，完善预测模型APP的形式和标准，为将来的APP应用做准备。\n
             **问答的知识来源是百度千帆大模型中自建的知识库，通过丰富知识库可以更新问答的内容。
             ''')
    st.divider()
    st.header('🤖导航机器人')
    st.sidebar.header('💡问答提示')
    st.sidebar.subheader('📫APP地址')
    st.sidebar.write('目前收录教学类和类APP，通过询问地址可以对APP进行使用，比如，决策去曲线分析APP的地址。其它的APP还有保序回归APP、食管癌远处转移APP')
    st.sidebar.divider()
    st.sidebar.subheader('📚机器学习知识类')
    st.sidebar.write('目前并没有大面积收集机器学习的知识，而是收录了一些独特的经验和体会，比如，DCA分析的注意事项等')
    #导航机器人
    st.write("api_key", st.secrets["API_key"])
    st.write("secret_key", st.secrets["secret_key"])
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "你好！我收藏我很多的医学APP，你可以问我索要APP的地址进行体验；我还有许多构建APP的体会，你在网络上没有找得到的可以问我哦"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        #prompt
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        #answer
        response = main(prompt)
        msg = json.loads(response)
        answer = msg["result"]
        st.session_state.messages.append(msg)#后台necessary，role 和content
        st.chat_message("assistant").write(answer)#展示