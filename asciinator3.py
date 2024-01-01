import cv2
import os
import sys
import argparse

def convert_frame_to_colored_ascii(frame):
    height, width, _ = frame.shape
    new_width = int(os.get_terminal_size().columns)
    aspect_ratio = width / height
    new_height = int(new_width / aspect_ratio * 0.5)
    resized_frame = cv2.resize(frame, (new_width, new_height))

    colored_ascii_frame = ""
    for row in resized_frame:
        for pixel in row:
            intensity = sum(pixel[:3]) / 3.0 / 255.0  # Average intensity of RGB values
            colored_ascii_frame += get_colored_ascii_char(intensity, pixel)
        colored_ascii_frame += "\n"

    return colored_ascii_frame

def get_colored_ascii_char(intensity, color):
    ascii_chars = "@§&%#*+=•-:. "  # Specified set of characters
    color_code = determine_color_code(color)
    return f"\033[38;2;{color[2]};{color[1]};{color[0]}m{ascii_chars[int(intensity * (len(ascii_chars) - 1))]}"

def determine_color_code(color):
    grayscale_value = sum(color) / 3.0
    color_codes = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15  # ANSI color codes for more colors
    ]
    # Map the grayscale value to the color codes
    index = int(grayscale_value / 21.33)  # Divide by approximately 21.33 for more color variety
    return color_codes[index]

def play_video(video_path, loop=False, jump_to_frame=None):
    video = cv2.VideoCapture(video_path)
    paused = False  # Variable to track whether the video is paused

    try:
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        if jump_to_frame is not None and 0 <= jump_to_frame < total_frames:
            video.set(cv2.CAP_PROP_POS_FRAMES, jump_to_frame)

        while True:
            if not paused:
                ret, frame = video.read()
                if not ret:
                    if loop:
                        video.release()
                        video = cv2.VideoCapture(video_path)
                        continue
                    else:
                        break

                # Print the colored ASCII art frame with carriage return
                colored_ascii_frame = convert_frame_to_colored_ascii(frame)
                sys.stdout.write(colored_ascii_frame)
                sys.stdout.flush()

            # Play at original speed (no sleep)
            # To control playback speed, adjust the sleep duration

            # Check for the 'q' key press to exit the loop
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break
            elif key == ord('p') or key == ord('P'):
                paused = not paused  # Toggle the pause state

    except KeyboardInterrupt:
        pass
    finally:
        video.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play a video in ASCII art in the terminal.")
    parser.add_argument("video_path", help="Path to the video file")
    parser.add_argument("-l", "--loop", action="store_true", help="Loop the video until 'q' is pressed")
    parser.add_argument("-j", "--jump", type=int, metavar="FRAME", help="Jump to a specific frame in the video")

    args = parser.parse_args()

    # Initialize OpenCV window for key capture
    cv2.namedWindow("Video to ASCII", cv2.WINDOW_NORMAL)

    play_video(args.video_path, loop=args.loop, jump_to_frame=args.jump)

    # Destroy the OpenCV window
    cv2.destroyAllWindows()
