# -*- coding: utf-8 -*-
import os
from pathlib import Path

import pandas as pd
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

def ytb_search(q, saving_path):
    request = youtube.search().list(part="snippet",
                                    maxResults=50,
                                    q=q,
                                    order="date",
                                    publishedBefore='2019-08-03T00:00:00Z',
                                    publishedAfter='2019-07-27T00:00:00Z',
                                    type="video"
                                    )
    response = request.execute()
    next_page_token = response['nextPageToken']
    # next page
    request_2 = youtube.search().list(part="snippet",
                                      maxResults=50,
                                      q=q,
                                      order="date",
                                      publishedBefore='2019-08-03T00:00:00Z',
                                      publishedAfter='2019-07-27T00:00:00Z',
                                      type="video",
                                      pageToken=next_page_token)
    response_2 = request_2.execute()
    next_page_token = response_2['nextPageToken']

    request_3 = youtube.search().list(part="snippet",
                                      maxResults=50,
                                      q=q,
                                      order="date",
                                      publishedBefore='2019-08-03T00:00:00Z',
                                      publishedAfter='2019-07-27T00:00:00Z',
                                      type="video",
                                      pageToken=next_page_token
                                      )
    response_3 = request_3.execute()
    next_page_token = response_3['nextPageToken']

    request_4 = youtube.search().list(part="snippet",
                                      maxResults=50,
                                      q=q,
                                      order="date",
                                      publishedBefore='2019-08-03T00:00:00Z',
                                      publishedAfter='2019-07-27T00:00:00Z',
                                      type="video",
                                      pageToken=next_page_token
                                      )
    response_4 = request_4.execute()

    response['items'] = response['items'] + response_2['items'] + response_3['items'] + response_4['items'] 
    video_info = []
    video_num =len(response['items'])
    print("    {} videos found".format(video_num))
    for i in range(video_num):
        try:
            video_id = response['items'][i]['id']['videoId']
        except KeyError:
            print("    Skip a {}".format(response['items'][i]['id']['kind']))
            continue
        response['items'][i]['snippet']['videoId'] = video_id
        video_info.append(response['items'][i]['snippet'])

    video_df = pd.DataFrame(video_info)[['videoId', 'publishedAt', 'channelId', 
                                        'channelTitle', 'title', 'description']]
    video_df_uoff = video_df[(video_df.channelId != 'UCPde4guD9yFBRzkxk2PatoA') &
                             (video_df.channelId != 'UCS_hnpJLQTvBkqALgapi_4g') &
                             (video_df.channelId != 'UCeLPm9yH_a_QH8n6445G-Ow') &
                             (video_df.channelId != 'UCG-coSVp89xFSWN4pbVL53w') &
                             (video_df.channelId != 'UCZ2gVH8X4ukWLRZ5yDda_4w')
                            ]
    video_df.to_csv(saving_path.joinpath(q+'.csv'), index=None, encoding='utf-8')


if __name__ == '__main__':
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "./client_secret_shawn.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    saving_path = Path('./ytb_result_2')
    keywords = [
                'nct dream', 'boom', 'nct dream AND reaction', 
                'nct dream AND dance', 'nct dream AND cover', 
                'nct dream AND lyrics', 'nct dream AND sub', 
                'nct dream AND audio', 'nct dream AND mix', 
                'nct dream AND mashup'
                'nct dream AND edit', 
                'nct dream AND fan', 'nct dream AND fancam', 'renjun', 
                'jeno', 'haechan', 'jaemin', 'jisung', 'chenle',
                '#nctdream', '#boom', 
                '#we_boom', '#renjun', '#jeno', 
                '#haechan', '#jaemin', '#jisung', '#chenle']
    for keyword in keywords:
        print("Searching {}".format(keyword))
        ytb_search(q=keyword, saving_path=saving_path)
