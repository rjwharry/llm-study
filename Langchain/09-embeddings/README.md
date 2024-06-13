# Embedding
- 임베딩이란 자연어 텍스트를 벡터로 변환하는 과정을 말한다.
- 주로 대규모로 사전학습된 모델(BERT, GPT)을 사용한다.
- 문서 임베딩은 문서를 특정 단위로 토큰화하고, 각 토큰을 벡터로 변환한 후, 각 토큰의 벡터를 평균하거나 가중 평균을 하는 등의 여러 방법을 통해 전체 문서를 임베딩 벡터를 계산하는 과정을 말한다.
- 문서 임베딩은 각 문서들 간의 유사도 측정, 추천, 클러스터링, 감정 분석 등에 활용될 수 있다.


## OpenAIEmbedding
- Langchain OpenAI 모듈에서 OpenAI의 임베딩 모델을 쉽게 사용할 수 있다
- `embed_query(text: str)` 함수로 단일 문자열을 벡터화할 수 있다.
- `embed_documents(text_list: List[str])` 함수로 문자열 리스트 형태의 단일 문서를 벡터화할 수 있다
- 모델마다 벡터 차원 기본값이 있으나, 매개변수로 차원을 조절할 수도 있다

## CacheBackedEmbeddings
- 같은 텍스트에 대한 중복 계산을 피하기 위한 embedder
- 캐시는 key-value로 저장되며, key값은 텍스트의 해시값이된다.
- `from_bytes_store(underlying_embedder, document_embedding_cache, namespace)` 함수 사용
    - `underlying_embedder`: 임베딩 계산할 embedder. OpenAIEmbedding 같은 클래스
    - `document_embedding_cache`: 캐시를 저장할 store. 파일시스템이나 메모리 DB 등을 활용할 수 있다.
    - `namespace`: 선택사항으로, 키 값 앞에 붙는 문자열이다. 같은 문자열에 대해 다른 모델을 적용할 때 캐시 데이터를 구분할 때 사용한다.

## Huggingface Embedding
- `HuggingFaceEmbeddings`: HuggingFace Transformer 라이브러리에서 제공하는 사전 학습된 모델 사용
- `HuggingFaceInferenceAPIEmbeddings`: 모델을 다운로드 받을 필요없이 HuggingFace API를 활용하여 임베딩할 수 있다.
- `HuggingFaceHubEmbeddings`: HuggingFace에서 호스팅하고 있는 임베딩 모델을 로컬에 받아서 사용할 수 있다.
- 이 모든 클래스들은 langchain과 community에서 구현한 것으로, 사용법은 OpenAIEmbeddings과 동일하다

## GPT4All
- `GPT4AllEmbeddings`: GPT4All에 있는 임베딩 모델을 사용할 수 있다
- 사용법은 다른 Embedding 객체와 동일하다