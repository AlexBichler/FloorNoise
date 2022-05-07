import os

def getAppDirectory():

    return r'C:\FloorNoise'

def initializeDirectory(app_dir):

    #Check if application directory exists.
    #If not, creates one with proper permissions

    if not os.path.isdir(app_dir):
        os.mkdir(app_dir, 0o777)
