import os
from PIL import Image

def get_gif_duration(gif):
    """Calculate the total duration of a GIF by summing the duration of each frame."""
    durations = 0
    for frame in range(gif.n_frames):
        gif.seek(frame)
        durations += gif.info['duration']
    return durations

def adjust_gif_speed(original_gif, target_duration, output_path):
    """Adjust GIF speed to match a target duration and save the adjusted GIF."""
    frames = []
    original_duration = get_gif_duration(original_gif)
    duration_ratio = target_duration / original_duration

    # Collect all frames and adjust their duration
    for frame in range(original_gif.n_frames):
        original_gif.seek(frame)
        new_duration = int(original_gif.info['duration'] * duration_ratio)
        frames.append(original_gif.copy().convert("RGBA"))
        frames[-1].info['duration'] = new_duration

    # Save the frames as a new GIF
    frames[0].save(output_path, save_all=True, append_images=frames[1:], loop=0)

def main(folder_path):
    gifs = [f for f in os.listdir(folder_path) if f.endswith('.gif')]
    gif_paths = [os.path.join(folder_path, gif) for gif in gifs]
    max_duration = 0

    # Find the GIF with the maximum duration
    for gif_path in gif_paths:
        with Image.open(gif_path) as gif:
            duration = get_gif_duration(gif)
            if duration > max_duration:
                max_duration = duration

    # Adjust the speed of each GIF to match the maximum duration
    for gif_path in gif_paths:
        with Image.open(gif_path) as gif:
            output_path = os.path.join(folder_path, os.path.splitext(os.path.basename(gif_path))[0] + "_.gif")
            adjust_gif_speed(gif, max_duration, output_path)

if __name__ == "__main__":
    folder_path = '/home/ismarou/Documents/Knockin_Papers/Videos_Dhruv'  # Change this to the path of your GIF folder
    main(folder_path)
