import os 
import requests as r 

def get_response_for(keyword,photo_per_page):
    url = f"https://unsplash.com/napi/search/photos?query={keyword}&per_page={photo_per_page}&xp=plus-freq%3Aone_in_four"
    resp = r.get(url)

    if resp.status_code == 200 :
        return resp.json()
    
def get_image_url(data):
    results = data["results"]
    img_url = [x["urls"]["raw"] for x in results if x["premium"] is False ]
    img_url = [x.split("?")[0] for x in img_url]

    return img_url

def download(img_url , max_downloads , dest_dir="images" , tags = ""):
    successfully_downloaded = 0

    for url in img_url:
        if successfully_downloaded < max_downloads:
            resp = r.get(url)
            file_name = url.split("/")[-1]

            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            
            with open(f"{dest_dir}/{tags}{file_name}.jpeg", "wb") as f :
                f.write(resp.content)
                successfully_downloaded += 1

        else:
            break

    return successfully_downloaded

def scrape(keyword,num_of_results):
    success_count = 0

    while success_count < num_of_results:
        data = get_response_for(keyword, photo_per_page=20)
        max_downloads = num_of_results - success_count

        if data:
            img_url = get_image_url(data)
            success_download = download(img_url , max_downloads , tags=keyword )
            success_count += success_download
            

        else:
            print("Error: no data returned")
            break

if __name__ == "__main__" :

    scrape("football",10)





    

