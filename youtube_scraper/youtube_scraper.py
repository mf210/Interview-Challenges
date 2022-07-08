import os

import xlsxwriter
from googleapiclient.discovery import build


api_key = os.environ.get('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)
channels_id = set()
next_page_token = None

# collect the channels id related to a particular query
for _ in range(1):
    request = youtube.search().list(
        part='snippet',
        q='learning english',
        type='channel',
        pageToken=next_page_token
    )
    response = request.execute()
    next_page_token = response['nextPageToken']
    channels_id.update(item['snippet']['channelId'] for item in response['items'])

# get the subscriber_count, custom_url of each channel 
request = youtube.channels().list(
        part='id,snippet,statistics',
        id=','.join(channels_id)
    )
response = request.execute()

############# write excel file #############
work_book = xlsxwriter.Workbook('output.xlsx')
work_sheet = work_book.add_worksheet('Channels')
row = 0
# Header of worksheet
work_sheet.write(row, 0, 'Title')
work_sheet.write(row, 1, 'Subscribers Count')
work_sheet.write(row, 2, 'Link')
row += 1
# Write all data
for item in response['items']:
    work_sheet.write(row, 0, item['snippet'].get('title'))
    work_sheet.write(row, 1, item['statistics'].get('subscriberCount', 'hidden'))
    work_sheet.write(row, 2, f"https://www.youtube.com/channel/{item['id']}")
    row += 1
work_book.close()