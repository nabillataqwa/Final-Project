import time
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
import RPi.GPIO as gpio

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('Exception message: ' + str(e))
    exit(1)

def enrollFinger():
    print("Enrolling Finger")
    time.sleep(2)
    print('Waiting for finger...')
    print("Place Finger")
    while ( f.readImage() == False ):
        pass
    f.convertImage(0x01)
    result = f.searchTemplate()
    positionNumber = result[0]
    if ( positionNumber >= 0 ):
        print('Template already exists at position #' + str(positionNumber))
        print("Finger ALready")
        print("   Exists     ")
        time.sleep(2)
        return
    print('Remove finger...')
    print("Remove Finger")
    time.sleep(2)
    print('Waiting for same finger again...')
    print("Place Finger")
    print("   Again    ")
    while ( f.readImage() == False ):
        pass
    f.convertImage(0x02)
    if ( f.compareCharacteristics() == 0 ):
        print("Fingers do not match")
        print("Finger Did not")
        print("   Mactched   ")
        time.sleep(2)
        return
    f.createTemplate()
    positionNumber = f.storeTemplate()
    print('Finger enrolled successfully!')
    print("Stored at Pos:")
    print(str(positionNumber))
    print("successfully")
    print('New template position #' + str(positionNumber))
    time.sleep(2)

def searchFinger():
    try:
        print('Waiting for finger...')
        while( f.readImage() == False ):
            #pass
            time.sleep(.5)
            return
        f.convertImage(0x01)
        result = f.searchTemplate()

        characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
        print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

        positionNumber = result[0]
        accuracyScore = result[1]
        if positionNumber == -1 :
            print('No match found!')
            print("No Match Found")
            time.sleep(2)
            return False, ""
        else:
            print('Found template at position #' + str(positionNumber))
            print("Found at Pos:")
            print(str(positionNumber))
            time.sleep(2)
            return True, str(positionNumber)

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        # exit(1)
        return False
    
def deleteFinger():
    positionNumber = 0
    count=0
    print("Delete Finger")
    print("Position: ")
    print(str(count))
    positionNumber=count
    if f.deleteTemplate(positionNumber) == True :
        print('Template deleted!')
        time.sleep(2)

if __name__ == "__main__":
    while 1:
        # enrollFinger()
        # deleteFinger()
        searchFinger()