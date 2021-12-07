import mysql.connector
import sqlite3
db = mysql.connector.connect(
    host="45.77.229.75",
    user="sneaky",
    passwd="Dominus7206!",
    database="coolart"
)


cur = db.cursor()
con = sqlite3.connect("resources/Databases/database.db")
litecur = con.cursor()
# cur.execute("CREATE TABLE gallery (messageId bigint, memberId bigint, upvotes integer);")
# cur.execute("CREATE TABLE artLevels (member bigint, exp integer, artAmount integer, rank integer);")
# cur.execute("CREATE TABLE upvotes (memberId bigint, postMessageId bigint);")
# cur.execute("CREATE TABLE announcements (title text, content text, mentions text, time text, showIcon boolean, showAuthor boolean, authorId bigint, channelId bigint);")
# cur.execute("CREATE TABLE refferals (memberId integer, refcode integer);")
# cur.execute("CREATE TABLE applications (appMessageId bigint, memberId bigint);")

litecur.execute("SELECT * FROM artLevels")

for record in litecur.fetchall():
    print(record)
    cur.execute("INSERT INTO artLevels VALUES (%s,%s,%s,%s)", record)
    
db.commit()
db.close()

