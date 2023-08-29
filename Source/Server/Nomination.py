"""
작성자 : 이승신, 주혜인
작성일 : 23/08/25, 23/08/28-29
내용 : 레시피와 찜목록, 선호 음식을 기반으로 사용자에게 음식을 추천해주는 하이브리드 모델 알고리즘입니다.
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

from Source.Common.DBConnector import DBConnector


class Nomination:
    __instance__ = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance__, cls):
            cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    def __init__(self):
        self.user_likes = dict()
        self.recipes = None

    def load_dataset(self):
        db = DBConnector()

        # --- 사용자 선호 정보 조회
        query_1 = "\"USER_ID\", \"RECIPE_ID\""
        query_2 = "\"TB_PREFER\" natural join \"TB_RECIPE\""
        rows = db.select_data(query_1, query_2)

        # --- 협업 필터링용 유저-선호 평가 행렬 생성
        for (k_, v_) in rows:
            if k_ not in self.user_likes.keys() or not isinstance(self.user_likes[k_], list):
                self.user_likes[k_] = list()

            self.user_likes[k_].append(v_)

        # --- 레시피 데이터 조회
        query_3 = "\"RECIPE_ID\", \"RECIPE_TY\", \"RECIPE_INGR\""
        query_4 = "\"TB_RECIPE\""
        rows = db.select_data(query_3, query_4)

        recipes = dict()
        recipes["RECIPE_ID"] = list()
        recipes["RECIPE_TY"] = list()
        recipes["RECIPE_INGR"] = list()

        for (i, j, k) in rows:
            recipes["RECIPE_ID"].append(i)
            recipes["RECIPE_TY"].append(j)
            recipes["RECIPE_INGR"].append(k)

        self.recipes = pd.DataFrame.from_dict(data=recipes, orient="columns")

    def get_content_filtering(self, recipe_nm):
        # --- TF-IDF 벡터화 (콘텐츠 기반 필터링)
        # ** TfidfVectorizer : Convert a collection of raw documents to a matrix of TF-IDF features.
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        # tfidf_vectorizer = TfidfVectorizer(analyzer='word')
        tfidf_matrix = tfidf_vectorizer.fit_transform(self.recipes['RECIPE_INGR'])

        # 코사인 유사도 계산 (콘텐츠 기반 필터링)
        cosine_sim_content = linear_kernel(tfidf_matrix, tfidf_matrix)

        # 콘텐츠 기반 필터링 결과 → 디버깅 완료
        content_idx = self.recipes[self.recipes['RECIPE_ID'] == recipe_nm].index[0]
        content_sim_scores = list(enumerate(cosine_sim_content[content_idx]))
        content_sim_scores = sorted(content_sim_scores, key=lambda x: x[1], reverse=True)

        return content_sim_scores

    def get_collaborative_filtering(self, user):
        ratings = pd.DataFrame(index=self.user_likes.keys(), columns=self.recipes['RECIPE_ID'])
        for user, liked_recipes in self.user_likes.items():
            ratings.loc[user, liked_recipes] = 1

        ratings = ratings.fillna(0)

        # 코사인 유사도 계산 (협업 필터링)
        cosine_sim_collaborative = cosine_similarity(ratings.T)

        # 협업 필터링 결과
        user_idx = ratings.index.get_loc(user)
        collaborative_sim_scores = list(enumerate(cosine_sim_collaborative[user_idx]))
        collaborative_sim_scores = sorted(collaborative_sim_scores, key=lambda x: x[1], reverse=True)

        return collaborative_sim_scores

    # === 하이브리드 모델 정의
    def get_hybrid_recommendations(self, collaborative_sim_scores, content_sim_scores, num_recommendations=2):
        # 가중치 조정 (실험적으로 조정)
        content_weight = 0.4  # 콘텐츠 기반 유사도 가중치
        collaborative_weight = 0.6  # 협업 필터링 유사도 가중치

        # 가중 평균하여 추천
        hybrid_sim_scores = [(idx, content_sim * content_weight + collaborative_sim * collaborative_weight)
                             for (idx, content_sim), (_, collaborative_sim)
                             in zip(content_sim_scores, collaborative_sim_scores)]

        hybrid_sim_scores = sorted(hybrid_sim_scores, key=lambda x: x[1], reverse=True)
        hybrid_sim_scores = hybrid_sim_scores[1:num_recommendations+1]

        recipe_indices = [i[0] for i in hybrid_sim_scores]
        return self.recipes['RECIPE_ID'].iloc[recipe_indices]

    def get_recommendation_list(self, user_id:str, user_taste: list):
        collaborative_result = self.get_collaborative_filtering(user_id)

        content_result = list()
        for i, v_ in enumerate(user_taste):
            result_ = self.get_content_filtering(int(v_))
            content_result.append(result_)

        hybrid_recommended_recipes = list()
        for i, v_ in enumerate(content_result):
            result_ = self.get_hybrid_recommendations(collaborative_result, v_)
            result_ = result_.tolist()
            hybrid_recommended_recipes.extend(result_)

        return hybrid_recommended_recipes


if __name__ == '__main__':
    nm = Nomination()

    # --- 추천에 사용할 개인화 정보
    user_ = 'lss'
    # recipe_title = ['동치미', '우유두부', '떡꼬치']
    recipe_title = ['1', '2', '3']

    # --- 현재 데이터셋 확보 후 함수 호출
    nm.load_dataset()
    result = nm.get_recommendation_list(user_, recipe_title)

    # --- 총 6종의 추천 음식을 리스트의 형태로 반환
    print(user_, "님의 추천 음식 :", result)
    # lss 님의 추천 음식 : ['굴깍두기', '배추밤김치', '오징어불고기', '무말랭이무침', '떡국', '돼지불고기']
