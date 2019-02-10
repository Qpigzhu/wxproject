from django.db import models

# Create your models here.

class Wx(models.Model):
    code_img = models.CharField(default="",max_length=300,null=True,blank=True,verbose_name="二维码")
    code = models.CharField(max_length=50,verbose_name="卡密")

    class Meta:
        verbose_name = "微信二维码管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
