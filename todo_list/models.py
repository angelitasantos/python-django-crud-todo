from django.db import models
from django.utils.safestring import mark_safe


class Todo(models.Model):
    choices_category = (    ('T', 'Trabalho'),
                            ('E', 'Estudo'),
                            ('L', 'Lazer'))
    choices_status = (  ('N', 'Não Iniciada'),
                        ('E', 'Em Andamento'),
                        ('F', 'Finalizada'))
    category = models.CharField(max_length=1, choices=choices_category, default="T")
    status = models.CharField(max_length=1, choices=choices_status, default="N")
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description

    def icon(self):
        if self.status == "N":
            classe = 'status-vermelho'
        elif self.status == "E":
            classe = 'status-amarelo'
        elif self.status == "F":
            classe = 'status-verde'

        icon = f'''<svg  class="{classe}" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bookmark-fill" viewBox="0 0 16 16">
                                    <path d="M2 2v13.5a.5.5 0 0 0 .74.439L8 13.069l5.26 2.87A.5.5 0 0 0 14 15.5V2a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2z"/>
                    </svg>'''

        return mark_safe(icon)