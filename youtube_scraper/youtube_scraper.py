import os

import xlsxwriter
from googleapiclient.discovery import build


api_key = os.environ.get('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)
query = 'learning english'
channels_id = set()
next_page_token = None
all_channel_items = []

for _ in range(3):
    # collect the channels id related to a particular query
    for _ in range(10):
        request = youtube.search().list(
            part='snippet',
            q=query,
            type='channel',
            pageToken=next_page_token
        )
        response = request.execute()
        next_page_token = response['nextPageToken']
        channels_id.update(item['snippet']['channelId'] for item in response['items'])

    # get the subscriber_count, custom_url of each channel 
    request = youtube.channels().list(
            part='statistics',
            id=','.join(channels_id)
        )
    channels_id.clear()
    response = request.execute()
    all_channel_items.extend(response['items'])

############# write excel file #############
work_book = xlsxwriter.Workbook('output.xlsx')
work_sheet = work_book.add_worksheet('Channels')
row = 0
# Header of worksheet
work_sheet.write(row, 0, 'Subscribers Count')
work_sheet.write(row, 1, 'Link')
row += 1
# Write all data
for item in all_channel_items:
    work_sheet.write(row, 0, item['statistics'].get('subscriberCount', 'hidden'))
    work_sheet.write(row, 1, f"https://www.youtube.com/channel/{item['id']}")
    row += 1
work_book.close()