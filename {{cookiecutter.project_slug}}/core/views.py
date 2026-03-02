from django.shortcuts import render, redirect
from django.contrib import messages
# from .models import Service, Product, TeamMember  # Uncomment when models are added


def home(request):
    # services = Service.objects.all()[:3]
    # products = Product.objects.filter(is_featured=True)[:3]
    context = {
        # 'services': services,
        # 'products': products,
    }
    return render(request, 'core/home.html', context)


def about(request):
    # team_members = TeamMember.objects.all()
    context = {
        # 'team_members': team_members,
    }
    return render(request, 'core/about.html', context)


def services(request):
    # services = Service.objects.all()
    context = {
        # 'services': services,
    }
    return render(request, 'core/services.html', context)


def products(request):
    # products = Product.objects.all()
    context = {
        # 'products': products,
    }
    return render(request, 'core/products.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if all([name, email, subject, message]):
            # TODO: Send email or save to DB
            # from django.core.mail import send_mail
            # send_mail(f'Contact: {subject}', f'From: {name} ({email})\n\n{message}', email, ['you@example.com'])
            messages.success(request, f"Thanks {name}! Your message has been received. We'll get back to you shortly.")
        else:
            messages.error(request, "Please fill in all required fields.")

        return redirect('contact')

    return render(request, 'core/contact.html', {})
