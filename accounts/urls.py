from django.urls import path
from .views import ( 
    login_view, 
    logout_view, 
    home_view,
    libros_view,
    prestaciones_view,
    generos_view,
    crear_prestacion_view,
    crear_devolucion_view,
)


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
    
    path('libros/', libros_view, name='libros'),
    path('prestaciones/', prestaciones_view, name='prestaciones'),
    path('prestaciones/nueva/', crear_prestacion_view, name='crear_prestacion'),
    path('generos/', generos_view, name='generos'),
    path('devoluciones/nueva/',crear_devolucion_view,name='crear_devolucion'),
    
    
]
