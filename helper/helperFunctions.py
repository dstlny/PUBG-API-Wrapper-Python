def returnMapName(codename):
    map_dict = {
        "Baltic_Main": "Erangel",
        "Erangel_Main": "Erangel",
        "DihorOtok_Main": "Vikendi",
        "Desert_Main": "Mirimar",
        "Savage_Main": "Sanhok"
    }

    return map_dict.get(codename.strip())

def getSeasonRank(rank):

    rank = int(rank)
    
    if rank <= 0:
        return 'Unranked'
    elif 1 <= rank <= 199:
        return 'Beginner V'
    elif 200 <= rank <= 399:
        return 'Beginner IV'
    elif 400 <= rank <= 599:
        return 'Beginner III'
    elif 600 <= rank <= 799:
        return 'Beginner II'
    elif 800 <= rank <= 999:
        return 'Beginner I'
    elif 1000 <= rank <= 1199:
        return 'Novice V'
    elif 1200 <= rank <= 1399:
        return 'Novice IV'
    elif 1400 <= rank <= 1599:
        return 'Novice III'
    elif 1600 <= rank <= 1799:
        return 'Novice II'
    elif 1800 <= rank <= 1999:
        return 'Novice I'
    elif 2000  <= rank <= 2199:
        return 'Experienced V'
    elif 2200 <= rank <= 2399:
        return 'Experienced IV'
    elif 2400 <= rank <= 2599:
        return 'Experienced III'
    elif 2600 <= rank <= 2799:
        return 'Experienced II'
    elif 2800 <= rank <= 2999:
        return 'Experienced I'
    elif 3000 <= rank <= 3199:
        return 'Skilled V'
    elif 3200 <= rank <= 3399:
        return 'Skilled IV'
    elif 3400 <= rank <= 3599:
        return 'Skilled III'
    elif 3600 <= rank <= 3899:
        return 'Skilled II'
    elif 3800 <= rank <= 3999:
        return 'Skilled I'
    elif 4000 <= rank <= 4199:
        return 'Specialist V'
    elif 4200 <= rank <= 4399:
        return 'Specialist IV'
    elif 4400 <= rank <= 4599:
        return 'Specialist III'
    elif 4600 <= rank <= 4799:
        return 'Specialist II'
    elif 4800 <= rank <= 4999:
        return 'Specialist I'
    elif 5000 <= rank <= 5999:
        return 'Expert'
    else:
        return 'Survivor'

def regionCheck(season):

    _NEEDS_REGION = ['division.bro.official.2017-beta', 'division.bro.official.2017-pre1', 'division.bro.official.2017-pre2', 'division.bro.official.2017-pre3', 'division.bro.official.2017-pre4', 'division.bro.official.2017-pre5', 'division.bro.official.2017-pre6', 'division.bro.official.2017-pre7',
        'division.bro.official.2017-pre8','division.bro.official.2017-pre9','division.bro.official.2018-01','division.bro.official.2018-02','division.bro.official.2018-03','division.bro.official.2018-04','division.bro.official.2018-05','division.bro.official.2018-06','division.bro.official.2018-07',
        'division.bro.official.2018-08','division.bro.official-2018-09','division.bro.official.2018-05','division.bro.official.2018-06','division.bro.official.2018-07', 'division.bro.official.2018-08','division.bro.official.2018-09']

    if season in _NEEDS_REGION:
        print('this season will need a region, which you will be asked to enter shortly')
