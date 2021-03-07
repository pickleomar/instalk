import os ,requests,json,datetime

def cookie():
    cookie = requests.cookies.RequestsCookieJar()
    sess = open('session_id_goes_here.txt', 'r').read()
    cookie.set("sessionid", "%s" % str(sess), domain='.instagram.com', path='/')
    return cookie

url_user =''
def downloader(link, name,path):
    type = ''
    if link.find('jpg') != -1:
        type = 'jpg'
    elif link.find('mp4') != -1:
        type = 'mp4'
    r = requests.get(link)
    c=name + '.' + type
    with open(path+c, 'wb+') as f:
        f.write(r.content)


def get_id():    #given user id "id_" return id
    id_ = url_user
    r = requests.get('https://www.instagram.com/%s/?__a=1'%id_,cookies=cookie()).text
    return json.loads(r)["graphql"]["user"]['id']

##############################STORIES#################################

def get_story_links(value):   #value=0 for photos   #value=1 for vids
    api = "https://i.instagram.com/api/v1/feed/reels_media/?reel_ids=%d" % int(get_id())
    videos = []
    photos = []
    closefriends=[]
    req = requests.get(api, cookies=cookie(), headers=headers).text
    try:
      story_lenght=len(json.loads(req)['reels_media'][0]['items'])
      for n in json.loads(req)['reels_media'][0]['items']:
           if str(n).find('video_versions') == -1:
               photos.append(n['image_versions2']['candidates'][0]['url'])
               if str(n).find('audience') >= 0:
                   closefriends.append(n['image_versions2']['candidates'][0]['url'])
           elif str(n).find('video_versions') >= 0:
               videos.append(n['video_versions'][0]['url'])
               if str(n).find('audience') >= 0:
                   closefriends.append(n['video_versions'][0]['url'])


    except:
        print('No stories were found in the past 24h')

    if value==0:
        return photos
    elif value == 1:
        return videos
    elif value == 2:
        return closefriends

def all_story_media_download(media_type):
    count=0
    if media_type== 'mp4':
        media=get_story_links(1)
    elif media_type == 'closefriends':
        media=get_story_links(2)
    else:
        media=get_story_links(0)
    time=datetime.datetime.now().strftime("%d_%m_%Y@%H:%M:%S")
    for v in media:
       file=open('stories_log.txt',"a")
       file.write('[%s]:'%time+v+'\n')
       file.close()
    for m in media:
        name = datetime.datetime.now().strftime("%d_%m_%Y@%H_%M_%S")
        if media_type == 'mp4':
            name+='_vid'
            downloader(m, name, os.getcwd()+"\\stories\\")
        elif media_type =='closefriends':
            name+='_closefriend'
            downloader(m, name, os.getcwd()+"\\closefrnds\\")
        else:
            name+='_pic'
            downloader(m, name, os.getcwd()+"\\stories\\")

headers = {
    'x-ig-app-id': '936619743392459',
    'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

print(get_id())
all_story_media_download('mp4')
all_story_media_download('jpg')
all_story_media_download('closefriends')