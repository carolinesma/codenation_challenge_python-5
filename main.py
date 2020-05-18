from datetime import datetime, timedelta

# constantes
FLATE_RATE = 0.36
DAY_RATE = 0.09
NIGHT_RATE = 0.0

records = [

    {'source': '48-996355555', 'destination': '48-666666666',
        'end': 1564610974, 'start': 1564610674},

    {'source': '41-885633788', 'destination': '41-886383097',
        'end': 1564506121, 'start': 1564504821},

    {'source': '48-996383697', 'destination': '41-886383097',
        'end': 1564630198, 'start': 1564629838},

    {'source': '48-999999999', 'destination': '41-885633788',
        'end': 1564697158, 'start': 1564696258},

    {'source': '41-833333333', 'destination': '41-885633788',
        'end': 1564707276, 'start': 1564704317},

    {'source': '41-886383097', 'destination': '48-996384099',
        'end': 1564505621, 'start': 1564504821},

    {'source': '48-999999999', 'destination': '48-996383697',
        'end': 1564505721, 'start': 1564504821},

    {'source': '41-885633788', 'destination': '48-996384099',
        'end': 1564505721, 'start': 1564504821},

    {'source': '48-996355555', 'destination': '48-996383697',
        'end': 1564505821, 'start': 1564504821},

    {'source': '48-999999999', 'destination': '41-886383097',
        'end': 1564610750, 'start': 1564610150},

    {'source': '48-996383697', 'destination': '41-885633788',
        'end': 1564505021, 'start': 1564504821},

    {'source': '48-996383697', 'destination': '41-885633788',
        'end': 1564627800, 'start': 1564626000}
]


def classify_by_phone_number(records):
    rate_list = []
    for x in records:
        rate = calc_rate(x)

        if not (rate_list):
            rate_list.append({'source': x['source'], 'total': round(
                rate, 2)})
        else:
            count = 0
            equal = False
            while count < len(rate_list) and not equal:
                equal = x['source'] in rate_list[count]['source']
                count += 1
            count -= 1

            if equal:
                rate_list[count]['total'] = round(
                    (rate_list[count]['total'] + rate), 2)
            else:
                rate_list.append(
                    {'source': x['source'], 'total': round(rate, 2)})

    sorted = sorted_rate_list(rate_list)
    return sorted


def calc_rate(record):
    time_start = datetime.fromtimestamp(record['start'])
    time_end = datetime.fromtimestamp(record['end'])

    # calculo de duração da ligação em minutos inteiros
    time_elapsed = int((time_end - time_start).seconds//60)

    # calcula a taxa das ligações que começam e terminam no período diurno
    if time_elapsed and (time_start.hour < 22) and (time_start.hour >= 6):
        if (time_end.hour < 22) and (time_end.hour >= 6):
            rate = FLATE_RATE + DAY_RATE * time_elapsed

    # calcula a taxa das ligações que começcam e terminam no período noturno
    elif time_elapsed and (time_start.hour >= 22) or (time_start.hour < 6):
        if (time_end.hour >= 22) or (time_end.hour < 6):
            rate = FLATE_RATE + NIGHT_RATE * time_elapsed

    # calcula a taxa das ligações minuto a minuto
    # para a ligações que tiveram início ou fim em períodos diferentes
    else:
        i = 0
        while i <= time_elapsed:
            rate = FLATE_RATE
            if (time_start.hour < 22) and (time_start.hour >= 6):
                rate += DAY_RATE
                time_start += timedelta(minutes=1)
            else:
                rate += NIGHT_RATE
                time_start += timedelta(minutes=1)
        i += 1
    return rate


def sorted_rate_list(rate_list):
    for i in range(1, len(rate_list)):
        dict = rate_list[i]
        j = i-1
        while j >= 0 and dict['total'] > rate_list[j]['total']:
            rate_list[j+1] = rate_list[j]
            j -= 1
        rate_list[j+1] = dict
    return rate_list
