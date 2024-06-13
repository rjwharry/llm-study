# Vector Store
- 벡터들을 저장하는 store를 말하며, 벡터를 만드는 임베딩 작업이 핵심이다
- 여러 오픈소스나 서비스 중인 vector store들이 있으며 상황에 맞게 선택하여 사용해야 한다
- vector store에 사용자 query를 넣어서 유사도 등의 특정 기준을 기반으로 store에 있는 embedding을 가져와서 반환해주는 기능이 있다.

## Retriever
- vector store 클래스를 감싸서 store에 검색하는 통일된 retrieve 인터페이스를 따르도록 한다
- 그 어떤 vector store를 사용하더라도 retriever에 대한 인터페이스가 동일하다.
- `search_type`을 통해 검색할 때 어떤 기준으로 검색할 지 정할 수 있다. 기본값은 `similarity`이다
    - `similarity`: 임베딩 벡터 사이의 코사인 유사도를 계산하여 가장 유사한 문서를 가져온다
    - `MMR`: 관련성 높은 항목을 선택함과 동시에 내용의 다양성을 유지하는 방법이다.
    - `similarity_score_threshold`: 유사도가 지정한 threshold를 넘는 항목만 가져온다.
- `search_kwargs`로 여러 옵션을 제공할 수 있다
    - `k`: 유사도가 높은 문서 순으로 k개를 가져온다
    - `score_threshold`: `similarity_score_threshold` 타입으로 검색할 때 사용되는 threshold 값
    - `fetch_k`: `MMR` 알고리즘이 사용하는 후보 문서 개수. 기본값: 20
    - `lambda_mult`: 다양성의 정도를 나타내며, 1로 갈수록 유사도에 기반하며, 0으로 갈수록 다양성에 기반하여 검색한다.
    - `filter`: 문서의 metadata에 대해 필터링걸어서 원하는 문서에서만 가져올 수 있도록 한다.
- 개발, 테스트용으로 `Chroma`와 `Faiss`를 많이 사용하며, Production에서는 `Pinecone`을 많이 사용하는 거 같음

## Faiss
- 효율적인 유사도 검색과 클러스터링을 위한 라이브러리
- 유사도 기반으로 검색하는 함수 지원
    - `similarity_search(query)`: query에 대해 유사도가 높은 순서로 문서 리스트 반환
    - `similarity_search_with_score(query)`: query에 대해 유사도가 높은 순서로 문서와 유사도 점수 tuple 리스트로 반환
- `save_local`과 `load_local`로 Faiss 인덱스를 파일로 저장하고 불러올 수 있다
- 바이트 형태로 직렬화해서 저장할 수도 있는데, `pickle`을 사용하는 대신 `serialize_to_bytes()` 함수로 직렬화해야 Faiss 인덱스만 직렬화되서 용량이 작다. `deserialize_from_bytes`로 역직렬화를 할 수 있다
- `merge_from(db)` 함수로 서로 다른 faiss를 병합할 수 있다
- `similarity_search_with_score`와 같은 함수에 filter 매개변수를 전달하여 문서를 필터링할 수 있다
- `max_marginal_relevance_search` 함수로 MMR 알고리즘 기반으로 문서를 검색할 수 있다.
- `delete`로 vector store에서 문서를 삭제할 수 있다

## Chroma
- 개발자 생산성에 초점을 맞춘 AI 기반 오픈소스 Vector Store
- `in-memory`, `in-memory-with-persistence`, `docker` 방식으로 사용할 수 있다
- 기본적으로 `in-memory` 방식이며, `from_documents` 함수에 `persist_directory` 매개변수로 경로를 전달하여 로컬에 데이터를 저장할 수 있다. 
- Chroma Client로 로컬 혹은 배포된 Chroma를 바라보는 Client 객체를 만든 후 Langchain Chroma 객체에 넣어서 사용할 수 있다
- `Faiss`와 마찬가지로 `similarity_search`와 `similarity_search_with_score` 함수를 제공하고, retriever로도 사용할 수 있으며, MMR 기반 검색, 필터링도 제공하고 있다.