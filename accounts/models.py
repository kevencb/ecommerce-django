from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

# Clases para crear un nuevo usuario y un super usuario
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('E-mail no encontrado.')
        if not username:
            raise ValueError('Username no encontrado.')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        
        user.set_password(password) # Pasamos el password
        user.save(using = self._db) # Registramos el usuario en la DB
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        
        user.is_admin =  True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using = self._db)
        return user
        

# Esta clase se va a extender desde AbstractBaseUser
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)
    
    # Campos por defecto por django
    date_joined = models.DateTimeField(auto_now=True) #Fecha en la que se esta creando el usuario
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    # Indicamos como queremos que sea el proceso de resgistro y que datos son obligatorios
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    # Incluimos nuestros metodos para crear un usuario y un super usuario instanciando esta clase
    objects = MyAccountManager()
    
    # Cremos el label en las tablas de registro al momento de listar
    def __str__(self):
        return self.email
    
    # Esta función nos permite saber si tiene perfil de administrador y solo si es admin va tener permisos para reealizar modificaciones y acceso a los mòdulos
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
    
    
    