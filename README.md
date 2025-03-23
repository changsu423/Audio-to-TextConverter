# 수업 녹음 및 텍스트 변환 앱 (Class Recording & Transcription App)

이 앱은 Streamlit으로 만든 수업 녹음 및 텍스트 변환 애플리케이션입니다. 강의나 수업을 녹음하고 자동으로 텍스트로 변환할 수 있습니다.

## 주요 기능

- 🎙️ 오디오 녹음 기능
- 🔄 음성-텍스트 변환 (Speech-to-Text)
- 💾 녹음 저장 및 관리
- 📄 텍스트 변환 결과 저장
- 📱 반응형 디자인

## 설치 및 실행 방법

### 로컬에서 실행하기

1. 이 저장소를 클론합니다:
```bash
git clone https://github.com/yourusername/class-recording-app.git
cd class-recording-app
```

2. 필요한 패키지를 설치합니다:
```bash
pip install -r requirements.txt
```

3. 앱을 실행합니다:
```bash
streamlit run app.py
```

### Streamlit Cloud에서 실행하기

1. GitHub에 이 저장소를 포크합니다.
2. [Streamlit Cloud](https://streamlit.io/cloud)에 로그인합니다.
3. "New app" 버튼을 클릭합니다.
4. 포크한 저장소와 `app.py` 파일을 선택합니다.
5. "Deploy"를 클릭합니다.

## 실제 STT API 연동하기

현재 앱은 데모 목적으로 텍스트 변환을 시뮬레이션합니다. 실제 Speech-to-Text 서비스를 사용하려면 다음과 같은 서비스에 연결할 수 있습니다:

- [Google Speech-to-Text API](https://cloud.google.com/speech-to-text)
- [Azure Speech Services](https://azure.microsoft.com/services/cognitive-services/speech-services/)
- [Whisper API (OpenAI)](https://openai.com/research/whisper)

`app.py` 파일에서 `simulate_transcription` 함수를 수정하여 실제 API를 호출하도록 구현하세요.

## 파일 설명

- `app.py`: 메인 Streamlit 애플리케이션
- `requirements.txt`: 필요한 Python 패키지 목록
- `sample.wav`: 데모용 샘플 오디오 파일
- `recordings.json`: 녹음 데이터 저장 파일

## 기여하기

1. 이 저장소를 포크합니다.
2. 새 브랜치를 만듭니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다.

## 라이센스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
