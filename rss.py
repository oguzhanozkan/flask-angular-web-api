import feedparser 
from dateutil import parser
import pandas as pd
import time
import os
import csv_import_mongo
from datetime import datetime
import find_different

url = [
    "http://www.mynet.com/haber/rss/sondakika",
    "http://www.haberturk.com/rss/manset.xml",
    "https://www.cnnturk.com/feed/rss/all/news",
    "https://www.sabah.com.tr/rss/gundem.xml",
    "https://www.ahaber.com.tr/rss/son24saat.xml",
    "https://www.ntv.com.tr/son-dakika.rss",
    "http://feeds.bbci.co.uk/turkce/rss.xml"
]

rss_feed = []

def rss_feed_from_url_and_save_csv(url, fname):
    for link in url:
        haberler = feedparser.parse(link)
        location = link.split(".", 2)[1]
        for haber in haberler.entries:
            date_f1 = parser.parse(haber.updated)
            date_f2_string = str(date_f1)
            news_date_str = date_f2_string[0:16]
            news_date = datetime.strptime(news_date_str, '%Y-%m-%d %H:%M')
            rss_feed.append((haber.title, haber.link, haber.description, news_date, location))

    df = pd.DataFrame(rss_feed, columns=['title', 'link', 'description', 'updated', 'location'])
    df.to_csv(fname, encoding="utf-8")


rss_feed_from_url_and_save_csv(url, 'haberler.csv')
data_first_insert = pd.read_csv('haberler.csv')

data_first_insert = data_first_insert.loc[:, ~data_first_insert.columns.str.contains('^Unnamed')]
data_first_insert['updated'] = data_first_insert['updated'].astype('datetime64[ns]')

csv_import_mongo.insert_data(data_first_insert)


while(True):

    print('15 dakika bekeleme başladı')
    time.sleep(900)
    print('15 dakika bekleme bitti')
    print('haberler_secon.csv dosyası olusturuldu')
    rss_feed_from_url_and_save_csv(url, 'haberler_second.csv')
    data_haberler_second = pd.read_csv('haberler_second.csv')
    data_haberler_second['updated'] = data_haberler_second['updated'].astype('datetime64[ns]')
    print('haberler_second.csv ve haberler.csv arasındaki faklar bulundu ve different.csv olarak kaydedildi')
    find_different.find_difference_to_between_two_dataframe(data_first_insert, data_haberler_second)
    print('different.csv dosyası okundu')
    data_different = pd.read_csv('different.csv')
    print('difrent.csv dosyasından Unnamed clonu atıldı')
    data_different = data_different.loc[:, ~data_different.columns.str.contains('^Unnamed')]
    print('different.csv nin updated kolonunun tipi datetime yapıldı')
    data_different['updated'] = data_different['updated'].astype('datetime64[ns]')

    data_different = data_different.drop_duplicates()
    print('data_different mongodb ye import edildi')
    csv_import_mongo.insert_data(data_different)

    print('haberler.csv ve different.csv dosyaları birleştirldi')
    data_haberler_with_data_different = data_first_insert.append(data_different)

    print('csv uzantılı dosyalar silindi')
    os.remove('haberler_second.csv')
    os.remove('haberler.csv')
    os.remove('different.csv')

    print('haberler.csv dosyası oluşturuldu ve tekrarlanan değerler atıldı')
    data = data_haberler_with_data_different.drop_duplicates()
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
    data['updated'] = data['updated'].astype('datetime64[ns]')
    data.to_csv('haberler.csv', encoding="utf-8")

