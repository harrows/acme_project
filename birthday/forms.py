# birthday/forms.py
from django import forms

from django.core.exceptions import ValidationError
from .validators import real_age
from .models import Birthday 
from django.core.mail import send_mail
from .models import Birthday, Congratulation

BEATLES = ['John Lennon', 'Paul McCartney', 'George Harrison', 'Ringo Starr']

# Для использования формы с моделями меняем класс на forms.ModelForm.
class BirthdayForm(forms.ModelForm):
    class Meta:
        model = Birthday
        exclude = ('author',)
    
    first_name = forms.CharField(label='Имя', max_length=20)
    last_name = forms.CharField(
        label='Фамилия', required=False, help_text='Необязательное поле'
    )
    birthday = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'}),
        # В аргументе validators указываем список или кортеж 
        # валидаторов этого поля (валидаторов может быть несколько).
        validators=(real_age,),
    )

    def clean(self):
        super().clean()
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        if f'{first_name} {last_name}' in BEATLES:
            # Отправляем письмо, если кто-то представляется 
            # именем одного из участников Beatles.
            send_mail(
                subject='Another Beatles member',
                message=f'{first_name} {last_name} пытался опубликовать запись!',
                from_email='birthday_form@acme.not',
                recipient_list=['admin@acme.not'],
                fail_silently=True,
            )
            raise ValidationError(
                'Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!'
            ) 
        

class CongratulationForm(forms.ModelForm):
    
    class Meta:
        model = Congratulation
        fields = ('text',) 