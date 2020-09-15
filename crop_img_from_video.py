import os
import argparse

import cv2


def get_subdir_paths(source):
    if os.path.isfile(source):
        return [source]
    return [os.path.join(source, file_) for file_ in os.listdir(source)]


def open_video(video_files, output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for video_path in video_files:
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ConnectionError("Cannot open video %s" % video_path)
        
        frame_idx = -1
        while True:
            has_frame, frame = cap.read()
            
            if not has_frame:
                print("End of %s file" % video_path)
                break

            frame_idx += 1
            if frame_idx % 3 != 0:
                continue
            
            cv2.imshow(video_path, frame)

            key = cv2.waitKey(0) & 0xFF
            if key == ord('q'):
                break

            elif key == ord('d'):
                continue

            elif key == ord('s'):
                video_file = os.path.split(video_path)[-1]
                video_name, video_ext = os.path.splitext(video_file)
                image_path = video_name + str(frame_idx) + ".png"
                cv2.imwrite(os.path.join(output_dir, image_path), frame)

        cv2.destroyAllWindows()
        cap.release()
        # Log file
        with open("logfile.log", "a") as f:
            f.write(video_path + '\n')

if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument('--source', type=str, default="dataset/video/container/", help="Directory contains video.")
    parse.add_argument('--output-dir', type=str, default="output/", help="Output directory")
    opt = parse.parse_args()

    video_files = get_subdir_paths(opt.source)
    print(video_files)
    open_video(video_files, opt.output_dir)
