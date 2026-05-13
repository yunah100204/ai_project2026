import streamlit as st

st.set_page_config(page_title="MBTI 진로 추천", page_icon="✨")

st.title("✨ MBTI 기반 진로 추천 프로그램")
st.write("MBTI를 선택하면 추천 진로 2가지와 관련 정보를 알려줍니다.")

mbti_data = {
    "INTJ": [
        {
            "job": "데이터 분석가",
            "major": "데이터사이언스학과, 통계학과",
            "personality": "논리적이고 분석적인 사람",
            "salary": "평균 연봉 약 4,500만원"
        },
        {
            "job": "연구원",
            "major": "자연과학계열 학과",
            "personality": "집중력이 높고 탐구심이 강한 사람",
            "salary": "평균 연봉 약 5,000만원"
        }
    ],

    "INTP": [
        {
            "job": "프로그래머",
            "major": "컴퓨터공학과",
            "personality": "창의적이고 문제 해결을 좋아하는 사람",
            "salary": "평균 연봉 약 4,800만원"
        },
        {
            "job": "대학교수",
            "major": "교육학과, 전공 관련 학과",
            "personality": "지식을 탐구하고 설명하는 것을 좋아하는 사람",
            "salary": "평균 연봉 약 6,000만원"
        }
    ],

    "ENTJ": [
        {
            "job": "기업 경영인",
            "major": "경영학과",
            "personality": "리더십이 강하고 목표 지향적인 사람",
            "salary": "평균 연봉 약 7,000만원"
        },
        {
            "job": "마케팅 매니저",
            "major": "광고홍보학과",
            "personality": "전략적으로 생각하는 사람",
            "salary": "평균 연봉 약 5,000만원"
        }
    ],

    "ENTP": [
        {
            "job": "광고 기획자",
            "major": "광고홍보학과",
            "personality": "아이디어가 많고 활동적인 사람",
            "salary": "평균 연봉 약 4,500만원"
        },
        {
            "job": "창업가",
            "major": "경영학과",
            "personality": "도전을 좋아하고 창의적인 사람",
            "salary": "평균 연봉 약 6,000만원"
        }
    ],

    "INFJ": [
        {
            "job": "심리상담사",
            "major": "심리학과",
            "personality": "공감 능력이 뛰어난 사람",
            "salary": "평균 연봉 약 4,000만원"
        },
        {
            "job": "작가",
            "major": "문예창작학과",
            "personality": "상상력이 풍부하고 감수성이 깊은 사람",
            "salary": "평균 연봉 약 3,500만원"
        }
    ],

    "INFP": [
        {
            "job": "일러스트레이터",
            "major": "디자인학과",
            "personality": "감성이 풍부하고 창의적인 사람",
            "salary": "평균 연봉 약 3,800만원"
        },
        {
            "job": "사회복지사",
            "major": "사회복지학과",
            "personality": "배려심이 많고 따뜻한 사람",
            "salary": "평균 연봉 약 3,300만원"
        }
    ],

    "ENFJ": [
        {
            "job": "교사",
            "major": "교육학과",
            "personality": "사람들을 이끄는 것을 좋아하는 사람",
            "salary": "평균 연봉 약 5,000만원"
        },
        {
            "job": "HR 담당자",
            "major": "경영학과",
            "personality": "소통 능력이 뛰어난 사람",
            "salary": "평균 연봉 약 4,500만원"
        }
    ],

    "ENFP": [
        {
            "job": "유튜버",
            "major": "미디어커뮤니케이션학과",
            "personality": "에너지가 넘치고 표현력이 좋은 사람",
            "salary": "평균 연봉 다양함"
        },
        {
            "job": "행사 기획자",
            "major": "관광경영학과",
            "personality": "사교적이고 아이디어가 풍부한 사람",
            "salary": "평균 연봉 약 4,000만원"
        }
    ],

    "ISTJ": [
        {
            "job": "공무원",
            "major": "행정학과",
            "personality": "책임감이 강하고 꼼꼼한 사람",
            "salary": "평균 연봉 약 4,500만원"
        },
        {
            "job": "회계사",
            "major": "회계학과",
            "personality": "정확성과 계산 능력이 좋은 사람",
            "salary": "평균 연봉 약 6,000만원"
        }
    ],

    "ISFJ": [
        {
            "job": "간호사",
            "major": "간호학과",
            "personality": "세심하고 배려심 있는 사람",
            "salary": "평균 연봉 약 4,500만원"
        },
        {
            "job": "유치원 교사",
            "major": "유아교육과",
            "personality": "따뜻하고 책임감 있는 사람",
            "salary": "평균 연봉 약 3,500만원"
        }
    ],

    "ESTJ": [
        {
            "job": "경찰관",
            "major": "경찰행정학과",
            "personality": "원칙적이고 리더십 있는 사람",
            "salary": "평균 연봉 약 5,000만원"
        },
        {
            "job": "은행원",
            "major": "경제학과",
            "personality": "체계적이고 신뢰감 있는 사람",
            "salary": "평균 연봉 약 5,500만원"
        }
    ],

    "ESFJ": [
        {
            "job": "승무원",
            "major": "항공서비스학과",
            "personality": "친절하고 서비스 정신이 강한 사람",
            "salary": "평균 연봉 약 4,500만원"
        },
        {
            "job": "호텔리어",
            "major": "호텔관광학과",
            "personality": "사람을 잘 챙기는 사람",
            "salary": "평균 연봉 약 4,000만원"
        }
    ],

    "ISTP": [
        {
            "job": "정비사",
            "major": "자동차공학과",
            "personality": "손재주가 좋고 실용적인 사람",
            "salary": "평균 연봉 약 4,200만원"
        },
        {
            "job": "파일럿",
            "major": "항공운항학과",
            "personality": "침착하고 판단력이 좋은 사람",
            "salary": "평균 연봉 약 7,000만원"
        }
    ],

    "ISFP": [
        {
            "job": "바리스타",
            "major": "호텔외식조리학과",
            "personality": "감각적이고 차분한 사람",
            "salary": "평균 연봉 약 3,300만원"
        },
        {
            "job": "플로리스트",
            "major": "원예학과",
            "personality": "예술 감각이 좋은 사람",
            "salary": "평균 연봉 약 3,000만원"
        }
    ],

    "ESTP": [
        {
            "job": "스포츠 코치",
            "major": "체육학과",
            "personality": "활동적이고 추진력이 있는 사람",
            "salary": "평균 연봉 약 4,000만원"
        },
        {
            "job": "영업직",
            "major": "경영학과",
            "personality": "사람들과 대화하는 것을 좋아하는 사람",
            "salary": "평균 연봉 약 5,000만원"
        }
    ],

    "ESFP": [
        {
            "job": "배우",
            "major": "연극영화과",
            "personality": "표현력이 뛰어나고 밝은 사람",
            "salary": "평균 연봉 다양함"
        },
        {
            "job": "메이크업 아티스트",
            "major": "뷰티미용학과",
            "personality": "감각적이고 트렌드에 민감한 사람",
            "salary": "평균 연봉 약 3,500만원"
        }
    ]
}

selected_mbti = st.selectbox(
    "MBTI를 선택하세요",
    list(mbti_data.keys())
)

st.subheader(f"📌 {selected_mbti} 추천 진로")

for career in mbti_data[selected_mbti]:
    st.markdown(f"""
    ### 💼 {career['job']}
    - 🎓 적합한 학과: {career['major']}
    - 😊 잘 맞는 성격: {career['personality']}
    - 💰 평균 연봉: {career['salary']}
    """)
