import FileMgmt as f
import FloorNoiseDB as db
import random

def writeUserData(cursor):

    file = open('Users.txt', 'r')
    lines = file.readlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        user = line.split(',')
        
        query = '''
                INSERT INTO User (FirstName, LastName)
                VALUES(?, ?)
                '''

        cursor.execute(query, user)

def writeManufacturerData(cursor):

    file = open('Manufacturers.txt', 'r')
    lines = file.readlines()

    for line in lines:

        line = line.strip()
        
        if not line:
            continue

        query = '''
                INSERT INTO Manufacturer(ManuName)
                VALUES(?)
                '''

        cursor.execute(query, [line])

def writePedalData(cursor):

    file = open('Pedals.txt', 'r')
    lines = file.readlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        pedal_details = line.split(',')
        
        query = '''
                INSERT INTO Pedal (ManuID, PedalName, Description, IsStereoIn,
                                   IsStereoOut, HasMIDI, HasTapTempo,
                                   HasExpressionJack, VoltageMin, VoltageMax, mAmps)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''

        cursor.execute(query, pedal_details)

def writeEffectTypeData(cursor):

    file = open('EffectType.txt', 'r')
    lines= file.readlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        query = '''
                INSERT INTO EffectType(EffectName)
                VALUES(?)
                '''

        cursor.execute(query, [line])

def writePedalEffectData(cursor):

    file = open('PedalEffect.txt', 'r')
    lines = file.readlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        details = line.split(',')
        
        query = '''
                INSERT INTO PedalEffect (PedalID, EffectID)
                VALUES(?, ?)
                '''

        cursor.execute(query, details)

def writeGenreTagData(cursor):

    file = open('GenreTags.txt', 'r')
    lines = file.readlines()

    for line in lines:

        line = line.strip()
        
        if not line:
            continue

        query = '''
                INSERT INTO GenreTag(GenreName)
                VALUES(?)
                '''

        cursor.execute(query, [line])

def writePedalOwnerData(cursor):

    cursor.execute('SELECT UserID FROM User')
    users = cursor.fetchall()

    cursor.execute('SELECT PedalID FROM Pedal')
    pedals = cursor.fetchall()

    pedalCount = len(pedals)

    #Assigns a random number of random pedals to each user
    for userID in users:

        userPedalCount = random.randint(1,pedalCount)
        
        for i in range(userPedalCount):

            pedalIndex = random.randint(0, (pedalCount-1))

            query = '''
                    INSERT INTO PedalOwner(UserID, PedalID)
                    VALUES(?, ?)
                    '''

            cursor.execute(query, (userID[0], pedals[pedalIndex][0]))

def writeUserBoardData(cursor):

    cursor.execute('SELECT * FROM User')
    users = cursor.fetchall()

    cursor.execute('SELECT GenreID FROM GenreTag')
    genres = cursor.fetchall()
    genreCount = len(genres)
    
    for user in users:
        
        query = 'SELECT OwnerID FROM PedalOwner WHERE UserID=?'
        cursor.execute(query, str(user[0]))

        pedals = cursor.fetchall()
        pedalCount = len(pedals)
        
        #User random creates 1-5 boards
        boardCount = random.randint(1, 5)

        for i in range(boardCount):

            genreID = genres[random.randint(0, genreCount-1)][0]
            boardName = user[1] + '\'s Board #' + str(i+1)
            
            query = '''
                    INSERT INTO UserBoard(UserID, GenreID, BoardName)
                    VALUES(?, ?, ?)
                    '''
            
            cursor.execute(query, (user[0], genreID, boardName))

def writePedalBoardData(cursor):

    cursor.execute('SELECT * FROM UserBoard')
    boards = cursor.fetchall()

    for board in boards:

        query = '''
                SELECT OwnerID
                FROM PedalOwner
                WHERE UserID=?
                '''

        userID = str(board[1])
        cursor.execute(query, userID)
        
        pedals = cursor.fetchall()
        pedalCount = len(pedals)

        boardPedalCount = random.randint(1, pedalCount)

        for i in range(boardPedalCount):

            pedalIndex = random.randint(0, pedalCount-1)

            query = '''
                    INSERT INTO PedalBoard(UserBoardID, OwnerID)
                    VALUES(?, ?)
                    '''

            cursor.execute(query, (board[0], pedals[pedalIndex][0]))
            
def writeSampleData(connection):

    cursor = connection.cursor()

    #Checks for User Data
    cursor.execute('''
                   SELECT *
                   FROM User
                   ''')

    entry = cursor.fetchone()

    if entry is None:
        writeUserData(cursor)
        connection.commit()
        
    #Checks for Manufacturer Data
    cursor.execute('''
                   SELECT *
                   FROM Manufacturer
                   ''')

    entry = cursor.fetchone()

    if entry is None:
        writeManufacturerData(cursor)
        connection.commit()

    #Checks for Pedal Data
    cursor.execute('''
                   SELECT *
                   FROM Pedal
                   ''')

    entry = cursor.fetchone()

    if entry is None:
        writePedalData(cursor)
        connection.commit()

    #Checks for Effect Type Data
    cursor.execute('''
                   SELECT *
                   FROM EffectType
                   ''')

    entry = cursor.fetchone()

    if entry is None:
        writeEffectTypeData(cursor)
        connection.commit()

    #Checks for PedalEffect Data
    cursor.execute('''
                   SELECT *
                   FROM PedalEffect
                   ''')

    entry = cursor.fetchone()

    if entry is None:
        writePedalEffectData(cursor)
        connection.commit()

    #Checks for Genre Data
    cursor.execute('''
                   SELECT *
                   FROM GenreTag
                   ''')

    entry = cursor.fetchone()

    if entry is None:
        writeGenreTagData(cursor)
        connection.commit()

    #Checks for PedalOwner Data
    cursor.execute('''
                   SELECT *
                   FROM PedalOwner
                   ''')

    entry = cursor.fetchone()

    if entry is None:
        writePedalOwnerData(cursor)
        connection.commit()

    #Checks for UserBoard Data
    cursor.execute('''
                   SELECT *
                   FROM UserBoard
                   ''')

    entry = cursor.fetchone()

    if entry is None:
        writeUserBoardData(cursor)
        connection.commit()
        
    #Checks for PedalBoard Data
    cursor.execute('''
                   SELECT *
                   FROM PedalBoard
                   ''')

    entry = cursor.fetchone()

    if entry is None:
        writePedalBoardData(cursor)
        connection.commit()
        
def main():

    app_dir = f.getAppDirectory()
    db_name = db.getDatabaseName(app_dir)
    connection = db.getDatabaseConnection(db_name)
    
    writeSampleData(connection)

if __name__ == '__main__':
    main()
    
