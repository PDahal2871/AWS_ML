from django.shortcuts import render,redirect, HttpResponse
import boto3
import os
from .forms import AWSForm
from .models import Aws
from django.core.files.storage import FileSystemStorage

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
aws_access_key_id= 'ASIATPQJ4OLPPPQYGGVZ'
aws_secret_access_key= 'rdy6ZrttLqMXfip9Z65Gq0zFifrGQXRAd0QXkTmw'
aws_session_token= 'FwoGZXIvYXdzEHoaDLdZTNVyTKwy5VeBSCLYAX4PuLnWOHgoaDh4SRsVcjRnR6KFy/CPfB/6IgOqfMu68Iwz0hCTEgRO2A/X6+m3ZGhHTBIjqNd7C1/zUdhSR/PIsZUX5MhB7Irh6FbI2Z//WV6dIZcydak1y8csA9UHSxLO3tn9+bXaH7Dh5j+SwjHg9sY+EO/G2kwLFuaBBeUEDROEFPUHqrUWZuhe+sTKVEpthUg/hiMG6f2Q5HnpVq/ng8scVXs8SzK4WOl1qML9VmoWQqkHRqTi19jVTrNkZAibPj4ENSzwni7Mf8IIYZ5Ei5iXVSyExCjXsd37BTItRQL+5IRK89JrGuJa0Y/4SMAQ+Lxo9IgaXZGQ2jzcbBc32rG2bBjIcs4RG9NO'

#def face_recognize(img_path):
client = boto3.client('rekognition', region_name='us-east-1', aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      aws_session_token=aws_session_token
                      )


def view(request, id):
    image = Aws.objects.get(id=id)
    media = os.path.join(BASE_DIR, 'media')
    file_path = os.path.join(media,str(image.pic))
    with open(file_path, 'rb') as image:
        response = client.detect_faces(Image={'Bytes': image.read()}, Attributes=['ALL'])
    for face in response['FaceDetails']:
        Gender = str(face['Gender']['Value'])
        Agerange = str(face['AgeRange']['Low']) + ' to ' + str(face['AgeRange']['High']) + ' years'
        for emotions in face['Emotions']:
            #print(emotions)
            if(emotions['Type'] == 'HAPPY'):
                Happy = str(emotions['Confidence']) + ' %'

            if (emotions['Type'] == 'SURPRISED'):
                Surprised = str(emotions['Confidence']) + ' %'

            if (emotions['Type'] == 'SAD'):
                Sad = str(emotions['Confidence']) + ' %'

            if (emotions['Type'] == 'CALM'):
                Calm = str(emotions['Confidence']) + ' %'

            if (emotions['Type'] == 'ANGRY'):
                Angry = str(emotions['Confidence']) + ' %'


        Sunglass = str(face['Sunglasses']['Value'])
        if(Sunglass == True):
            Sg = 'Have Sunglasses'
        else:
            Sg = "Dont have Sunglasses"

        Mustache = str(face['Mustache']['Value'])
        if(Mustache == True):
            Mt = "Have Mustache"
        else:
            Mt = "Dont have Mustache"

        Beard = str(face['Beard']['Value'])
        if (Beard == True):
            beard = "Have Beard"
        else:
            beard = "Dont have Beard"

    print("Image is ", str(image))
    return render(request,'view.html', {'gender' : Gender, 'agerange':Agerange, 'happy':Happy,
                                        'surprised':Surprised, 'sad':Sad, 'calm':Calm, 'angry' : Angry,
                                        'sg':Sg, 'mt':Mt, 'beard':beard,'image':image})


def upload(request):

    if request.method == 'POST':
        form = AWSForm(request.POST, request.FILES)
        if(form.is_valid()):
            form.save()
            return redirect('images')


    else:
        form = AWSForm()
    return render(request, 'index.html', {'form': form})


def display_images(request):
    if request.method == 'GET':
        # getting all the objects of hotel.
        images = Aws.objects.all()
        print("Images are ", images)
        return render(request, 'images.html',
                       {'images': images})


def delete(request, id):
    aws = Aws.objects.get(id=id)
    aws.delete()
    return redirect('/images')

def success(request):
    return HttpResponse('successfully uploaded')