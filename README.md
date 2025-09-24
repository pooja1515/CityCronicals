# 📰 CityChronicles: AI-Powered Gujarati News Platform

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![NLP](https://img.shields.io/badge/NLP-BERT%20%7C%20Transformers-yellowgreen)](https://huggingface.co/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🚀 Overview
**CityChronicles** is an **AI-powered platform** that processes and analyzes **Gujarati news articles** using state-of-the-art Natural Language Processing (NLP).  
It enables **automatic classification, summarization, and retrieval** of news content, making regional-language journalism more accessible and intelligent.  

This project is especially useful for:
- 📰 News readers seeking **concise summaries**  
- 📊 Researchers analyzing **regional trends**  
- 🧠 Students learning **NLP for Indic languages**  

---

## ✨ Features
- **Gujarati Language Support:** Built specifically for regional news processing.  
- **Automated Summarization:** Generates crisp, context-aware summaries.  
- **Topic Classification:** Categorizes news into politics, sports, economy, etc.  
- **Named Entity Recognition (NER):** Extracts people, places, organizations.  
- **Semantic Search:** Find relevant articles using embeddings.  
- **Scalable NLP Pipeline:** Built to extend to other Indic languages.  

---

## 🛠️ Tech Stack
- **Language Models:** BERT (mBERT / IndicBERT)  
- **NLP Frameworks:** Hugging Face Transformers, NLTK, SpaCy  
- **Backend:** Python 3.11  
- **Database:** FAISS / Chroma (for embeddings & retrieval)  
- **Frontend:** Streamlit (optional UI for demos)  

---

## ⚡ Installation
Clone the repository:

```bash
git clone https://github.com/yourusername/citychronicles.git
cd citychronicles
```
Create a virtual environment and install dependencies:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```
Run preprocessing and model pipeline:
```bash
python preprocess.py
python train.py
```
Launch the Streamlit demo:
```bash
streamlit run app.py
```
## 📂 Project Structure
```bash
citychronicles/
│
├─ app.py              # Streamlit frontend (demo)
├─ preprocess.py       # Text cleaning and preprocessing
├─ train.py            # Training & fine-tuning models
├─ requirements.txt    # Python dependencies
├─ data/               # Sample Gujarati news dataset
├─ models/             # Trained/fine-tuned models
└─ README.md
```
## 🌟 Future Enhancements

- Add multilingual support (Hindi, Marathi, etc.)
- Deploy as a full web app for journalists and readers
- Integrate real-time news feeds via APIs
- Add fact-checking modules

## 👩‍💻 Author
- Made with ❤️ by [Pooja Dave](https://www.linkedin.com/in/poojaddave)
- Connect on [LinkedIn](https://www.linkedin.com/in/poojaddave)


## 📄 License
- This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
- ⭐ Don’t forget to star this repo if you found it helpful!
