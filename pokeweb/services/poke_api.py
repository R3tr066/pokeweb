import requests
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


class PokemonTCGAPI:
    """Service class for interacting with Pokemon TCG API"""

    def __init__(self):
        self.base_url = settings.POKEMON_TCG_BASE_URL
        self.api_key = settings.POKEMON_TCG_API_KEY
        self.headers = {
            'X-Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }

    def _make_request(self, endpoint, params=None):
        """Make a GET request to the Pokemon TCG API"""
        url = f"{self.base_url}/{endpoint}"

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Pokemon TCG API request failed: {e}")
            return None

    def get_cards(self, page=1, page_size=20, search_query=None):
        """Get cards with optional search"""
        cache_key = f"pokemon_cards_{page}_{page_size}_{search_query or 'all'}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        params = {
            'page': page,
            'pageSize': page_size
        }

        if search_query:
            params['q'] = search_query

        data = self._make_request('cards', params)

        if data:
            # Cache for 15 minutes
            cache.set(cache_key, data, 900)

        return data

    def get_card_by_id(self, card_id):
        """Get a specific card by ID"""
        cache_key = f"pokemon_card_{card_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        data = self._make_request(f'cards/{card_id}')

        if data:
            # Cache for 1 hour
            cache.set(cache_key, data, 3600)

        return data

    def search_cards_by_name(self, name, page=1, page_size=20):
        """Search cards by name"""
        search_query = f'name:"{name}"'
        return self.get_cards(page=page, page_size=page_size, search_query=search_query)

    def get_cards_by_set(self, set_id, page=1, page_size=20):
        """Get cards from a specific set"""
        search_query = f'set.id:{set_id}'
        return self.get_cards(page=page, page_size=page_size, search_query=search_query)

    def get_sets(self, page=1, page_size=20):
        """Get Pokemon card sets"""
        cache_key = f"pokemon_sets_{page}_{page_size}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        params = {
            'page': page,
            'pageSize': page_size
        }

        data = self._make_request('sets', params)

        if data:
            # Cache for 1 hour
            cache.set(cache_key, data, 3600)

        return data

    def get_set_by_id(self, set_id):
        """Get a specific set by ID"""
        cache_key = f"pokemon_set_{set_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        data = self._make_request(f'sets/{set_id}')

        if data:
            # Cache for 1 hour
            cache.set(cache_key, data, 3600)

        return data