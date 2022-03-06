from django.shortcuts import render
from django.db import connection
from datetime import timedelta, datetime
from django.http import HttpResponse, JsonResponse
from .forms import SpendingTrsForm
from .models import SpendingTrs


# Create your views here.
def add_record(request):
    if request.method == "POST":
        form = SpendingTrsForm(request.POST)
        print(type(form.data['date']))

        # print(user)
        if form.is_valid():
            # form.cleaned_data['user'] = request.user
            form.save()
            print(connection.queries)
        else:
            print(form.errors)
        return render(request, 'Record/add_transaction.html', {"form": SpendingTrsForm(initial={'user': request.user})})
    else:
        form = SpendingTrsForm(initial={'user': request.user})
        # form.data['user'] = request.user
        return render(request, 'Record/add_transaction.html', {"form": form})


def show_record(request):
    record = SpendingTrs.objects.all().filter(user=request.user).order_by('-date')

    print(SpendingTrs.objects.all().filter(user=request.user).order_by('-date').query)

    return render(request, 'Record/show.html', {'records': record})


def edit_record(request, id):
    record = SpendingTrs.objects.get(id=id)
    print(connection.queries)

    return render(request, 'Record/edit_transaction.html', {'record': record})


def update_record(request, id):
    record = SpendingTrs.objects.get(id=id)
    form = SpendingTrsForm(request.POST, instance=record)

    if form.is_valid():
        form.save()
        print(connection.queries)
    else:
        print(form.errors)

    return render(request, 'Record/show.html', {'records': SpendingTrs.objects.all().filter(user=request.user).order_by('-date')})


def delete_record(request, id):
    record = SpendingTrs.objects.get(id=id)
    record.delete()
    print(connection.queries)

    return render(request, 'Record/show.html', {'records': SpendingTrs.objects.all().filter(user=request.user).order_by('-date')})


def record_chart(request):
    labels = ['Food', 'Travel', 'Healthcare', 'Entertainment', 'Bills', 'Other']
    data = [0, 0, 0, 0, 0, 0]

    records = SpendingTrs.objects.all().filter(user=request.user)
    print(records.query)
    for record in records:
        # print(record.category)
        if record.category == 'Food':
            data[0] += record.amount
        if record.category == 'Travel':
            data[1] += record.amount
        if record.category == 'Healthcare':
            data[2] += record.amount
        if record.category == 'Entertainment':
            data[3] += record.amount
        if record.category == 'Bills':
            data[4] += record.amount
        if record.category == 'Other':
            data[5] += record.amount

    return JsonResponse(data={
        'labels': labels,
        'data': data
    })


def group_record(request):
    if request.method == 'GET':
        category = request.GET.get('category[]', None)
        order_by = request.GET.get('orderby[]', None)

        records = SpendingTrs.objects.all().filter(category=category, user=request.user)
        print(records.query)
        begin = getattr(records.first(), 'date')

        # Daily
        daily_label = ['', '', '', '', '', '', '']
        daily_data = [0, 0, 0, 0, 0, 0, 0]
        # daily_records = records.order_by('-date')[:7]
        for i in range(7):
            subrecords = records.filter(date=begin-timedelta(days=i))

            for record in subrecords:
                daily_data[6-i] += record.amount

            daily_label[6-i] = (begin-timedelta(days=i)).strftime('%Y/%m/%d')

        print(subrecords.query)
        if order_by == 'By Amount':
            daily_label = [x for _, x in sorted(zip(daily_data, daily_label))]
            daily_data = sorted(daily_data)
        # print(daily_label, daily_data)

        # Weekly
        weekly_label = ['', '', '', '', '']
        weekly_data = [0, 0, 0, 0, 0]
        for i in range(5):
            subrecords = records.filter(date__range=[begin - timedelta(weeks=i+1) + timedelta(days=1),
                                              begin - timedelta(weeks=i)])
            for record in subrecords:
                weekly_data[4-i] += record.amount

            temp_start = (begin - timedelta(weeks=i+1) + timedelta(days=1)).strftime('%Y/%m/%d')
            temp_end = (begin - timedelta(weeks=i)).strftime('%Y/%m/%d')
            label = temp_start + ' - ' + temp_end
            weekly_label[4-i] = label

        print(subrecords.query)
        if order_by == 'By Amount':
            weekly_label = [x for _, x in sorted(zip(weekly_data, weekly_label))]
            weekly_data = sorted(weekly_data)

        # Monthly
        monthly_label = ['', '', '', '', '']
        monthly_data = [0, 0, 0, 0, 0]
        begin_month = begin.month
        begin_year = begin.year
        month_selector = begin_month
        year_selector = begin_year
        for i in range(5):
            if month_selector < 1:
                month_selector = 12
                year_selector -= 1
                # print(month_selector, year_selector)
                subrecords = records.filter(date__month=month_selector,
                                     date__year=year_selector)
                for record in subrecords:
                    monthly_data[4 - i] += record.amount
                monthly_label[4 - i] = str(year_selector) + "/" + str(month_selector)
                month_selector -= 1
                print(subrecords.query)
            else:
                # print(month_selector, year_selector)
                subrecords = records.filter(date__month=month_selector,
                                     date__year=year_selector)
                for record in subrecords:
                    monthly_data[4 - i] += record.amount
                monthly_label[4 - i] = str(year_selector) + "/" + str(month_selector)
                month_selector -= 1

                print(subrecords.query)
        if order_by == 'By Amount':
            monthly_label = [x for _, x in sorted(zip(monthly_data, monthly_label))]
            monthly_data = sorted(monthly_data)

        return JsonResponse(data={
            'dailydata': daily_data,
            'dailylabel': daily_label,
            'weeklydata': weekly_data,
            'weeklylabel': weekly_label,
            'monthlydata': monthly_data,
            'monthlylabel': monthly_label,
        })

    return HttpResponse('OK')


def dummy(request):

    return HttpResponse('got')