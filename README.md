# Raspberry Pi Shrink
This utility will shrink your raspberry pi image, and make it so you can put the image on a smaller SD card.

## Read the instructions carefully

If you have an issue with the software, please open an issue or attempt to fix yourself, and commit the fix.  The reason I wrote this is because other utilities on github were not working for me, and since it takes a long time to copy many gigs from an SD card, I wanted to make a utility that I know works.


## Gparted
After Gpared opend, resize/move this image so that it's smaller.
Don't worry, The image is on a loopback so you are NOT actuall resizing the image on your sd card.  You are resizing the image that you made a copy of in earlier steps.

You will need to write down this number:
resize2fs-p /dev/loop0 (THIS NUMBER)K

Here is an example:
![img](http://ww2.audstanley.com:8081/cpp/photos/gparted.png)
In this picture, I would write down: 4864000K
DO NOT CLOSE OUT GPARTED UNTIL YOU WRITE THAT NUMBER DOWN.
When you go back to the terminal after closing gparted, you will be prompted to type in
that exact number.

