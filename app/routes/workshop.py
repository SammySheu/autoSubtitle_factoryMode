from flask import Blueprint, render_template, request, jsonify
from app.module.db import Video, addVideo, updateVideo

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from werkzeug.utils import secure_filename
import os
import datetime
import json

workshop = Blueprint('workshop', __name__)

@workshop.route('/', methods=['GET'])
@jwt_required()
def workshopGet():
    payload = get_jwt_identity()
    dbVideos = Video.query.filter(Video.video_owner == payload['user_id'])
    workshopVideos = []
    userVideos = []
    for row in dbVideos:
        if row.is_converted:
            workshopVideos.append( [row.video_url, row.srt_url] )
        else: 
            userVideos.append( [row.video_url, row.srt_url] )
    return render_template('workshop_page.html', user_videos = userVideos, workshop_videos = workshopVideos)


@workshop.route('/upload-video', methods=['POST'])
@jwt_required()
def upload():
    file = request.files['file_from_user']
    time_now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S_')
    file_name = time_now + secure_filename(file.filename)
    file_path = os.path.join( 'app/','userFiles', file_name)
    payload = get_jwt_identity()
    file.save(file_path)
    video = Video(
        video_name  = file_name,
        video_url   = file_path,
        video_owner = payload['user_id']
    )
    addVideo(video)
    return jsonify(msg = 'Upload successfully'), 200

@workshop.route('/add-subtitles', methods=['POST'])
@jwt_required()
def add_subtitles():
    video_path = json.loads(request.data)
    video_name = video_path.split('/')[1].split('.')[0]
    files =  os.listdir('app/srtFiles/')
    if (f'{video_name}.srt') in files:
        msg = 'SRT already exist'
    else:
        msg = 'Successfully add subtitles'
        os.system(f'autosub -S zh-TW -D zh-TW -o ./app/srtFiles/{video_name}.srt ./app/{video_path}')
        video_to_update = Video.query.filter(Video.video_url == f'app/{video_path}').first()
        video_to_update.srt_url = f'app/srtFiles/{video_name}.srt'
        updateVideo()
    return jsonify(msg)

@workshop.route('/update-subtitles', methods=['POST'])
def update_subtitles():
    videoPath = request.form.get("video_path")
    videoName_wo_ext = videoPath.split('/')[1].split('.')[0]
    with open(f'app/srtFiles/{videoName_wo_ext}.srt', 'r') as f:
        content = f.readlines()
        index = 1
        for i in range(2, len(content), 4):
            content[i] = f'{request.form[str(index)]}\n'
            index += 1
    content = ''.join(content)
    with open(f'app/srtFiles/{videoName_wo_ext}.srt', 'w') as f:
        f.write(content)

    return jsonify('Update subtitles successfully')

@workshop.route('/merge-subtitles', methods=['POST'])
def merge_subtitles():
    video_path = json.loads(request.data)
    video_to_update = Video.query.filter_by(video_url = f'app/{video_path}').first()
    video_name = video_path.split('/')[1].split('.')[0]
    
    if video_to_update.is_converted:
        os.system(f'rm {video_path}')
        os.system(f"ffmpeg -y -i userFiles/{video_name}.mp4 -vf 'subtitles=./srtFiles/{video_name}.srt' ./workshopFiles/{video_name}.mp4")
    else:
        video_to_update.video_url = 'app/workshopFiles/' + video_path.split('/')[1]
        video_to_update.is_converted = True
        updateVideo()
        os.system(f"ffmpeg -y -i app/{video_path} -vf 'subtitles=./app/srtFiles/{video_name}.srt' ./app/workshopFiles/{video_name}.mp4")

    # os.system(f'rm {video_path}')
    return jsonify('Merge Successfully')


@workshop.route('/edit-subtitles/<videoDirectory>/<videoName>', methods=['GET'])
def edit_subtitles(videoDirectory, videoName):
    videoPath = videoDirectory + '/' + videoName
    videoName_wo_ext = videoName.split('.')[0]
    with open(f'app/srtFiles/{videoName_wo_ext}.srt', 'r', encoding='UTF-8') as f:
        lines = []
        while True:
            line = []
            [line.append(f.readline().strip()) for i in range(3)]
            lines.append(line)
            if not f.readline():
                break
    return render_template('edit_subtitles.html', lines = lines, videoPath = videoPath)

