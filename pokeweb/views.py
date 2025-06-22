from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
from .services.poke_api import PokemonTCGAPI
import json


def home(request):
    """Home page view"""
    return render(request, 'home.html')


@cache_page(60 * 15)  # Cache for 15 minutes
def cards_list(request):
    """Display paginated list of Pokemon cards"""
    api = PokemonTCGAPI()
    page = request.GET.get('page', 1)
    search = request.GET.get('search', '')

    try:
        page = int(page)
    except (ValueError, TypeError):
        page = 1

    if search:
        data = api.search_cards_by_name(search, page=page)
    else:
        data = api.get_cards(page=page)

    context = {
        'cards': data.get('data', []) if data else [],
        'current_page': page,
        'total_count': data.get('totalCount', 0) if data else 0,
        'page_size': data.get('pageSize', 20) if data else 20,
        'search_query': search,
    }

    return render(request, 'cards/list.html', context)


def card_detail(request, card_id):
    """Display detailed view of a specific card"""
    api = PokemonTCGAPI()
    data = api.get_card_by_id(card_id)

    if not data:
        return render(request, 'cards/not_found.html', {'card_id': card_id})

    context = {
        'card': data.get('data', {})
    }

    return render(request, 'cards/detail.html', context)


@cache_page(60 * 30)  # Cache for 30 minutes
def sets_list(request):
    """Display list of Pokemon card sets"""
    api = PokemonTCGAPI()
    page = request.GET.get('page', 1)

    try:
        page = int(page)
    except (ValueError, TypeError):
        page = 1

    data = api.get_sets(page=page)

    context = {
        'sets': data.get('data', []) if data else [],
        'current_page': page,
        'total_count': data.get('totalCount', 0) if data else 0,
        'page_size': data.get('pageSize', 20) if data else 20,
    }

    return render(request, 'sets/list.html', context)


def set_detail(request, set_id):
    """Display detailed view of a specific set"""
    api = PokemonTCGAPI()
    set_data = api.get_set_by_id(set_id)
    cards_data = api.get_cards_by_set(set_id, page_size=50)

    if not set_data:
        return render(request, 'sets/not_found.html', {'set_id': set_id})

    context = {
        'set': set_data.get('data', {}),
        'cards': cards_data.get('data', []) if cards_data else [],
    }

    return render(request, 'sets/detail.html', context)


# API endpoints for AJAX requests
@require_http_methods(["GET"])
def api_search_cards(request):
    """API endpoint for searching cards"""
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)

    if not query:
        return JsonResponse({'error': 'Search query is required'}, status=400)

    try:
        page = int(page)
    except (ValueError, TypeError):
        page = 1

    api = PokemonTCGAPI()
    data = api.search_cards_by_name(query, page=page)

    if data:
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Failed to fetch data'}, status=500)


@require_http_methods(["GET"])
def api_card_detail(request, card_id):
    """API endpoint for getting card details"""
    api = PokemonTCGAPI()
    data = api.get_card_by_id(card_id)

    if data:
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Card not found'}, status=404)