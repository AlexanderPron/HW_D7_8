from django.db import models
import uuid
from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy

class Author(models.Model):  
  full_name = models.TextField(verbose_name="Автор")  
  birth_year = models.SmallIntegerField(verbose_name="год рождения")  
  country = models.CharField(max_length=2, verbose_name="Страна")

  def __str__(self):
    return(self.full_name)
  
  class Meta:
    verbose_name = 'Автор'
    verbose_name_plural = 'Авторы'

class PublishingHouse(models.Model):
  name = models.TextField(verbose_name="Издательство")
  
  def __str__(self):
    return(self.name)
  
  class Meta:
    verbose_name = 'Издательство'
    verbose_name_plural = 'Издательства'

class Book(models.Model):  
  ISBN = models.CharField(max_length=13, verbose_name="ISBN")  
  title = models.TextField(verbose_name="Название")  
  description = models.TextField(verbose_name="Описание")  
  year_release = models.SmallIntegerField(verbose_name="Год издания")  
  author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
  copy_count = models.SmallIntegerField(default=1, verbose_name="Копий")
  price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Цена")
  ph_name = models.ForeignKey(PublishingHouse, on_delete=models.CASCADE, null=True, blank=True, related_name='books', verbose_name="Издательство")
  book_img = models.ImageField(upload_to='book_pics/%Y/%m/%d', blank=True, verbose_name="Изображение")
  def __str__(self):
    return(self.title)
  
  @property
  def pic_url(self):
    if self.book_img and hasattr(self.book_img, 'url'):
      return self.book_img.url
  
  class Meta:
    verbose_name = 'Книга'
    verbose_name_plural = 'Книги'
  
class Friend(models.Model):
  friend_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  first_name = models.CharField(max_length=100, verbose_name="Имя")
  last_name = models.CharField(max_length=100, verbose_name="Фамилия")
  mail = models.EmailField(max_length=254, verbose_name="Почта")  
  address = models.TextField(verbose_name="Адрес")  

  def __str__(self):
    return('{} {}'.format(self.last_name, self.first_name))
  
  class Meta:
    verbose_name = 'Друг'
    verbose_name_plural = 'Друзья'

class BookInUse(models.Model):
  book_title = models.ForeignKey(Book, on_delete=models.DO_NOTHING, related_name='books', verbose_name="Книга")
  user_id = models.ForeignKey(Friend, on_delete=models.DO_NOTHING, related_name='friends', verbose_name="Кто взял")
  start_use_date = models.DateField(auto_now=False, auto_now_add=False, default= date.today, verbose_name="Дата выдачи")

  def __str__(self):
    return('{}'.format(self.book_title))
  
  class Meta:
    verbose_name = 'В пользовании'
    verbose_name_plural = 'В пользовании'


class UserProfile(models.Model):  
  age = models.IntegerField()  
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  
  def __str__(self):
    return('{}(id-{})'.format(self.user.username, self.user_id))
  
  def get_absolute_url(self):
    return reverse('profile-show', args=[str(self.user_id)])
  
  class Meta:
    verbose_name = 'Профиль'
    verbose_name_plural = 'Профили'
