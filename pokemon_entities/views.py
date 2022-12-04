import folium
import logging

from django.shortcuts import render
from .models import Pokemon
from django.utils import timezone
from django.shortcuts import get_list_or_404, get_object_or_404


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)

LOGGER = logging.getLogger(__file__)
logging.basicConfig(level=logging.ERROR)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = get_list_or_404(Pokemon)

    local_time = timezone.localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_coordinates = pokemons.entities.filter(
        appeared_at__lte=local_time,
        disappeared_at__gte=local_time)

    for pokemon_entities in pokemon_coordinates:
        add_pokemon(
            folium_map, pokemon_entities.latitude,
            pokemon_entities.longitude,
            request.build_absolute_uri(pokemon_entities.image.url)
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    local_time = timezone.localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_coordinates = pokemon.entities.filter(
        appeared_at__lte=local_time,
        disappeared_at__gte=local_time)
    pokemon_image = request.build_absolute_uri(pokemon.image.url)

    for pokemon_entities in pokemon_coordinates:
        add_pokemon(
            folium_map, pokemon_entities.latitude,
            pokemon_entities.longitude,
            pokemon_image
        )

    previous_evolution = None
    next_evolution = None

    if pokemon.previous_evolution:
        pokemon_previous_evolution = pokemon.previous_evolution
        previous_evolution = {
            'title_ru': pokemon_previous_evolution.title_ru,
            'pokemon_id': pokemon_previous_evolution.id,
            'img_url': request.build_absolute_uri(pokemon_previous_evolution.image.url)
        }
    
    next_evolution = pokemon.next_evolutions.first()
    if next_evolution:
        next_evolution = {
                'pokemon_id': next_evolution.id,
                'title_ru': next_evolution.title_ru,
                'img_url': request.build_absolute_uri(next_evolution.image.url)
                }
    
    pokemon_info = {
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'img_url': pokemon_image,
        'description': pokemon.description,
        'previous_evolution': previous_evolution,
        'next_evolution': next_evolution
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_info
    })
