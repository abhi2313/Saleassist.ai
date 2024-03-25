

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from django.http import Http404

class ProductList(APIView):
    """
    View to list all products or create a new product.
    """
    
    def get(self, request, format=None):
        """
        Get all products.

        Returns:
            Response: Response with list of products.
        """
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create a new product.


        Returns:
            Response: Response with created product data or validation errors.
        """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(APIView):
    """
    View to retrieve, update or delete a product instance.
    """

    def get_object(self, pk):
        """
        Get product instance by primary key.

     

        Returns:
            Product: Product instance.

        Raises:
            Http404: If product does not exist.
        """
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Retrieve a product instance.


        Returns:
            Response: Response with product data.

        Raises:
            Http404: If product does not exist.
        """
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Update a product instance.

   

        Returns:
            Response: Response with updated product data or validation errors.

        Raises:
            Http404: If product does not exist.
        """
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Delete a product instance.


        Returns:
            Response: Response with HTTP status 204.

        Raises:
            Http404: If product does not exist.
        """
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
