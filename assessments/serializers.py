from rest_framework import serializers

from assessments.models import Question, Option, AssessmentType
from assessments.models import Assessment, AssessmentResult



class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)  # Nest the options within the question

    class Meta:
        model = Question
        fields = ['id', 'question', 'level', 'timer', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options')  # Extract options data
        question = Question.objects.create(**validated_data)  # Create question instance
        
        # Create option instances for the question
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)

        return question

    def update(self, instance, validated_data):
        options_data = validated_data.pop('options')
        instance.question = validated_data.get('question', instance.question)
        instance.level = validated_data.get('level', instance.level)
        instance.timer = validated_data.get('timer', instance.timer)
        instance.save()

        # Delete existing options and create new ones (simplified update logic)
        instance.options.all().delete()
        for option_data in options_data:
            Option.objects.create(question=instance, **option_data)

        return instance



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


class AssessmentTypeSerializer(serializers.ModelSerializer):
    suborg_name = serializers.SerializerMethodField()

    class Meta:
        model = AssessmentType
        fields = ['id', 'name', 'suborg', 'suborg_name', 'passing_criteria', 'positive_marks', 'negative_marks', 'time', 'trigger_point', 'refresher_days']
        
    
    def get_suborg_name(self, obj):
        return obj.suborg.name