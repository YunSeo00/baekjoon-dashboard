import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.patches import RegularPolygon

# 모듈 수준에서 session_state 객체 정의
if "selected_users" not in st.session_state:
    st.session_state["selected_users"] = []

# 등급을 숫자로 변환하는 함수
def tier_to_num(tier):
    division = 1
    for char in tier[::-1]:
        if char.isdigit():
            division = int(char)
            break
    
    if tier.startswith("Bronze"):
        return 2.0 - 0.2 * (division - 1)
    elif tier.startswith("Silver"):
        return 3.0 - 0.2 * (division - 1)
    elif tier.startswith("Gold"):
        return 4.0 - 0.2 * (division - 1)
    elif tier.startswith("Platinum"):
        return 5.0 - 0.2 * (division - 1)
    elif tier.startswith("Diamond"):
        return 6.0 - 0.2 * (division - 1)
    elif tier.startswith("Ruby"):
        return 7.0 - 0.2 * (division - 1)
    elif tier == "Master":
        return 8.0
    else:
        return 1.2

# 등급 범위에 따라 텍스트로 변환하는 함수 정의
def tier_avg_to_text(avg_tier):
    if avg_tier <= 1.2:
        return "Bronze 5"
    elif 1.2 < avg_tier <= 1.4:
        return "Bronze 4"
    elif 1.4 < avg_tier <= 1.6:
        return "Bronze 3"
    elif 1.6 < avg_tier <= 1.8:
        return "Bronze 2"
    elif 1.8 < avg_tier <= 2.0:
        return "Bronze 1"
    elif 2.0 < avg_tier <= 2.2:
        return "Silver 5"
    elif 2.2 < avg_tier <= 2.4:
        return "Silver 4"
    elif 2.4 < avg_tier <= 2.6:
        return "Silver 3"
    elif 2.6 < avg_tier <= 2.8:
        return "Silver 2"
    elif 2.8 < avg_tier <= 3.0:
        return "Silver 1"
    elif 3.0 < avg_tier <= 3.2:
        return "Gold 5"
    elif 3.2 < avg_tier <= 3.4:
        return "Gold 4"
    elif 3.4 < avg_tier <= 3.6:
        return "Gold 3"
    elif 3.6 < avg_tier <= 3.8:
        return "Gold 2"
    elif 3.8 < avg_tier <= 4.0:
        return "Gold 1"
    elif 4.0 < avg_tier <= 4.2:
        return "Platinum 5"
    elif 4.2 < avg_tier <= 4.4:
        return "Platinum 4"
    elif 4.4 < avg_tier <= 4.6:
        return "Platinum 3"
    elif 4.6 < avg_tier <= 4.8:
        return "Platinum 2"
    elif 4.8 < avg_tier <= 5.0:
        return "Platinum 1"
    elif 5.0 < avg_tier <= 5.2:
        return "Diamond 5"
    elif 5.2 < avg_tier <= 5.4:
        return "Diamond 4"
    elif 5.4 < avg_tier <= 5.6:
        return "Diamond 3"
    elif 5.6 < avg_tier <= 5.8:
        return "Diamond 2"
    elif 5.8 < avg_tier <= 6.0:
        return "Diamond 1"
    elif 6.0 < avg_tier <= 6.2:
        return "Ruby 5"
    elif 6.2 < avg_tier <= 6.4:
        return "Ruby 4"
    elif 6.4 < avg_tier <= 6.6:
        return "Ruby 3"
    elif 6.6 < avg_tier <= 6.8:
        return "Ruby 2"
    elif 6.8 < avg_tier <= 7.0:
        return "Ruby 1"
    elif avg_tier > 7.0:
        return "Master"
    else:
        return 1.2

csv_path = "/Users/thjeong/Desktop/BOAZ/adv/files/new_users_detail.csv"  
user_df = pd.read_csv(csv_path)

# 사용자 검색창을 사이드바에 추가
user_search = st.sidebar.text_input("### **사용자 검색**", key="user_search", help="도움말: 백준 사이트에서 사용하는 아이디를 입력하세요.")

# 사용자가 검색어를 입력한 경우
if user_search:
    exact_match = user_df['user_id'].str.lower() == user_search.lower()

    # 정확한 일치하는 사용자가 있는 경우
    if exact_match.any():
        filtered_user = user_df[exact_match]

        st.sidebar.write("검색 결과:")
        st.sidebar.write(filtered_user[['user_rank', 'user_id', 'user_tier']].to_markdown(index=False))

        st.sidebar.write("")

        # 사용자가 있을 때 분석 등록 버튼 추가
        if st.sidebar.button("사용자 등록", key=f"register_button_{user_search}"):
            if user_search not in st.session_state["selected_users"]:
                st.session_state["selected_users"].append(user_search)

    # 정확한 일치하는 사용자가 없는 경우
    else:
        st.sidebar.write("검색 결과가 없습니다.")
        st.sidebar.write(pd.DataFrame({"user_rank": [0], "user_id": [user_search], "user_tier": ["Bronze 5"]}).to_markdown(index=False))

        st.sidebar.write("")

        # 사용자가 없을 때 분석 등록 버튼 추가
        if st.sidebar.button("사용자 등록", key=f"register_button_{user_search}"):
            selected_user = user_search
            if selected_user not in st.session_state["selected_users"]:
                st.session_state["selected_users"].append(selected_user)

# 제목 title 넣기
st.title('*BAEKJOON: Group-based Problem Recommendation Service*')

st.write("")
st.write("")
st.write("")

# 팁 추가
st.write("### **💡 Tips**")
st.write("1. 백준 그룹 문제 추천 서비스 대시보드는 실제 백준 사이트의 정보를 참조하여 기능합니다.") 
st.write("2. 백준 등급은 **Bronze**부터 **Master**등급까지 구성되어 있습니다.")
st.write("3. **Master** 등급을 제외한 각 등급마다 **5**개의 구간으로 나누어집니다. (예: Silver 1 ~ Silver 5)")
st.write("4. 백준 그룹 문제 추천 서비스는 **Silver 5**이상 등급부터 사용하는 것을 권장합니다.")
st.write("5. 사용자 아이디의 등급이 **Silver 5 미만**이거나 존재하지 않을 경우, **Bronze 5**로 적용됩니다.")
st.write("6. 그래프는 선택된 사용자의 **현재 카테고리별 점수**를 나타내며, **Group Average**는 그룹의 평균 점수를 나타냅니다.")
st.write("7. Silver 5 미만 사용자의 경우 시각화가 제한되며, 그룹 카테고리 점수 평균에 따로 영향을 주지 않습니다.")

st.write("")
st.write("")
st.write("")

st.markdown("""
    <div style="display: block; text-align: left; margin-left: 0px;">
        <h3>✔️ Check Baekjoon Tier</h3>
    </div>
""", unsafe_allow_html=True)

st.sidebar.write("")
st.sidebar.write("")

# 등록된 사용자 정보 표시, 선택된 사용자들의 등급 정보 추출
if st.session_state["selected_users"]:
    unique_selected_users = list(set(st.session_state["selected_users"]))

    st.write("🔍  **조회하고 싶은 사용자를 선택하고 개인 및 그룹의 현재 백준 등급과 카테고리별 점수를 확인하세요!** 🔍")
    selected_users = st.multiselect("", unique_selected_users)

    # 등록된 사용자 리스트 표시
    st.sidebar.write("### **등록된 사용자 목록** 💻")
    st.sidebar.write("사용자 아이디 두 번 클릭 시 그룹에서 **제외**")

    for user in st.session_state["selected_users"]:
        delete_button_clicked = st.sidebar.button(f"{user}", key=f"delete_button_{user}")
        if delete_button_clicked:
            st.session_state["selected_users"].remove(user)
            break  

    if selected_users:
        selected_user_info = user_df[user_df['user_id'].isin(selected_users)][['user_id', 'user_tier', 'implement', 'ds', 'dp', 'graph', 'search', 'string', 'math', 'opt', 'geo', 'adv']]
        
        # 그룹 평균 등급 계산
        all_users = selected_users + list(selected_user_info[selected_user_info['user_id'].isin(selected_users) == False]['user_id'])
        average_tiers = [tier_to_num(tier) for tier in selected_user_info['user_tier'].tolist()] + [1.2] * (len(all_users) - len(selected_user_info))
        average_tier = np.mean(average_tiers)

        # 평균 티어를 텍스트로 변환
        average_tier_text = tier_avg_to_text(average_tier)

        # 선택된 각 사용자에 대해 만약 데이터셋에 없는 경우 기본값으로 1.2 설정
        for user in selected_users:
            user_tier = tier_to_num(selected_user_info[selected_user_info['user_id'] == user]['user_tier'].values[0]) if user in selected_user_info['user_id'].values else 1.2

        st.write("")

        # 텍스트로 변환된 등급 표시
        st.write(f"<div style='text-align: center; font-size: xx-large;'><strong> ➡️ 현재 그룹의 백준 평균 등급은 <span style='color: red;'>{average_tier_text}</span>입니다.</strong></div>", unsafe_allow_html=True)

        st.write("")
        st.write("")
        st.write("")
        st.write("")

        # 사용자에 대한 레이더 차트 그리기
        if selected_users:
            st.write("### 🏆 **Individual Ratings by Category**")

            st.write("")
            st.write("")

            # 개인 사용자에 대한 레이더 차트 그리기
            fig, axs = plt.subplots(3, 3, subplot_kw=dict(polar=True), figsize=(12, 12))
            fig.suptitle("Ratings by Category", fontsize=20)

            num_selected_users = len(selected_users)

            for i in range(3):
                for j in range(3):
                    idx = i * 3 + j
                    
                    # 해당 인덱스에 사용자 정보가 있는 경우
                    if idx < num_selected_users:
                        user = selected_users[idx]
                        user_info = selected_user_info[selected_user_info['user_id'] == user]
                        
                        # categories와 values 설정. 처음 요소를 마지막에 추가하여 배열 길이 일치시킴
                        categories = ['implement', 'ds', 'dp', 'graph', 'search', 'string', 'math', 'opt', 'geo', 'adv']
                        values = user_info[categories].values.flatten().tolist()
                        values += [values[0]] 

                        # 각 카테고리의 수 만큼 각도 설정
                        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
                        angles += angles[:1]  

                        ax = axs[i, j]
                        ax.plot(angles, values, 'o-', linewidth=2)

                        # 레이팅 그룹 평균에 대한 레이더 차트 그리기
                        average_values = np.mean(selected_user_info[categories].values, axis=0).tolist()
                        average_values += [average_values[0]]  
                        ax.plot(angles, average_values, 'o-', linewidth=2, color='red', alpha=0.5)

                        ax.fill(angles, average_values, alpha=0.25)

                        # 각도를 설정할 때, 리스트가 아닌 NumPy 배열로 변환
                        ax.set_thetagrids(np.array(angles[:-1]) * 180 / np.pi, categories)
                        ax.set_title(f"{user}'s Ratings", fontsize=10, fontweight='bold')
                        #ax.legend(loc='upper right', bbox_to_anchor=(0, 0))

                        # 표현 범위를 100까지로 조절
                        ax.set_ylim(0, 100)
                    else:
                        # 해당 인덱스에 사용자 정보가 없는 경우
                        axs[i, j].axis('off')

            # 레이아웃 조정
            plt.tight_layout(rect=[0, 0, 1, 0.96])

            # Streamlit에서 그림 표시
            st.pyplot(fig)

