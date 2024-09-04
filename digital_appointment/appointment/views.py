from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework_simplejwt import authentication
from . import serializers
from .models import Appointment
from django.db.models import Q
from drf_spectacular.utils import extend_schema


class AppointmentView(APIView):
    """
    permission to any authenticate user use post or personal get
    if user is provider or patient work for both
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    """save Schema of api for guide other Distributor"""

    @extend_schema(tags=['Appointment'], responses=serializers.AppointmentSerializer)
    def post(self, request):
        serializer = serializers.AppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        validate_appointment = Appointment.objects.filter(user=request.user)
        serializer = serializers.AppointmentSerializer(validate_appointment, many=True)
        return Response(serializer.data)


class AppointmentDetailView(APIView):
    """
    permission to any authenticate user use retrieve or put or delete
    method if user is provider or patient work for both
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    """save Schema of api for guide other Distributor"""

    @extend_schema(tags=['Appointment'], responses=serializers.AppointmentSerializer)
    def get(self, request, pk):
        validate_appointment = Appointment.objects.filter(
            Q(user=request.user) |
            Q(id=pk)
        ).first()
        serializer = serializers.AppointmentSerializer(validate_appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        validate_appointment = Appointment.objects.filter(user=request.user, id=pk).first()
        serializer = serializers.AppointmentSerializer(validate_appointment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        validate_appointment = Appointment.objects.filter(user=request.user, id=pk).first()
        if validate_appointment:
            validate_appointment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
