from django.db import models

# Create your models here.




class default_images(models.Model):
    objects=None
    id=models.AutoField(primary_key=True)
    image=models.ImageField(upload_to='images')
    
    class Meta:
        db_table='default_images'
    

class user_upload(models.Model):
    objects=None
    id=models.AutoField(primary_key=True)    
    image=models.ImageField(upload_to='user_upload')

    class Meta:
        db_table='user_upload'

class generated_memes(models.Model):
    objects=None
    id=models.AutoField(primary_key=True)    
    image=models.ImageField(upload_to='memes')

    class Meta:
        db_table='meme_generated'