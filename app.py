import streamlit as st
import tempfile
import os
import time
from datetime import datetime
import json
import base64
from io import BytesIO
import numpy as np
from pathlib import Path

# Initialize session state variables
if 'recordings' not in st.session_state:
    st.session_state.recordings = []
if 'selected_recording_index' not in st.session_state:
    st.session_state.selected_recording_index = None
if 'is_converting' not in st.session_state:
    st.session_state.is_converting = False
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False
if 'temp_audio_path' not in st.session_state:
    st.session_state.temp_audio_path = None

# Helper functions for file operations
def load_recordings():
    """Load recordings from a JSON file if it exists."""
    recordings_file = Path("recordings.json")
    if recordings_file.exists():
        with open(recordings_file, "r", encoding="utf-8") as f:
            try:
                # Load recordings but recreate audiodata from Base64
                recordings_data = json.load(f)
                for recording in recordings_data:
                    if 'audio_base64' in recording and recording['audio_base64']:
                        recording['audiodata'] = base64.b64decode(recording['audio_base64'])
                    else:
                        recording['audiodata'] = None
                return recordings_data
            except json.JSONDecodeError:
                return []
    return []

def save_recordings(recordings):
    """Save recordings to a JSON file."""
    recordings_data = []
    for recording in recordings:
        # Make a copy of the recording without the audiodata
        rec_copy = recording.copy()
        # Convert audiodata to Base64 for storage
        if 'audiodata' in rec_copy and rec_copy['audiodata']:
            rec_copy['audio_base64'] = base64.b64encode(rec_copy['audiodata']).decode('utf-8')
        else:
            rec_copy['audio_base64'] = None
        # Remove the binary data
        if 'audiodata' in rec_copy:
            del rec_copy['audiodata']
        recordings_data.append(rec_copy)
        
    with open("recordings.json", "w", encoding="utf-8") as f:
        json.dump(recordings_data, f, ensure_ascii=False, indent=2)

def get_audio_download_link(audio_bytes, filename="recording.wav"):
    """Generate a download link for audio file."""
    b64 = base64.b64encode(audio_bytes).decode()
    href = f'<a href="data:audio/wav;base64,{b64}" download="{filename}">Download Audio</a>'
    return href

def get_text_download_link(text, filename="transcript.txt"):
    """Generate a download link for text file."""
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:text/plain;base64,{b64}" download="{filename}">Download Transcript</a>'
    return href

def simulate_transcription(audio_bytes):
    """Simulate audio transcription (in a real app, you would call an STT API here)."""
    # In a real implementation, you would send the audio to a Speech-to-Text service
    # For demo purposes, we'll just wait and return sample text
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.03)  # Simulate processing time
        progress_bar.progress(i + 1)
    
    # Sample Korean transcript (similar to the React app's demo text)
    transcript = (
        "안녕하세요, 오늘 수업에서는 주요 개념에 대해 설명드리겠습니다. "
        "첫 번째로 중요한 점은 데이터의 구조화입니다. 데이터를 체계적으로 정리하면 "
        "분석이 용이해지고 인사이트를 도출하기 쉬워집니다. 두 번째는 알고리즘의 선택인데, "
        "문제에 따라 적절한 알고리즘을 선택하는 것이 중요합니다. 마지막으로 결과의 시각화를 "
        "통해 정보를 효과적으로 전달할 수 있습니다. 질문 있으신가요?"
    )
    return transcript

# Load recordings at startup
if not st.session_state.recordings:
    st.session_state.recordings = load_recordings()

# App title and description
st.title("🎙️ 수업 녹음 및 텍스트 변환 앱")
st.write("수업을 녹음하고 자동으로 텍스트로 변환하세요.")

# Create tabs
tab1, tab2, tab3 = st.tabs(["녹음", "녹음 목록", "상세 보기"])

# Tab 1: Recording
with tab1:
    st.subheader("수업 녹음")
    
    # Recording status indicator
    if st.session_state.is_recording:
        st.markdown("### 🔴 녹음 중...")
    
    # Recording buttons
    col1, col2 = st.columns(2)
    with col1:
        if not st.session_state.is_recording:
            if st.button("🎤 녹음 시작", use_container_width=True):
                st.session_state.is_recording = True
                # Use streamlit-webrtc in a real implementation
                # For this demo, we'll simulate recording
                st.session_state.temp_audio_path = tempfile.NamedTemporaryFile(delete=False, suffix='.wav').name
                st.experimental_rerun()
        else:
            if st.button("⏹️ 녹음 중지 및 저장", use_container_width=True):
                st.session_state.is_recording = False
                
                # In a real implementation, we would save the actual recorded audio
                # For this demo, we'll use a sample audio file or placeholder
                
                # Create a new recording entry
                new_recording = {
                    "id": int(time.time() * 1000),
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "title": f"녹음 {len(st.session_state.recordings) + 1}",
                    "audiodata": open("sample.wav", "rb").read() if Path("sample.wav").exists() else b"PLACEHOLDER",
                    "duration": 15,  # Placeholder duration in seconds
                    "transcript": None
                }
                
                # Add to recordings and save
                st.session_state.recordings.insert(0, new_recording)
                save_recordings(st.session_state.recordings)
                
                # Automatically select the new recording
                st.session_state.selected_recording_index = 0
                
                st.experimental_rerun()
    
    # Display recording instructions
    st.markdown("---")
    st.info("마이크 접근 권한을 허용하고 녹음 버튼을 클릭하여 수업을 녹음하세요. 녹음이 끝나면 텍스트로 변환할 수 있습니다.")
    
    # Recently recorded audio (if any)
    if st.session_state.selected_recording_index is not None and st.session_state.selected_recording_index == 0:
        recent_recording = st.session_state.recordings[0]
        st.subheader("방금 녹음됨:")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ 재생", use_container_width=True):
                # In a real app, we would play the audio
                st.audio(recent_recording["audiodata"], format="audio/wav")
        
        with col2:
            if not recent_recording["transcript"] and not st.session_state.is_converting:
                if st.button("🔄 텍스트로 변환", use_container_width=True):
                    st.session_state.is_converting = True
                    st.experimental_rerun()

# Tab 2: Recording List
with tab2:
    st.subheader("🗂️ 녹음 목록")
    
    if not st.session_state.recordings:
        st.info("녹음 기록이 없습니다.")
    else:
        for i, recording in enumerate(st.session_state.recordings):
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    title = recording["title"]
                    date = recording["date"]
                    duration = f"{recording['duration']}초" if 'duration' in recording else ""
                    has_transcript = "✅ 텍스트 변환 완료" if recording.get("transcript") else ""
                    
                    if st.button(f"**{title}**\n{date} | {duration} {has_transcript}", key=f"rec_{i}", use_container_width=True):
                        st.session_state.selected_recording_index = i
                        st.experimental_rerun()
                
                with col2:
                    st.audio(recording["audiodata"], format="audio/wav")

# Tab 3: Detailed View
with tab3:
    if st.session_state.selected_recording_index is not None:
        recording = st.session_state.recordings[st.session_state.selected_recording_index]
        
        # Header with recording info
        st.subheader(f"📄 {recording['title']}")
        st.caption(f"녹음일: {recording['date']} | 길이: {recording.get('duration', '?')}초")
        
        # Audio playback
        st.audio(recording["audiodata"], format="audio/wav")
        
        # Audio download button
        st.markdown(get_audio_download_link(recording["audiodata"], f"{recording['title']}.wav"), unsafe_allow_html=True)
        
        # Transcription section
        st.markdown("---")
        st.subheader("텍스트 변환")
        
        if st.session_state.is_converting and recording.get("transcript") is None:
            st.info("음성을 텍스트로 변환하는 중...")
            transcript = simulate_transcription(recording["audiodata"])
            
            # Update recording with transcript
            recording["transcript"] = transcript
            st.session_state.recordings[st.session_state.selected_recording_index] = recording
            save_recordings(st.session_state.recordings)
            
            st.session_state.is_converting = False
            st.experimental_rerun()
            
        elif recording.get("transcript"):
            # Display transcript
            st.text_area("변환된 텍스트:", value=recording["transcript"], height=200, disabled=True)
            
            # Text download button
            st.markdown(get_text_download_link(recording["transcript"], f"{recording['title']}-텍스트변환.txt"), unsafe_allow_html=True)
        else:
            st.info("아직 텍스트로 변환되지 않았습니다.")
            if st.button("🔄 텍스트로 변환"):
                st.session_state.is_converting = True
                st.experimental_rerun()
        
        # Edit and delete options
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            new_title = st.text_input("제목 수정:", value=recording["title"])
            if new_title != recording["title"]:
                if st.button("제목 저장"):
                    recording["title"] = new_title
                    st.session_state.recordings[st.session_state.selected_recording_index] = recording
                    save_recordings(st.session_state.recordings)
                    st.success("제목이 변경되었습니다.")
        
        with col2:
            if st.button("🗑️ 녹음 삭제", use_container_width=True):
                if st.session_state.recordings:
                    st.session_state.recordings.pop(st.session_state.selected_recording_index)
                    save_recordings(st.session_state.recordings)
                    st.session_state.selected_recording_index = None
                    st.success("녹음이 삭제되었습니다.")
                    st.experimental_rerun()
    else:
        st.info("녹음을 선택하여 상세 정보를 확인하세요.")
