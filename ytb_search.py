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
                                    publishedAfter='2019-07-27T00:00:00Z'
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
                                      pageToken=next_page_token)
    response_2 = request_2.execute()

    response['items'] = response['items'] + response_2['items']
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
    saving_path = Path('./ytb_result')
    keywords = ['nct dream', 'boom', 'reaction', 'dance', 'cover', 'lyrics', 
                'sub', 'audio', 'mix', 'mashup', 'edited', 'fan', 'renjun', 
                'jeno', 'haechan', 'jaemin', 'jisung', 'chenle',
                '#nctdream', '#boom', '#we_boom', '#renjun', '#jeno', 
                '#haechan', '#jaemin', '#jisung', '#chenle']
    for keyword in keywords:
        print("Searching {}".format(keyword))
        ytb_search(q=keyword, saving_path=saving_path)



