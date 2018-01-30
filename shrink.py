import os
import sys
from subprocess import Popen, PIPE
import subprocess, re
from time import sleep
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read

sdbCheck = False

class c:
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    CYAN = '\033[36m'
    MAGENTA = '\033[35'
    RED = '\033[31m'
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def query_yes_no(question, default="no"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

if sys.platform != "linux":
        if sys.platform != "linux2":
            print(c.RED+"\nThis script was written for Linux OS."+c.DEFAULT)
            sys.exit()
  
if os.getuid() is not 0:
    print(c.RED+"Please run as sudo:\n\t"+c.YELLOW+"sudo python shrink.py\n"+c.DEFAULT)
    sys.exit()
else:
    print("##############################################################")
    print("#                                                            #")
    print("# "+c.RED+"Raspberry Pi Shrink"+c.DEFAULT+"                                        #")
    print("#   "+c.YELLOW+"Please take note of the device you wish to clone"+c.DEFAULT+"         #")
    print("#   "+c.YELLOW+"and please read the instructions given along the way"+c.DEFAULT+"     #")
    print("#                                                            #")
    print("#                                                            #")
    print("# Software written by "+c.CYAN+"Richard Stanley"+c.DEFAULT+" (audstanley):          #")
    print("#   "+c.BLUE+"https://www.github.com/audstanley/RaspberryPiShrink"+c.DEFAULT+"      #")
    print("#   Based off of the guide:                                  #")
    print("#     aoakley.com/articles/2015-10-09-resizing-sd-images.php #")
    print("#   Feel free to contribute, and make this software better   #")
    print("#                                                            #")
    print("##############################################################")
    print("Going to launch df -h, so you can take note of the drive you wish to clone...")
    #sleep(3)
    print("\n\n")
    p = Popen(["df", "-h"], stdout=PIPE)
    out, err = p.communicate()
    print(out)

    # Check for dependencies, and automatically install them if needed
    p = Popen(["whereis", "gparted"], stdout=PIPE)
    out1, err = p.communicate()
    p = Popen(["whereis", "dcfldd"], stdout=PIPE)
    out2, err = p.communicate()
    
    if out1[8:] == "\n" or out2[7:] == "\n":
        print(c.YELLOW+"Installing dependencies\n  This may take a minute..."+c.DEFAULT)
        p = Popen(["sudo","apt-get","update"], stdout=PIPE).communicate()
        p = Popen(["sudo","apt-get","install","dcfldd", "gparted", "pv", "-y"], stdout=PIPE).communicate()

    #dependencies = query_yes_no("Would you like to install dependencies? : ")
    #if dependencies:
    #    p = Popen(["sudo","apt-get","update"], stdout=PIPE)
    #    out, err = p.communicate()
    #    print(out)
    #    p = Popen(["sudo","apt-get","install","dcfldd", "gparted", "pv", "-y"], stdout=PIPE)
    #    out, err = p.communicate()
    #    print(out)
    #    print("\n\n\n")
    username = raw_input(c.YELLOW+"Please enter your username: "+c.DEFAULT)
    imageName = raw_input("\n"+c.YELLOW+"Please enter the name of the image you wish to create\
        \n\t(Ex: piImage, "+ c.RED +" leave out: .img"+c.YELLOW+"): "+c.DEFAULT)
    if bool(re.search(r"\.img$", imageName)):
        imageName = imageName[:-4]
    if imageName == "":
        imageName = "piImage"
    device = raw_input("\n"+c.YELLOW+"Enter the device you want to create an image of...\n\t"+c.RED+\
        "You should not attempt to make an image of your internal drives"+c.YELLOW+"\n\t(Ex. sdc): "+c.DEFAULT)
    if device == "sdb" or device == "/dev/sdb":
        sdbCheck = query_yes_no(c.RED+"Are you SURE, usually sdb is an internal drive (y, yes, n, no): "+c.DEFAULT)
        if not sdbCheck:
            sys.exit()
        else:
            device = "sdb"
    while True:
        if bool(re.search(r"\w{3}", device)):
            break
        else:
            print(c.RED+"ERROR"+c.DEFAULT+": The device should only be three letters long (Ex. sdc)")
            device = raw_input("\nEnter the device you want to create an image of (Ex. sdc): ")
    if bool(re.search(r"\/dev\/([a-z]{3})\d*", device)):
        device = re.findall(r"\/dev\/([a-z]{3})\d*", device)[0]
    print(c.YELLOW+"First, we need to copy the whole image"+c.CYAN)
    p = Popen(["sudo", "dcfldd", "if=/dev/" + device, "of=" + imageName + ".img"], stdout=PIPE)
    out, err = p.communicate()
    print(out)
    print(c.DEFAULT)
    sleep(1)
    #p = Popen(["sudo", "umount", "/dev/" + device + "1", "/dev/" + device + "2"], stdout=PIPE).communicate()
    #print(c.YELLOW+"Feel free to remove your SD card now, if you want...")
    #sleep(4)
    p = Popen(["sudo", "sync"], stdout=PIPE).communicate()
    sleep(1)
    p = Popen(["sudo", "fdisk", "-l", imageName + ".img"], stdout=PIPE)
    out, err = p.communicate()
    print(out)
    startSector = int(re.findall(r"\.img2\s+(\d{1,})", out)[0])
    p = Popen(["sudo", "losetup", "-d", "/dev/loop0"], stdout=PIPE).communicate()
    sleep(1)
    print("startSector: "+c.BLUE+"{}".format(startSector) + c.DEFAULT)
    p = Popen(["sudo", "losetup", "/dev/loop0", imageName + ".img", "-o", str((startSector * 512))], stdout=PIPE).communicate()
    print("\n" + c.RED + "Instructions:" + c.YELLOW)
    print("    Be prepaired to take note of the new size of the image...")
    print("    Write down the info as soon as you have a successfull shrinking of the image,")
    print("    Read ALL OF THESE STEPS before you close any windows from gparted...")
    print("    When gparted opens: ")
    print("      1. Select the partition")
    print("      2. Right click and resize the partition")
    print("      3. You may need to make the partition larger than the 'Used' size")
    print("        (Ususally about 1.5gb larger than 'Used')")
    print("       4. Ctrl-Enter to 'Apply all operations'")
    print("       5. If the resize is unsuccessful,")
    print("         Try resizing the partition a little larger")
    print("       6.  When the resize "+c.RED+"IS"+c.YELLOW+" successful:")
    print("         a. You will need to click 'Details'")
    print("         b. click 'shrink file system'")
    print("         c. "+c.RED+"WRITE DOWN"+c.YELLOW+": resize2f-p /dev/loop0 "+c.BLUE+"#######K"+c.YELLOW)
    print("         d. You just need those numbers in the next step\n"+c.DEFAULT)
    sleep(3)

    p = Popen(["sudo", "gparted", "/dev/loop0"], stdout=PIPE).communicate()
    imageLetter = "K"
    imageSize = None
    while type(imageSize) is not int:
        imageSize = raw_input(c.YELLOW+"What is the size of the image from gparted? "+c.BLUE+"########"+c.DEFAULT+": ")
        if bool(re.search(r"^\d{1,}$", imageSize)) is False:
            if bool(re.search(r"^\+\d{1,}", imageSize)):
                imageSize = imageSize[1:]
            if bool(re.search(r"\d{1,}\w$", imageSize)):
                m = re.findall(r"\d{1,}(\w)$", imageSize)
                imageSize = imageSize[:-1]
                imageLetter = m[0]
        if bool(re.search(r"^\d{1,}$", imageSize)):
            imageSize = int(imageSize)


    p = Popen(["sudo", "losetup", "-d", "/dev/loop0"], stdout=PIPE).communicate()
    sleep(3)
    p = Popen(["sudo", "losetup", "/dev/loop0", imageName + ".img"], stdout=PIPE)
    out, err = p.communicate()
    print(out)
    sleep(5)
    
    # Check to see if the loop0 is busy
    '''
    out.lower()
    if out == "device is busy":
        i = 1
        while out == "device is busy":
            print(c.YELLOW+"/dev/loop0 seems to be busy, trying to reset.."+c.DEFAULT)
            p = Popen(["sudo", "losetup", "-d", "/dev/loop0"], stdout=PIPE).communicate()
            sleep(i*2)
            p = Popen(["sudo", "losetup", "/dev/loop0", imageName + ".img"], stdout=PIPE)
            out, err = p.communicate()
            print(out)
            sleep(i*3)
            if i == 5:
                print(c.RED+"\nCannot seem to access /dev/loop0, you may need to restart your computer"+c.DEFAULT)
                sys.exit()
            i = i+1
    '''
    print(c.YELLOW+"Deleting the excess space from " + imageName + ".img\n  This may take a few seconds\
    \n  If you see: "+c.CYAN+"Re-reading the partition table failed.: Invalid argument"+c.YELLOW+"\
    \n  This is OK, The process was still a success"+c.DEFAULT)
    startSector = int(startSector)
    p = Popen(["sudo", "fdisk", "/dev/loop0"], stdin=PIPE, stdout=PIPE, shell=False)
    flags = fcntl(p.stdout, F_GETFL) # get current p.stdout flags
    fcntl(p.stdout, F_SETFL, flags | O_NONBLOCK)
    sleep(2)
    p.stdin.write("d\n")
    sleep(1)
    p.stdin.write("2\n")
    sleep(1)
    p.stdin.write("n\n")
    sleep(1)
    p.stdin.write("p\n")
    sleep(1)
    p.stdin.write("2\n")
    sleep(1)
    p.stdin.write(str(startSector) + "\n")
    sleep(1)
    p.stdin.write("+" +  str(imageSize) + imageLetter + "\n")
    sleep(4)
    p.stdin.write("w\n")
    sleep(4)

    int(imageSize)

    p = Popen(["sudo", "fdisk", "-l", imageName + ".img"], stdout=PIPE)
    out, err = p.communicate()
    endSector = int(re.findall(r"\.img2\s+\d{1,}\s+(\d{1,})", out)[0])
    p = Popen(["sudo", "losetup", "-d", "/dev/loop0"], stdout=PIPE).communicate()
    sleep(1)

    p = Popen(["sudo", "truncate", "-s", str((endSector+1) * 512), imageName + ".img"], stdout=PIPE).communicate()
    sleep(1)
    print(c.YELLOW+"Writing zeros in the empty part of the partition so the file will zip smaller..."+c.DEFAULT)
    startSector = int(startSector)
    print(c.CYAN)
    p = Popen(["sudo", "losetup", "/dev/loop0", imageName + ".img", "-o", str(startSector * 512)], stdout=PIPE)
    out, err = p.communicate()
    print(c.DEFAULT)
    sleep(1)
    p = Popen(["sudo", "mkdir", "-p", "/mnt/imageroot"], stdout=PIPE)
    out, err = p.communicate()
    sleep(1)
    p = Popen(["sudo", "mount", "/dev/loop0", "/mnt/imageroot"], stdout=PIPE)
    out, err = p.communicate()
    sleep(1)
    p = Popen(["sudo", "dcfldd", "if=/dev/zero", "of=/mnt/imageroot/zero.txt"], stdout=PIPE)
    out, err = p.communicate()
    print(out)
    sleep(2)
    p = Popen(["sudo", "rm", "/mnt/imageroot/zero.txt"], stdout=PIPE).communicate()
    sleep(10)
    p = Popen(["sudo", "umount", "/mnt/imageroot"], stdout=PIPE).communicate()
    sleep(1)
    p = Popen(["sudo", "rmdir", "/mnt/imageroot"], stdout=PIPE).communicate()
    sleep(1)
    p = Popen(["sudo", "losetup", "-d", "/dev/loop0"], stdout=PIPE).communicate()
    sleep(1)
    print(c.YELLOW+"Now zipping the image...\n  This could take a long time."+c.DEFAULT)
    
    p = Popen(["sudo", "chown", username + ":" + username, imageName + ".img"], stdout=PIPE)
    out, err = p.communicate()
    
    p = Popen(["sudo", "zip", imageName + ".zip", imageName + ".img"], stdout=PIPE)
    out, err = p.communicate()
    print(out)
    #p2 = Popen(["sudo", "pv", imageName + ".img"], stdout=p)
    #out, err = p2.communicate()
    p = Popen(["sudo", "chown", username + ":" + username, imageName + ".zip"], stdout=PIPE)
    out, err = p.communicate()
    print("Image shrinking is complete.")
#except:
#    print(c.RED+"If you are having problems using the utility, You might want to restart your machine")
#    print("Sometimes there is an issue with the loopback device, and a restart will fix the issue."+c.DEFAULT)
