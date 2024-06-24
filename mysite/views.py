from django.shortcuts import render
from django.http  import HttpResponse

from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import re

def  index(request):
    return render(request, 'index.html')
    