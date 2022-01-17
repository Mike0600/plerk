#Django
from django.db.models import Count, Sum, Q

#Django restframework
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions

#Models
from .models import Company, Transaction 

#Serializers
from .serializers import CompanySerializer, TransactionSerializer


class TransactionsListView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all().annotate(Count('company_id', distinct=True))
    

def check_transactions(status):
        trans = (Transaction.objects.filter(transaction_status=f'{status}').values())
        total_paid_transactions: int = 0
        for trans in list(trans):
            total_paid_transactions += int(trans['price'])
        return total_paid_transactions




class ListCompanyService(APIView):
   # permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        company_id = request.GET['id']
        company_name = (Company.objects.filter(id=company_id)).values()[0]['name']
        company_sales_with = (Transaction.objects.all()).filter(company_id=company_id, final_charge=True).values()
        company_sales_with_no = Transaction.objects.filter(company_id=company_id, final_charge=False).values()

        data = {
            'companyID' : company_id,
            'companyName' : company_name,
            'companySalesWithFinalCharge' : company_sales_with,
            'companySalesWithNoFinalCharge' : company_sales_with_no,
        }
        return Response(data)


class ListResumeService(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        company_sales = (Transaction.objects.values_list('company_id_id').annotate(company_count=Count('company_id_id')).order_by('-company_count'))
        top_seller_id = list(company_sales)[0][0]
        top_seller_sales = list(company_sales)[0][1]
        top_seller_name = (Company.objects.filter(id=top_seller_id)).values()[0]['name']

        loser_seller_id = list(company_sales)[company_sales.count()-1][0]
        loser_seller_sales = list(company_sales)[company_sales.count()-1][1]
        loser_seller_name = (Company.objects.filter(id=loser_seller_id)).values()[0]['name']

        total_closed_transactions = check_transactions('C')
        total_pending_transactions = check_transactions('P')

        non_approved_transacions = company_sales.filter(approbal_status=False)
        non_approved_company_id = list(non_approved_transacions)[0][0]
        non_approved_company_sales = list(company_sales)[0][1]
        non_approved_company_name = (Company.objects.filter(id=non_approved_company_id)).values()[0]['name']

        
        data = {
            'topSeller' : {
                'topSellerName' : top_seller_name,
                'numberSales' : top_seller_sales,
            },
            'loserSeller' : {
                'loserSellerId':loser_seller_name,
                'numberSales' : loser_seller_sales,
            },
            'totalClosedTransactions' : total_closed_transactions,
            'totalPendingTransactions' : total_pending_transactions,
            'mostNonApproved' : {
                'mostNonApprovedCompanyName' :non_approved_company_name,
                'mostNonApprovedCompanySales': non_approved_company_sales,
            },
        }
            

        return Response(data)

def days(month):
    if month % 2 == 0:
            return 31

    else:
        return 30


def check_date(date):
    month = int((date.split('-'))[1])
    year = int((date.split('-'))[0])
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        if month == 2:
            return 29
        else:
            return days(month)
    else:
        if month == 2:
            return 28
        else:
            return days(month)

        

class MonthResumeService(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        date_request = request.GET['date']
        last_day_month = check_date(date_request)

        transactions_per_month = Transaction.objects.filter(date__range=[f"{date_request}-01", f"{date_request}-{last_day_month}"])
        total_spend = transactions_per_month.aggregate(total=Sum('price', filter=Q(final_charge=True))).values()
        non_approved_trasactions_total = transactions_per_month.aggregate(total=Sum('price', filter=Q(final_charge=False))).values()
        data = {
            'transactionsInMonth' : transactions_per_month.values(),
            'totalSpend' : list(total_spend)[0],
            'non_approved_trasactions_total' : list(non_approved_trasactions_total)[0],
            }
        return Response(data)



class CompanysListView(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [permissions.IsAuthenticated]

