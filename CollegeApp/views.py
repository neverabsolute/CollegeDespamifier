from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from .models import College

from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return 

@method_decorator(csrf_exempt, name='dispatch')
class CollegeAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    @csrf_exempt
    @api_view(['POST'])
    def post(self, request, *args, **kwargs):
        authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
        request_body = request.data

        filters = {}
        domains = []
        # try accessing keys
        try:
            domains = request_body['domains']
            filters = request_body['filters']
        except Exception as e:
            # send 400 status code for bad request
            content = {'error': 'No domains or filters specified.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # check if domains is list of strings
        if not isinstance(domains, list) and all(isinstance(domain, str) for domain in domains):
            content = {'error': 'Invalid domain(s).'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # check if filters is dict
        if not isinstance(filters, dict):
            content = {'error': 'Invalid filter(s).'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        college_dict = {}

        for domain in domains:
            total_filters = 0
            passed_filters = 0
            college_info = None
            if '@' in domain:
                parsed_domain = domain.split('@')[1]
            else:
                parsed_domain = domain

            try:
                college_info = College.objects.get(domain = parsed_domain)
            except College.MultipleObjectsReturned:
                college_info = College.objects.filter(domain = parsed_domain)[0]
            except College.DoesNotExist:
                continue
            try:
                # SAT Score
                if filters.get('optOutStatus').get('useSATScore') == 'true':
                    filter_data = filters.get('sat')
                    if filter_data.get('min') and college_info.sat:
                        total_filters += 1
                        if int(filter_data.get('min')) <= college_info.sat:
                            passed_filters += 1
                    if filter_data.get('max') and college_info.sat:
                        total_filters += 1
                        if int(filter_data.get('max')) >= college_info.sat:
                            passed_filters += 1
                # ACT Score
                if filters.get('optOutStatus').get('useACTScore') == 'true':
                    filter_data = filters.get('act')
                    if filter_data.get('min') and college_info.act:
                        total_filters += 1
                        if int(filter_data.get('min')) <= college_info.act:
                            passed_filters += 1
                    if filter_data.get('max') and college_info.act:
                        total_filters += 1
                        if int(filter_data.get('max')) >= college_info.act:
                            passed_filters += 1
                # Tuition
                if filters.get('optOutStatus').get('useTution') == 'true':
                    filter_data = filters.get('tuition')
                    if filter_data.get('max') and college_info.tuition:
                        total_filters += 1
                        if int(filter_data.get('max')) >= college_info.tuition:
                            passed_filters += 1
                # Student Body Size
                if filters.get('optOutStatus').get('useStudentBodySize') == 'true':
                    filter_data = filters.get('studentbodysize')
                    if filter_data.get('min') and college_info.undergrad_student_body:
                        total_filters += 1
                        if int(filter_data.get('min')) <= college_info.undergrad_student_body:
                            passed_filters += 1
                    if filter_data.get('max') and college_info.undergrad_student_body:
                        total_filters += 1
                        if int(filter_data.get('max')) >= college_info.undergrad_student_body:
                            passed_filters += 1
                # Acceptance Rate
                if filters.get('optOutStatus').get('useAcceptanceRate') == 'true':
                    filter_data = filters.get('acceptanceRate')
                    if filter_data.get('min') and college_info.acceptance:
                        total_filters += 1
                        if int(filter_data.get('min')) <= college_info.acceptance:
                            passed_filters += 1
                    if filter_data.get('max') and college_info.acceptance:
                        total_filters += 1
                        if int(filter_data.get('max')) >= college_info.acceptance:
                            passed_filters += 1
                # School Rankings
                if filters.get('optOutStatus').get('useRanking') == 'true':
                    filter_data = filters.get('schoolRankings')
                    if filter_data.get('lowestRanking') and college_info.overall_rank:
                        total_filters += 1
                        if int(filter_data.get('lowestRanking')) <= college_info.overall_rank:
                            passed_filters += 1
                # Region
                if filters.get('optOutStatus').get('useStates') == 'true':
                    filter_data = filters.get('states')
                    if filter_data:
                        total_filters += 1
                        if college_info.state in filter_data:
                            passed_filters += 1
            except:
                content = {'error': 'Invalid Filters'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            if total_filters != passed_filters:
                college_dict[domain] = True
            else:
                college_dict[domain] = False

        return Response(college_dict, status=status.HTTP_200_OK)