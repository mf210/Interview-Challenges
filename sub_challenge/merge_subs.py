import webvtt
import xlsxwriter


def merge_captions():
    en_captions = webvtt.read('en_70105212.vtt').captions
    en_cap_id = 0
    for de_caption in webvtt.read('de_70105212.vtt'):
        sub_time = de_caption.start.split('.')[0]
        de_sub = de_caption.text
        en_sub = en_captions[en_cap_id].text
        en_cap_id += 1
        try:
            while en_captions[en_cap_id].end_in_seconds <= (de_caption.end_in_seconds + 1):
                en_sub += ' ' + en_captions[en_cap_id].text
                en_cap_id += 1
        except IndexError:
            break
            
        yield (sub_time, en_sub, de_sub)

    yield (sub_time, en_sub, de_sub)

############# write excel file #############
work_book = xlsxwriter.Workbook('output.xlsx')
work_sheet = work_book.add_worksheet('Subtitles')
row = 0
# Header of worksheet
work_sheet.write(row, 0, 'Time')
work_sheet.write(row, 1, 'Subtitle')
work_sheet.write(row, 2, 'Translation')
row += 1
# Write all data
for data in merge_captions():
    work_sheet.write(row, 0, data[0])
    work_sheet.write(row, 1, data[1])
    work_sheet.write(row, 2, data[2])
    row += 1
work_book.close()