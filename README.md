# Raspberry Pi Shrink
This utility will shrink your raspberry pi image, and make it so you can put the image on a smaller SD card.

## Read the instructions carefully

If you have an issue with the software, please open an issue or attempt to fix yourself, and commit the fix.  The reason I wrote this is because other utilities on github were not working for me, and since it takes a long time to copy many gigs from an SD card, I wanted to make a utility that I know works.


## To run

```sh
git clone https://github.com/audstanley/RaspberryPiShrink;
cd RaspberryPiShrink;
sudo python shrink.py
```

## Gparted
After Gpared opend, resize/move this image so that it's smaller.
Don't worry, The image is on a loopback so you are NOT actuall resizing the image on your sd card.  You are resizing the image that the python script made a copy of.  Also, if you get an error in gparted when you resize the image, than it could be because you tried to shrink the image too small, so just try again and give the image an additional 600M or 800M, and that will solve the problem.  In some cases I had to add 1Gb on really large Raspberry Pi SD cards. (if I had like 6Gb of things that were installed on the SD card).  Otherwise, just play with the numbers.  It's not going to hurt anything if the shrinking fails, you can just try again from within GParted.

**You will need to write down this number from gparted:**
> **resize2fs-p /dev/loop0 (THIS NUMBER)K**

Here is an example:

![img](http://ww2.audstanley.com:8081/cpp/photos/gparted.png)

In this picture, I would write down: 4864000K
DO NOT CLOSE OUT GPARTED UNTIL YOU WRITE THAT NUMBER DOWN.
When you go back to the terminal after closing gparted, you will be prompted to type in
that exact number.

## After Gparted
Once you have successfully shrunken the image, the python script will take care of the rest of the operations, including zipping the files, and changing permissions to the username that you were prompted for in the beginning of the script
