import cv2
import os
import sys
import argparse
import datetime

#Expand edition

def convert_frame_to_colored_ascii(frame):
    height, width, _ = frame.shape
    new_width = int(os.get_terminal_size().columns)
    aspect_ratio = width / height
    new_height = int(new_width / aspect_ratio * 0.5)
    resized_frame = cv2.resize(frame, (new_width, new_height))

    colored_ascii_frame = ""
    for row in resized_frame:
        for pixel in row:
            intensity = sum(pixel[:3]) / 3.0 / 255.0
            colored_ascii_frame += get_colored_ascii_char(intensity, pixel)
        colored_ascii_frame += "\n"

    return colored_ascii_frame

def get_colored_ascii_char(intensity, color):
    ascii_chars = "@§&%#*+=•-:. ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŒœŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽžअआइईउऊऋऌऍऎएऐऑऒओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलळऴवशषसहा"
    return f"\033[38;2;{color[2]};{color[1]};{color[0]}m{ascii_chars[int(intensity * (len(ascii_chars) - 1))]}"

def determine_color_code(color):
    grayscale_value = sum(color) / 3.0
    color_codes = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
    ]
    index = int(grayscale_value / 21.33)
    return color_codes[index]

def get_current_time(frame_number, frame_rate):
    total_seconds = frame_number / frame_rate
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    milliseconds = (total_seconds - int(total_seconds)) * 1000
    return int(hours), int(minutes), int(seconds), int(milliseconds)

def get_frame_number_from_time(time, frame_rate):
    total_seconds = (time.hour * 3600) + (time.minute * 60) + time.second + (time.microsecond / 1e6)
    return int(total_seconds * frame_rate)

def play_video(video_path, loop=False, jump_to_frame=None, jump_to_time=None):
    video = cv2.VideoCapture(video_path)
    paused = False

    try:
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_rate = video.get(cv2.CAP_PROP_FPS)

        if jump_to_frame is not None and 0 <= jump_to_frame < total_frames:
            video.set(cv2.CAP_PROP_POS_FRAMES, jump_to_frame)
        elif jump_to_time is not None:
            frame_number = get_frame_number_from_time(jump_to_time, frame_rate)
            if 0 <= frame_number < total_frames:
                video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        frame_counter = int(video.get(cv2.CAP_PROP_POS_FRAMES))

        while True:
            if not paused:
                ret, frame = video.read()
                if not ret:
                    if loop:
                        video.release()
                        video = cv2.VideoCapture(video_path)
                        frame_counter = 0
                        continue
                    else:
                        break

                colored_ascii_frame = convert_frame_to_colored_ascii(frame)
                sys.stdout.write(colored_ascii_frame)
                sys.stdout.flush()

                sys.stdout.write(f"\rFrame: {frame_counter}/{total_frames}")

                hours, minutes, seconds, milliseconds = get_current_time(frame_counter, frame_rate)
                total_hours, total_minutes, total_seconds, _ = get_current_time(total_frames, frame_rate)

                sys.stdout.write(f" | Time: {hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03} / "
                                 f"Total: {total_hours:02}:{total_minutes:02}:{total_seconds:02}.000")
                sys.stdout.flush()

                frame_counter += 1

            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break
            elif key == ord('p') or key == ord('P'):
                paused = not paused

    except KeyboardInterrupt:
        pass
    finally:
        video.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play a video in ASCII art in the terminal.")
    parser.add_argument("video_path", help="Path to the video file")
    parser.add_argument("-l", "--loop", action="store_true", help="Loop the video until 'q' is pressed")
    parser.add_argument("-j", "--jump", type=int, metavar="FRAME", help="Jump to a specific frame in the video")
    parser.add_argument("-jt", "--jump_time", type=str, metavar="TIME", help="Jump to a specific time in the video (format: HH:MM:SS)")

    args = parser.parse_args()

    if args.jump_time:
        try:
            jump_time = datetime.datetime.strptime(args.jump_time, "%H:%M:%S").time()
        except ValueError:
            print("Invalid time format. Use the format HH:MM:SS.")
            sys.exit(1)
    else:
        jump_time = None

    cv2.namedWindow("Video to ASCII", cv2.WINDOW_NORMAL)

    play_video(args.video_path, loop=args.loop, jump_to_frame=args.jump, jump_to_time=jump_time)

    cv2.destroyAllWindows()
