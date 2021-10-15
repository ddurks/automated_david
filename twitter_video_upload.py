import os
import sys
from twitter_api import get_credentials
from TwitterAPI import TwitterAPI

def post_video_status(file_path, text=''):
    creds = get_credentials()
    twitter = TwitterAPI(creds['CONSUMER_KEY'], creds["CONSUMER_SECRET"], creds['ACCESS_TOKEN'], creds['ACCESS_TOKEN_SECRET'])

    bytes_sent = 0
    total_bytes = os.path.getsize(file_path)
    file = open(file_path, 'rb')

    def check_status(r):
        if r.status_code < 200 or r.status_code > 299:
            print(r.status_code)
            print(r.text)
            sys.exit(0)

    # initialize media upload and get a media reference ID in the response
    r = twitter.request('media/upload', {'command':'INIT', 'media_type':'video/mp4', 'total_bytes':total_bytes})
    check_status(r)

    media_id = r.json()['media_id']
    segment_id = 0

    # start chucked upload
    while bytes_sent < total_bytes:
        chunk = file.read(4*1024*1024)

        # upload chunk of byets (5mb max)
        r = twitter.request('media/upload', {'command':'APPEND', 'media_id':media_id, 'segment_index':segment_id}, {'media':chunk})
        check_status(r)
        segment_id = segment_id + 1
        bytes_sent = file.tell()
        print('[' + str(total_bytes) + ']', str(bytes_sent))

    # finalize the upload
    r = twitter.request('media/upload', {'command':'FINALIZE', 'media_id':media_id})
    check_status(r)

    # post Tweet with media ID from previous request
    r = twitter.request('statuses/update', {'status':text, 'media_ids':media_id})
    check_status(r)