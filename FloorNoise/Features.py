def getEffectTypeRanking(cursor):

    query = '''
            SELECT
                E.EffectName,
                COUNT(*)
            FROM PedalOwner PO
            INNER JOIN PedalEffect PE
                ON PE.PedalID = PO.PedalID
            INNER JOIN EffectType E
                ON E.EffectID = PE.EffectID
            GROUP BY E.EffectID
            ORDER BY COUNT(*) DESC
            '''

    cursor.execute(query)
    ranking = cursor.fetchall()

    for effect in ranking:
        print(str(effect[1]) + ' ' + effect[0] + ' pedals owned.')

def getMostOwnedPedalByEffect(cursor, effect):
    
    query = '''
            SELECT
                P.PedalName
            FROM PedalOwner PO
            INNER JOIN Pedal P 
                    ON P.PedalID = PO.PedalID
            INNER JOIN PedalEffect PE
                    ON PO.PedalID = PE.PedalID
            INNER JOIN EffectType E
                ON E.EffectID = ?
            WHERE 
                    PE.EffectID = ?
            GROUP BY PO.PedalID 
            HAVING COUNT(*) = ( SELECT COUNT(*)
                                FROM PedalOwner PO
                                INNER JOIN PedalEffect PE
                                    ON PO.PedalID = PE.PedalID
                                WHERE PE.EffectID=?
                                GROUP BY PO.PedalID
                                ORDER BY COUNT(*) DESC
                                LIMIT 1
                              )
            '''

    cursor.execute(query, (str(effect[0]), str(effect[0]), str(effect[0])))
    pedal = cursor.fetchone()
    
    print('Most popular ' + effect[1] + ' pedal: ' + pedal[0])

def getPedalsByManufacturer(cursor, manufacturer):

    query = '''
            SELECT PedalName
            FROM Pedal
            WHERE ManuID=?
            '''
    
    cursor.execute(query, [str(manufacturer[0])])
    pedals = cursor.fetchall()

    print(manufacturer[1] + ' Pedals:')
    
    for pedal in pedals:
        print(pedal[0])

def getPopularPedalPairing(cursor, pedal):

    query = '''
            SELECT
                P1.PedalName,
                P2.PedalName,
                Man1.ManuName,
                Man2.ManuName
            FROM PedalOwner PO
            INNER JOIN PedalBoard PB
                ON PB.OwnerID = PO.OwnerID
            INNER JOIN PedalBoard PB_2
                ON PB.UserBoardID = PB_2.UserBoardID
            INNER JOIN PedalOwner PO_2
                ON PO_2.OwnerID = PB_2.OwnerID
                AND PO_2.PedalID <> ?
            INNER JOIN Pedal P1
                ON P1.PedalID = ?
            INNER JOIN Pedal P2 
                ON PO_2.PedalID = P2.PedalID
            INNER JOIN Manufacturer Man1
                ON P1.ManuID = Man1.ManuID
            INNER JOIN Manufacturer Man2
                ON P2.ManuID = Man2.ManuID
            WHERE PO.PedalID = ?
            GROUP BY P2.PedalID
            ORDER BY COUNT(*) DESC
            LIMIT 1; 
            '''

    cursor.execute(query, (str(pedal[0]), str(pedal[0]), str(pedal[0])))
    entry = cursor.fetchone()

    print(entry[2] + ' ' + entry[0] + ' is most often paired with a(n) ' + entry[3] + ' ' + entry[1])

def getManufacturersMostPopularPedals(cursor):

    query = '''
            SELECT
                M.ManuName,
                (
                    SELECT
			P.PedalName
                    FROM Pedal P
                    INNER JOIN PedalOwner PO
			ON PO.PedalID = P.PedalID
                    WHERE P.ManuID = M.ManuID
                    GROUP BY PO.PedalID
                    ORDER BY COUNT(*) DESC
                    LIMIT 1
                ) AS MostPopular
            FROM Manufacturer M
            ORDER BY M.ManuName
            '''

    cursor.execute(query)
    entries = cursor.fetchall()

    for entry in entries:
        print(entry[0] + ': ' + entry[1])

def getPedalsWithSpecialPowerRequirements(cursor):

    query = '''
            SELECT
                M.ManuName,
                P.PedalName,
                P.VoltageMin,
                P.VoltageMax,
                P.mAmps
            FROM Pedal P
            INNER JOIN Manufacturer M
                ON M.ManuID = P.ManuID
            WHERE
                VoltageMin > 9
                OR VoltageMax > 9
                OR mAmps > 100
            '''

    cursor.execute(query)

    entries = cursor.fetchall()

    for entry in entries:
        print(entry[0] + ' ' + entry[1] + ' Power Specifications:')
        print('Minimum Voltage: ' + str(entry[2]))
        print('Maximum Voltage: ' + str(entry[3]))
        print('Required mAmps: ' + str(entry[4]) + '\n')

def getTop3UsersWithMostPedals(cursor):

    query = '''
            SELECT
                (U.FirstName || ' ' || U.LastName) AS UserName,
                Count(*) AS Pedals
            FROM PedalOwner PO
            INNER JOIN User U
                ON PO.UserID = U.UserID
            GROUP BY U.UserID
            ORDER BY COUNT(*) DESC
            LIMIT 3
            '''

    cursor.execute(query)

    entries = cursor.fetchall()

    for entry in entries:
        print(entry[0] + ': ' + str(entry[1]) + ' pedals')

def getPercentOfOwnershipByPedal(cursor):

    query = '''
            SELECT
                P.PedalName,
                M.ManuName,
                CASE
                    WHEN P.PedalID NOT IN (SELECT PO.PedalID FROM PedalOwner PO) THEN
			0.00
                    ELSE
			ROUND((CAST(Count(*) AS REAL)/CAST((SELECT Count(*) FROM PedalOwner) AS REAL))*100, 2)
                END AS Percent
            FROM PedalOwner PO
            LEFT OUTER JOIN Pedal P
                ON P.PedalID = PO.PedalID
            LEFT OUTER JOIN Manufacturer M
                ON M.ManuID = P.ManuID
            GROUP BY P.PedalID
            ORDER BY Percent
            '''

    cursor.execute(query)

    entries = cursor.fetchall()

    for entry in entries:
            print(entry[1] + ' ' + entry[0] + ': ' + str(entry[2]) + '% of pedals owned.')
    
