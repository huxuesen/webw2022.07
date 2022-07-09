from django.db import models


class SystemMailSetting(models.Model):
    mail_server = models.CharField(max_length=32,
                                   null=False,
                                   default='localhost',
                                   verbose_name='邮箱服务器')
    mail_port = models.IntegerField(null=False, default=25, verbose_name='端口')
    mail_username = models.CharField(max_length=64,
                                     null=False,
                                     default='默认用户名',
                                     verbose_name='用户名')
    mail_sender = models.CharField(max_length=64,
                                   null=False,
                                   default='默认用户名@mail.com',
                                   verbose_name='发件人')
    mail_password = models.CharField(max_length=64,
                                     null=False,
                                     default='默认密码',
                                     verbose_name='密码')

    class Meta:
        verbose_name = "系统邮箱"
        verbose_name_plural = "系统邮箱"

    def __str__(self):
        return self.mail_server


class Notification(models.Model):
    type_choice = ((0, 'Bark'), (1, '自定义通知'), (2, '邮箱'), (3, '微信'), (4, 'Telegram'))
    name = models.CharField(max_length=32,
                            null=False,
                            verbose_name='通知方式名称',
                            unique=True,
                            default='默认名称')
    type = models.IntegerField(null=False,
                               choices=type_choice,
                               default='邮箱',
                               verbose_name='通知方式类型')
    content = models.CharField(max_length=512,
                               null=False,
                               verbose_name='Key / 自定义Url'
                               )

    class Meta:
        verbose_name = "通知方式"
        verbose_name_plural = "通知方式"

    def __str__(self):
        return self.name


class Log(models.Model):
    class Meta:
        verbose_name = "日志查看"
        verbose_name_plural = "日志查看"


class TelegramSetting(models.Model):
    token = models.CharField(max_length=100,
                             null=False,
                             verbose_name='Telegram Bot Token')

    class Meta:
        verbose_name = "Telegram Bot 设置"
        verbose_name_plural = "Telegram Bot 设置"

    def __str__(self):
        return 'Telegram Bot ' + self.token
