import FileMgmt as f
import FloorNoiseDB as db

def main():

    app_dir = f.getAppDirectory()

    f.initializeDirectory(app_dir)
    db.initializeDatabase(app_dir)
    

if __name__ == '__main__':
    main()
