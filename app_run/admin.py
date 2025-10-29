from django.contrib import admin

# Register your models here.
from .models import Run
from .models import AthleteInfo
from .models import Challenge

admin.site.register(Run)
admin.site.register(AthleteInfo)
admin.site.register(Challenge)
