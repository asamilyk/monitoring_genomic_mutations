from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse
import json
import logging

from .models import FilterHistory

@login_required
def filter_history(request):
    logger = logging.getLogger(__name__)
    
    history = FilterHistory.objects.filter(user=request.user)
    return render(request, 'user/filter_history.html', {
        'history': history
    })


@login_required
@require_POST
def save_filter(request):
    try:
        logger = logging.getLogger(__name__)
        logger.info("Попытка сохранить фильтр")
        
        filter_name = request.POST.get('filter_name', '')
        logger.info(f"Название фильтра: {filter_name}")
        
        logger.info(f"POST данные: {dict(request.POST)}")

        filter_params = {}
        for key, value in request.POST.items():
            if key.startswith('filter_param_'):
                param_name = key.replace('filter_param_', '')
                filter_params[param_name] = value
                logger.info(f"Найден параметр фильтра: {param_name}={value}")
        
        if not filter_params:
            logger.warning("Нет параметров фильтра в запросе")
            messages.warning(request, "Нет активных фильтров для сохранения.")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
        logger.info(f"Сохраняем фильтр для пользователя {request.user.username} с параметрами: {filter_params}")
        filter_history = FilterHistory.objects.create(
            user=request.user,
            filter_name=filter_name,
            filter_params=json.dumps(filter_params)
        )
        
        logger.info(f"Фильтр успешно сохранен с ID: {filter_history.id}")
        messages.success(request, f"Фильтр '{filter_name}' успешно сохранен.")
        
        return redirect('user:filter_history')
    
    except Exception as e:
        import traceback
        logger.error(f"Ошибка при сохранении фильтра: {str(e)}")
        logger.error(traceback.format_exc())
        messages.error(request, f"Ошибка при сохранении фильтра: {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', '/'))



@login_required
@require_POST
def delete_filter(request, filter_id):
    filter_history = get_object_or_404(FilterHistory, id=filter_id, user=request.user)
    filter_history.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    messages.success(request, "Фильтр удален из истории.")
    return redirect('filter_history')
