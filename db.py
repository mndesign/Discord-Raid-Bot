import settings
import pymysql
import datetime

class MySql():
    def __init__(self) -> None:
        self.now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.sqldb = pymysql.connect( user=settings.SQL_USER, passwd=settings.SQL_PW, host=settings.SQL_HOST, port=3306, db=settings.SQL_DB )
            self.sqldb.autocommit(True)
        except Exception as e:
            print(f"{self.now} - DB - {str(e)}")

    def query(self, query):
        try:
            if self.sqldb is None:
                self.__init__()
            else:
                self.sqldb.ping(True)
                cur = self.sqldb.cursor()
                cur.execute(query)
                res = cur.fetchall()
                cur.close()
                return res
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.sqldb.rollback()

    def playerStats(self):
        query = f"SELECT username,raids_joined, raids_hosted, SUM(raids_joined) + SUM(raids_hosted) AS raidTotal FROM users GROUP by id ORDER BY raidTotal DESC LIMIT 10"
        result = self.query(query)
        return result
        

    def groupStats(self):
       query = f"SELECT channel, count(channel) as raid_started from stats group by channel ORDER BY raid_started DESC;"
       result = self.query(query)
       return result

    def pokemonStats(self, query):
        query = f"SELECT channel, pokemon, count(pokemon) as number from stats WHERE pokemon = '{query}' group by channel ORDER BY number DESC LIMIT 10;"
        result = self.query(query)
        return result
    
    def ownStats(self, userid):
        query = f"SELECT * FROM users WHERE id = '{userid}'"
        result = self.query(query)
        return result

    def getProfile(self, user_id):
        query = f"SELECT ingame_name, trainer_code, id FROM users WHERE id={user_id}"
        result = self.query(query)
        return result

    def getChannel(self, channelID):
        query = f"SELECT * FROM channel WHERE id = '{channelID}'"
        result = self.query(query)
        return result

    def addRaidStat(self, user_id, channel, pokemon):
        query = f"INSERT INTO `stats` (`id`, `channel`, `user`, `pokemon`, `raid_started`, `date`, `raid_id`) VALUES ('', '{channel}', '{user_id}', '{pokemon}', '1', '{self.now}', 'Discord')"
        result = self.query(query)
        return result

    def startRaid(self, participants):
        i=1
        sqlOrder = ""
        sqlQuery = ""
        sqlUpdate = ""

        for single in participants:
            sqlQuery += f"`id` = '{str(single)}' OR "
            sqlOrder += f"WHEN '{str(single)}' THEN {str(i)} "
            sqlUpdate += f"'{single}',"
            i += 1

        sqlQuery = sqlQuery[:-4]
        sqlOrder = sqlOrder[:-1]
        sqlUpdate = sqlUpdate[:-1]

        self.query(f"UPDATE users SET raids_joined = raids_joined +1 WHERE id IN ({sqlUpdate})")
        embedParticipants = self.query(f"SELECT id, ingame_name FROM users WHERE {sqlQuery} ORDER BY CASE id {str(sqlOrder)} END;")
        return embedParticipants
    
    def profileSetup(self, userid, display_name, ign, trainercode, level, country, team):  
        query = f"INSERT INTO users (`id`, `username`, `ingame_name`, `trainer_code`, `level`, `country`, `team`, `raids_joined`, `raids_hosted`) VALUES ('{userid}','{display_name}','{ign}','{trainercode}','{level}','{country}','{team}','0','0')"
        result = self.query(query)
        print(f"{self.now} - Profile created - {userid}")
        return result
    
    def profileChange(self, queryString, userid):
        query = f"UPDATE `users` SET {queryString[:-2]} WHERE `id` = '{userid}'"
        result = self.query(query)
        print(f"{self.now} - Profile changed - {userid}")
        return result
    
    def deleteProfile(self, user_id):
        query = f"DELETE FROM users WHERE id={user_id}"
        result = self.query(query)
        print(f"{self.now} - Profile deleted - {user_id}")
        return result