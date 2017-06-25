#-*-coding:utf-8-*-
from django.db import models

# Create your models here.

class UserInfo(models.Model):
    # 用户名 1个字节可以储存1个英文字母或者半个汉字，换句话说，1个汉字占据2个字节的存储空间
    uname=models.CharField(max_length=20)
    # 用户密码 sha1加密的字符串长度 40
    upwd=models.CharField(max_length=40)
    # 邮箱
    uemail=models.CharField(max_length=30)
    # 收件人
    ushou=models.CharField(max_length=20,default='')
    # 收件地址
    uaddress=models.CharField(max_length=100,default='')
    # 收件邮编
    uyoubian=models.CharField(max_length=6,default='')
    # 收件人手机
    uphone=models.CharField(max_length=11,default='')

    #default,blank是python层面的约束，不影响数据表结构




