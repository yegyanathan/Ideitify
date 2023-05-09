import os
import argparse
import concurrent.futures

from GoogleImageScraper import GoogleImageScraper
from patch import webdriver_executable

parser = argparse.ArgumentParser(description='Google Image Scraper')
parser.add_argument('--folder_name', type=str, help='Folder to save the images')
parser.add_argument('--query', type=str, help='query string')
parser.add_argument('--num_samples', type=int, help='Number of images to download')

args = parser.parse_args()


def worker_thread(search_key):
    image_scraper = GoogleImageScraper(
        webdriver_path, 
        image_path, 
        search_key, 
        number_of_images, 
        headless, 
        min_resolution, 
        max_resolution, 
        max_missed)
    image_urls = image_scraper.find_image_urls()
    image_scraper.save_images(image_urls, keep_filenames)

    del image_scraper

if __name__ == "__main__":

    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', webdriver_executable()))
    image_path = os.path.join("images", args.folder_name)

    search_keys = list(set([args.query]))

    number_of_images = args.num_samples               
    headless = True                     
    min_resolution = (0, 0)             
    max_resolution = (9999, 9999)       
    max_missed = 10                     
    number_of_workers = 1               
    keep_filenames = False              


    with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executor:
        executor.map(worker_thread, search_keys)
