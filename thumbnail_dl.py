import os
from googleapiclient.discovery import build
import requests

# YouTube Data API v3を初期化
api_key = 'AIzaSyBI70xk9YKm8zKT91oEoJ_tWNLn-O5wilw'
youtube = build('youtube', 'v3', developerKey=api_key)

def get_playlist_video_ids(playlist_id):
    video_ids = []

    # プレイリスト内の最初のページの動画を取得
    playlist_items = youtube.playlistItems().list(
        part='snippet',
        maxResults=50,  # ページごとの最大結果数
        playlistId=playlist_id
    ).execute()

    # 各動画のvideo_idを取得
    for item in playlist_items['items']:
        video_id = item['snippet']['resourceId']['videoId']
        video_ids.append(video_id)

    # プレイリストの次のページが存在する場合、続きの動画を取得
    while 'nextPageToken' in playlist_items:
        next_page_token = playlist_items['nextPageToken']
        playlist_items = youtube.playlistItems().list(
            part='snippet',
            maxResults=50,
            playlistId=playlist_id,
            pageToken=next_page_token
        ).execute()

        for item in playlist_items['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_ids.append(video_id)

    return video_ids

def get_video_thumbnail(video_id, output_dir):
    try:
        # 動画の詳細情報を取得
        video_response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        # サムネイル情報を取得
        thumbnails = video_response['items'][0]['snippet']['thumbnails']

        # サムネイルURLを取得
        thumbnail_url = thumbnails['maxres']['url'] if 'maxres' in thumbnails else thumbnails['high']['url']

        # サムネイルをダウンロード
        response = requests.get(thumbnail_url)

        # ファイルの保存先ディレクトリを作成
        os.makedirs(output_dir, exist_ok=True)

        # ファイルパスを生成
        file_name = os.path.join(output_dir, f'{video_id}_thumbnail.jpg')

        # サムネイルをファイルに保存
        with open(file_name, 'wb') as f:
            f.write(response.content)

        print(f'Saved thumbnail for video {video_id} to {file_name}')

    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    video_ids = get_playlist_video_ids(playlist_id="PLnxIuXySyoibyDJtvzxklXJTX3__yft7d")
    for ids in video_ids:
        print(f"サムネイルのダウンロードを開始しました。\nvideo_id = {ids}")
        get_video_thumbnail(video_id=ids, output_dir='E:\歌も歌ってるよ～！')
        print(f"サムネイルのダウンロードを終了しました。\nvideo_id = {ids}")

