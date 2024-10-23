from django.shortcuts import get_object_or_404
from django.db.models import F, Q, Sum, FloatField, Count
from django.http import JsonResponse, HttpResponse
from django.http import FileResponse, Http404
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from zola.serializers import (ItemListSerializer1, ItemEmotionSerializer, ItemRecommendSerializer,
                                ItemLiSerializer, ItemUserSerializer, ItemCreateSerializer,
                                ItemResultSerializer, ItemSerializer, ItemSearchSerializer,
                                ItemLibrarySerializer, LeaderboardSerializer, ItemFilterSerializer,
                                ItemNewSerializer, ItemAvailableSerializer, ItemResultUpdateSerializer,
                                ItemAvailableSerializer1, LibraryFilterSerializer, ItemLibrarySerializer1)

from zola.models import Item, ItemResult, Library_Filter_CHOICES, LibraryFilter
from accounts.models import Account, UserProfile
from orgss.models import Role1, Weightage
from assessments.models import AssessmentResult
from assign.models import SeriesAssignUser

from users.models import UserRightsMapping
from competency.models import Competency
from series.models import Seasons, ItemSeason
from zola.utils import string_to_words, save_words_to_excel, detect_words

import string
from collections import Counter
import json
from datetime import datetime
import spacy
import threading
nlp = spacy.load('en_core_web_sm')

from rest_framework.permissions import AllowAny
from rest_framework import filters
from rest_framework.filters import SearchFilter

from django.db.models.functions import PercentRank

import csv

from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import render



class ItemViewSet(LoggingMixin, ViewSet):
    serializer_class = ItemListSerializer1
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Item, id=pk)

    @staticmethod
    def get_queryset():
        return Item.objects.all()

    def list(self, request):
        suborg_id = self.request.query_params.get('suborg_id')
        user = self.request.user
        user_role = user.user_role
        if user_role not in ['admin', 'super_admin']:
            response = {
                'status': 'Failed',
                'message': 'You are not authorized to access these details'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if user_role == 'admin':
            suborg = user.role.suborg
            users = Account.objects.filter(role__suborg=suborg)
            roles = Role1.objects.filter(suborg=suborg)
        elif user_role == 'super_admin' and suborg_id:
            users = Account.objects.filter(role__suborg__id=suborg_id)
            roles = Role1.objects.filter(suborg__id=suborg_id)
        elif user_role == 'super_admin':
            org = user.org
            users = Account.objects.filter(org=org)
            roles = Role.objects.filter(suborg__org=org)

        series_assign = SeriesAssignUser.objects.filter(user__in=users, is_completed=True)
        items_data = Item.objects.filter(role__in=roles)
        items = ItemResult.objects.filter(user__in=users).count()
        assessments = AssessmentResult.objects.filter(user__in=users).count()
        competency_list = [
            {'id': instance.id, 'competency_name': instance.competency_name}
            for item in items_data
            for instance in item.competencys.all()
        ]
        
        response = {
            'status': 'Success',
            'message': 'Retrieved Successfully',
            'competency_list': competency_list,
            'items': items,
            'assessments': assessments,
            'series_completed': series_assign.count()
        }
        return Response(response, status=status.HTTP_200_OK)
       
    def retrieve(self, request, **kwargs):
        pk = kwargs.pop('pk')
        response = {
            'status': 'Success',
            'message': 'Retrieved Successfully',
            'data': self.serializer_class(self.get_object(pk)).data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        request_data  = {
            'item_name': request.data.get('item_name'),
            'item_description': request.data.get('item_description'),
            'item_video': request.data.get('item_video'),
            'item_background': request.data.get('item_background'),
            'category': request.data.get('category'),
            'thumbnail': request.data.get('thumbnail'),
            'item_gender': request.data.get('item_gender'),
            'role': request.data.get('role'),
            'level': request.data.get('level'),
            'expert': request.data.get('expert'),
        }
        
        request_data['competencys'] = request.data.get('competencys').split(',')
        
        serializer =  ItemCreateSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'Success',
                'message': 'Item was successfully created.',
                'data': serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'status': 'Failed',
            'message': 'Failed to create item',
            'data': serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        instance = self.get_object(pk)
        request_data  = {
            'item_name': request.data.get('item_name', instance.item_name),
            'item_description': request.data.get('item_description', instance.item_description),
            'item_video': request.data.get('item_video', instance.item_video),
            'item_background': request.data.get('item_background', instance.item_background),
            'category': request.data.get('category', instance.category),
            'thumbnail': request.data.get('thumbnail', instance.thumbnail),
            'item_gender': request.data.get('item_gender', instance.item_gender),
            'role': request.data.get('role', instance.role.id),
            'level': request.data.get('level', instance.level),
            'expert': request.data.get('expert', instance.expert),
            'is_live': request.data.get('is_live', instance.is_live),
            'is_approved': request.data.get('is_approved', instance.is_approved)
        }
        
        if request.data.get('competencys'):
            request_data['competencys'] = request.data.get('competencys').split(',')
        else:
            request_data['competencys'] = list(instance.competencys.values_list('id', flat=True))
            
        serializer =  ItemCreateSerializer(instance, data=request_data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'Success',
                'message': 'Item was successfully updated.',
                'data': serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'status': 'Failed',
            'message': 'Failed to update item',
            'data': serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        response = {
            'status': 'Success',
            'message': 'Item was successfully deleted.',
        }
        return Response(response, status=status.HTTP_200_OK)

class LeaderBoardViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        competency_id = request.query_params.get('competency_id')
        suborg_id = request.query_params.get('suborg_id')
        if not competency_id or not suborg_id:
            response = {
                'status': 'Failed',
                'message': 'Competency ID and Suborg ID are required'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        try:
            competency = Competency.objects.get(id=competency_id)
        except Competency.DoesNotExist:
            response = {
                'status': 'Failed',
                'message': 'Competency does not exist'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        users = Account.objects.filter(role__suborg__id=suborg_id)
        leaderboard_results = []
        for user in users:
            try:
                user_competency = UserProfile.objects.get(user=user).competency_score
                user_competency = json.loads(user_competency)
            except:
                continue
            user_competency_score = user_competency.get(competency.competency_name)
            if user_competency_score:
                score = sum([int(x) for x in user_competency_score.split(',')])
                user_data = {
                    'name': user.first_name + ' ' + user.last_name,
                    'score': score,
                }
                leaderboard_results.append(user_data)
        response = {
            'status': 'Success',
            'message': 'Retrieved Successfully',
            'data': leaderboard_results
        }
        return Response(response, status=status.HTTP_200_OK)

class CompetencyBoardViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        suborg_id = request.query_params.get('suborg_id')
        if not suborg_id:
            response = {
                'status': 'Failed',
                'message': 'Suborg ID is required'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        users = Account.objects.filter(role__suborg__id=suborg_id).select_related('userprofile')
        competency_results = {}
        for user in users:
            user_profile = getattr(user, 'userprofile', None)
            if user_profile and user_profile.competency_score:
                try:
                    user_competency = json.loads(user_profile.competency_score)
                except json.JSONDecodeError:
                    continue 

                for competency_name, score in user_competency.items():
                    score = sum(int(x) for x in score.split(','))
                    competency_results[competency_name] = competency_results.get(competency_name, 0) + score
        response = {
            'status': 'Success',
            'message': 'Retrieved Successfully',
            'data': competency_results
        }
        return Response(response, status=status.HTTP_200_OK)
    
class ItemHandleViewSet(LoggingMixin, ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemUserSerializer

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Item, id=pk)

    @staticmethod
    def get_queryset():
        return Item.objects.all()

    
    def list(self, request):
        queryset = self.get_queryset().filter(role__suborg=request.user.role.suborg)
        admin_user = False
        try:
            user_rights = UserRightsMapping.objects.filter(user=request.user)
            if user_rights:
                for rights in user_rights:
                    if rights.right.name.lower() == 'approve':
                        admin_user = True
                        queryset = queryset.filter(is_approved=False)
                        break
                    elif rights.right.name.lower() == 'creator':
                        admin_user = True
                        queryset = queryset.filter(is_live=False)
                        break
        except:
            pass
        
        if not admin_user:
            queryset = queryset.filter(role=self.request.user.role).order_by('-id')

        serializer_data = self.serializer_class(queryset, many=True).data
        response = {
            'status': 'Success',
            'message': 'Retrieved Successfully',
            'data': serializer_data,
        }
        return Response(response, status=status.HTTP_200_OK)

    def retrieve(self, request, **kwargs):
        pk = kwargs.pop('pk')
        response = {
            'status': 'Success',
            'message': 'Retrieved Successfully',
            'data': self.serializer_class(self.get_object(pk)).data
        }
        return Response(response, status=status.HTTP_200_OK)
       
class ItemProcessingViewSet(LoggingMixin, ViewSet):
    #permission_classes = [IsAuthenticated, SaaSAccessPermissionItem]
    permission_classes = [IsAuthenticated]
    serializer_class = ItemListSerializer1
    
    def list(self, request):
        score = 0
        def process_user_data(userprofile_instance, user_power_words, user_weak_words, score, competencys, emotion_words):
            print("\n\nStarting Thread: UserProfile")
            userprofile_instance.scenarios_attempted += 1
            userprofile_instance.user_powerwords = ",".join(filter(None, [userprofile_instance.user_powerwords, ", ".join(user_power_words)]))
            userprofile_instance.user_weakwords = ",".join(filter(None, [userprofile_instance.user_weakwords, ", ".join(user_weak_words)]))
            userprofile_instance.scenarios_attempted_score = ",".join(filter(None, [userprofile_instance.scenarios_attempted_score, str(score)]))
            print("\n\nCompleted Thread: UserProfile")
            print("\n\nStarting Thread: Update Competency")
            competency_score = json.loads(userprofile_instance.competency_score or '{}')

            for competency in competencys:
                sub_competencies = competency.sub_competency.all()
                power_word_list = []
                negative_word_list = []
                score = 0

                for sub_competency in sub_competencies:
                    power_words = sub_competency.power_words.all()
                    power_word_count = sub_competency.power_words.count()
                    negative_words = sub_competency.negative_words.all()
                    negative_word_count = sub_competency.negative_words.count()
                    negative_word_weight = 0
                    power_word_weight = 0

                    for power_word in power_words:
                        name = power_word.word.word_name.lower()
                        power_word_list.append(name)
                        if name in emotion_words:
                            power_word_weight += power_word.weight
                        
                    for negative_word in negative_words:
                        name = negative_word.word.word_name.lower()
                        negative_word_list.append(name)
                        if name in emotion_words:
                            negative_word_weight += negative_word.weight
                    score += competency_weightage*(power_word_count*power_word_weight - negative_word_count*negative_word_weight)
                
                competency_name = str(competency.competency_name)
                        
                if competency_name in competency_score:
                    competency_score[competency_name] += ',' + str(score)
                    competency_score[competency_name] = competency_score[competency_name]
                else:
                    competency_score[competency_name] = str(score)

            userprofile_instance.competency_score = json.dumps(competency_score)
            userprofile_instance.save()
            print("\n\nCompleted Thread: Update Competency")
        try:
            instance = Item.objects.get(id=request.query_params.get('id'))
        except Item.DoesNotExist:
            response = {
                'status': 'Failed',
                'message': 'Scenario does not exist'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        
        userprofile_instance = UserProfile.objects.get(user=request.user)
        emotion_str = request.query_params.get('item_emotion').lower()
        
        competencys = instance.competencys.all().prefetch_related(
            'sub_competency__power_words__word',
            'sub_competency__negative_words__word'
        )
        
        power_word_list = []
        negative_word_list = []
        user_power_words = []
        user_weak_words = []
        
        for competency in competencys:
            competencies_weightage = Weightage.objects.filter(competency=competency, suborg=request.user.role.suborg).first()
            competency_weightage = competencies_weightage.weightage if competencies_weightage else 1
            sub_competencies = competency.sub_competency.all()
            for sub_competency in sub_competencies:
                power_words = sub_competency.power_words.all()
                power_word_count = sub_competency.power_words.count()
                negative_words = sub_competency.negative_words.all()
                negative_word_count = sub_competency.negative_words.count()
                negative_word_weight = 0
                power_word_weight = 0

                for power_word in power_words:
                    name = power_word.word.word_name.lower()
                    power_word_list.append(name)
                    if name in emotion_str:
                        user_power_words.append(name)
                        power_word_weight += power_word.weight
                    
                for negative_word in negative_words:
                    name = negative_word.word.word_name.lower()
                    negative_word_list.append(name)
                    if name in emotion_str:
                        user_weak_words.append(name)
                        negative_word_weight += negative_word.weight
                score += competency_weightage*(power_word_count*power_word_weight - negative_word_count*negative_word_weight)
        
        user_power_words = list(set(user_power_words))
        user_weak_words = list(set(user_weak_words))

        # Check if both user_power_words and user_weak_words are empty
        if not user_power_words and not user_weak_words:
            score = 0
        else:
            # Proceed with score calculation logic when words are detected
            instance.item_emotion = instance.item_emotion + ',' + emotion_str
            instance.item_answercount += 1
            processing_thread = threading.Thread(
                target=process_user_data,
                args=(userprofile_instance, user_power_words, user_weak_words, score, competencys, emotion_str)
            )
            processing_thread.start()

            words = string_to_words(
                request.user.username,
                emotion_str,
                power_word_list,
                negative_word_list
            )

        
        
        """
        instance.item_emotion = instance.item_emotion + ',' + emotion_str
        user_power_words = list(set(user_power_words))
        user_weak_words = list(set(user_weak_words))
        instance.item_answercount += 1
        processing_thread = threading.Thread(
            target=process_user_data,
            args=(userprofile_instance, user_power_words, user_weak_words, score, competencys, emotion_str)
        )
        processing_thread.start()
        
        words = string_to_words(
            request.user.username,
            emotion_str,
            power_word_list,
            negative_word_list
        )
        """
        """
        detected_power_words = [word for word in words if 'power' in detect_words(word).lower()]
        detected_weak_words = [word for word in words if 'weak' in detect_words(word).lower()]

        score = score + (2*len(detected_power_words)) - (1*len(detected_weak_words))
        word_save_thread = threading.Thread(
            target=save_words_to_excel,
            args=(words,)
        )
        word_save_thread.start()
        """
        data = {
            'id': instance.id,
            'item_name': instance.item_name,
            'coming_across_as': instance.coming_across_as
        }
        instance.save()
        
        response_data = {
            'id': data.get('id'),
            'item_name': data.get('item_name'),
            'coming_across_as': data.get('coming_across_as'),
            'compentency_score': score,
            'powerword_detected': user_power_words,
            'weekword_detected': user_weak_words,
            'power_word_list': power_word_list,
            'negative_word_list': negative_word_list,
            #'power_word_learned': detected_power_words,
            #'negative_word_learned': detected_weak_words
        }
        
        itemresult = ItemResult.objects.create(
                user=request.user, 
                item=instance,
                created_at=datetime.now(),
                score=score
            )
        itemresult.save()
        
        serialized_data = self.serializer_class(instance=instance, data=data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()

        response = {
            'status': 'Success',
            'message': 'Item was successfully created.',
            'data': response_data,
        }
        return Response(response, status=status.HTTP_200_OK)
        
class ItemList(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemLiSerializer
    permission_classes = [IsAuthenticated]

    def list(self,request):
        user = request.user
        u2 = user.role_id

        items = Item.objects.filter(role = u2).order_by('-id')
        serializer = ItemLiSerializer(items, many=True)
        
        if items:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ItemAnalysticsViewSet(LoggingMixin, ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response({"status": "error", "message": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        user_instance = UserProfile.objects.get(user__id=user_id)
        try:
            assessments_result = AssessmentResult.objects.filter(user=request.user)
        except AssessmentResult.DoesNotExist:
            assessments_result = None
        try:
            items_result = ItemResult.objects.filter(user=request.user)
        except AssessmentResult.DoesNotExist:
            items_result = None
        
        series_assigned_data = SeriesAssignUser.objects.filter(user__id=user_id)
        series_progress = {}
        competency_assigned = []
        for series_assign in series_assigned_data:
            seasons = Seasons.objects.filter(series=series_assign.series)
            for season in seasons:
                items = ItemSeason.objects.filter(season=season).values_list('item__competencys__competency_name', flat=True)
                competency_assigned.extend(items)
            series_progress[series_assign.series.name] = series_assign.progress
        strong_competency = []
        weak_competency = []
        competency_attempted = 0
        if user_instance.competency_score:
            for compentency, score in json.loads(user_instance.competency_score).items():
                if compentency in competency_assigned:
                    competency_attempted += 1
                score = sum([int(x) for x in score.split(',')])
                if score > 0:
                    strong_competency.append({'competency': compentency, 'score': score})
                elif score < 0:
                    weak_competency.append({'competency': compentency, 'score': score})
        user_details = {
            'power_words_used': user_instance.user_powerwords,
            'week_words_used': user_instance.user_weakwords,
            'scenarios_attempted': user_instance.scenarios_attempted,
            'scenarios_attempted_score': user_instance.scenarios_attempted_score,
            'competency_score': json.loads(user_instance.competency_score) if user_instance.competency_score else {},
            'strong_competency': strong_competency,
            'weak_competency': weak_competency,
            'assessments_attempted': assessments_result.count() if assessments_result else 0,
            'items_attempted': items_result.count() if items_result else 0,
            'series_progress': series_progress,
            'competency_assigned': len(competency_assigned),
            'competency_attempted': competency_attempted
        }
        
        response = {
            'status': 'Success',
            'message': 'Retrieved Successfully',
            'data': user_details,
        }
        
        return Response(response, status=status.HTTP_200_OK)

class CompetencyAttemptAnalyticsViewSet(LoggingMixin, ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        suborg_result = {}
        global_result = {}
        try:
            current_user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            response = {
                'status': 'Failed',
                'message': 'User Profile does not exist'
            }
            return Response(response, status=status.HTTP_200_OK)

        # Check if competency_score exists and is valid JSON
        if not current_user_profile.competency_score:
            response = {
                'status': 'Failed',
                'message': 'No Competency Score Found'
            }
            return Response(response, status=status.HTTP_200_OK)

        try:
            user_competency_score = json.loads(current_user_profile.competency_score)
        except (json.JSONDecodeError, TypeError):
            response = {
                'status': 'Failed',
                'message': 'Invalid Competency Score Format'
            }
            return Response(response, status=status.HTTP_200_OK)

        if not user_competency_score:
            response = {
                'status': 'Failed',
                'message': 'No Competency Score Found, Please Attempt Your Scenario First'
            }
            return Response(response, status=status.HTTP_200_OK)

        cumalative_competencies_score = {}

        for user_competency, score_str in user_competency_score.items():
            cumalative_competencies_score[user_competency] = sum(int(score) for score in score_str.split(','))

        suborg_user_profiles = UserProfile.objects.filter(
            user__role__suborg=request.user.role.suborg
        ).prefetch_related('user')

        global_user_profiles = UserProfile.objects.all().prefetch_related('user')

        comparision = {
            'better': 0,
            'lower': 0,
            'score': 0,
            'percentile': 0,
        }

        def get_competency_scores(user_profiles, competency_name):
            scores = []
            for profile in user_profiles:
                if profile.competency_score:
                    competency_score = json.loads(profile.competency_score)
                    score_str = competency_score.get(competency_name, '')
                    user_scores = [int(score) for score in score_str.split(',') if score.strip()]
                    scores.extend(user_scores)
            return scores

        for name, score in cumalative_competencies_score.items():
            suborg_scores = get_competency_scores(suborg_user_profiles, name)
            global_scores = get_competency_scores(global_user_profiles, name)

            def calculate_metrics(user_scores, current_score):
                better_count = sum(1 for s in user_scores if s <= current_score)
                lower_count = sum(1 for s in user_scores if s > current_score)
                if (better_count + lower_count) > 0:
                    percentile = (better_count / (better_count + lower_count)) * 100
                else:
                    percentile = 0
                return {
                    'better': better_count,
                    'lower': lower_count,
                    'score': current_score,
                    'percentile': percentile,
                }

            suborg_result[name] = calculate_metrics(suborg_scores, score)
            global_result[name] = calculate_metrics(global_scores, score)

        if cumalative_competencies_score is not None:
            response = {
                'status': 'success',
                'message': 'Retrieved Successfully',
                'data': {
                    'suborg_result': suborg_result,
                    'global_result': global_result
                }
            }
        else:
            response = {
                'status': 'Failed',
                'message': 'No Entry has been recorded, Attempt First To See Results'
            }
        return Response(response, status=status.HTTP_200_OK)



class DownloadFiles(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        filepath = 'words.xlsx'
        try:
            return FileResponse(open(filepath, 'rb'), as_attachment=True, filename='words.xlsx')
        except FileNotFoundError:
            raise Http404("The file does not exist.")


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def item_result(request, pk):
    try: 
        item_result = Item.objects.get(pk=pk) 
    except Item.DoesNotExist: 
        return Response({'message': 'The scenario does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    
    if request.method == 'PUT': 
        item_data = JSONParser().parse(request) 
        
        #itemli = Item.objects.get(id=pk)
        item = Item.objects.values_list('item_answer').get(id=pk)
        
        with open('sean/read.txt', 'w') as f:
            item_list = str(item_data)
            f.write(item_list)
        
        text = open('sean/read.txt').read() 
        lower_case = text.lower()   
        cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
        
        tokenized_words = cleaned_text.split()
    

        stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "your", "yours", "yourself",
              "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
              "they", "them", "their", "theirs", "themselves", "these",
              "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
              "does", "did", "doing", "a", "an", "the", "and", "or", "because", "as",
              "of", "at", "by", "for", "with", "about", "against", "into", "through", "during", "before",
              "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
              "further", "then", "here", "there", "any", "both", "each",
              "few", "other", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
              "too", "s", "t", "can", "will", "just", "don"]

        final_words = []
        for word in tokenized_words:
            if word not in stop_words:
                final_words.append(word)

        emotion_c1 = []
        with open('sean/emotions.txt', 'r') as file:
            for line in file:
                clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
                word, emotion = clear_line.split(':')
                
                if word in final_words:
                    emotion_c1.append(emotion)


        emotion_count = Counter(emotion_c1)
        emotions = str(emotion_count)[9: -2]
        unique_list = list(set(emotion_c1))
        my_string = ", ".join(unique_list)
        

        print(emotions)

        
        #return JsonResponse(emotions, safe=False, status=status.HTTP_200_OK)
        

        #const myJSON =  JSON.stringify(emotions);

        with open('sean/dump.txt', 'a') as f:
            item1_list = str(item_data)
            f.write(item1_list)

       
        serializer = ItemEmotionSerializer(item_result, data=item_data)
        
        if serializer.is_valid(): 
            
            item_result.item_answercount = F('item_answercount') + 1
            item_result.coming_across_as = my_string
            serializer.save()
            return JsonResponse({'data': serializer.data, 'coming_across_as': emotions}, safe=False, status=status.HTTP_200_OK)
            
            #return Response(serializer.data)
            
            
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def item_rec(request, pk):
    try: 
        item_result = Item.objects.get(pk=pk) 
    except Item.DoesNotExist: 
        return Response({'message': 'The scenario does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    if request.method == 'GET': 
        #item_data = JSONParser().parse(request) 
        
        
        serializer = ItemRecommendSerializer(item_result)
        #serializer = ItemRecoSerializer(item_result)
        return Response(serializer.data)
       
        if item_result:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class SubmitScoreView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access this view

    def post(self, request, *args, **kwargs):
        user = request.user  # Authenticated user
        item_id = request.data.get('item')
        score = request.data.get('score')

        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

        # Save the item result
        item_result = ItemResult.objects.create(user=user, item=item, score=score)
        item_result.save()

        return Response({"message": "Score submitted successfully!"}, status=status.HTTP_201_CREATED)

class CheckLevelProgressionView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access this view

    def get(self, request, *args, **kwargs):
        user = request.user  # Get the authenticated user
        user_profile = UserProfile.objects.get(user=user)
        current_level = user_profile.current_level

        # Calculate total score for the current level
        total_score = ItemResult.objects.filter(user=user, item__level=current_level).aggregate(
            total_score=Sum('score')
        )['total_score']

        if total_score is None:
            total_score = 0

        # Check if total score for the current level is 70 or more
        if total_score >= 180:
            if current_level < 3:
                user_profile.current_level += 1
                user_profile.save()
                return Response({"message": f"You have been promoted to level {user_profile.current_level}!"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "You have already reached the highest level."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Your total score for this level is not enough to move to the next level. Your score needs to be more than 180"}, status=status.HTTP_200_OK)



class ItemSearchView(generics.ListAPIView):
    serializer_class = ItemSearchSerializer

    def get_queryset(self):
        queryset = Item.objects.all().prefetch_related('competencys')  # Prefetch competencys for optimization
        tags = self.request.query_params.get('tags', None)
        competency_id = self.request.query_params.get('competency', None)

        if tags:
            tag_list = tags.split(',')
            queryset = queryset.filter(Q(tags__icontains=tag_list[0]))
            for tag in tag_list[1:]:
                queryset = queryset.filter(Q(tags__icontains=tag))

        if competency_id:
            queryset = queryset.filter(competencys__id=competency_id)

        return queryset





class ItemLibraryAPIView(generics.ListAPIView):
    queryset = Item.objects.all()  # Fetch all items from the database
    serializer_class = ItemLibrarySerializer
    filter_backends = [filters.SearchFilter]  # Enable searching
    search_fields = ['name', 'description', 'tags']  



class LeaderboardPercentileAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get query parameters
        competency_id = self.request.query_params.get('competency_id')
        suborg_id = self.request.query_params.get('suborg_id')

        # Validate query parameters
        if not competency_id or not suborg_id:
            return []

        # Retrieve the user's account
        user = self.request.user
        try:
            user_account = Account.objects.get(email=user.email)
        except Account.DoesNotExist:
            return []

        # Check if the user has a sub_org mapped
        if user_account.sub_org is None:
            return Response(
                {"status": "Failed", "message": "Please map and create a sub-organization."},
                status=status.HTTP_400_BAD_REQUEST
            )

        org_id = user_account.org.id
        suborg_id = user_account.sub_org.id

        # Get summed scores for each user filtered by competency and suborg
        item_results = (
            ItemResult.objects.filter(
                item__competencys__id=competency_id,
                user__org_id=org_id,
                user__sub_org_id=suborg_id
            )
            .values('user__email')
            .annotate(total_score=Sum('score'))  # Sum scores for each user
            .order_by('-total_score')  # Order by total score in descending order
        )

        if not item_results.exists():
            return []

        # Get scores and calculate percentiles
        scores = [result['total_score'] for result in item_results]
        scores.sort(reverse=True)  # Sort scores in descending order

        def calculate_percentile(score, scores):
            total_scores = len(scores)
            lower_scores = len([s for s in scores if s <= score])  # Include scores equal to the current score
            percentile = (lower_scores / total_scores) * 100
            return percentile

        leaderboard_data = []
        for result in item_results:
            user_email = result['user__email']
            total_score = result['total_score']
            percentile = calculate_percentile(total_score, scores)
            leaderboard_data.append({
                'user_email': user_email,
                'total_score': total_score,
                'percentile': percentile
            })

        # Sort by percentile in descending order
        sorted_leaderboard = sorted(leaderboard_data, key=lambda x: x['percentile'], reverse=True)

        return sorted_leaderboard

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if isinstance(queryset, Response):
            return queryset  # Return the error response if there is one

        return Response({
            "status": "Success",
            "message": "Retrieved Successfully",
            "data": queryset
        })

class DownloadCSV(APIView):
    #permission_classes = [IsAuthenticated]  # Optional: add this if you want authentication

    def get(self, request, *args, **kwargs):
        # Create the HttpResponse object with the appropriate CSV header
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="item_emotions.csv"'

        # Create a CSV writer
        writer = csv.writer(response)
        
        # Write header
        writer.writerow(['Item Name', 'Item Emotion'])
        
        # Fetch all items and write their `item_emotion` to the CSV
        items = Item.objects.all().values_list('item_name', 'item_emotion')
        for item in items:
            writer.writerow(item)

        return response     


class LibraryFilterChoicesView(APIView):
    """
    API View to return the available choices for library_filter.
    """
    def get(self, request):
        # Convert the choices into a list of dictionaries
        choices = [{"value": key, "label": label} for key, label in Library_Filter_CHOICES]
        return Response(choices, status=status.HTTP_200_OK)


class ItemFilterView(generics.ListAPIView):
    serializer_class = ItemFilterSerializer

    def get_queryset(self):
        queryset = Item.objects.all()
        # Get query parameters
        library_filter = self.request.query_params.get('library_filter', None)
        tags = self.request.query_params.get('tags', None)
        competency_id = self.request.query_params.get('competency', None)

        # Filter by library_filter (case-insensitive)
        if library_filter:
            queryset = queryset.filter(library_filter__name__iexact=library_filter)

        # Filter by tags (comma-separated values, case-insensitive)
        if tags:
            tag_list = tags.split(',')
            for tag in tag_list:
                queryset = queryset.filter(tags__icontains=tag.strip())

        # Filter by competency
        if competency_id:
            queryset = queryset.filter(competencys__id=competency_id)

        return queryset



class ItemCreateAPIView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemNewSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)  # for handling file uploads        

def upload_item_view(request):
    competencies = Competency.objects.all()
    #roles = Role1.objects.all()
    return render(request, 'newitem/upload_item.html', {
        'competencies': competencies,
        
    })    

class AvailableItemsView(generics.ListAPIView):
    serializer_class = ItemAvailableSerializer1
    #serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_profile = user.userprofile
        current_level = user_profile.current_level

        # Calculate the total score for the current user for all items at the current level
        total_score = ItemResult.objects.filter(
            user=user,
            item__level=current_level
        ).aggregate(total=Sum('score'))['total'] or 0

        # Define score thresholds for each level
        level_thresholds = {
            1: 180,  # Need 180 to move to level 2
            2: 360,  # Need 360 to move to level 3
        }

        # Check if user has enough score to access the next level
        next_level_threshold = level_thresholds.get(current_level)

        # Create the level range based on the user's current level
        if next_level_threshold and total_score < next_level_threshold:
            # User is restricted to their current level and all previous levels
            level_range = list(range(1, current_level + 1))
        else:
            # User can access the current level, previous levels, and the next level
            level_range = list(range(1, current_level + 2))

        # Return items that belong to the levels within the calculated level range
        return Item.objects.filter(
            level__in=level_range,
            itemseason__season__series__seriesassignuser__user=user,
            itemseason__season__series__seriesassignuser__is_completed=False
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Check the user's total score and display message if they can't move to the next level
        user = request.user
        current_level = user.userprofile.current_level

        total_score = ItemResult.objects.filter(
            user=user,
            item__level=current_level
        ).aggregate(total=Sum('score'))['total'] or 0

        # Define level thresholds again
        level_thresholds = {
            1: 180,
            2: 360,
        }

        # Calculate if user has met the threshold
        next_level_threshold = level_thresholds.get(current_level)

        if next_level_threshold and total_score < next_level_threshold:
            message = f'Your total score is {total_score}. You need {next_level_threshold - total_score} more points to reach the next level.'
        else:
            message = 'You are eligible to access the next level items.'

        # Add message to the response
        return Response({
            'items': serializer.data,
            'message': message,
            'current_level': current_level,
            'total_score': total_score
        }, status=status.HTTP_200_OK)

class ItemResultCreateView(generics.CreateAPIView):
    queryset = ItemResult.objects.all()
    serializer_class = ItemResultUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Save the logged-in user as the user for the item result
        serializer.save(user=self.request.user)

class ItemResultListView(generics.ListAPIView):
    queryset = ItemResult.objects.all()
    serializer_class = ItemResultUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter to show only the logged-in user's item results
        return ItemResult.objects.filter(user=self.request.user)     

class LibraryFilterItemCountView(APIView):
    def get(self, request, *args, **kwargs):
        library_filters = LibraryFilter.objects.all()
        total_item_count = 0
        data = []
        
        for library_filter in library_filters:
            items = library_filter.item_set.all()
            item_count = items.count()
            item_names = [item.item_name for item in items]
            total_item_count += item_count
            data.append({
                'library_name': library_filter.name,
                'item_count': item_count,
                'item_names': item_names,
            })
        
        response_data = {
            'total_items': total_item_count,
            'libraries': data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

# API to download items mapped to each library filter as CSV
@permission_classes([AllowAny])
class DownloadLibraryItemsCSVView(APIView):
    def get(self, request, *args, **kwargs):
        library_filters = LibraryFilter.objects.all()
        total_item_count = 0
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="library_items.csv"'

        writer = csv.writer(response)
        
        # Calculate total items
        for library_filter in library_filters:
            total_item_count += library_filter.item_set.count()

        # Write total items count at the top
        writer.writerow(['Total Items', total_item_count])
        writer.writerow([])  # Empty row for spacing
        writer.writerow(['Library Name', 'Item Count', 'Item Names'])

        for library_filter in library_filters:
            items = library_filter.item_set.all()
            item_names = [item.item_name for item in items]
            writer.writerow([library_filter.name, items.count(), ', '.join(item_names)])

        return response