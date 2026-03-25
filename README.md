# 🛡️ Video Piracy Detection System

A deep learning-based video fingerprinting system that detects pirated content using feature extraction and similarity search.

Built with **PyTorch + FAISS + Streamlit**, this project allows content creators to:
- Register original videos
- Generate unique fingerprints
- Detect pirated copies
- File copyright claims

---

## 🚀 Features

### 🔒 Register Original Content
- Upload a video
- Extract frame-level features using ResNet50
- Generate a unique token
- Store embeddings in FAISS vector database

### 🔍 Piracy Detection
- Upload a suspected video
- Extract features
- Perform similarity search against database
- Detect matches with confidence score

### ⚖️ Legal Workflow
- Submit copyright claims
- Generate claim ID
- Store claims in JSON
- Simulate legal verification pipeline

### 📊 System Dashboard
- View registered videos
- Monitor database size
- Track claims
- Export claim data

---

## 🧠 How It Works

### 1. Feature Extraction
- Frames are sampled from video at intervals
- Each frame is passed through **ResNet50 (without classifier)**
- Output: 2048-dimensional feature vectors

### 2. Fingerprinting
- Features are L2 normalized
- Stored in **FAISS (Inner Product Index)**

### 3. Matching
- Query video → extract features
- Perform nearest neighbor search
- Filter results using similarity threshold
- Return best matches with confidence scores

---

## 🛠️ Tech Stack

### Machine Learning / Computer Vision
- PyTorch
- Torchvision (ResNet50)
- OpenCV
- NumPy

### Backend / Search
- FAISS (Facebook AI Similarity Search)
- JSON (metadata & claims storage)

### Frontend
- Streamlit
- Custom CSS (Cybersecurity UI)

---

## 📁 Project Structure
pirate_prufen/
│
├── app.py
├── feature_extractor.py
├── vector_store.py
├── requirements.txt
│
├── faiss_index.index
├── metadata.json
├── claims.json
│
└── test_video.mp4

---

## ⚙️ Installation

```bash
git clone https://github.com/code-rh11Reyhan/video-fingerprinting-piracy-detection.git
cd video-fingerprinting-piracy-detection
pip install -r requirements.txt


## 🔁 User Workflow

1. **Register Original Video**
   - User uploads original content
   - System extracts frame-level features
   - A unique token is generated and stored

2. **Upload Suspected Video**
   - User uploads a potentially pirated video
   - System extracts features in the same way

3. **Similarity Matching**
   - Features are compared using FAISS
   - If similarity exceeds threshold → flagged as piracy

4. **Legal Action**
   - User submits a copyright claim
   - System generates a claim certificate


## ⚙️ Algorithm & Approach

### 1. Frame Sampling
- Videos are split into frames at fixed intervals
- Reduces computation while preserving content structure

### 2. Feature Extraction (Deep Learning)
- Model: ResNet50 (pretrained on ImageNet)
- Final classification layer removed
- Each frame → 2048-dimensional feature vector

### 3. Feature Normalization
- L2 normalization applied
- Ensures consistent similarity comparison

### 4. Vector Database (FAISS)
- Index type: Inner Product (cosine similarity)
- Stores all frame embeddings efficiently

### 5. Similarity Search
- Query video features are compared with stored vectors
- Top-K nearest neighbors retrieved

### 6. Threshold Filtering
- Matches above threshold (e.g., 75%) are considered piracy
- Best match per video token is returned

## 💡 Why This Works

- Deep neural networks capture **visual semantics**, not raw pixels
- Even if videos are:
  - Cropped
  - Resized
  - Slightly edited

  → Features remain similar

- FAISS enables **fast similarity search** across large datasets
- Frame-level matching ensures robustness against partial piracy


Note: Current implementation performs frame-level matching and selects best matches. Future versions will include temporal aggregation for full-video similarity scoring.