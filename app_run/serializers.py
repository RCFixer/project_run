from rest_framework import serializers
from .models import Run
from .models import User
from .models import AthleteInfo
from .models import Challenge

class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name']

class RunSerializer(serializers.ModelSerializer):
    athlete_data = AthleteSerializer(read_only=True, source='athlete')

    class Meta:
        model = Run
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    runs_finished = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type', 'runs_finished']

    def get_type(self, obj):
        return 'coach' if obj.is_staff is True else 'athlete'

    def get_runs_finished(self, obj):
        return obj.runs.filter(status='finished').count()


class AthleteInfoUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AthleteInfo
        fields = ['goals', 'weight']


class AthleteInfoDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = AthleteInfo
        fields = '__all__'

class ChallengeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Challenge
        fields = ['full_name', 'athlete']
