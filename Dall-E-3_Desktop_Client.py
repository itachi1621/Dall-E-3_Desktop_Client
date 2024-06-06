import aiohttp
import dotenv
import os
import random
import time
import io
import asyncio
import threading
from PIL import Image, PngImagePlugin
import argparse
import signal
import sys

dotenv.load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_KEY', "")
MAX_IMAGES = int(os.getenv('MAX_IMAGES', 1))
QUALITY = os.getenv("QUALITY", "standard")
JOB = 1
USE_REVISED = os.getenv('USE_REVISED', 'False').lower() in ('true', '1', 't')

threads = []
stop_event = threading.Event()


async def create_images(prompt: str, number_of_images: int, pic_size: str, job_number: int):
    try:
        if OPENAI_KEY == "":
            print("OpenAI API Key is missing")
            return
        if number_of_images < 1:
            print("Number of images should be greater than 0")
            return

        pic_size = pic_size.strip().lower()

        if pic_size in ('s', 'standard'):
            pic_size = "1024x1024"
        elif pic_size in ('l', 'landscape', '16:9', 'land'):
            pic_size = "1792x1024"
        elif pic_size in ('p', 'portrait', '9:16', 'port'):
            pic_size = "1024x1792"
        else:
            pic_size = "1024x1024"


        async with aiohttp.ClientSession() as session:
            if 1 <= number_of_images <= MAX_IMAGES:
                image_data_list = []

                for _ in range(number_of_images):
                    async with session.post('https://api.openai.com/v1/images/generations', headers={'Authorization': 'Bearer ' + OPENAI_KEY},
                                            json={
                                                'model': "dall-e-3",
                                                'prompt': prompt,
                                                'n': 1,
                                                'size': pic_size,
                                                'quality': QUALITY,
                                            }) as resp:
                        if resp.status != 200:
                            if not image_data_list:
                                print("Unable to get Image")
                            continue

                        response = await resp.json()
                        revised_prompt = response['data'][0]['revised_prompt']
                        image_url = response['data'][0]['url']
                        image_data_list.append((prompt, revised_prompt, image_url))

                        if USE_REVISED:
                            prompt = revised_prompt

                files = []
                for original_prompt, revised_prompt, image_url in image_data_list:
                    async with session.get(image_url) as resp:
                        if resp.status != 200:
                            print("Unable to get image url")
                            continue
                        data = io.BytesIO(await resp.read())
                        random_id = str(random.randrange(1000, 4000))
                        file_name = f"{int(time.time())}{random_id}_D3D.png"

                        # Load the image and add metadata
                        image = Image.open(data)
                        meta = PngImagePlugin.PngInfo()
                        meta.add_text("Original Prompt", original_prompt)
                        meta.add_text("Revised Prompt", revised_prompt)

                        # Save the image with metadata
                        os.makedirs("output", exist_ok=True)
                        image.save(f"output/{file_name}", pnginfo=meta)

                        files.append(file_name)

                print(f"\nJOB {job_number} Completed\n\nContinue Input--->")
            else:
                print('Invalid Number of Images Configured in the config file')
    except Exception as e:
        print(f"Error in creating images: {e}")


def run_in_thread(loop, prompt, number_of_images, pic_size, job_number):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(create_images(prompt, number_of_images, pic_size, job_number))


def get_number_of_images():
    while True:
        try:
            numOfImgs = input("Enter number of images to generate leave blank for default of 1: ")
            if numOfImgs == "":
                return 1
            if numOfImgs.isdigit():
                return int(numOfImgs)
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"Error getting number of images: {e}")


def get_pic_size():
    while True:
        try:
            pic_size = input("Enter the size of the images (s for standard, l for landscape, p for portrait) leave blank for standard: ").strip().lower()
            if pic_size in ('', 's', 'standard', 'l', '16:9', 'p', 'portrait', '9:16'):
                return pic_size if pic_size else 's'
            print("Invalid input. Please enter a valid size.")
        except Exception as e:
            print(f"Error getting picture size: {e}")


def get_prompt():
    while True:
        try:
            prompt = input("Enter the prompt for the image generation (or type /q, quit, exit to stop): ").strip()
            if prompt:
                if prompt.lower() in ['/q', 'quit', 'exit', 'q']:
                    print("Exiting...")
                    return None
                return prompt
            print("Prompt cannot be empty. Please enter a prompt.")
        except Exception as e:
            print(f"Error getting prompt: {e}")


def signal_handler(sig, frame):
    print('Exiting...')
    stop_event.set()
    for thread in threads:
        thread.join()
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description='Generate images using OpenAI API.')
    parser.add_argument('--prompt', type=str, help='The prompt for the image generation')
    parser.add_argument('--number_of_images', type=int, default=1, help='Number of images to generate')
    parser.add_argument('--pic_size', type=str, default='s', help='Size of the images (s for standard, l for landscape, p for portrait)')

    args = parser.parse_args()
    global JOB

    if args.prompt:
        loop = asyncio.get_event_loop()
        thread = threading.Thread(target=run_in_thread, args=(loop, args.prompt, args.number_of_images, args.pic_size, JOB))
        thread.start()
        threads.append(thread)
        print(f"Job {JOB} is now running in the background.")
        JOB += 1
    else:
        while not stop_event.is_set():
            prompt = get_prompt()
            if not prompt:
                break

            number_of_images = get_number_of_images()
            pic_size = get_pic_size()

            loop = asyncio.new_event_loop()
            thread = threading.Thread(target=run_in_thread, args=(loop, prompt, number_of_images, pic_size, JOB))
            thread.start()
            threads.append(thread)
            print(f"Job {JOB} is now running in the background.")
            JOB += 1

    # Wait for all threads to complete before exiting
    for thread in threads:
        thread.join()
    print("All jobs completed. Exiting...")


if __name__ == "__main__":
    main()
