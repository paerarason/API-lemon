from rest_framework import generics
from .models import MenuItem, Category,Cart,Orders,DeliveryProfile,orders_places
from .serializers import MenuItemSerializer, CategorySerializer,CartSerializer,OrderSerializer,CurrentUserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes,throttle_classes
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle
from .delivery import place_order
from django.contrib.auth.models import User,Group
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes=[]
    
@api_view(["GET","POST"])
@permission_classes([])
def cat_detail(request,pk):
    try:
        menu=Category.objects.get(id=pk)
        m=MenuItem.objects.filter(category=menu)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=="GET":
        serializer=MenuItemSerializer(m,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    serializer_class = MenuItemSerializer
    permission_classes=[]
    ordering_fields = ['price', 'inventory']
    filterset_fields = ['price', 'inventory']
    search_fields = ['title']

class MenuItemsViewAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    serializer_class = MenuItemSerializer
    permission_classes=[]
    ordering_fields = ['price', 'inventory']
    filterset_fields = ['price', 'inventory']
    search_fields = ['title']
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def Menu_list(request):
    if request.method=="POST":
        if request.user.groups.filter(name="Manager").exists():
           serializer_item=MenuItemSerializer(data=request.data)
           serializer_item.is_valid(raise_exception=True)
           serializer_item.save()
           return Response(serializer_item.data,status.HTTP_201_CREATED)
        else:
           return Response({"message":"you are  not allowed to do that task-"})
    if request.method=="GET":
        item=MenuItem.objects.select_related('category').all()
        serializer_item=MenuItemSerializer(item,many=True)
        return Response(serializer_item.data,status=status.HTTP_200_OK)
    return Response({"message":"you are not authenticate to this operations"})
    

@api_view(["GET","PUT","PATCH","DELETE"])
@throttle_classes([UserRateThrottle])
def Menu_detail(request,pk):
    try:
        menu=MenuItem.objects.get(id=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=="GET":
        serializer=MenuItemSerializer(menu)
        return Response(serializer.data,status=status.HTTP_200_OK)
    user=request.user
    if user.groups.filter(name='Manager').exists():
        
        if request.method=="PUT":
            serializer=MenuItemSerializer(menu,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method=="PATCH":
            serializer=MenuItemSerializer(menu,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        elif request.method=="DELETE":
            menu.delete()
            return Response(status=status.HTTP_200_OK)
    else:
        return Response({"message":"you are not allowed here"},status=status.HTTP_403_FORBIDDEN)


@api_view(["GET","POST","DELETE"])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def Cart_list(request):
    if request.user.groups.filter(name='customer').exists(): 
        try:
            cart=Cart.objects.get(user=request.user)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND) 
        if request.method=="GET":
           serializer_item=CartSerializer(cart)
           return Response(serializer_item.data,status=status.HTTP_200_OK)
        elif request.method=="POST":
           serializer_item=MenuItemSerializer(data=request.data)
           serializer_item.is_valid(raise_exception=True)
           cart.menu=serializer_item.save()
           return Response(serializer_item.data,status.HTTP_201_CREATED)    
        else:
            menu=cart.menu
            menu.delete()
            return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def Order_list(request):
    if request.user.groups.filter(name='Manager').exists():
      if request.method=="GET":
        order=Orders.objects.all()
        serializer=OrderSerializer(order)
        return Response(serializer.data,status=status.HTTP_200_OK)
    if request.user.groups.filter(name='customer').exists():
       try:
            order=Orders.objects.get(customer=request.user)
       except:
            return Response(status=status.HTTP_404_NOT_FOUND)
       if request.method=="GET":
         serializer=OrderSerializer(order)
         return Response(serializer.data,status=status.HTTP_200_OK)
       elif request.method=="POST":
         serializer_item=OrderSerializer(data=request.data)
         serializer_item.is_valid(raise_exception=True)
         order=serializer_item.save()
         place_order(order)
         return Response(serializer_item.data,status.HTTP_201_CREATED)
    if request.user.groups.filter(name='customer').exists():
        try:
            order=Orders.objects.get(delivery_crew=request.user)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method=="GET":
          serializer=OrderSerializer(order)
          return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(status=status.HTTP_403_FORBIDDEN)
    

@api_view(["GET","PUT","PATCH","DELETE"])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def Order_detail(request,pk):
    if request.user.groups.filter(name='customer').exists():
       try:
            order=Orders.objects.get(id=pk)
       except:
            return Response(status=status.HTTP_404_NOT_FOUND)
       if request.method=="GET":
           serializer=OrderSerializer(order) 
           return Response(serializer.data)
       elif request.method=="PUT":
           serializer=OrderSerializer(order,data=request.data)
           if serializer.is_valid():
              serializer.save()
              return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
           else:
              return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.user.groups.filter(name='DeliveryCrew').exists():
        if request.method=="PATCH":
           serializer=OrderSerializer(order,data=request.data,partial=True)
           if serializer.is_valid():
              order=serializer.save()
              if order.delivery_status==True:
                crew=order.delivery_crew
                profile=DeliveryProfile.objects.get(user=crew)
                profile.availability_status=True
              return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
           else:
              return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.user.groups.filter(name='manager').exists():
        if request.method=="DELETE":
            order.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.user.groups.filter(name='DeliveryCrew').exists():
        if request.method=="PATCH":
            serializer=OrderSerializer(order,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)        
        if request.method=="GET":
           serializer=OrderSerializer(order)
           return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(status=status.HTTP_403_FORBIDDEN)





'''     <<   groups view methods   >>        ''' 

@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def Groups_list(request):
    if request.user.groups.filter(name='Manager').exists():
       user=User.objects.filter(groups__name='Manager')
       if request.method=="GET" and user!=None:
           serializer=CurrentUserSerializer(user,many=True)
           return Response(serializer.data,status=status.HTTP_200_OK)
       elif request.method=="POST":
           serializer=CurrentUserSerializer(data=request.data)
           if serializer.is_valid():
              hey=serializer.save()
              print(hey)
              my_group = Group.objects.get(name='Manager') 
              my_group.user_set.add(hey)
              return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def Groups_detail(request,pk):
    if request.user.groups.filter(name='Manager').exists():
       try:
            user=User.objects.get(id=pk)
       except:
            return Response(status=status.HTTP_404_NOT_FOUND)
       if request.method=="DELETE":
           user.delete()
           return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def delivery_list(request):
    if request.user.groups.filter(name='Manager').exists():
       user=User.objects.filter(groups__name='DeliveryCrew')
       print(user)
       if request.method=="GET" and user!=None:
           serializer=CurrentUserSerializer(user,many=True)
           return Response(serializer.data,status=status.HTTP_200_OK)
       elif request.method=="POST":
           serializer=CurrentUserSerializer(data=request.data)
           if serializer.is_valid():
              serializer.save()
              return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def delivery_detail(request,pk):
    if request.user.groups.filter(name='Manager').exists():
       try:
            user=User.objects.get(id=pk)
       except:
            return Response(status=status.HTTP_404_NOT_FOUND)
       if request.method=="DELETE":
           user.delete()
           return Response(status=status.HTTP_200_OK)
    else:
       return Response(status=status.HTTP_400_BAD_REQUEST)







@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle])
@throttle_classes([UserRateThrottle])
def managerview(request):
    if request.user.groups.filter(name='Manager').exists():
      return Response({"message":"Manager here"})
    else:
      return Response({"message":"you are  not allowed here"})  