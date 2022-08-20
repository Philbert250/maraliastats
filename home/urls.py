from django.urls import path
from .import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    path('', views.welcome, name='home'),
    path('/signin', views.signin, name='signing'),
    path('/signin', views.logout_user, name='logout_user'),
    path('/generaldata', views.generaldata, name='general'),
    path('/allcase', views.allcase, name='all_case'),
    path('<int:id>/deletecase/', views.delcase, name='deleteCase'),
    path('<int:id>/updatecase/', views.updatecase, name='updateCase'),
    path('/severecase', views.severecase, name='all_severe'),
    path('<int:id>/deletesevere/', views.delsevere, name='deleteSevere'),
    path('<int:id>/updatesevere/', views.updatesevere, name='updateSevere'),
    path('/deathcase', views.deathcase, name='all_death'),
    path('<int:id>/deletedeath/', views.deldeath, name='deleteDeath'),
    path('<int:id>/updatecdeath/', views.updatedeath, name='updateDeath'),
    path('/upgradecase', views.upgradecase, name='upgrade_case'),
    path('/upgradesevere', views.upgradesevere, name='upgrade_severe'),
    path('/upgradedeath', views.upgradedeath, name='upgrade_death')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)