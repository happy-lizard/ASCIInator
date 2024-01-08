# ASCIInator
A minimalistic CLI ASCII art video player

# How it works
It converts each frame of the video into ascii art based on intensity of each pixel, gets color, colors each frame with colorama and outputs the result into the terminal

# Installation
Just install cv2 and argsparse with pip,

pip3 install cv2

pip3 install argsparse

# Usage
python3 asciinator3  <video/image path>

-l = loop, will loop the video

-j = jumps to a specified frame, example usage: python3 asciinator3.py /media/my/3/gif/1701924589071801.gif  -j 128

                                                                                                             HH MM SS
                                                                                                              |  |  |
                                                                                                              V  V  V

-jt = jumps to specifed time, example usage: python3 asciinator3.py /media/my/3/gif/1701924589071801.gif  -jt 00:12:34

You can pause the video by going into the popup window and pressing p on your keyboard, you can quit by pressing q in the same window

Will play any photo or image of any format(such as mp4, webm, gif, jpg, png, webp and many more), you can reduce or increase the quality of the output by zooming in and out of the terminal window, additionally, you can rezise the window itself and it 

will provide a similar effect, currently only supported on Linux, audio playback is currently not available in any stables, but is experimentally available in Continuous.

If you want to add or remove UNICODE characters for the frames to be converted in, tweak this:


    def get_colored_ascii_char(intensity, color):

        ascii_chars = "@§&%#*+=•-:. " <-- this
    
        color_code = determine_color_code(color)
    
        return f"\033[38;2;{color[2]};{color[1]};{color[0]}m{ascii_chars[int(intensity * (len(ascii_chars) - 1))]}"

# Have fun :)
