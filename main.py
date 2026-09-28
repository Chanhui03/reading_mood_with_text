from enum import Enum
from pydantic import BaseModel
from dotenv import load_dotenv
from typesafe_sdk import TypeSafeClient, Choice, Score

# 1. 27가지 기본 감정을 고정된 값(Enum)으로 정의합니다.
class Emotion27(str, Enum):
    ADMIRATION = "ADMIRATION"                   # 존경
    ADORATION = "ADORATION"                     # 흠모
    AESTHETIC_APPRECIATION = "AESTHETIC_APPRECIATION" # 심미적 감상
    AMUSEMENT = "AMUSEMENT"                     # 즐거움
    ANXIETY = "ANXIETY"                         # 걱정
    AWE = "AWE"                                 # 경외감
    AWKWARDNESS = "AWKWARDNESS"                 # 어색함
    BOREDOM = "BOREDOM"                         # 지루함
    CALMNESS = "CALMNESS"                       # 차분함
    CONFUSION = "CONFUSION"                     # 혼란스러움
    CRAVING = "CRAVING"                         # 간절함
    DISGUST = "DISGUST"                         # 역겨움
    EMPATHETIC_PAIN = "EMPATHETIC_PAIN"         # 공감적 고통
    ENTRANCEMENT = "ENTRANCEMENT"               # 황홀경
    ENVY = "ENVY"                               # 부러움, 질투
    EXCITEMENT = "EXCITEMENT"                   # 흥분됨, 신남
    FEAR = "FEAR"                               # 두려움
    HORROR = "HORROR"                           # 공포
    INTEREST = "INTEREST"                       # 흥미, 호기심
    JOY = "JOY"                                 # 기쁨
    NOSTALGIA = "NOSTALGIA"                     # 향수, 그리움
    ROMANCE = "ROMANCE"                         # 로맨스
    SADNESS = "SADNESS"                         # 슬픔
    SATISFACTION = "SATISFACTION"               # 만족
    SEXUAL_DESIRE = "SEXUAL_DESIRE"             # 성적 욕구
    SYMPATHY = "SYMPATHY"                       # 공감
    TRIUMPH = "TRIUMPH"                         # 승리감

# 2. Jev 모델이 응답할 완벽한 JSON 구조를 Pydantic 모델로 강제합니다.
class EmotionAnalysisResponse(BaseModel):
    primary_emotion: Emotion27      # 가장 주된 감정
    secondary_emotion: Emotion27    # 부가적인 감정
    confidence_score: float         # 판독 신뢰도 (0.0 ~ 1.0)
    intensity: int                  # 감정의 강도 (1 ~ 9)

# 3. Jev API 호출 함수
def analyze_emotion_with_jev(input_text: str) -> EmotionAnalysisResponse:
    print(f'[Jev API 호출 중...] 입력 텍스트: "{input_text}"')
    
    load_dotenv()

    # Jev 모델이 27가지 감정을 정확히 분류할 수 있도록 각 감정의 의미(기준)를 딕셔너리로 정의합니다.
    emotion_criteria = {
        Emotion27.ADMIRATION.value: "존경하거나 우러러보는 감정",
        Emotion27.ADORATION.value: "깊이 흠모하거나 애정을 느끼는 감정",
        Emotion27.AESTHETIC_APPRECIATION.value: "예술이나 아름다움을 감상하는 감정",
        Emotion27.AMUSEMENT.value: "재미있거나 즐거운 감정",
        Emotion27.ANXIETY.value: "걱정, 불안, 초조함",
        Emotion27.AWE.value: "경외감, 압도되는 느낌",
        Emotion27.AWKWARDNESS.value: "어색하고 민망한 감정",
        Emotion27.BOREDOM.value: "지루함, 따분함",
        Emotion27.CALMNESS.value: "차분하고 평온한 상태",
        Emotion27.CONFUSION.value: "혼란스럽거나 당혹스러운 감정",
        Emotion27.CRAVING.value: "무언가를 간절히 원하거나 갈망함",
        Emotion27.DISGUST.value: "역겨움, 혐오감, 강한 불쾌감",
        Emotion27.EMPATHETIC_PAIN.value: "타인의 고통에 공감하여 느끼는 아픔",
        Emotion27.ENTRANCEMENT.value: "무언가에 매료된 황홀경",
        Emotion27.ENVY.value: "부러움이나 질투",
        Emotion27.EXCITEMENT.value: "흥분되고 신나는 감정",
        Emotion27.FEAR.value: "두려움, 무서움",
        Emotion27.HORROR.value: "소름 끼치는 공포",
        Emotion27.INTEREST.value: "흥미, 호기심, 관심",
        Emotion27.JOY.value: "기쁨, 행복함",
        Emotion27.NOSTALGIA.value: "과거에 대한 향수나 그리움",
        Emotion27.ROMANCE.value: "로맨틱한 감정",
        Emotion27.SADNESS.value: "슬픔, 우울함",
        Emotion27.SATISFACTION.value: "만족스러움",
        Emotion27.SEXUAL_DESIRE.value: "성적 욕구",
        Emotion27.SYMPATHY.value: "타인에 대한 동정이나 공감",
        Emotion27.TRIUMPH.value: "승리감, 성취감"
    }

    with TypeSafeClient() as client:
        result = client.system_one(
            state=input_text,  
            questions={
                "primary_emotion": Choice(
                    criteria=emotion_criteria
                ),
                "secondary_emotion": Choice(
                    criteria=emotion_criteria
                ),
                "intensity": Score(
                    criteria=[
                        "1점: 감정이 아주 희미하게 느껴짐",
                        "2점: 감정이 약하게 느껴짐",
                        "3점: 감정이 조금 느껴짐",
                        "4점: 감정이 어느 정도 느껴짐",
                        "5점: 감정이 뚜렷하고 일반적인 수준으로 느껴짐",
                        "6점: 감정이 꽤 강하게 느껴짐",
                        "7점: 감정이 강하게 느껴짐 (행동에 영향을 줄 정도)",
                        "8점: 감정이 매우 강하게 느껴짐 (이성적 판단이 흐려질 정도)",
                        "9점: 감정이 통제하기 힘들 정도로 극도로 강렬함"
                    ]
                )
            }
        )

    # 응답 데이터 파싱 및 신뢰도 추출 (수정 완료: answers 접근 및 속성명 변경)
    primary_emotion_answer = result.answers["primary_emotion"]
    secondary_emotion_answer = result.answers["secondary_emotion"]
    intensity_answer = result.answers["intensity"]

    parsed_data = {
        "primary_emotion": primary_emotion_answer.choice,
        "secondary_emotion": secondary_emotion_answer.choice,
        "confidence_score": primary_emotion_answer.confidence, 
        "intensity": int(round(intensity_answer.score))
    }

    return EmotionAnalysisResponse(**parsed_data)

# 4. 프로그램 실행의 진입점이 되는 main 함수
def main():
    customer_review = input("입력: ")
    
    try:
        # API 호출 및 결과 받아오기
        analysis = analyze_emotion_with_jev(customer_review)
        
        print("\n[분석 완료 - 수신된 데이터]")
        print(analysis.model_dump_json(indent=2))
        
        print("\n[시스템 후속 조치 판단]")
        
        if analysis.confidence_score < 0.7:
            print("-> ⚠️ 신뢰도가 낮습니다. 관리자 검수(Human Review) 대기열로 보냅니다.")
            return

        # Python 3.10+ match-case를 통한 라우팅
        match analysis.primary_emotion:
            case Emotion27.DISGUST | Emotion27.HORROR | Emotion27.FEAR:
                if analysis.intensity >= 7:
                    print("-> 🚨 심각한 불만/공포 감지됨. 최우선 순위로 전문 상담원에게 즉시 연결합니다.")
                    
            case Emotion27.CRAVING | Emotion27.INTEREST:
                print("-> 🎯 고객이 흥미/간절함을 보이고 있습니다. 관련 상품의 구매 링크를 챗봇이 제안합니다.")
                
            case Emotion27.CONFUSION | Emotion27.AWKWARDNESS:
                print("-> ❓ 고객이 혼란스러워합니다. 상세한 이용 가이드라인(FAQ)을 발송합니다.")
                
            case _:
                print("-> 🤖 일반적인 상태입니다. 기본 AI 챗봇이 응대를 계속합니다.")

    except Exception as e:
        print(f"감정 분석 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()