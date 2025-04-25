# Podcast AI Summarizer 🎙️

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://podcast-ai-summarize.streamlit.app/)

A powerful AI-powered tool that automatically summarizes podcast episodes by analyzing their RSS feeds. Built with Streamlit and powered by advanced AI models.

## 🌟 Features

- **Automated Summarization**: Generate concise summaries of podcast episodes using AI
- **RSS Feed Integration**: Works with any podcast RSS feed
- **Guest Information Extraction**: Automatically identifies and extracts guest information
- **Key Moments Highlighting**: Identifies and highlights important moments in the episode
- **Beautiful UI**: Clean and intuitive interface for easy navigation
- **Cloud Deployment**: Accessible anywhere through Streamlit Cloud and Render

## 🚀 Live Demo

Try the app live:
- [Podcast AI Summarizer (Streamlit)](https://podcast-ai-summarize.streamlit.app/)
- [Podcast AI Summarizer (Render)](https://podcast-ai-summarize.onrender.com/)

## 🔍 Find Podcast RSS Feeds

Need a podcast RSS feed? Use the [Castos RSS Feed Finder](https://castos.com/tools/find-podcast-rss-feed/) to easily find RSS feeds for any podcast.

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/harshalgondaliya/podcast-ai-summarize.git
cd podcast-ai-summarize
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run podcast_frontend.py
```

## 💡 How to Use

1. Open the app in your browser
2. Find a podcast RSS feed using the [Castos RSS Feed Finder](https://castos.com/tools/find-podcast-rss-feed/)
3. Paste the RSS feed URL into the input field
4. Click "Process Feed" to generate the summary
5. View the generated summary, guest information, and key moments

## 🧠 Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI Models**: 
  - WhisperX for speech-to-text
  - ChatGPT for summarization
- **Dependencies**:
  - feedparser
  - requests
  - beautifulsoup4
  - openai
  - whisperx
  - torch
  - torchaudio

## 📝 Project Structure

```
podcast-ai-summarize/
├── content/              # Podcast content storage
├── .streamlit/           # Streamlit configuration
├── podcast_frontend.py   # Main application file
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Castos](https://castos.com/) for the RSS feed finder tool
- [OpenAI](https://openai.com/) for the AI models
- [WhisperX](https://github.com/m-bain/whisperX) for speech recognition

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

---

Made with ❤️ by [Harshal Gondaliya](https://github.com/harshalgondaliya)

## Project Demo GIF

<div align="center">
   <img src="content/podcast/podcast.gif" width="100%" max-width="800"/>
</div>

## Demo

Here's a breakdown of what's happening in the demo GIF:

1. You open the app and navigate to the main page.
2. Find a podcast RSS feed URL from [Listen Notes](https://www.listennotes.com) or [Castos](https://castos.com/tools/find-podcast-rss-feed/).
3. You input the RSS feed URL of the podcast episode you want to summarize.
4. You click the "Process a Podcast Feed" button.
5. The app downloads the podcast episode in mp3 format.
6. The WhisperX model transcribes the speech to text.
7. The ChatGPT 3.5 Turbo model generates a summary.
8. [5.](#demo), [6.](#demo) and [7.](#demo) are running using GPU in [Modal](https://modal.com) backend.
9. The [Streamlit](https://streamlit.io) frontend displays the summary, episode details, guest info, and highlights.

Feel free to explore the interface and generate summaries for your favorite podcasts!

## Features

- **Automated Summarization:** Using the power of AI, this project can automatically download podcast episodes, transcribe the speech to text, and generate concise summaries.
- **WhisperX for Transcription:** The project employs the WhisperX model to convert spoken words in podcast episodes into text.
- **ChatGPT 3.5 Turbo for Summarization:** The OpenAI ChatGPT 3.5 Turbo model is used to create informative and coherent summaries based on the transcribed text.
- **Frontend with Streamlit:** The summarized content, along with episode details, guest information, and highlights are presented through an interactive and user-friendly Streamlit frontend.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/tekeburak/podcast-summarizer.git
   cd podcast-summarizer

2. Install the required dependencies using pip:
   ```bash
   pip install streamlit modal

3. Deploy backend to Modal:
   ```bash
   modal deploy /content/podcast/podcast_backend.py

4. Run the Streamlit app:
   ```bash
   streamlit run podcast_frontend.py

### Local Usage

1. Access the Streamlit frontend by opening a web browser and navigating to [http://localhost:8501](localhost:8501).
2. On the homepage, you'll find an input field where you can paste the RSS feed URL of the podcast you want to summarize.
3. Click the "Process a Podcast Feed" button to initiate the summarization process.
4. The app will start by downloading the podcast episode in mp3 format and then use the WhisperX model to transcribe the speech to text.
5. Once transcribed, the text data is fed into the ChatGPT 3.5 Turbo model to generate a summary.
6. The summary, along with episode details, guest information, and highlights, will be displayed on the Streamlit interface.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`.
3. Implement your feature and make necessary changes.
4. Commit and push your changes: `git commit -m "Add feature" && git push origin feature-name`.
5. Submit a pull request detailing the changes you've made.