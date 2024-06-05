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

dotenv.load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_KEY', "")
MAX_IMAGES = int(os.getenv('MAX_IMAGES', 1))
QUALITY = os.getenv("QUALITY", "standard")
JOB = 1
USE_REVISED = os.getenv('USE_REVISED', 'False').lower() in ('true', '1', 't')

threads = []


async def create_images(prompt: str, number_of_images: int, pic_size: str, job_number: int):
    try:
        if OPENAI_KEY == "":
            print("OpenAI API Key is missing")
            return
        if number_of_images < 1:
            print("Number of images should be greater than 0")
            return

        useRevised = USE_REVISED
        pic_size = pic_size.strip().lower()

        if pic_size in ('s', 'standard'):
            pic_size = "1024x1024"
        elif pic_size in ('l', 'landscape', '16:9', 'land'):
            pic_size = "1792x1024"
        elif pic_size in ('p', 'portrait', '9:16', 'port'):
            pic_size = "1024x1792"
        else:
            pic_size = "1024x1024"

        #print("Submitted Job " + str(job_number))

        async with aiohttp.ClientSession() as session:
            if 1 <= number_of_images <= MAX_IMAGES:
                image_data_list = []

                for i in range(number_of_images):
                    async with session.post('https://api.openai.com/v1/images/generations', headers={'Authorization': 'Bearer ' + OPENAI_KEY},
                                            json={
                                                'model': "dall-e-3",
                                                'prompt': prompt,
                                                'n': 1,
                                                'size': pic_size,
                                                'quality': QUALITY,
                                            }) as resp:
                        if resp.status != 200:
                            if i == 0:
                                print("Unable to get Image")
                            continue

                        response = await resp.json()
                        revised_prompt = response['data'][0]['revised_prompt']
                        image_url = response['data'][0]['url']
                        image_data_list.append((prompt, revised_prompt, image_url))

                        if useRevised:
                            prompt = revised_prompt

                files = []
                for original_prompt, revised_prompt, image_url in image_data_list:
                    async with session.get(image_url) as resp:
                        if resp.status != 200:
                            print("Unable to get image url")
                            continue
                        data = io.BytesIO(await resp.read())
                        random_id = str(random.randrange(1000, 4000))
                        file_name = str(int(time.time())) + random_id + "_" + "D3D" + ".png"

                        # Load the image and add metadata
                        image = Image.open(data)
                        meta = PngImagePlugin.PngInfo()
                        meta.add_text("Original Prompt", original_prompt)
                        meta.add_text("Revised Prompt", revised_prompt)

                        # Save the image with metadata
                        os.makedirs("output", exist_ok=True)
                        image.save(f"output/{file_name}", pnginfo=meta)

                        files.append(file_name)

                print("JOB " + str(job_number) + " Completed \n --->")
            else:
                print('Invalid Number of Images Configured in the config file')
                return

    except Exception as e:
        print(e)
        return


def run_in_thread(loop, prompt, number_of_images, pic_size, job_number):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(create_images(prompt, number_of_images, pic_size, job_number))


def main():
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
        print("Job " + str(JOB) + " is now running.")
        JOB += 1
    else:
        while True:
            prompt = input("Enter the prompt for the image generation (or type /q, quit, exit to stop): ")
            if prompt.lower() in ['/q', 'quit', 'exit']:
                print("Exiting...")
                break
            number_of_images = int(input("Enter the number of images to generate: "))
            pic_size = input("Enter the size of the images (s for standard, l for landscape, p for portrait): ")

            loop = asyncio.new_event_loop()
            thread = threading.Thread(target=run_in_thread, args=(loop, prompt, number_of_images, pic_size, JOB))
            thread.start()
            threads.append(thread)
            print("Job " + str(JOB) + " is now running.")
            JOB += 1

    # Wait for all threads to complete before exiting
    for thread in threads:
        thread.join()
    print("All jobs completed. Exiting...")


if __name__ == "__main__":
    main()
