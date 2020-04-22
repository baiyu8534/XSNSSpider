import requests

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    'referer': "https://www.xsnvshen.com/album"
}
# 22204/32662
response = requests.get("https://img.xsnvshen.com/album/22204/32662/030.jpg", headers=headers)

with open('./test.jpg', "wb") as f:
    f.write(response.content)

# https://www.xsnvshen.com/album/hd/?p=1
