class Label_Maps:

#        {'calculus':'Calculus',
#        'trigonometry' 'precalc' 'trig_and_precalc': 'Calculus Prep',
#        'algebra2': 'Algebra 2',
#        'none': 'None',
#        'stats': 'Statistics',
#        'adv_app_math' 'adv_math' 'geometry' 'adv_alg': 'Remedial',
#        'bad''pre_alg''accounting' 'col_alg' : 'Other'}
    hs_label_categ = {'accounting':'Other',
        'adv_alg': 'Remedial',
        'adv_app_math': 'Remedial',
        'adv_math': 'Remedial',
        'alg_trig': 'Remedial',
        'algebra1': 'Other',
        'algebra2': 'Algebra 2',
        'bad': 'Other' ,
        'calculus': 'Calculus',
        'col_alg': 'Other',
        'data_science': 'Other',
        'discrete_math': 'Other',
        'finite_math': 'Other',
        'geo_alg_trig': 'Remedial',
        'geo_trig': 'Remedial',
        'geometry': 'Geometry',
        'int_math_1': 'Other',
        'int_math_2': 'Other',
        'int_math_3': 'Other',
        'inter_alg': 'Algebra 2',
        'intr_prob_stat': 'Other',
        'math_anal': 'Calculus Prep',
        'no_math': 'NoMath',
        'not_sure': 'Other',
        'pre_alg': 'Other',
        'precalc': 'Calculus Prep',
        'prob': 'Other',# not sure if remedial stats or other
        'stats': 'Statistics',
        'trig_and_precalc': 'Calculus Prep',
        'trigonometry': 'Calculus Prep',
        'unknown': 'Other'}
   
    hs_label_categ_lst = ['Calculus Prep','Remedial','Other','Algebra 2',
            'NoMath', 'Geometry', 'Calculus', 'Statistics']

# Provides numeric values for grade strings.
# Need to change scores for non-letter 
    gradesMap = {'A+':4.0, 'A':4.0,'A-':3.7, #need to update the grade values
                'B+':3.3,'B':3.0,'B-':2.7,
                'C+':2.3,'C':2.0,'C-':1.7, 
                'D+':1.3,'D':1.0,'D-':0.7,
                'F':0.0, 'W':0.0,'WU':0.0,   
                'CR':2.0, 'NC':0.0, 'RP':1.0 # RP stands for repeat
                #,'X1':?, 'X2':? # the grade not enterred symbols on app-dat
                }

    yrmap={ '204':'2004','205':'2005','206':'2006','207':'2007','208':'2008',
            '209':'2009','210':'2010','211':'2011','212':'2012','213':'2013',
            '214':'2014','215':'2015','216':'2016','217':'2017','203':'2003'}

    #SAT CR+M -> ACT Composite
    #on second though this is a shitty map.
    satTOact={ '1600':'36',
        '1560':'35',
        '1510':'34',
        '1460':'33',
        '1420':'32',
        '1380':'31',
        '1340':'30',
        '1300':'29',
        '1260':'28',
        '1220':'27',
        '1190':'26',
        '1150':'25',
        '1110':'24',
        '1070':'23',
        '1030':'22',
        '990':'21',
        '950':'20',
        '910':'19',
        '870':'18',
        '830':'17',
        '790':'16',
        '740':'15',
        '690':'14',
        '640':'13',
        '590':'12',
        '530':'11'}
# use this map only.
    actTOsat={
        '36': '1600',
        '35': '1560',
        '34': '1510',
        '33': '1460',
        '32': '1420',
        '31': '1380',
        '30': '1340',
        '29': '1300',
        '28': '1260',
        '27': '1220',
        '26': '1190',
        '25': '1150',
        '24': '1110',
        '23': '1070',
        '22': '1030',
        '21': '990',
        '20': '950',
        '19': '910',
        '18': '870',
        '17': '830',
        '16': '790',
        '15': '740',
        '14': '690',
        '13': '640',
        '12': '590',
        '11': '530',
        }; actTOsat.update({str(x) : '400' for x in range(0,11)})
