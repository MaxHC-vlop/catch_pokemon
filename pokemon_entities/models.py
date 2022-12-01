from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(
        verbose_name='Название на русском', max_length=200
        )
    title_en = models.CharField(
        verbose_name='Название на английском', max_length=200, blank=True
        )
    title_jp = models.CharField(
        verbose_name='Название на японском', max_length=200, blank=True
        )
    image = models.ImageField(
        verbose_name='Изображение покемона', upload_to='pokemons', blank=True
        )
    description = models.TextField(
        verbose_name='Описание покемона', blank=True
        )
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='next_evolutions',
        verbose_name='Предыдущая эволюция',
        null=True,
        blank=True,
        )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE,
        verbose_name='Покемон', related_name='entity'
        )
    latitude = models.FloatField(
        verbose_name='Широта'
        )
    longitude = models.FloatField(
        verbose_name='Долгота'
        )
    appeared_at = models.DateTimeField(
        verbose_name='Появился', null=True
        )
    disappeared_at = models.DateTimeField(
        verbose_name='Исчез', null=True
        )
    level = models.IntegerField(
        verbose_name='Уровень', null=True
        )
    health = models.IntegerField(
        verbose_name='Здоровье', null=True
        )
    attack = models.IntegerField(
        verbose_name='Атака', null=True
        )
    protection = models.IntegerField(
        verbose_name='Защита', null=True
        )
    endurance = models.IntegerField(
        verbose_name='Выносливость', null=True
        )

    def __str__(self):
        pokemon = f'{self.pokemon.title_ru}'

        return pokemon