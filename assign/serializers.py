from rest_framework import serializers

from assign.models import SeriesAssignUser
from assign.models import AssessmentProgress, ItemProgress

from series.serializers import SeriesListSerializer

class SeriesAssignUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeriesAssignUser
        fields = ["user", "series", "is_completed", "progress"]
        
class SeriesAssignUserListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    series = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.username
    
    def get_series(self, obj):
        return SeriesListSerializer(obj.series).data
    
    class Meta:
        model = SeriesAssignUser
        fields = ["id", "user", "series", "is_completed", "progress"]

class AssessmentProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentProgress
        fields = ["user", "assessment_season", "is_completed"]
        
class ItemProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemProgress
        fields = ["user", "item_season", "is_completed"]
