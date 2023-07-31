from rest_framework import serializers
from .models import Player, RankingSource, Ranking

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class RankingSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RankingSource
        fields = '__all__'

class RankingSerializer(serializers.ModelSerializer):
    ranking_src = RankingSourceSerializer()
    player = PlayerSerializer()

    class Meta:
        model = Ranking
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data.get('id', None) if len(data) == 1 else data