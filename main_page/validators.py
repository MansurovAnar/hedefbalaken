from django.views import View
from django.http import JsonResponse
import json
from django.contrib.auth.models import User

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if username:
            if len(username) < 3 and len(username) > 0:
                return JsonResponse({'username_error': 'İstifadəçi adı minimum 3 simovoldan ibarət ola bilər.'}, status=408)
            if not str(username).isalnum():
                return JsonResponse({'username_error': 'İstifadəçi adı hərf və rəqəmdən ibarət ola bilər.'}, status=400)
            if User.objects.filter(username=username).exists():
                return JsonResponse({'username_error': 'Bu istifadəçi adı artıq mövcuddur.'}, status=409)
        elif not data['username']:
            return JsonResponse({'username_error': 'İstifadəçi adı mütləqdir.'}, status=406)
        return JsonResponse({'username_valid': True})

class FirstnameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        firstname = data['first_name']

        if firstname:
            if len(firstname) < 3 and len(firstname) > 0:
                return JsonResponse({'firstname_error': 'Ad minimum 3 hərfdən ibarət ola bilər.'}, status=408)
            if not str(firstname).isalpha():
                return JsonResponse({'firstname_error': 'Ad ancaq hərfdən ibarət ola bilər.'}, status=400)
        elif not data['first_name']:
            return JsonResponse({'firstname_error': 'Ad mütləqdir.'}, status=406)
        return JsonResponse({'firstname_valid': True})

class LastnameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        lastname = data['last_name']

        if lastname:
            if len(lastname) < 3 and len(lastname) > 0:
                return JsonResponse({'lastname_error': 'Soyad minimum 3 hərfdən ibarət ola bilər.'}, status=408)
            if not str(lastname).isalpha():
                return JsonResponse({'lastname_error': 'Soyad ancaq hərfdən ibarət ola bilər.'}, status=400)
        elif not data['last_name']:
            return JsonResponse({'lastname_error': 'Soyad mütləqdir.'}, status=406)
        return JsonResponse({'lastname_valid': True})
