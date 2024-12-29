"""Views of pages app."""
from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    template_name = 'pages/rules.html'


def page_403(request, reason=""):
    """Custom 403 page."""
    return render(request, 'pages/403csrf.html', status=403)


def page_404(request, exception):
    """Custom 404 page."""
    return render(request, 'pages/404.html', status=404)


def page_500(request):
    """Custom 500 page."""
    return render(request, 'pages/500.html', status=500)
