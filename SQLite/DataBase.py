import sqlite3
from discord.ext import commands
class DataBase():
    def __init__(self):
        self.conn=sqlite3.connect(r'SQLite/DataBase.db')
    def addGuild(self,guildId: int):
        self.conn.execute("""CREATE TABLE "{}"
        (SongName TEXT,
        Artist TEXT,
        SongURL TEXT,
        YTurl TEXT);
        """.format(guildId))
        self.conn.execute("""INSERT INTO GUILD
        VALUES ("{}",{},{},{},{},{})
        """.format(guildId,-1,0,0,0,0))
        self.conn.commit()
    def insert(self,guild_id: int,songname: str,artist: str,url: str,YTurl: str):
        try:
            self.conn.execute("""INSERT INTO "{}" 
            VALUES ("{}","{}","{}","{}")""".format(guild_id,songname,artist,url,YTurl))
            self.conn.execute('UPDATE GUILD SET Total=(Total+1) WHERE GuildID="{}"'.format(guild_id))
            self.conn.commit()
            return True
        except sqlite3.OperationalError:
            self.addGuild(guild_id)
            self.insert(guild_id,songname,artist,url,YTurl)
            return True
        except Exception as e:
            print(type(e))
            exit()
    def getGuilds(self):
        return self.conn.execute('SELECT * FROM GUILD')
    # Debugging Command
    def show(self,guildId: int):
        for i in self.conn.execute('SELECT * FROM "{}"'.format(guildId)):
            print(i[0],i[1],i[3])
            print(i[2])
    def show_guild(self,guildId: int):
        print(self.conn.execute('SELECT * FROM GUILD WHERE GuildID="{}"'.format(guildId)).fetchone())
    def show_database(self):
        for i in self.conn.execute("""SELECT sql FROM sqlite_master WHERE type = 'table'"""):
            print(i)
    def set_Loop(self,guild_id: int):
        self.conn.execute('UPDATE GUILD set Loop=(Loop+1)%3 WHERE GuildID="{}"'.format(guild_id))
        self.conn.commit()
        return self.conn.execute('SELECT Loop FROM GUILD WHERE GuildID="{}"'.format(guild_id)).fetchone()[0]
    def set_shuffle(self,guild_id: int):
        self.conn.execute('UPDATE GUILD set Shuffle=(Shuffle+1)%2 WHERE GuildID="{}"'.format(guild_id))
        self.conn.commit()
        return self.conn.execute("""SELECT Shuffle FROM GUILD WHERE GuildID="{}"
        """.format(guild_id)).fetchone()[0]

    def set_allDay(self,guildID: int):
        self.conn.execute('UPDATE GUILD SET ALLDAY=(ALLDAY+1)%2 WHERE GuildID="{}"'.format(guildID))
        self.conn.commit()
        return self.conn.execute("""SELECT ALLDAY FROM GUILD WHERE GuildID="{}" """.format(guildID)).fetchone()[0]

    def get_song(self,guildid: int):
        _,Position,Total,Shuffle,Loop,dump=self.conn.execute('SELECT * FROM GUILD WHERE GuildID="{}"'.format(guildid)).fetchone()
        if(Position==(Total-1) and Shuffle==0):
            if(Loop==2):Position=-1
            else:
                self.removeQueue(guildid)
                return None
        Position+=1
        self.set_position(guildid,Position)
        if(Loop==1):
            return self.conn.execute('SELECT * FROM "{}" LIMIT 1 OFFSET {}'.format(guildid,Position))
        if(Shuffle):
            return self.get_random_song(guildid)
        return self.conn.execute('SELECT * FROM "{}" LIMIT 1 OFFSET {}'.format(guildid,Position)).fetchone()

    def set_position(self,guild_id: int,Position: int):
        self.conn.execute('UPDATE GUILD set Position={} WHERE GuildID="{}"'.format(Position,guild_id))
        self.conn.commit()
    def get_random_song(self,guildid: int):
        return self.conn.execute("""SELECT * FROM "{}" ORDER 
        BY Random() Limit 1 ;""".format(guildid)).fetchone()
    def remove(self,guildid: int,songname: str,artist: str):
        self.conn.execute("""DELETE FROM "{}"
        WHERE SongName="{}" AND Artist="{}"
        """.format(guildid,songname,artist))
        self.conn.commit()
    def getSimilarSongs(self,guildID: int,query:str):
        data=self.conn.execute("""SELECT * FROM "{}"
        LIMIT 1
        WHERE SongName LIKE %{}%
        """.format(guildID,query)).fetchone()
        return data
    def removeQueue(self,guildid: int):
        self.conn.execute("""DELETE FROM "{}" """.format(guildid))
        self.conn.execute("""UPDATE GUILD
        SET Total=0,Position=-1,Shuffle=0,Loop=0
        WHERE GuildID='{}'""".format(guildid))
        self.conn.commit()
    def close(self):
        self.conn.close()
    def __del__(self):
        self.close()
if __name__=='__main__':
    a=DataBase()
    a.conn.execute("""CREATE TABLE GUILD
    (GuildID TEXT,
    Position INT,
    Total INT,
    Shuffle INT,
    Loop INT,
    ALLDAY INT)""")
    # try:
    #     a=DataBase()
    #     a.conn.execute("""CREATE TABLE GUILD
    #     (GuildID TEXT,
    #     Position INT,
    #     Total INT,
    #     Shuffle INT,
    #     Loop INT)""")
    #     a.insert(12,'Boom','TS','WWW','WWW')
    #     a.insert(12,'Soom','SM','WWW','SJS')
    #     a.insert(12,'TOOM','SJJS','WWW','JSJS')
    #     a.insert(43,'Soom','SM','WWW','SJS')
    #     a.insert(43,'TOOM','SJJS','WWW','JSJS')
    #     a.insert(69,'DJJD','SJD','JJJ','JJSJ')
    #     a.show_guild(12)
    #     a.show(12)
    #     a.show(43)
    #     a.show(69)
    #     a.set_shuffle(12)
    #     a.show_guild(12)
    #     a.set_Loop(12)
    #     a.show_guild(12)
    #     a.set_shuffle(12)
    #     a.set_Loop(12)
    #     a.show_guild(12)
    #     print(a.get_song(12))
    #     a.show_guild(12)
    #     a.show_guild(69)
    #     a.show_guild(43)
    # except Exception as e:
    #     print(e)
    #     os.remove('DataBase.db')
    # a.removeQueue(731096094242635885)
    # a.insert(731096094242635885,'I know Something','Lin','WWW','WWW')
    # print(a.get_song(731096094242635885))
    # print(a.get_current_song(731096094242635885))
    # a.show(731096094242635885)
    # a.show_guild(731096094242635885)
    # a.show(731096094242635885)
    # print(a.get_song(731096094242635885))