from rest_framework import serializers

from series.models import Series, Seasons, SeasonLota, ItemSeason
#from series.models import AssessmentSeason, ItemSeason, LearningCourseSeason, QuadGameSeason
from series.models import AssessmentSeason, LearningCourseSeason, ItemSeason
from assessments.serializers import AssessmentListSerializer
from zola.serializers import ItemUserSerializer
from learningcourse.serializers import LearningCourseListSerializer
from rest_framework import viewsets

from zola.models import Item
from orgss.models import SubOrg1


class SeriesSerializer(serializers.ModelSerializer):
    sub_org = serializers.SlugRelatedField(queryset=SubOrg1.objects.all(), slug_field='name')

    class Meta:
        model = Series
        fields = ["name", "description", "thumbnail", "sub_org"]


class SeriesListSerializer(serializers.ModelSerializer):
    sub_org = serializers.SerializerMethodField()
    seasons = serializers.SerializerMethodField()
    
    def get_sub_org(self, obj):
        return obj.sub_org.name
    
    def get_seasons(self, obj):
        data = Seasons.objects.filter(series=obj)
        return SeasonsListAssignSerializer(data, many=True).data
    
    class Meta:
        model = Series
        fields = ["id", "name", "description", "thumbnail", "sub_org",
                  "seasons"]



class SeasonSerializer(serializers.ModelSerializer):
    series = serializers.SlugRelatedField(queryset=Series.objects.all(), slug_field='name')

    class Meta:
        model = Seasons
        fields = ["name", "description", "thumbnail", "series"]


class SeasonLotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonLota
        fields = ["name", "image", "season"]
        
class SeasonLotaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonLota
        fields = ["id", "name", "image"]

class AssessmentSeasonListAssignSerializer(serializers.ModelSerializer):
    assessments = serializers.SerializerMethodField()
    
    def get_assessments(self, obj):
        return AssessmentListSerializer(obj.assessments).data
    
    class Meta:
        model = AssessmentSeason
        fields = ["id", "assessments"]
       
class ItemSeasonListAssignSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()
    
    def get_item(self, obj):
        return ItemUserSerializer(obj.item).data
    
    class Meta:
        model = ItemSeason
        fields = ["id", "item"]
       
class LearningCourseListAssignSerializer(serializers.ModelSerializer):
    learning_course = serializers.SerializerMethodField()
    
    def get_learning_course(self, obj):
        return LearningCourseListSerializer(obj.learning_course).data
    
    class Meta:
        model = LearningCourseSeason
        fields = ["id", "learning_course"]
        


class SeasonsListAssignSerializer(serializers.ModelSerializer):
    series = serializers.SerializerMethodField()
    assessments = serializers.SerializerMethodField()
    item = serializers.SerializerMethodField()
    learning_course = serializers.SerializerMethodField()
    
    seasonlota = serializers.SerializerMethodField()
    
    def get_series(self, obj):
        return obj.series.name
    
    def get_assessments(self, obj):
        data = AssessmentSeason.objects.filter(season=obj, assessments__is_live=True)
        return AssessmentSeasonListAssignSerializer(data, many=True).data
    
    def get_item(self, obj):
        data = ItemSeason.objects.filter(season=obj, item__is_live=True)
        return ItemSeasonListAssignSerializer(data, many=True).data
 
    def get_learning_course(self, obj):
        data = LearningCourseSeason.objects.filter(season=obj)
        return LearningCourseListAssignSerializer(data, many=True).data
    
  
    def get_seasonlota(self, obj):
        data = SeasonLota.objects.filter(season=obj)
        return SeasonLotaListSerializer(data, many=True).data
    
    class Meta:
        model = Seasons
        fields = ["id", "name", "description", "thumbnail", "series",
                  "assessments", "item", "learning_course", "seasonlota"]


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class ItemSeasonSerializer(serializers.ModelSerializer):
    item = serializers.SlugRelatedField(queryset=Item.objects.all(), slug_field='item_name')
    season = serializers.SlugRelatedField(queryset=Seasons.objects.all(), slug_field='name')

    class Meta:
        model = ItemSeason
        fields = ['id', 'item', 'season']


class ItemSeasonCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSeason
        fields = ['id', 'item', 'season']

class SeasonAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seasons
        fields = ['id', 'name', 'series']

class SeriesAdminSerializer(serializers.ModelSerializer):
    seasons = SeasonSerializer(many=True, read_only=True)

    class Meta:
        model = Series
        fields = ['id', 'name', 'sub_org', 'seasons']        

