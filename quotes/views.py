from django.shortcuts import render, redirect
import requests
import json
from .forms import StockForm
from .models import Stock
from django.contrib import messages

# Create your views here.
def home(request):


	if request.method == 'POST':
		ticker = request.POST['ticker']
		# pk_f7d2284f14d64a9293638feab9c6911b
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/%s/quote?token=pk_f7d2284f14d64a9293638feab9c6911b" %ticker)
		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error..."
		return render(request, 'home.html', {'api': api})
	else:
	   return render(request, 'home.html', {'ticker': "Please enter a Ticker Symbol above"})



def about(request):
	return render(request, 'about.html', {})

def add_stock(request):
	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock Has Been Added"))
			return redirect('add_stock')
	else:

		ticker = Stock.objects.all()
		output = []
		for ticker_item in ticker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/%s/quote?token=pk_f7d2284f14d64a9293638feab9c6911b" %str(ticker_item))
			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error..."

		return render(request, 'add_stock.html', {'ticker': ticker, 'output': output })

def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock %s Has Been Deleted" %item))
	return redirect(delete_stock)

def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request, 'delete_stock.html', {'ticker': ticker})