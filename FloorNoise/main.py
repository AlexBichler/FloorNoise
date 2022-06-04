import FileMgmt as f
import FloorNoiseDB as db
import SampleData as sample
import Features as ftr

def main():

    app_dir = f.getAppDirectory()

    f.initializeDirectory(app_dir)
    db.initializeDatabase(app_dir)

    db_name = db.getDatabaseName(app_dir)
    connection = db.getDatabaseConnection(db_name)   

    sample.writeSampleData(connection)

    cursor = connection.cursor()

    #Gets Effect ranking
    print('Getting Effect Rankings')
    print('***************************************')
    ftr.getEffectTypeRanking(cursor)
    print('***************************************\n')

    #Gets most popular pedal by effect
    print('Getting most Popular Pedal By Effect')
    cursor.execute('''
                   SELECT *
                   FROM EffectType
                   ORDER BY Random()
                   LIMIT 1
                   ''')

    effect = cursor.fetchone()

    print('***************************************')
    ftr.getMostOwnedPedalByEffect(cursor, effect)
    print('***************************************\n')
    
    #Gets all pedals by manufacturer
    print('Getting All Pedals By Manufacturer')
    cursor.execute('''
                   SELECT *
                   FROM Manufacturer
                   ORDER BY Random()
                   LIMIT 1
                   ''')

    manufacturer = cursor.fetchone()

    print('***************************************')
    ftr.getPedalsByManufacturer(cursor, manufacturer)
    print('***************************************\n')

    #Gets Popular Pedal Pairing
    print('Getting Popular Pairing for Specified Pedal')
    cursor.execute('''
                   SELECT *
                   FROM Pedal
                   ORDER BY Random()
                   LIMIT 1
                   ''')

    pedal = cursor.fetchone()

    print('***************************************')
    ftr.getPopularPedalPairing(cursor, pedal)
    print('***************************************\n')

    #Gets Most Popular Pedal by Manufacturer
    print('Getting Manufacturers Most Popular Pedals')
    cursor.execute('''
                   SELECT *
                   FROM Manufacturer
                   ORDER BY Random()
                   LIMIT 1
                   ''')

    manufacturer = cursor.fetchone()
    print('***************************************')
    ftr.getManufacturersMostPopularPedals(cursor)
    print('***************************************\n')

    #Get Pedals With Special Power Requirements
    print('Getting pedals with Special Power Requirements (Voltage>9 or mAmps>100)')
    print('***************************************')
    ftr.getPedalsWithSpecialPowerRequirements(cursor)
    print('***************************************\n')

    #Get Percent of Pedal Ownership
    print('Get Percent of Ownership')
    print('***************************************')
    ftr.getPercentOfOwnershipByPedal(cursor)
    print('***************************************\n')
    
    #Get Top 3 Users with Most Pedals
    print('Getting Top 3 Users with Most Pedals')
    print('***************************************')
    ftr.getTop3UsersWithMostPedals(cursor)
    print('***************************************\n')
    
if __name__ == '__main__':
    main()
