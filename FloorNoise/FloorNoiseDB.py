import os
import sys
import sqlite3 as sql

def getDatabaseName(app_dir):

    return app_dir + r'\FloorNoise.db'

def getDatabaseConnection(db_name):

    connection = None
    db_exists = os.path.exists(db_name)

    #Connects to database.
    #If no database file is found, one is automatically created.
    try:
        connection = sql.connect(db_name)
    except:
        sys.exit('Cannot connect to database.')

    #Enables Foreign Key constraints for new database
    if not db_exists:
        connection.cursor().execute('PRAGMA foreign_keys = ON;')
    
    return connection

def getTableNames():

    return ['User',
            'Manufacturer',
            'Pedal',
            'EffectType',
            'PedalEffect',
            'PedalOwner',
            'GenreTag',
            'UserBoard',
            'PedalBoard']

def getTableCreationQueries():

    tbl_Queries = []

    #User Table
    tbl_Queries.append( '''
                        CREATE TABLE User(
                            UserID INTEGER PRIMARY KEY,
                            FirstName TEXT NOT NULL,
                            LastName TEXT NOT NULL
                        )
                        ''')

    #Manufacturer Table
    tbl_Queries.append( '''
                        CREATE TABLE Manufacturer(
                            ManuID INTEGER PRIMARY KEY,
                            ManuName TEXT NOT NULL
                        )
                        ''')

    #Pedal Table
    tbl_Queries.append( '''
                        CREATE TABLE Pedal(
                            PedalID INTEGER PRIMARY KEY,
                            ManuID INTEGER NOT NULL,
                            PedalName TEXT NOT NULL,
                            Description TEXT,
                            IsStereoIn INTEGER,
                            IsStereoOut INTEGER,
                            HasMIDI INTEGER,
                            HasTapTempo INTEGER,
                            HasExpressionJack INTEGER,
                            VoltageMin INTEGER,
                            VoltageMax INTEGER,
                            mAmps INTEGER,
                            FOREIGN KEY (ManuID) REFERENCES Manufacturer (ManuID)
                        )
                        ''')

    #EffectType Table
    tbl_Queries.append( '''
                        CREATE TABLE EffectType(
                            EffectID INTEGER PRIMARY KEY,
                            EffectName TEXT NOT NULL
                        )
                        ''')

    #PedalEffect Table
    tbl_Queries.append( '''
                        CREATE TABLE PedalEffect(
                            PedalID INTEGER NOT NULL,
                            EffectID INTEGER NOT NULL,
                            FOREIGN KEY (PedalID) REFERENCES Pedal (PedalID),
                            FOREIGN KEY (EffectID) REFERENCES EffectType (EffectID)
                        )
                        ''')

    #PedalOwner Table
    tbl_Queries.append( '''
                        CREATE TABLE PedalOwner(
                            OwnerID INTEGER PRIMARY KEY,
                            UserID INTEGER NOT NULL,
                            PedalID INTEGER NOT NULL,
                            FOREIGN KEY (UserID) REFERENCES User (UserID),
                            FOREIGN KEY (PedalID) REFERENCES Pedal (PedalID)
                        )
                        ''')

    #GenreTag Table
    tbl_Queries.append( '''
                        CREATE TABLE GenreTag(
                            GenreID INTEGER PRIMARY KEY,
                            GenreName TEXT NOT NULL
                        )
                        ''')
    #UserBoard Table
    tbl_Queries.append( '''
                        CREATE TABLE UserBoard(
                            UserBoardID INTEGER PRIMARY KEY,
                            UserID INTEGER NOT NULL,
                            GenreID INTEGER NOT NULL,
                            BoardName TEXT NOT NULL,
                            Description TEXT,
                            FOREIGN KEY (UserID) REFERENCES User (UserID),
                            FOREIGN KEY (GenreID) REFERENCES GenreTag (GenreID)
                        )
                        ''')

    #PedalBoard Table
    tbl_Queries.append( '''
                        CREATE TABLE PedalBoard(
                            PedalBoardID INTEGER PRIMARY KEY,
                            UserBoardID INTEGER NOT NULL,
                            OwnerID INTEGER NOT NULL,
                            FOREIGN KEY (UserBoardID) REFERENCES UserBoard (UserBoardID),
                            FOREIGN KEY (OwnerID) REFERENCES PedalOwner (OwnerID)
                        )
                        ''')
    
    return tbl_Queries

def validateTableDefinitions(tbl_Names, tbl_Queries):

    tbl_Ct = len(tbl_Names)

    if tbl_Ct != len(tbl_Queries):
        sys.exit('The expected number of tables and the number of table definitions do not match.')

    for i in range(0, tbl_Ct):

        #Gets table name from query "CREATE TABLE table_name("
        #And removes "(" from end of the name
        tbl_Query_Name = tbl_Queries[i].split()[2][:-1]
        
        if tbl_Names[i] != tbl_Query_Name:
            sys.exit('Expecting table \'' +  tbl_Names[i] + '\' but instructions are for table \'' + tbl_Query_Name + '\'.')

def initializeDatabase(app_dir):

    db = getDatabaseName(app_dir)
    connection = getDatabaseConnection(db)
    cursor = connection.cursor()

    tbl_Names = getTableNames()
    tbl_CreationQueries = getTableCreationQueries()
    tbl_Ct = len(tbl_Names)

    validateTableDefinitions(tbl_Names, tbl_CreationQueries)
    
    for i in range(0, tbl_Ct):

        #Checks for existence of table by name
        cursor.execute( '''
                        SELECT count(name)
                        FROM sqlite_master
                        WHERE
                            type = 'table' AND
                            name = \'''' + tbl_Names[i] + '\'')

        if cursor.fetchone()[0] == 0:
            cursor.execute(tbl_CreationQueries[i])


    connection.commit()
    connection.close()
