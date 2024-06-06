# Dall-E-3_Desktop_Client
## Image Generation with OpenAI Dall-e-3 API

This script allows you to generate images using OpenAI's DALL-E 3 model via a command-line interface. The script supports asynchronous image creation, handles user inputs, and saves images with metadata.

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
git clone https://github.com/itachi1621/Dall-E-3_Desktop_Client.git
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
## Output
Images are stored in the output folder of the directory

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

## OpenAI Dall E 3 Pricing
![Screenshot from 2024-06-06 14-25-22](https://github.com/itachi1621/Dall-E-3_Desktop_Client/assets/62318474/4610c819-ed3d-4c64-a44a-9ac0b4391727)


## Sample Images

<p align="center">
  <img src="https://github.com/itachi1621/Dall-E-3_Desktop_Client/assets/62318474/28f0a052-4c2c-4217-8a7d-7ad2d015583b" width="400">
    <img src="https://github.com/itachi1621/Dall-E-3_Desktop_Client/assets/62318474/a55cc793-da84-43c3-b409-be11f6089e18" width="400">
  <img src="https://github.com/itachi1621/Dall-E-3_Desktop_Client/assets/62318474/cb3d27b7-7962-491f-8fda-20fe1f691002" width="300">
    <img src="https://github.com/itachi1621/Dall-E-3_Desktop_Client/assets/62318474/a4ed6a65-8f01-436e-b588-1e966ccd9725" width="300">
</p>


## Contributing
Feel free to open issues or submit pull requests if you have suggestions or improvements.

## License
This project is licensed under the MIT License.
