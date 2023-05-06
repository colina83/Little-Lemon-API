from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser, BasePermission
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User,Group
from .serializers import GroupSerializer,MenuItemSerializer,CategorySerializer
from rest_framework.views import APIView
from .models import MenuItem,Category
from django.contrib.auth import authenticate,login

# Create your views here.

#App to test if there is authentication 
@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message": "This is a secret message!"})

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name="Manager").exists():
        return Response({"message": "Only Manager Should see"})
    else:
        return Response({"message": "you are not authorized"},403)
    
# 1. The admin can assign users to the manager group

@api_view(['POST'])
#The decorator below ensures that only an admin can assign users to the manager group
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User,username=username)
        managers = Group.objects.get(name='Manager')
        if request.method == 'POST':
            managers.user_set.add(user)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)            
        return Response({"message:ok"})
        
    return Response({"message:ok"}, status.HTTP_400_BAD_REQUEST)

# 2.- You can access the manager group with an admin token
@api_view(['GET'])
@permission_classes([IsAdminUser])
def manager_group(request):
    try:
        manager_group = Group.objects.get(name='Manager')
    except Group.DoesNotExist:
        return Response({'error': 'Manager group does not exist'}, status=status.HTTP_404_NOT_FOUND)
    serializer = GroupSerializer(manager_group)
    return Response(serializer.data)

#3.- The admin can add menu items
class MenuItemView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self,request):
        menu_items = MenuItem.objects.all()
        serializer = MenuItemSerializer(menu_items,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
    

#4.- The admin can add categories and view categories

class CategoryView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self,request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
    
#5.- Managers Can Log in
class ManagerLoginView(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})

        return Response({'error': 'Invalid credentials'})


# 7. Managers can assign users to the delivery crew

#Creating a Class that inherits from Base Permission

class CanAddtoDeliveryCrewGroup(BasePermission):
    def has_permission(self, request):
        user = request.user
        if user.is_authenticated and user.groups.filter(name='Manager').exists():
            return user.has_perm('auth.add_user') and user.has_perm('auth.change_user')
        return False

@api_view(['POST'])
@permission_classes([CanAddtoDeliveryCrewGroup])
def delivery_crew(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        delivery_crew = Group.objects.get(name='Delivery crew')
        if request.method == 'POST':
            delivery_crew.user_set.add(user)
        else:
            return Response({"message": "You can only add users"}, status.HTTP_400_BAD_REQUEST)               
        return Response({"message": "ok"})
    return Response({"message": "ok"}, status.HTTP_400_BAD_REQUEST)