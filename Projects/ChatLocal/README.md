# ChatLlama
- Llam3를 이용하여 chatGPT 클론 웹앱 구현
- session_id 별로 대화내용을 redis에 기록하고 있음.
## Tech Stack
- Streamlit
- Langchain
- Redis
## QuickStart
```bash
cd yamls && docker compose up -d && cd -
streamlit run main.py
```