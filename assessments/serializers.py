from rest_framework import serializers

from assessments.models import Question, Option, AssessmentType
from assessments.models import Assessment, AssessmentResult

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question', 'level', 'timer']
        
class QuestionListSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    
    def get_options(self, obj):
        options_data = Option.objects.filter(question=obj)
        serializers = OptionListSerializer(options_data, many=True)
        return serializers.data
    
    class Meta:
        model = Question
        fields = ['question', 'level', 'timer', 'options']
        
class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'question', 'option', 'is_correct']
        
class OptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['option', 'is_correct']
    
class AssessmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentType
        fields = ['id', 'name', 'suborg', 'passing_criteria', 'positive_marks', 'negative_marks', 
                  'time', 'trigger_point', 'refresher_days']

class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ['id', 'assessment_type', 'questions', 'access', 'is_live', 'is_approved']
        
class AssessmentListSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    assessment_type = serializers.SerializerMethodField()
    
    def get_questions(self, obj):
        questions_data = QuestionListSerializer(obj.questions, many=True)
        return questions_data.data
    
    def get_assessment_type(self, obj):
        return AssessmentTypeSerializer(obj.assessment_type).data
    
    class Meta:
        model = Assessment
        fields = ['id', 'questions', 'access', 'assessment_type', 'is_live', 'is_approved']

class AssessmentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentResult
        fields = ['id', 'user', 'assessment', 'phase', 'result']
