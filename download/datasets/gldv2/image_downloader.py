'''Downloads an image from an url and saves it locally'''


## Importing Necessary Modules
import requests  # to get image from the web
import shutil  # to save it locally



## Set up the image URL and filename
def download_image(image_url, filename="../images/image.jpeg"):

    # Specify 'User-Agent' by typing 'about:' on chrome browser
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}

    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, headers=headers, stream=True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print('Image sucessfully Downloaded: ', filename)
    else:
        print('Image Couldn\'t be retreived')

