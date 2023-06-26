from django.shortcuts import render
from django.shortcuts import redirect
from django.db import transaction
from PIL import Image, ImageDraw, ImageFont
import textwrap
from .models import *
from .forms import *
from django.conf import settings


# Create your views here.



def home(request):
    data=default_images.objects.all()
    context={"data":data}
    return render(request, "home.html",context)

def customise(request,id,slug):
    if slug == "default":
        data=default_images.objects.get(id=id)
    else:
        data=user_upload.objects.get(id=id)
    context={"data":data, "id":id, "slug":slug}
    return render(request, "customise.html",context)             


def user_uploads(request):
    try:
        with transaction.atomic():
            if request.method=="POST":
                form = CustomUploadForm(request.POST  or None , request.FILES  or None)
                if form.is_valid():
                    save = form.save()
                    return redirect('customise', id=save.id, slug="uploaded")  
                return redirect('home')    
    except Exception as e:
        context={"exception":e}
        return render(request, 'exception.html',context) 

def generate(request,id,slug):
    if request.method == "POST":
        cp1 = request.POST.get('cap_1')
        cp2 = request.POST.get('cap_2')
        cp3 = request.POST.get('cap_3')
        color = request.POST.get('color')
        if slug == "default":
            data=default_images.objects.get(id=id)
        else:
            data=user_upload.objects.get(id=id)
        im = Image.open(f"media/{data.image}")
        draw = ImageDraw.Draw(im)
        image_width, image_height = im.size
        font_path = str(settings.BASE_DIR / 'impact' / 'impact.ttf')
        font = ImageFont.truetype(font=font_path, size=int(image_height/10))
        char_width, char_height = font.getsize('A')
        chars_per_line= image_width // char_width

        top_text = cp1.upper()
        mid_text = cp2.upper()
        bottom_text = cp3.upper()

        top_lines= textwrap.wrap(top_text, width=chars_per_line)
        mid_lines= textwrap.wrap(mid_text, width=chars_per_line)
        bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line)

        y=10
        for line in top_lines:
            line_width, line_height= font.getsize(line)
            x= (image_width - line_width)/2
            draw.text((x,y), line, fill=str(color), font=font)
            y+=line_height

        y = image_height // 2 - 15
        for line in mid_lines:
            line_width, line_height= font.getsize(line)
            x= (image_width - line_width)/2
            draw.text((x,y), line, fill=str(color), font=font)
            y+=line_height
        
        y= image_height - char_height * len(bottom_lines) - 15
        for line in bottom_lines:
            line_width, line_height= font.getsize(line)
            x= (image_width - line_width)/2
            draw.text((x,y), line, fill=str(color), font=font)
            y+=line_height
        save_path = "./media/meme/meme.jpg"
        db_path = "meme/meme.jpg"
        im.save(save_path)

        url = generated_memes.objects.create(image=db_path)
        return render(request, 'result.html', {"url":url})
    return render(request, 'result.html')
        