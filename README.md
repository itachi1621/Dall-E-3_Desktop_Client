# Dall-E-3_Desktop_Client
## Image Generation with OpenAI Dall-e-3 API

This project allows you to generate images using OpenAI's DALL-E model via a command-line interface. The script supports asynchronous image creation, handles user inputs, and saves images with metadata.

## Features
- Asynchronous image generation using aiohttp and asyncio.
- Supports standard, landscape, and portrait image sizes.
- Saves generated images with metadata (original and revised prompts).
- Handles multiple jobs concurrently with threading.
- Configurable via environment variables.

## Prerequisites
- Python 3.10+
- OpenAI API Key

Required Python packages: aiohttp, python-dotenv, Pillow, argparse, asyncio

## Installation
1. Clone the repository:

```bash
git clone https://github.com/yourusername/image-generation-openai.git
cd DAll-E-3-Desktop_Client
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```
3. Set up your environment variables. Create a .env file in the project directory and add your OpenAI API key:

```env
OPENAI_KEY=your_openai_api_key
MAX_IMAGES=5
QUALITY=standard
USE_REVISED=False
```

## Usage
Run the script with the following command:

```bash
python Dall-E-3_Desktop_Client.py
```
### Command-Line Arguments
You can also provide the prompt, number of images, and image size as command-line arguments:
**Note Only *prompt* is required other arguments are optional

```bash
python Dall-E-3_Desktop_Client.py --prompt "A futuristic cityscape" --number_of_images 3 --pic_size "l"
```

Bring up help info
```
python Dall-E-3_Desktop_Client.py --help
```
### Interactive Mode

If no command-line arguments are provided, the script will run in interactive mode, prompting you for the necessary inputs.

#### Environment Variables
- OPENAI_KEY: Your OpenAI API key.
- MAX_IMAGES: Maximum possible number of images to generate per job. e.g only allow the user to generate up to 2 images (May also be dependent on your OpenAI Tier Limits)
- QUALITY: Image quality setting. use `standard` or `HD`
- USE_REVISED: Use the revised prompt returned by the API for subsequent image generation (True/False). By Default Dalle will generate a new prompt per image and will give varrying results.

## Troubleshooting
Ensure you have a valid OpenAI API key set in your .env file.
Check that the required Python packages are installed.
Verify that the environment variables are correctly set.

## Contributing
Feel free to open issues or submit pull requests if you have suggestions or improvements.

## License
This project is licensed under the MIT License.
