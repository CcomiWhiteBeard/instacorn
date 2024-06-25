from django.db import models

# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    print( )
    print('class Person(models.Model):', first_name, 'last_name=', last_name, 'age=', age)

    def __str__(self) -> str:
        return self.from_name + '' + self.last_name+'' + self.age
    
