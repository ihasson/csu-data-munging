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
        'geometry': 'Remedial',
        'int_math_1': 'Other',
        'int_math_2': 'Other',
        'int_math_3': 'Other',
        'inter_alg': 'Remedial',
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
