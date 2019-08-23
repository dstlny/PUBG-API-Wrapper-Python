from config import user_settings


def returnMapName(codename):
    mapDict = {
        "Baltic_Main": "Erangel",
        "Erangel_Main": "Erangel",
        "DihorOtok_Main": "Vikendi",
        "Desert_Main": "Mirimar",
        "Savage_Main": "Sanhok"
    }

    return mapDict.get(codename.strip())

class RangeDict(dict):
    ''' 
      An implementation of dict which allows you to use range as a key  
    '''

    def __getitem__(self, item):
        if type(item) != range:
            return ''.join([self[key] for key in self if item in key])
        else:
            return super().__getitem__(item)

def getSeasonRank(rank):

    check = RangeDict({
        range(-20, 1): 'Unranked',

        range(1, 200): 'Beginner V', 
        range(200, 400): 'Beginner IV', 
        range(400, 600): 'Beginner III',
        range(600, 800): 'Beginner II', 
        range(800, 1000): 'Beginner I',

        range(1000, 1200): 'Novice V',
        range(1200, 1400): 'Novice IV',
        range(1400, 1600): 'Novice III',
        range(1600, 1800): 'Novice II', 
        range(1800, 2000): 'Novice I', 

        range(2000, 2200): 'Experienced V', 
        range(2200, 2400): 'Experienced IV', 
        range(2400, 2600): 'Experienced III', 
        range(2600, 2800): 'Experienced II', 
        range(2800, 3000): 'Experienced I', 

        range(3000, 3200): 'Skilled V', 
        range(3200, 3400): 'Skilled IV', 
        range(3400, 3600): 'Skilled III', 
        range(3600, 3800): 'Skilled II', 
        range(3800, 4000): 'Skilled I', 

        range(4000, 4200): 'Specialist V', 
        range(4200, 4400): 'Specialist IV', 
        range(4400, 4600): 'Specialist III', 
        range(4600, 4800): 'Specialist II', 
        range(4800, 5000): 'Specialist I', 

        range(5000, 6000): 'Expert',

        range(6000, 9999): 'Survivor'
    })
    return check[int(rank)]

if not user_settings.GUI:

    def regionCheck(season):

        seasonsThatNeedRegion = ['division.bro.official.2017-beta', 'division.bro.official.2017-pre1', 'division.bro.official.2017-pre2', 'division.bro.official.2017-pre3', 'division.bro.official.2017-pre4', 'division.bro.official.2017-pre5', 'division.bro.official.2017-pre6', 'division.bro.official.2017-pre7',
            'division.bro.official.2017-pre8','division.bro.official.2017-pre9','division.bro.official.2018-01','division.bro.official.2018-02','division.bro.official.2018-03','division.bro.official.2018-04','division.bro.official.2018-05','division.bro.official.2018-06','division.bro.official.2018-07',
            'division.bro.official.2018-08','division.bro.official-2018-09','division.bro.official.2018-05','division.bro.official.2018-06','division.bro.official.2018-07', 'division.bro.official.2018-08','division.bro.official.2018-09']

        if season in seasonsThatNeedRegion:
            print('this season will need a region, which you will be asked to enter shortly')
