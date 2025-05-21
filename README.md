# 🕌 AI Quran Video Composer

An intelligent Python tool that automatically generates beautiful Quran recitation videos by combining:

- **Precise word-level audio timing** from Tarteel.ai metadata
- **AI-powered background video selection** using OpenAI and Pexels API
- **Synchronized Arabic text and English translations**
- **Professional video composition** with MoviePy

## ✨ Features

- 🎯 **Word-level synchronization** - Each Arabic word appears exactly when recited
- 🤖 **AI-powered backgrounds** - Intelligent selection of appropriate background videos
- 🌍 **Multi-language support** - Arabic text with English translations
- 🎨 **Customizable styling** - Fonts, colors, and layout options
- 📱 **Social media ready** - Optimized 9:16 aspect ratio for mobile platforms
- 🔊 **High-quality audio** - Supports multiple renowned reciters

## 🎬 Example Videos

<!-- Placeholder for example videos - these will be added to the repository -->

### Sample Outputs

- [Surah An-Nisa (4:134) - Mahmoud Khalil Al-Husary](./examples/4-134-134-MAHMOUD_KHALIL_AL_HUSARY.mp4) - "Whoever desires the reward of this world - then with Allah is the reward of this world and the Hereafter"
- [Surah Al-Hijr (15:2-5) - Muhammad Al-Minshawi](./examples/15-2-5-MUHAMMAD_AL_MINSHAWI.mp4) - "The day will come when the disbelievers will certainly wish they had submitted to Allah"
- [Surah Taha (20:124-126) - Mahmoud Khalil Al-Husary](./examples/20-124-126-MAHMOUD_KHALIL_AL_HUSARY.mp4) - "Whoever turns away from My Reminder will certainly have a miserable life"

## 🚀 Quick Start

### Prerequisites

#### 1. Python 3.8+

Make sure you have Python 3.8 or higher installed:

```bash
python --version
```

#### 2. FFmpeg (Required)

FFmpeg is essential for video processing. Install it based on your operating system:

**macOS (using Homebrew):**

```bash
brew install ffmpeg
```

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**

- Follow the detailed guide: [How to Install FFmpeg on Windows](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/)

**Verify FFmpeg installation:**

```bash
ffmpeg -version
```

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/Ai-Quran-Video-Compser.git
cd Ai-Quran-Video-Compser
```

2. **Create a virtual environment (recommended):**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

_Note: The requirements.txt file was automatically generated from the project's imports using `pipreqs` to ensure all necessary dependencies are included._

4. **Set up API keys:**
   - Get a [Pexels API key](https://www.pexels.com/api/) for background videos
   - Get an [OpenAI API key](https://platform.openai.com/api-keys) for AI-powered content selection
   - Update the API keys in the notebook or create environment variables

## 📖 Usage

### Basic Usage with Jupyter Notebook

1. **Start Jupyter:**

```bash
jupyter notebook
```

2. **Open the main notebook:**

   - Navigate to `video_gen.ipynb`
   - Follow the step-by-step instructions in the notebook

3. **Configure your video:**

```python
# Set your parameters
surah_number = 1      # Surah Al-Fatiha
aya_start = 1         # First verse
aya_end = 7           # Last verse
reciter = Reciter.MUHAMMAD_AL_MINSHAWI
```

4. **Run the cells** to generate your video!

### Available Reciters

Currently supported reciters:

- `Reciter.MAHMOUD_KHALIL_AL_HUSARY`
- `Reciter.MUHAMMAD_AL_MINSHAWI`

_More reciters can be added by downloading their metadata files from [Tarteel.ai resources](https://qul.tarteel.ai/resources/recitation). Make sure to select files with the "with segmentation" tag for proper word-level timing data._

## 🏗️ Project Structure

```
Ai-Quran-Video-Compser/
├── video_gen.ipynb              # Main video generation notebook
├── data_processing.ipynb        # Data preprocessing utilities
├── utils.py                     # Core utility functions
├── quran_utils.py              # Quran-specific utilities
├── pexel_utils.py              # Pexels API integration
├── LLM_utils.py                # OpenAI API integration
├── prompts.py                  # AI prompts for video selection
├── data_processing_utils.py    # Audio data processing
├── requirements.txt            # Python dependencies
├── data/                       # Quran text and audio metadata
│   ├── quran/                 # Quran text and translations
│   ├── audio/                 # Reciter timestamp data
│   └── fonts/                 # Arabic fonts
├── temp/                       # Temporary processing files
└── examples/                   # Example output videos (coming soon)
```

## ⚙️ Configuration

### API Keys

Set your API keys in the notebook

```python
# In the notebook
PEXELS_API_KEY = "your_pexels_api_key_here"
OPENAI_API_KEY = "your_openai_api_key_here"
```

### Video Settings

Customize your video output:

```python
# Video dimensions (9:16 aspect ratio)
width = 1080
height = 1920

# Font settings
font_path = "data/fonts/Rakkas-Regular.ttf"
font_size = 80

# Colors
bg_color = (0, 0, 0)      # Black background
text_color = (255, 255, 255)  # White text
```

## 🔧 Advanced Features

### Custom Background Videos

The AI automatically selects appropriate background videos, but you can customize the selection criteria:

```python
# Modify video selection parameters
orientation = VideoOrientation.LANDSCAPE
quality = VideoQuality.HD
selection_method = "best"  # or "random"
```

### Audio Processing

Fine-tune audio synchronization:

```python
# Adjust silence detection parameters
min_silence_len = 100    # milliseconds
silence_thresh = -40     # dB
padding = 50            # milliseconds
```

## ⚠️ Important Notes

### Content Review

**Please carefully review generated videos before use.** Background videos are sourced from external APIs and may occasionally contain content that requires manual verification for Islamic compliance.

### API Costs

- **Pexels API**: Free tier available with rate limits
- **OpenAI API**: Pay-per-use pricing applies

### Performance

- Video generation can take several minutes depending on verse length
- Ensure stable internet connection for API calls
- Consider using SSD storage for faster processing

## 🚀 Potential Enhancements

The following features could significantly expand the project's capabilities:

### 🤖 ML-Powered Audio Segmentation

- **Automatic word detection**: Implement a machine learning model to detect word segments for any Quran audio file

### 🎬 AI Video Generation

- **Custom background creation**: Use video generation models to create contextually

### 🎙️ Extended Reciter Library

- **Popular reciters**: Add support for more renowned reciters

### 🌐 Additional Features

- **Multi-language translations**: Support for more languages (Urdu, French, Spanish, etc.)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Areas for improvement:

- Additional reciter support
- More language translations
- Enhanced video effects
- Performance optimizations
- Better error handling

## 📄 License

This project is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License - see the [LICENSE-CC-BY-NC-ND-4.0.md](LICENSE-CC-BY-NC-ND-4.0.md) file for details.

For commercial use, please contact the project maintainers.

## 🙏 Acknowledgments

- **[Tarteel.ai](https://qul.tarteel.ai/)** for providing precise Quran audio timing data
- **[Pexels](https://www.pexels.com/)** for high-quality background videos
- **OpenAI** for intelligent content selection
- The Muslim developer community for inspiration and feedback

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/Ai-Quran-Video-Compser/issues) page
2. Create a new issue with detailed information
3. Include your Python version, OS, and error messages

---

**Made with ❤️ for the Muslim community**

_"And We have certainly made the Quran easy for remembrance, so is there any who will remember?"_ - Quran 54:17
