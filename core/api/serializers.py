from rest_framework import serializers
from core.models import Director, Movie, Review


class MovieSerializer(serializers.ModelSerializer):
	director_id = serializers.CharField(source="director.id")

	class Meta:
		model = Movie
		exclude = ['director']

	def validate_director_id(self, value):
		director = Director.objects.filter(id=value).first()
		
		if not director:
			raise serializers.ValidationError('Director does not exist.')
		return value

	def create(self, validated_data):
		director_id = validated_data.pop('director')['id']
		
		director = Director.objects.get(id=director_id)
		movie = Movie.objects.create(director=director, **validated_data)
		
		return movie

class DirectorSerializer(serializers.ModelSerializer):
	movies = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='movie-detail')

	class Meta:
		model = Director
		fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
	author = serializers.StringRelatedField(read_only=True)
	movie = serializers.CharField(read_only=True, source='movie.id')
	class Meta:
		model = Review
		fields = '__all__'