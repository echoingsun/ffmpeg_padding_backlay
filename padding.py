import ffmpeg
import os
import csv

worksheet = '/Users/Lazybeam/Desktop/Work/videorework/worksheet.csv'
video_file_dir = '/Users/Lazybeam/Desktop/Work/videorework/original/'
output_file_dir = '/Users/Lazybeam/Desktop/Work/videorework/padded/'

video_list = []

with open(worksheet, 'r') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames

    for item in reader:
        video_list.append(item)

    f.close()

if 'padded' not in headers:
    headers.append('padded')

for video_item in video_list:

    try:
        filename = video_item['downloaded']

        if filename in os.listdir(video_file_dir):

            input_file = video_file_dir + filename
            output_file = output_file_dir + 'padded-' + filename
            # os.system("ffmpeg -i %s -filter_complex 'scale=1328:747, pad=1920:1080:296:150' %s" % (input_file, output_file))
            os.system("ffmpeg -i %s -filter_complex '[0:v]split=2[blur][vid];[blur]scale=1920:1080,"
                      "boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,ch)/20:chroma_power=1["
                      "bg];[vid]scale=1328:747:force_original_aspect_ratio=decrease[ov];[bg][ov]overlay=(W-w)/2:("
                      "H-h)/2' %s" % (input_file, output_file))


            video_item['padded'] = 'padded-' + filename
    except Exception as error:
        print(error)


with open(worksheet, 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(video_list)

    f.close()