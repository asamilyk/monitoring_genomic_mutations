# middleware.py
import logging
import traceback
from django.db.utils import DatabaseError, ProgrammingError, OperationalError
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse

logger = logging.getLogger(__name__)

class GlobalExceptionMiddleware:    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            return self.process_exception(request, e)
    
    def process_exception(self, request, exception):
        logger.error(f"Непойманное исключение: {str(exception)}")
        logger.error(traceback.format_exc())
        
        error_context = {
            'error_title': 'Произошла ошибка',
            'error_message': 'Что-то пошло не так. Пожалуйста, попробуйте позже.',
            'back_url': request.META.get('HTTP_REFERER', '/'),
            'is_ajax': request.headers.get('X-Requested-With') == 'XMLHttpRequest',
        }
        
        if isinstance(exception, (DatabaseError, ProgrammingError, OperationalError)):
            error_context['error_title'] = 'Ошибка доступа к данным'
            error_context['error_message'] = 'Не удалось получить данные из базы. Пожалуйста, обратитесь к администратору системы.'

            error_str = str(exception)
            if "relation" in error_str and "does not exist" in error_str:
                error_context['error_message'] = 'Требуемая таблица не существует в базе данных. Обратитесь к администратору системы.'
            elif "connection" in error_str.lower():
                error_context['error_message'] = 'Не удалось установить соединение с базой данных. Пожалуйста, повторите попытку позже.'
        
        elif isinstance(exception, ValueError):
            error_context['error_title'] = 'Некорректные данные'
            error_context['error_message'] = 'Введены некорректные данные. Пожалуйста, проверьте параметры запроса.'
        
        if settings.DEBUG:
            error_context['error_details'] = str(exception)
            error_context['error_traceback'] = traceback.format_exc()
        
        if error_context['is_ajax']:
            from django.http import JsonResponse
            return JsonResponse({
                'status': 'error',
                'title': error_context['error_title'],
                'message': error_context['error_message'],
            }, status=500)
        
        return render(request, 'error.html', error_context, status=500)
