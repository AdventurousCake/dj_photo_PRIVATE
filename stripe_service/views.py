from django.db.models import Prefetch
from django.shortcuts import render

from django.views.generic import TemplateView
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from stripe_service.models import Item, Order
from stripe_service.services.stripe import create_stripe_session


class SuccessesView(TemplateView):
    template_name = "stripe_page/successes.html"


class CancelView(TemplateView):
    template_name = "stripe_page/cancel.html"


class OrderPageView(TemplateView):
    template_name = "stripe_page/order.html"

    def get_context_data(self, pk, **kwargs):
        order = Order.objects.select_related('item').get(id=pk)

        context = super(OrderPageView, self).get_context_data(**kwargs)
        context.update({
            "order": order,
            "products": order.items,
            "order_total": order.get_discount_total_cost()
        })
        return context


class ProductLandingPageView(TemplateView):
    template_name = "stripe_page/index.html"

    def get_context_data(self, pk, **kwargs):
        # fixme
        # product = Item.objects.prefetch_related(Prefetch('order_set')).get(id=pk)
        product = Item.objects.get(id=pk)
        print(product)

        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            # "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY,
            "product": product,
            "order_total": product.order_set.first().get_discount_total_cost()
            # "order_total": product.order_set.first().get_discount_total_cost()
        })
        return context


# API
class CreateCheckoutSessionAPIView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        pass


class CreateCheckoutSessionAPIView(APIView):
    def get(self, request, pk):
        # product = Item.objects.get(id=pk)  # id=self.kwargs.get('pk')
        product = get_object_or_404(Item, id=pk)  # drf.get_obj
        print(product)

        # todo stripe logic
        create_stripe_session(product_name=product.id, currency=product.currency, quantity=1)

        return Response({})
