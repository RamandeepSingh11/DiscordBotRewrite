import youtube_dl
import asyncio
youtube_dl.utils.bug_reports_message = lambda: ''   #Suppressing Noise Console From YT_Dl
class Song:
    def __init__(self,url,track,artist,YTurl):
        self.track=track
        self.url=url
        self.artist=artist
        self.YTurl=YTurl
    def __str__(self):
        return 'Track: {}, Download URL: {} \n Artist: {}, URL: {}'.format(self.track,self.url[:5],self.artist,self.YTurl)
class YT:
    @staticmethod
    def InsertData(data: list,DataBase,guildID: int,url: str):
        if 'entries' in data:
            for i in data['entries']:
                if(not i.get('url',False)):continue
                DataBase.insert(guildID,i.get('track',i.get('title','Unknown')),i.get('artist'),i.get('url'),i.get('webpage_url',url))
        else:
            DataBase.insert(guildID,data.get('track',data.get('title','Unknown')),data.get('artist'),data.get('url'),data.get('webpage_url',url))
    @staticmethod
    async def grab(url: str,DataBase,guildID: int,opts: dict,loop=None):
        client=youtube_dl.YoutubeDL(opts)
        if(not loop):loop=asyncio.get_event_loop()
        try:
            data=await loop.run_in_executor(None,lambda: client.extract_info(url,download=False))
        except:
            return False
        YT.InsertData(data,DataBase,guildID,url)
        if(len(data)==0):
            return None
        if 'entries' in data:
            return len(data.get('entries'))
        return 1
if __name__=='__main__':
    print('nothing')