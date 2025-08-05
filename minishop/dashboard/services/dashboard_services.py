from django.db.models import Count
from payment.models import (Address, Payment, Order,
                            Product, OrderItem, Refund, ReturnRequest)
from django.db.models import Sum, Count
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.functions import TruncMonth , TruncDay
from collections import OrderedDict
from datetime import  timedelta
import calendar, datetime




class DashboardServices:
    def get_cards(self):
        today= timezone.now().date()
        yesterday= today - datetime.timedelta(days=1)
        
        order= self._get_orders_card(today, yesterday)
        revenue= self._get_revenue_card(today, yesterday)
        customers= self._get_customers_card(today, yesterday)
        refunds= self._get_refunds_card(today, yesterday)
        recent_orders= self._get_recent_orders()
        low_stock_products= self._get_low_stock_products()
        context= {
            'order':order,
            'revenue':revenue,
            'customers':customers,
            'refunds':refunds,
            'recent_orders':recent_orders,
            'low_stock_products':low_stock_products,
        }
        return context
        
    def _get_orders_card(self, today, yesterday):
        """
        Returns total number of orders and today's growth percentage
        compared to yesterday's orders.
        """
        total_orders= Order.objects.count()
        yesterday_orders= Order.objects.filter(created_at__date = yesterday).count()
        today_orders= Order.objects.filter(created_at__date = today).count()
        difference_orders= today_orders - yesterday_orders
        
        if yesterday_orders > 0:
            # Calculate percentage increase compared to yesterday
            percentage_orders = float((difference_orders / yesterday_orders) * 100)
        else: 
            # If no orders yesterday, set to 100% if today has orders
            percentage_orders = 100 if today_orders > 0 else 0
        context= {
            'total_orders':total_orders,
            'percentage_orders':round(percentage_orders, 2),
        }
        return context
    
    def _get_revenue_card(self, today, yesterday):
        """
        Returns total revenue and today's growth percentage
        compared to yesterday's revenue.
        """
        total_revenue= Order.objects.aggregate(total_revenue=Sum('total_price'))['total_revenue']or 0
        yesterday_revenue= Order.objects.filter(created_at__date = yesterday).aggregate(yesterday_revenue=Sum('total_price'))['yesterday_revenue']or 0
        today_revenue= Order.objects.filter(created_at__date = today).aggregate(today_revenue=Sum('total_price'))['today_revenue']or 0
        
        difference_revenue= today_revenue - yesterday_revenue
        
        if yesterday_revenue > 0:
            # Calculate percentage increase compared to yesterday
            percentage_revenue = float((difference_revenue / yesterday_revenue) * 100)
        else: 
            # If no orders yesterday, set to 100% if today has orders
            percentage_revenue = 100 if today_revenue > 0 else 0
        context= {
            'total_revenue':total_revenue,
            'percentage_revenue':round(percentage_revenue, 2),
        }
        return context
    
    def _get_customers_card(self, today, yesterday):
        """
        Returns total number of customers and today's growth percentage
        compared to yesterday's customers.
        """
        total_customers= User.objects.filter(is_superuser=False).count()
        yesterday_customers= User.objects.filter(is_superuser=False).filter(date_joined__date = yesterday).count()
        today_customers= User.objects.filter(is_superuser=False).filter(date_joined__date = today).count()
        
        difference_customers= today_customers - yesterday_customers
        
        if yesterday_customers > 0:
            # Calculate percentage increase compared to yesterday
            percentage_customers = float((difference_customers / yesterday_customers) * 100)
        else: 
            # If no orders yesterday, set to 100% if today has orders
            percentage_customers = 100 if today_customers > 0 else 0
        context= {
            'total_customers':total_customers,
            'percentage_customers':round(percentage_customers, 2),
        }
        return context
    
    def _get_refunds_card(self, today, yesterday):
        """
        Returns total refunds and today's growth percentage
        compared to yesterday's refunds.
        """
        total_refunds= Refund.objects.count()
        yesterday_refunds= Refund.objects.filter(created_at__date = yesterday).count()
        today_refunds= Refund.objects.filter(created_at__date = today).count()
        
        difference_refunds= today_refunds - yesterday_refunds
        
        if yesterday_refunds > 0:
            # Calculate percentage increase compared to yesterday
            percentage_refunds = float((difference_refunds / yesterday_refunds) * 100)
        else: 
            # If no orders yesterday, set to 100% if today has orders
            percentage_refunds = 100 if today_refunds > 0 else 0
        context= {
            'total_refunds':total_refunds,
            'percentage_refunds':round(percentage_refunds, 2),
        }
        return context

    def _get_recent_orders(self):
        """
        Get recent 5 orders 
        """
        orders = Order.objects.order_by('-id')[:5]
        return orders
    
    def _get_low_stock_products(self):
        """
        Get low stock products
        """
        products = Product.objects.filter( quantity__lte = 5).order_by('-id')[:5]
        return products
    
    
class DashboardChartsServices:
    def get_chats(self):
        orders_charts= self._orders_chart()
        context= {
            'orders_charts':orders_charts,
        }
        return context
        
   
    def _orders_chart(self):
        # Step 1: Monthly aggregated data from DB
        monthly_sales = (
            Order.objects
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(total=Sum('total_price'))
            .order_by('month')
        )

        # Step 2: Empty dict with all 12 months initialized as 0
        all_months = OrderedDict()
        for i in range(1, 13):
            month_label = calendar.month_abbr[i]  # Jan, Feb, etc.
            all_months[month_label] = 0
            
        # Step 3: Fill data from DB into our 12-month dict
        for entry in monthly_sales:
            month = entry['month']
            month_label = month.strftime('%b')  # Jan, Feb, etc.
            all_months[month_label] = float(entry['total'])

        # Step 4: Prepare Chart.js-compatible format
        chart_data = {
            "labels": list(all_months.keys()),
            "datasets": [{
                "label": "Monthly Sales",
                "data": list(all_months.values()),
                "backgroundColor": 'rgba(75, 192, 192, 0.2)',
                "borderColor": 'rgba(75, 192, 192, 1)',
                "borderWidth": 1
            }]
        }
        return chart_data
    
    def get_orders_weekly_chart_data(self):
        # Get current date and calculate last Monday
        today = datetime.datetime.today().date()
        this_monday = today - timedelta(days=today.weekday())  # Monday = 0
        this_sunday = this_monday + timedelta(days=6)

        # Queryset: Orders grouped by day within this week (Mon to Sun)
        daily_sales = (
            Order.objects
            .filter(created_at__date__gte=this_monday, created_at__date__lte=this_sunday)
            .annotate(day=TruncDay('created_at'))
            .values('day')
            .annotate(total=Sum('total_price'))
            .order_by('day')
        )

        # Initialize all 7 days with 0
        all_days = OrderedDict()
        for i in range(7):  # 0 to 6 (Mon to Sun)
            day = this_monday + timedelta(days=i)
            day_label = day.strftime('%a')  # Mon, Tue, etc.
            all_days[day_label] = 0
        # Fill actual data
        for entry in daily_sales:
            day_label = entry['day'].strftime('%a')
            all_days[day_label] = float(entry['total'])
        # Final Chart.js format
        chart_data = {
            "labels": list(all_days.keys()),
            "datasets": [{
                "label": "Daily Sales (Mon-Sun)",
                "data": list(all_days.values()),
                "backgroundColor": 'rgba(153, 102, 255, 0.2)',
                "borderColor": 'rgba(153, 102, 255, 1)',
                "borderWidth": 1
            }]
        }

        return {"weekly_chart": chart_data}