from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# class UserManager(BaseUserManager):
#     use_in_migrations = True

#     def createUser(self, email,nickname,password=None):
#         if not email:
#             raise ValueError('E-mail은 필수입니다')

#         user = self.model(
#             email = self.normalize_email(email),
#             nickname = nickname,
#         )

#         user.is_admin = False
#         user.is_superuser = False
#         user.is_staff = False
#         user.is_active = True

#         user.set_password(password)
#         user.save(using=self._db)

#         return user

# class CommunityUser(AbstractBaseUser,PermissionsMixin):
#     objects = UserManager()

#     email = models.EmailField(  #email 모델 따로 존재
#         max_length = 100,   #길이 설정
#         null = False,       #빈 값 안됩니다
#         unique = True,      #고유한 값이어야 합니다
#         verbose_name = "E-mail"
#     )

#     nickname = models.CharField(
#         max_length = 10,
#         null = False,
#         unique = True,
#         verbose_name = 'Nickname'
#     )

#     # like_post = models.ManyToManyField(to = Post, related_name = 'likers')

#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)

#     date_joined = models.DateTimeField(verbose_name='date_joined',auto_now_add=True)
#     last_login = models.DateTimeField(verbose_name='last_login',auto_now=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['nickname']

#     class Meta:

#         verbose_name = ('user')
#         verbose_name_plural = ('users')

#         def __str__(self):
#             return self.nickname
