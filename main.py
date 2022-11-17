import glob
import calendar
import os
import shutil


def get_folder_date(folder_name):
    # get last section of file name
    folder_date_raw = folder_name.split('_')[-1]

    # avoid enumeration
    folder_date = folder_date_raw.split(' ')[0]
    folder_date = folder_date.strip('/')

    year, month_id = folder_date.split('-')

    month_number = int(month_id)

    return year, month_number


def move_to_music_folder(mp3_file, dst_folder):
    library_path = f'{os.environ["MUSIC_FOLDER"]}/{os.environ["LIBRARY_FOLDER_NAME"]}'

    if not os.path.exists(library_path):
        os.mkdir(library_path)

    filename = os.path.basename(mp3_file)

    dst_folder = f'{library_path}/{dst_folder}'

    if not os.path.exists(dst_folder):
        print(f'Creating new month folder: {dst_folder}.')
        os.mkdir(dst_folder)

    mp3_file_dst_path = f'{dst_folder}/{filename}'

    print(f'Moving song to new path: {mp3_file_dst_path}.')

    shutil.move(mp3_file, mp3_file_dst_path)


def search_beatport_folder():
    beatport_downloads = glob.glob(f'{os.environ["DOWNLOAD_FOLDER"]}/beatport_tracks_*/')

    if len(beatport_downloads) == 0:
        print('No new beatport folders.')
        return

    beatport_downloads.sort()

    for beatport_folder in beatport_downloads:
        if len(os.listdir(beatport_folder)) == 0:
            continue

        year, month_number = get_folder_date(beatport_folder)

        calendar_month_name = calendar.month_name[month_number]

        song_folder_name = f'{calendar_month_name}-{year}'

        mp3_files = glob.glob(f'{beatport_folder}*.mp3', recursive=True)

        # Move mp3 files to month files
        for mp3_file in mp3_files:
            move_to_music_folder(mp3_file, song_folder_name)

        # Delete beatport folder in Downloads
        if len(os.listdir(beatport_folder)) == 0:
            print(f'Deleting empty folder: {beatport_folder}.')
            os.rmdir(beatport_folder)

        zip_file = beatport_folder.strip('/') + '.zip'

        # Removes zip file if still existing
        if os.path.exists(zip_file):
            print(f'Removing zip file: {zip_file}.')
            os.remove(zip_file)


if __name__ == '__main__':
    search_beatport_folder()
