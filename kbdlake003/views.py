from django.shortcuts import render
from django.http import HttpResponse
from django.http import FileResponse
import os
import glob
import datetime

# application/write_data.pyをインポートする
from .application import write_data

# Create your views here.
def index(request):
    return render(request, 'kbdlake003/index.html')

# ajaxでurl指定したメソッド
def get_blob(req):
    data = write_data.get_kbd_blob_list_search(req.GET.get("container"),req.GET.get("txt"))
    result=','.join(data)
    return HttpResponse(result)

def download_blob(req):

    path = os.getcwd()+'/kbdlake003/application/download'
    # 古いファイルは削除
    now = datetime.datetime.today()# 現在の日付を取得
    for file in glob.glob(path+'\*', recursive=True):
        t = os.path.getmtime(file)
        mtime = datetime.datetime.fromtimestamp(t)
        if(now - mtime).days >= 1: # 1日以上経過している場合は削除
            os.remove(file)

    # 空のフォルダは削除
    files = glob.glob(path+'\**', recursive=True)
    for file in files:
        try:
            os.rmdir(file)
        except OSError as e:
            pass

    folder_path = os.path.dirname(os.getcwd()+'/kbdlake003/application/download/'+req.GET.get("blob"))    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Blob取得 download_kbd_blob(container_name, blob_file_name, download_file_path)
    write_data.download_kbd_blob(req.GET.get("container"),req.GET.get("blob"),os.getcwd()+'/kbdlake003/application/download/'+req.GET.get("blob"))
    filename = os.path.basename(os.getcwd()+'/kbdlake003/application/download/'+req.GET.get("blob"))
    filepath = os.getcwd()+'/kbdlake003/application/download/'+req.GET.get("blob")
    return FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)
