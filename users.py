# ==============================================
# FILE: luxora_hotel/settings.py
# ==============================================
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key-here'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'users',
    'rooms',
    'bookings',
    'restaurant',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'luxora_hotel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'luxora_hotel.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'luxora_db',
        'USER': 'root',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'users:dashboard'
LOGOUT_REDIRECT_URL = 'users:login'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/luxora.log',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}

AUTH_USER_MODEL = 'users.User'

# ==============================================
# FILE: luxora_hotel/urls.py
# ==============================================
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('rooms/', include('rooms.urls')),
    path('bookings/', include('bookings.urls')),
    path('restaurant/', include('restaurant.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ==============================================
# FILE: users/models.py
# ==============================================
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('manager', 'Manager'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def is_manager(self):
        return self.role == 'manager'

# ==============================================
# FILE: rooms/models.py
# ==============================================
from django.db import models

class Room(models.Model):
    ROOM_TYPES = (
        ('standard', 'Standard'),
        ('deluxe', 'Deluxe'),
        ('suite', 'Suite'),
    )
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='rooms/', blank=True)

    def __str__(self):
        return f"{self.room_number} - {self.get_room_type_display()}"

# ==============================================
# FILE: bookings/models.py
# ==============================================
from django.db import models
from users.models import User
from rooms.models import Room

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.guest.username}"

# ==============================================
# FILE: restaurant/models.py
# ==============================================
from django.db import models
from users.models import User

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu/', blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_orders')
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    order_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='received')
    special_instructions = models.TextField(blank=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)

# ==============================================
# FILE: users/views.py
# ==============================================
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.utils.timezone import now
from .forms import UserRegistrationForm, UserProfileForm
from .models import User
from bookings.models import Booking
from rooms.models import Room
from restaurant.models import Order

def guest_required(view_func):
    decorated = user_passes_test(lambda u: u.is_authenticated and not u.is_manager(), login_url='users:login')(view_func)
    return decorated

def manager_required(view_func):
    decorated = user_passes_test(lambda u: u.is_authenticated and u.is_manager(), login_url='users:login')(view_func)
    return decorated

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'guest'
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('users:dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'guest/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'guest/profile.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'guest/login.html'
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_manager():
            return redirect('users:manager_dashboard')
        return redirect('users:dashboard')

@login_required
def dashboard(request):
    if request.user.is_manager():
        return redirect('users:manager_dashboard')
    upcoming = Booking.objects.filter(guest=request.user, status='confirmed', check_in__gte=now().date())
    recent_orders = Order.objects.filter(guest=request.user)[:3]
    return render(request, 'guest/dashboard.html', {'upcoming': upcoming, 'recent_orders': recent_orders})

@manager_required
def manager_dashboard(request):
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(is_available=True).count()
    total_bookings = Booking.objects.count()
    confirmed_bookings = Booking.objects.filter(status='confirmed').count()
    total_revenue = Booking.objects.filter(status__in=['confirmed','completed']).aggregate(Sum('total_price'))['total_price__sum'] or 0
    recent_bookings = Booking.objects.select_related('guest','room').order_by('-created_at')[:5]
    return render(request, 'admin/dashboard.html', {
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'total_bookings': total_bookings,
        'confirmed_bookings': confirmed_bookings,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
    })

# ==============================================
# FILE: users/forms.py
# ==============================================
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone', 'address']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address']

# ==============================================
# FILE: users/urls.py
# ==============================================
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='guest/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='guest/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='guest/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='guest/password_reset_complete.html'), name='password_reset_complete'),
]

# ==============================================
# FILE: users/apps.py
# ==============================================
from django.apps import AppConfig
from django.contrib.auth import get_user_model

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        User = get_user_model()
        if not User.objects.filter(username='manager').exists():
            User.objects.create_superuser(
                username='manager',
                email='manager@luxora.com',
                password='M@nager2026!',
                role='manager'
            )
            print("Default manager account created.")

# ==============================================
# FILE: rooms/views.py
# ==============================================
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from dateutil.parser import parse
from .models import Room
from .forms import RoomForm
from bookings.models import Booking
from users.views import guest_required, manager_required

@guest_required
def room_list(request):
    rooms = Room.objects.filter(is_available=True)
    q = request.GET.get('q')
    room_type = request.GET.get('type')
    if q:
        rooms = rooms.filter(Q(room_number__icontains=q) | Q(description__icontains=q))
    if room_type:
        rooms = rooms.filter(room_type=room_type)
    paginator = Paginator(rooms, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'guest/room_list.html', {'rooms': page_obj})

@guest_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']
        ci = parse(check_in).date()
        co = parse(check_out).date()
        nights = (co - ci).days
        if nights <= 0:
            messages.error(request, 'Invalid dates.')
            return redirect('rooms:room_list')
        total = nights * room.price_per_night
        Booking.objects.create(
            guest=request.user,
            room=room,
            check_in=ci,
            check_out=co,
            total_price=total,
            status='confirmed'
        )
        messages.success(request, f'Room {room.room_number} booked!')
        return redirect('bookings:my_bookings')
    return render(request, 'guest/book_room.html', {'room': room})

@manager_required
def manage_rooms(request):
    rooms = Room.objects.all()
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room added.')
            return redirect('rooms:manage_rooms')
    else:
        form = RoomForm()
    return render(request, 'admin/manage_rooms.html', {'rooms': rooms, 'form': form})

@manager_required
def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated.')
            return redirect('rooms:manage_rooms')
    else:
        form = RoomForm(instance=room)
    return render(request, 'admin/edit_room.html', {'form': form, 'room': room})

@manager_required
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.delete()
    messages.success(request, 'Room deleted.')
    return redirect('rooms:manage_rooms')

# ==============================================
# FILE: rooms/forms.py
# ==============================================
from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

# ==============================================
# FILE: rooms/urls.py
# ==============================================
from django.urls import path
from . import views

app_name = 'rooms'
urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('manage/', views.manage_rooms, name='manage_rooms'),
    path('edit/<int:room_id>/', views.edit_room, name='edit_room'),
    path('delete/<int:room_id>/', views.delete_room, name='delete_room'),
]

# ==============================================
# FILE: bookings/views.py
# ==============================================
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Booking
from users.views import guest_required, manager_required

@guest_required
def my_bookings(request):
    bookings = Booking.objects.filter(guest=request.user).order_by('-created_at')
    paginator = Paginator(bookings, 5)
    bookings_page = paginator.get_page(request.GET.get('page'))
    return render(request, 'guest/my_bookings.html', {'bookings': bookings_page})

@guest_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, guest=request.user)
    if booking.status not in ['cancelled', 'completed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled.')
    else:
        messages.error(request, 'Cannot cancel this booking.')
    return redirect('bookings:my_bookings')

@manager_required
def all_bookings(request):
    bookings = Booking.objects.select_related('guest', 'room').all().order_by('-created_at')
    paginator = Paginator(bookings, 10)
    bookings_page = paginator.get_page(request.GET.get('page'))
    return render(request, 'admin/all_bookings.html', {'bookings': bookings_page})

@manager_required
def update_booking_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Booking.STATUS_CHOICES):
            booking.status = new_status
            booking.save()
            messages.success(request, 'Booking status updated.')
    return redirect('bookings:all_bookings')

# ==============================================
# FILE: bookings/urls.py
# ==============================================
from django.urls import path
from . import views

app_name = 'bookings'
urlpatterns = [
    path('my/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('all/', views.all_bookings, name='all_bookings'),
    path('update/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),
]

# ==============================================
# FILE: restaurant/views.py
# ==============================================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import MenuItem, Order, OrderItem
from users.views import guest_required

@guest_required
def menu_list(request):
    items = MenuItem.objects.filter(is_available=True)
    category = request.GET.get('category')
    if category:
        items = items.filter(category=category)
    paginator = Paginator(items, 8)
    items_page = paginator.get_page(request.GET.get('page'))
    return render(request, 'guest/menu.html', {'menu_items': items_page})

@guest_required
def add_to_cart(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id)
    cart = request.session.get('cart', {})
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    request.session['cart'] = cart
    messages.success(request, f'{menu_item.name} added to cart.')
    return redirect('restaurant:menu')

@guest_required
def order_food(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, 'Cart is empty.')
            return redirect('restaurant:menu')
        total = 0
        order = Order.objects.create(guest=request.user, total_amount=0)
        for item_id, qty in cart.items():
            menu_item = MenuItem.objects.get(id=item_id)
            item_total = menu_item.price * qty
            total += item_total
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=qty,
                item_price=menu_item.price
            )
        order.total_amount = total
        order.save()
        request.session['cart'] = {}
        messages.success(request, 'Order placed!')
        return redirect('restaurant:order_history')
    return redirect('restaurant:menu')

@guest_required
def order_history(request):
    orders = Order.objects.filter(guest=request.user).order_by('-order_time')
    return render(request, 'guest/order_history.html', {'orders': orders})

# ==============================================
# FILE: restaurant/urls.py
# ==============================================
from django.urls import path
from . import views

app_name = 'restaurant'
urlpatterns = [
    path('menu/', views.menu_list, name='menu'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('order/', views.order_food, name='order_food'),
    path('history/', views.order_history, name='order_history'),
]