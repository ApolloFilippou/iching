# I Ching Oracle

This is a minimalist command-line I Ching divination tool that uses Google's Gemini API to deliver poetic oracle responses. It simulates traditional hexagram generation with coin tosses and interprets the result using an AI oracle trained in the voice of an ancient sage.

## What It Does
- Simulates hexagram casting based on classic I Ching coin tosses.
- Determines primary and (if applicable) secondary hexagrams and changing lines.
- Uses the Gemini 2.5 Flash API to generate a styled oracle interpretation of the hexagram, in the voice of a wise diviner.
- Outputs traditional hexagram line diagrams and trigram names.

## Setup
### 1. Install dependencies
- You’ll need Python 3.7+ and the google-genai package:

```bash
pip install google-genai
```

### 2. Get a Gemini API key
- Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to create an API key.
- Replace the placeholder API key in iching.py with your actual key:

```python
client = genai.Client(api_key='YOUR_API_KEY_HERE')
```

### 3. Usage
- Run the script from the command line:

```bash
python iching.py
```

- You'll be prompted to ask a question. The program will:
  - Cast a hexagram (via random coin toss simulation)
  - Display the hexagram and any resulting changes
  - Send the data to Gemini for interpretation
  - Output the Oracle’s response in an ancient, poetic tone

## Limitations
Requires a valid Gemini API key.

## License
This project is released under the MIT License.
