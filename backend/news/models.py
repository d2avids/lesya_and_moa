from django.db import models


def news_files_path(instance, filename) -> str:
    """Функция для формирования пути сохранения изображения.

    :param instance: Экземпляр модели.
    :param filename: Имя файла.
    :return: Путь к файлу.
    """
    filename = filename.split('.')
    last_news_instance = News.objects.last()
    instance_id = last_news_instance.id+1 if last_news_instance else 1
    return f'news/{instance_id}/{filename[0][:20]}.{filename[1]}'


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    image = models.ImageField(verbose_name='Изображение', upload_to=news_files_path)
    description = models.CharField(max_length=500, verbose_name='Краткое содержание')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
