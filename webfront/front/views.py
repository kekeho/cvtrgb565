import os
import sys
import glob
import shutil
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.conf import settings
import zipfile
CURRENT_DIRNAME = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIRNAME + '/../../')
import cvtrgb565


def front(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'index.html', context)
    elif request.method == 'POST':
        upload_file = request.FILES['file']
        file_name = default_storage.save(upload_file.name, upload_file)
        zip_filename = os.path.join(settings.MEDIA_ROOT, file_name)
        save_dir = ''.join(zip_filename.split('.')[:-1]) + '/'

        try:
            with zipfile.ZipFile(zip_filename) as zip_file:
                zip_file.extractall(save_dir)
        except zipfile.BadZipfile:
            os.remove(zip_filename)
            context = {'error': 'ZIPファイルではないものがアップロードされました'}
            return render(request, 'index.html', context)

        # erase uploaded zip file
        os.remove(zip_filename)

        directory = os.path.join(save_dir, '*.png')
        img_list = glob.glob(directory)
        tft_files_list = [''.join(x.split('.')[:-1])+'.tft' for x in img_list]

        for file in img_list:
            image = cvtrgb565.ImageClass(file)
            image.save()

        converted_zip_filename = settings.MEDIA_ROOT + '/cvt_' + file_name
        with zipfile.ZipFile(converted_zip_filename, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
            [new_zip.write(x, arcname=os.path.basename(x)) for x in tft_files_list]

        # erase extracted files
        shutil.rmtree(save_dir)

        context = {'download_url': settings.MEDIA_URL + 'cvt_' + file_name}
        return render(request, 'index.html', context)
