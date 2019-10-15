from __future__ import print_function
import numpy as np
from scipy.stats import norm


# =====================================#
# Overview of Fragility Curves Available #
# =====================================#
# Infinitely Stiff - unaffected by wind
# inf_stiff
#
# Transmission
# trans
#
# Substation
# sub
#
# Distribution
# dist_20yr
# dist_40yr
# dist_60yr
#
# Solar Power
# solar_res
# solar_utility #used in Watson dissertation
#
# Wind Power
# wind_yaw
# wind_nonyaw # used in Watson dissertation
#
# ---------------
# HAZUS Curves
# ---------------
#
# CECBL (Concrete Engineered Commercial Building 1 to 2 stories, HAZUS)
# cecbl_moderate
# cecbl_severe
# cecbl_destr
#
# CECBM (Concrete Engineered Commercial Building 3 to 5 stories, HAZUS)
# cecbm_moderate
# cecbm_severe
# cecbm_destr
#
# CECBH (Concrete Engineered Commercial Building 6+ stories, HAZUS)
# cecbh_moderate
# cecbh_severe
# cecbh_destr
#
# SECBL (Steel Engineered Commercial Building 1 to 2 stories, HAZUS)
# secbl_moderate
# secbl_severe
# secbl_destr
#
# SECBM (Steel Engineered Commercial Building 3 to 5 stories, HAZUS)
# secbm_moderate # Used in Watson dissertation to represent Natural Gas Power Plants
# secbm_severe
# secbm_destr
#
# SECBH (Steel Engineered Commercial Building 6+ stories, HAZUS)
# secbh_moderate # Used in Watson dissertation to represent Coal Power Plants
# secbh_severe
# secbh_destr


def fragility(wind_mph, curve="inf_stiff"):
    # print(wind_mph)
    # print(type(wind_mph))
    # if type(wind_mph) is not np.ndarray:
    # wind_mph = np.array(wind_mph)

    # =====================================#
    # General Fragility Curves             #
    # =====================================#

    if curve == "inf_stiff" or curve == "cecbl_destr" or curve == "cecbm_destr" or curve == "cecbh_destr" or curve == "secbh_destr":
        if type(wind_mph) is np.ndarray:

            p_failure = np.zeros(len(wind_mph))
        else:
            p_failure = 0.0

    # =====================================#
    # Fragility Curves based on literature #
    # =====================================#

    # Transmission Towers (per 0.23 km)
    # Transmission line fragility curves were based on a computational analysis of UK transmission towers [64]
    # Panteli M, Pickering C, Wilkinson S, Dawson R, Mancarella P. Power System Resilience to Extreme Weather: Fragility Modelling, Probabilistic
    # Impact Assessment, and Adaptation Measures. IEEE Trans Power Syst 2017 32:1-1. doi:10.1109/TPWRS.2016.2641463.

    elif curve == "trans_UK_base":
        wind_ms = wind_mph * 0.44704
        x = [41.16350883, 45.27810213, 50.51352572, 55.18578793, 59.48053428, 62.46734014, 66.01144875, 68.9942268,
             73.09673666, 76.82465998, 81.48447258, 86.51887172, 91.3679915, 96.21967444, 101.8216289, 107.6117921,
             114.3393371, 121.4440317, 127.8021164, 136.0327677, 142.0180967, 149.688882, 157.1725572]
        y = [0.003913894, 0.01369863, 0.033268102, 0.062622309, 0.109589041, 0.146771037, 0.205479452, 0.264187867,
             0.338551859, 0.414872798, 0.510763209, 0.604696673, 0.688845401, 0.759295499, 0.819960861, 0.874755382,
             0.919765166, 0.949119374, 0.968688845, 0.980430528, 0.992172211, 0.996086106, 1.0]
        p_failure = np.interp(wind_ms, x, y, left=0.0, right=1.0)

    elif curve == "trans_UK_robust":
        wind_ms = wind_mph * 0.44704
        x = [46.40296024, 51.82805717, 58.55999609, 62.29817202, 66.59584769, 70.3310943, 73.50427802, 76.11649735,
             79.10257088, 81.52658153, 84.51155657, 86.56281149, 88.9871883, 91.78505315, 94.21016229, 96.6345391,
             99.24565993, 102.2317335, 105.4041849, 108.3902584, 111.1899541, 114.7380905, 118.2869592, 122.2107807,
             125.9471258, 130.4330102, 135.2945795, 139.407342, 144.0828997, 149.5068981, 154.3702983, 158.6720018,
             162.9755361, 167.6507277]
        y = [0.001956947, 0.007827789, 0.029354207, 0.050880626, 0.082191781, 0.119373777, 0.160469667, 0.199608611,
             0.240704501, 0.285714286, 0.332681018, 0.369863014, 0.412915851, 0.459882583, 0.499021526, 0.542074364,
             0.587084149, 0.628180039, 0.673189824, 0.714285714, 0.75146771, 0.788649706, 0.821917808, 0.851272016,
             0.88258317, 0.908023483, 0.925636008, 0.945205479, 0.956947162, 0.968688845, 0.976516634, 0.98630137,
             0.98630137, 1.0]
        p_failure = np.interp(wind_ms, x, y, left=0.0, right=1.0)

    # Used in Watson Dissertation and Ouyang et al 2014, based on Quanta 2009 study
    # Quanta Technology, 2009, "Cost benefit analysis of the deployment of utility infrastructure upgrades and
    # storm hardening programs", Final report, prepared for the Public Utility Commission of Texas, Project No.36375, Raleigh, NC.
    elif curve == "trans_TX":
        p_failure = 2.0 * 10 ** (-7.0) * np.exp(0.0834 * wind_mph)
        p_failure = np.clip(p_failure, 0.0, 1.0)

    # Substation:
    # Substation fragility curves were based on data published for the grid in Mexico [66]

    # Lopez, Lopez A, E. PRL, Esobedo D de L, Sesma JS. Reliability and Vulnerability Analysis of Electrical Substations and Transmission Towers for Definition of Wind and Seismic Damage Maps for Mexico. 11er Am Conf Wind Eng 2009, 4:22-6
    elif curve == "sub_MX":
        wind_kmph = wind_mph * 1.60934
        x = [40.1487, 60.223, 80.2974, 100.372, 119.703, 139.777, 159.851, 179.926, 200.0, 220.074, 240.149, 260.223,
             281.041, 301.115]
        y = [0.0, 0.0136986, 0.0228311, 0.0273973, 0.0456621, 0.0639269, 0.0913242, 0.13242, 0.214612, 0.424658,
             0.648402, 0.803653, 0.890411, 0.931507]
        p_failure = np.interp(wind_kmph, x, y, left=0.0, right=1.0)


    # HAZUS functions, documented in Watson Dissertation (all are severe curves, for different terrains (k 1-5))
    elif curve == "sub_HAZUS_severe_k1":
        mu = 5.060
        sigma = 0.15
        p_failure = norm.cdf((np.log(wind_mph) - mu) / sigma)

    elif curve == "sub_HAZUS_severe_k2":
        mu = 5.094
        sigma = 0.124
        p_failure = norm.cdf((np.log(wind_mph) - mu) / sigma)

    elif curve == "sub_HAZUS_severe_k3":
        mu = 5.141
        sigma = 0.132
        p_failure = norm.cdf((np.log(wind_mph) - mu) / sigma)

    elif curve == "sub_HAZUS_severe_k4":
        mu = 5.185
        sigma = 0.139
        p_failure = norm.cdf((np.log(wind_mph) - mu) / sigma)

    elif curve == "sub_HAZUS_severe_k5":
        mu = 5.204
        sigma = 0.147
        p_failure = norm.cdf((np.log(wind_mph) - mu) / sigma)


    # Distribution Conductors:
    # Quanta Technology, 2009, "Cost benefit analysis of the deployment of utility infrastructure upgrades and
    # storm hardening programs", Final report, prepared for the Public Utility Commission of Texas, Project No.36375, Raleigh, NC.
    elif curve == "dist_cond_TX":
        p_failure = 8.0 * 10 ** -12.0 * wind_mph ** 5.1731
        p_failure = np.clip(p_failure, 0.0, 1.0)

    # Distribution Towers:
    # Quanta Technology, 2009, "Cost benefit analysis of the deployment of utility infrastructure upgrades and
    # storm hardening programs", Final report, prepared for the Public Utility Commission of Texas, Project No.36375, Raleigh, NC.
    elif curve == "dist_TX":
        p_failure = 0.0001 * np.exp(0.0421 * wind_mph)
        p_failure = np.clip(p_failure, 0.0, 1.0)

    # Salman AM, Li Y, Stewart MG. Evaluating system reliability and targeted
    # hardening strategies of power distribution systems subjected to hurricanes. Reliab Eng Syst Saf 2015;144: 319-33 doi:10.1016/j.ress.2015.07.028.
    elif curve == "dist_20yr":
        wind_ms = wind_mph * 0.44704
        x = [29.99952442, 49.69039806, 51.54896086, 53.17567889, 55.11128549, 56.6590574, 57.89603843, 59.13254387,
             60.36881153, 61.37252104, 62.9940077, 64.07476102, 65.38617016, 66.46716127, 67.47134636, 68.86170162,
             69.86612451, 70.79350359, 71.87544586, 72.8808199, 74.04147049, 75.04732011, 76.36324725, 77.83397537,
             79.53845056, 81.70732867, 83.79987635, 85.96970562, 87.59761259, 100.0777572]
        y = [0.0, 0.0, 0.018404908, 0.033742331, 0.064417178, 0.098159509, 0.141104294, 0.190184049, 0.242331288,
             0.294478528, 0.377300613, 0.435582822, 0.518404908, 0.573619632, 0.619631902, 0.68404908, 0.726993865,
             0.763803681, 0.806748466, 0.837423313, 0.865030675, 0.889570552, 0.914110429, 0.941717791, 0.95398773,
             0.975460123, 0.981595092, 0.990797546, 0.990797546, 0.996932515]
        p_failure = np.interp(wind_ms, x, y, left=0.0, right=1.0)

    elif curve == "dist_40yr":
        wind_ms = wind_mph * 0.44704
        x = [29.99976221, 43.64293527, 46.35587578, 48.13763257, 49.76387502, 52.00884577, 54.25262757, 56.10786132,
             58.34950302, 60.12626623, 61.82574785, 63.60227327, 65.45655586, 67.466115, 69.55390688, 71.87378133,
             73.18947068, 74.89156798, 76.59461645, 78.6854996, 80.7002901, 83.41227945, 86.12521996, 100.0777572]
        y = [0.003067485, 0.006134969, 0.009202454, 0.024539877, 0.04601227, 0.085889571, 0.141104294, 0.208588957,
             0.291411043, 0.371165644, 0.447852761, 0.530674847, 0.610429448, 0.687116564, 0.754601227, 0.828220859,
             0.855828221, 0.898773006, 0.929447853, 0.957055215, 0.966257669, 0.981595092, 0.984662577, 0.996932515]
        p_failure = np.interp(wind_ms, x, y, left=0.0, right=1.0)

    elif curve == "dist_60yr":
        wind_ms = wind_mph * 0.44704
        x = [30.0, 32.86821705, 35.65843915, 37.67322966, 40.92690351, 43.40490798, 45.49483997, 47.27398107,
             49.20792315, 51.06363247, 52.76358967, 54.619299, 56.24245018, 58.02087792, 59.87634946, 61.88685975,
             63.66647644, 65.59994293, 67.84467589, 69.93460789, 72.02501546, 74.27093737, 76.36205831, 78.22109669,
             80.46749417, 82.63708565, 84.80715271, 86.7451372, 89.53583488, 100.0777572]
        y = [0.0, 0.0, 0.006134969, 0.015337423, 0.042944785, 0.076687117, 0.116564417, 0.165644172, 0.217791411,
             0.279141104, 0.349693252, 0.411042945, 0.472392638, 0.530674847, 0.595092025, 0.659509202, 0.702453988,
             0.760736196, 0.803680982, 0.843558282, 0.877300613, 0.904907975, 0.929447853, 0.947852761, 0.969325153,
             0.981595092, 0.987730061, 0.987730061, 0.987730061, 0.996932515]
        p_failure = np.interp(wind_ms, x, y, left=0.0, right=1.0)

    # -----------------------------------------------------
    # Solar PV:
    # -----------------------------------------------------
    # Goodman JN. Performance Measures for Residential PV Structural Response to Wind Effects 2015.
    # 90_101_U_30 curve
    elif curve == "solar_res":
        solar_x = np.array([90.0, 110.2020202, 130.0, 150.0, 170])
        solar_y = [0.0, 0.106145251, 0.525139665, 0.865921788, 1.0]
        p_failure = np.interp(wind_mph, solar_x, solar_y, left=0.0, right=1.0)

    # Solar panel utility fragility cures are based on a performance based approach by Goodman of a residential system with a modification proposed by Watson [68] to better represent utility scale solar installations.
    # Goodman JN. Performance Measures for Residential PV Structural Response to Wind Effects 2015.
    # Watson E. Modeling Electrical Grid Resilience under Hurricane Wind Conditions with Increased Solar Photovoltaic and Wind Turbine Power Generation. George Washington University, 2018.

    elif curve == "solar_utility":
        x = np.array([90.0, 110.2020202, 130.0, 150.0, 170]) + 30.0
        y = [0.0, 0.106145251, 0.525139665, 0.865921788, 1.0]
        p_failure = np.interp(wind_mph, x, y, left=0.0, right=1.0)

    # -----------------------------------------------------
    # Wind Turbines:
    # -----------------------------------------------------
    # Rose S, Jaramillo P, Small MJ, Grossmann I, Apt J. Quantifying the hurricane risk to offshore wind turbines. Proc Natl Acad Sci 2012: 109:3247-52 doi:10.1073/pnas.1111769109.
    # Curves are for windspeed at a hub height of 90m
    # https://www.pnas.org/content/pnas/suppl/2012/02/07/1111769109.DCSupplemental/pnas.1111769109_SI.pdf?targetid=STXT

    # Yawing Offshore Wind Turbine
    elif curve == "wind_yaw":
        wind_knots = wind_mph * 0.868976  # ground wind speed
        wind_knots_HH = wind_knots * 0.9 / 0.8  # hub height windspeed, based on Figure 1 of https://www.nhc.noaa.gov/aboutwindprofile.shtml
        x = [120.0657132, 124.3653638, 128.6646451, 132.3713997, 136.0777849, 139.7836162, 143.9335195, 147.3418872,
             150.0079808, 152.6744437, 154.8949881, 156.671276, 160.5181763, 163.1789151, 165.5436676, 168.3517534,
             171.4532406, 173.2241738, 176.4737465, 179.2785087, 182.9732613, 184.7471488, 187.5563425, 191.404166,
             193.6245258, 196.1416106, 199.1036906, 202.2151487, 205.1788905, 209.180339, 212.7375308, 216.2950919,
             219.7045675]
        y = [0.0, 0.00124533, 0.00498132, 0.00498132, 0.00747198, 0.01369863, 0.0249066, 0.0373599, 0.056039851,
             0.072229141, 0.095890411, 0.115815691, 0.170610212, 0.225404732, 0.276463263, 0.337484433, 0.419676214,
             0.475716065, 0.559153176, 0.642590286, 0.723536737, 0.759651308, 0.813200498, 0.861768369, 0.886674969,
             0.910336239, 0.932752179, 0.947696139, 0.95890411, 0.97135741, 0.98007472, 0.98630137, 1]
        p_failure = np.interp(wind_knots, x, y, left=0.0, right=1.0)


    # Non-Yawing Offshore Wind Turbine
    elif curve == "wind_nonyaw":
        wind_knots = wind_mph * 0.868976  # ground wind speed
        wind_knots_HH = wind_knots * 0.9 / 0.8  # hub height windspeed, based on Figure 1 of https://www.nhc.noaa.gov/aboutwindprofile.shtml
        x = [97.38019084, 101.0869454, 108.7957023, 116.0578022, 120.2056744, 123.7586193, 128.1954614, 131.2997183,
             133.5139848, 135.5818276, 137.2039366, 139.5655501, 141.0403122, 142.6635291, 144.1390297, 145.9107014,
             147.9785442, 149.8997786, 151.9694679, 154.3364361, 157.1482148, 160.4059119, 164.7018696, 169.4437458,
             175.0759815, 180.8574107, 188.5670909, 194.7940692]
        y = [0, 0.00124533, 0.00996264, 0.03113325, 0.056039851, 0.093399751, 0.169364882, 0.232876712, 0.298879203,
             0.352428394, 0.412204234, 0.484433375, 0.537982565, 0.590286426, 0.638854296, 0.689912827, 0.743462017,
             0.785803238, 0.826899128, 0.863013699, 0.899128269, 0.927770859, 0.95392279, 0.97260274, 0.98630137,
             0.99377335, 0.99626401, 1]
        p_failure = np.interp(wind_knots_HH, x, y, left=0.0, right=1.0)
        return p_failure


    # =====================================#
    # Fragility Curves based on HAZUS      #
    # =====================================#
    # Source: FEMA. HAZUS Hurricane Model User Guidance 2018:201.

    # HAZUS Functions - Moderate
    # --------------------------

    # CECBL (Concrete Engineered Commercial Building 1 to 2 stories, HAZUS)
    elif curve == "cecbl_moderate":
        x = [0.0, 62.61246774615756, 67.68295875247745, 72.55843087393887, 77.4339029954003, 82.50439400172019,
             88.0624322201862, 92.4503571295015, 96.74077259638753, 101.03118806327359, 105.32160353015965,
             109.61201899704571, 112.92734003963949, 115.85262331251633, 119.4063007699371, 121.50817097341158,
             123.26334093713771, 125.35979394936612, 127.35873751916529, 128.91888859803296, 130.5626191989828,
             132.42922852548517, 134.37941737406976, 135.2987921169739, 137.6947384166635, 140.034965034965,
             142.37519165326648, 144.43681986462735, 146.4705882352941, 148.03073931416174, 150.5659848173217,
             153.10123032048162, 155.83149470850003, 159.53685352081072, 163.43723121797984, 167.14259003029053,
             170.84794884260123, 175.13836430948726, 179.42877977637335, 183.71919524325938, 188.00961071014547,
             192.3000261770315, 196.59044164391753, 199.32070603193597]
        y = [0.0, 0.008095898591766515, 0.008095898591766515, 0.008095898591766515, 0.008095898591766515,
             0.008095898591766515, 0.007198896145177214, 0.0076392428007756585, 0.011814381461263679,
             0.02146938961364242, 0.03973562125327734, 0.06165509922083956, 0.09325133085463677, 0.12042718275500675,
             0.163190943838327, 0.192340201121193, 0.23069602573734826, 0.2672399054113932, 0.3087711186884743,
             0.3396280028511436, 0.36752123974674167, 0.4121058005355528, 0.44827293918203026, 0.4737853973391166,
             0.5177368086458998, 0.5568620620273514, 0.6027008803868309, 0.642814829798301, 0.6680704320167131,
             0.6987877824654686, 0.7367365230083321, 0.7705479781926065, 0.8036134817126553, 0.8428264419999958,
             0.8741109879351805, 0.8993575295228189, 0.9283877905215248, 0.9500463223228063, 0.9698782309601244,
             0.9795332391125029, 0.9872311510177777, 0.992058655093967, 0.9940157513410708, 0.9919281820108268]
        p_failure = np.interp(wind_mph, x, y, left=0.0, right=1.0)

    # CECBM (Concrete Engineered Commercial Building 3 to 5 stories, HAZUS)
    elif curve == "cecbm_moderate":
        x = [0.0, 62.605961807172775, 67.66790870982766, 72.5351653469958, 77.40242198416394, 82.65905915230553,
             86.9422449930135, 91.22543083372145, 95.50861667442942, 99.59711224965065, 102.51746623195154,
             104.85374941779224, 107.19003260363297, 109.13693525850022, 110.88914764788075, 112.44666977177457,
             114.43251047973916, 115.21127154168607, 117.11923614345596, 118.48206800186304, 120.18560782487191,
             122.18118304611085, 123.54401490451792, 125.24755472752676, 127.2431299487657, 128.60596180717278,
             130.46633545515706, 132.88914764788075, 135.03074056823473, 137.56171401956217, 140.48206800186304,
             144.37587331159756, 148.4643688868188, 152.1634839310666, 155.86259897531437, 160.14578481602234,
             164.4289706567303, 168.71215649743826, 172.99534233814623, 176.9864927806241, 180.39357242664178,
             185.06613879832324, 189.73870517000464, 194.80065207265952, 199.0838379133675]
        y = [0.0, 0.007616169714162568, 0.007616169714162568, 0.007616169714162568, 0.007616169714162568,
             0.006249164893671777, 0.011326611369780082, 0.02304379554541436, 0.043874345190986874, 0.0782346261445479,
             0.11573974146821131, 0.14948827263470377, 0.1870583358172393, 0.2244679777883607, 0.2453993737457092,
             0.2847275754679166, 0.3225732124156473, 0.3432418293359988, 0.38497459563723335, 0.41504870168802843,
             0.4503908909415988, 0.49667841811161484, 0.5267525241624099, 0.5620947134159803, 0.6080242155139631,
             0.6355921460605252, 0.6721319197084842, 0.7180811226569916, 0.7552371635354225, 0.7916910774670327,
             0.829625822877136, 0.8675923927380869, 0.9024835633944205, 0.9273825797676436, 0.9540391737672119,
             0.9714847590953788, 0.9773433511831959, 0.9851548073002856, 0.9919247359350966, 0.9927221554137161,
             0.9913258576327864, 0.9915713605393235, 0.9915713605393235, 0.9915713605393235, 0.9917077510429552]
        p_failure = np.interp(wind_mph, x, y, left=0.0, right=1.0)

    # CECBH (Concrete Engineered Commercial Building 6+ stories, HAZUS)
    elif curve == "cecbh_moderate":
        x = [0.0, 62.972056358684256, 67.36198407710035, 71.65435784621829, 75.94673161533626, 79.65378168866539,
             82.38529226901318, 85.0680258747119, 87.06788183532367, 88.43363712549757, 90.21128686826358,
             92.14068719882673, 93.70155038759688, 95.28409223176664, 97.21349256232975, 98.77435575109993,
             100.35689759526966, 102.09119002723654, 103.45694531741043, 104.96903153153153, 106.9688874921433,
             108.33464278231719, 110.19900714668157, 112.62701655143513, 115.20244081290593, 118.09003771213074,
             121.01665619107479, 124.9188141630002, 129.0160800335219, 133.30845380263983, 137.6008275717578,
             141.89320134087575, 146.1855751099937, 150.47794887911166, 155.16053844542216, 159.84312801173266,
             164.91593337523568, 169.9887387387387, 175.06154410224175, 180.1343494657448, 185.20715482924786,
             189.88974439555832, 194.96254975906137, 199.25492352817932]
        y = [0.0, 0.006306975753439081, 0.007990942735371265, 0.01613510210288327, 0.03078989661475151,
             0.06210585614453512, 0.09561206763241636, 0.12955015858333674, 0.1712454122519529, 0.1974081942892505,
             0.23011880485906122, 0.2801871076156446, 0.31566332389975793, 0.35162530264745495, 0.4041683701627985,
             0.44250926591042883, 0.4814154985511845, 0.5318466176932747, 0.5689906710073862, 0.6080997902800661,
             0.65463103780691, 0.6847327541065429, 0.7212033640052321, 0.767020026497982, 0.8088312276377522,
             0.8458890394755221, 0.8737248201274365, 0.9116031088535934, 0.9392499051232094, 0.9614570364025307,
             0.9750701292913018, 0.9834747140645881, 0.9908375972147775, 0.993122184952369, 0.9928461742423883,
             0.9929235980116726, 0.9930074737617305, 0.9930913495117883, 0.9931752252618463, 0.9932591010119043,
             0.9933429767619621, 0.9934204005312464, 0.9935042762813043, 0.9937116613776014]
        p_failure = np.interp(wind_mph, x, y, left=0.0, right=1.0)

    # SECBL (Steel Engineered Commercial Building 1 to 2 stories, HAZUS)
    elif curve == "secbl_moderate":
        x = [0.0, 62.64249633, 67.71453079, 72.59148701, 77.46844322, 82.54047769, 88.10020777, 92.48946837,
             96.78118984, 101.0729113, 105.3646328, 109.6563542, 113.7529975, 116.6791712, 119.0851363, 120.7758144,
             122.7265969, 124.8236881, 126.6281619, 128.3838661, 130.4809573, 132.4805093, 134.4312918, 135.3509464,
             137.5525438, 139.649635, 141.4541088, 143.209813, 145.3556737, 147.891691, 150.6227865, 153.1588037,
             155.8898992, 159.5963859, 163.4979509, 167.2044376, 170.9109243, 175.2026458, 179.4943672, 183.7860887,
             188.0778102, 192.3695317, 196.6612531, 199.3923486]
        y = [0.0, 0.008502601, 0.008502601, 0.008502601, 0.008502601, 0.008502601, 0.00760701, 0.008046664, 0.01299684,
             0.023157727, 0.040483342, 0.064843417, 0.101787359, 0.12875858, 0.163234189, 0.185590794, 0.225593859,
             0.264149051, 0.294464807, 0.332778189, 0.371954325, 0.418683278, 0.456584689, 0.482057003, 0.523646543,
             0.562022617, 0.590815867, 0.627105215, 0.665622593, 0.706203812, 0.74711087, 0.779785568, 0.811537254,
             0.850517355, 0.881752674, 0.90588478, 0.932557108, 0.952097276, 0.971637443, 0.981277259, 0.986748505,
             0.990786807, 0.992871091, 0.990786807]
        p_failure = np.interp(wind_mph, x, y, left=0.0, right=1.0)

    # SECBM (Steel Engineered Commercial Building 3 to 5 stories, HAZUS)
    elif curve == "secbm_moderate":
        x = [0.0, 62.24836782800065, 67.31943873738524, 72.19546845794733, 77.55884612809075, 81.94739806944796,
             86.23949123724407, 90.53329073723606, 94.8298352064127, 98.9744967387536, 101.3488217194303,
             102.65514884498509, 104.61344619005362, 106.9647430460422, 109.25088767767818, 110.68714824146355,
             112.25868319671306, 114.2588863530022, 115.04494003870735, 116.96823424564428, 118.34209132255916,
             120.05877146933719, 122.0711319598995, 123.44498903681435, 125.16145787925603, 127.17321360223494,
             128.54693466716316, 130.42039248459903, 132.86066363261375, 135.0167032593118, 137.5626252126912,
             140.49917387502035, 144.41142719207954, 148.51672149744275, 152.2293757815761, 155.94275340218377,
             160.23863017615332, 164.53228129943264, 168.82437446722875, 173.1171724244101, 177.11574399711233,
             180.5285669664449, 185.2096254472062, 189.89061397894588, 194.96168488833044, 199.2526299029927]
        y = [0.0, 0.007367203302945491, 0.007367203302945491, 0.007367203302945491, 0.006470981462495473,
             0.006910944911443728, 0.011082450205174732, 0.021250494358643568, 0.04106514450386545, 0.07546413034442612,
             0.10296419961761205, 0.1242345312976254, 0.15194627963407914, 0.1899096677658012, 0.22738634579327033,
             0.248326260870942, 0.28770539499570513, 0.325600044334839, 0.34629542836558835, 0.3880822411261049,
             0.4181952949652249, 0.4535832544938505, 0.49993072681426476, 0.5300437806533846, 0.5646891563713519,
             0.6089113026129845, 0.6385463714705312, 0.6727435414299833, 0.7187522513785364, 0.7559564115797056,
             0.7924575355371443, 0.8308715952229211, 0.8710382665078001, 0.9041756616848751, 0.928324766549364,
             0.9550158824522204, 0.9724840608697185, 0.9821306668614712, 0.9863021721552021, 0.9929505087170858,
             0.9937489609022139, 0.992350854831112, 0.9925966756787782, 0.9925966756787782, 0.9925966756787782,
             0.9927332428163705]
        p_failure = np.interp(wind_mph, x, y, left=0.0, right=1.0)

    # SECBH (Steel Engineered Commercial Building 6+ stories, HAZUS)
    elif curve == "secbh_moderate":
        x = [0.0, 62.916122584943366, 67.30219853431046, 71.59080612924717, 75.87941372418388, 79.5832111925383,
             82.31232511658894, 84.9927048634244, 86.99080612924718, 88.3553630912725, 90.06105929380413,
             92.05916055962692, 93.42371752165224, 95.19980753571693, 97.12751499000669, 98.68700866089276,
             100.26816196609667, 102.00093271152565, 103.36548967355097, 104.87624916722186, 106.87435043304464,
             108.23890739506996, 110.1016359464061, 112.5275149900067, 115.1006795469687, 117.98574283810794,
             120.90979347101933, 124.80852764823453, 128.9021985343105, 133.1908061292472, 137.4794137241839,
             141.7680213191206, 146.0566289140573, 150.34523650899402, 155.02371752165226, 159.7021985343105,
             164.77055296469024, 169.83890739506998, 174.90726182544975, 179.97561625582946, 185.04397068620924,
             189.72245169886745, 194.79080612924722, 199.07941372418392]
        y = [0.0, 0.007409339719466113, 0.009018132056106687, 0.01811837153609286, 0.03397878891549766,
             0.0628431596153114, 0.09791880488082993, 0.132949761470331, 0.1745449880260006, 0.20064317482038985,
             0.23380600288353448, 0.28215531987683873, 0.31266278937165004, 0.35163925951267727, 0.4040660280533698,
             0.44231953472459795, 0.4811371117953397, 0.5314585471547497, 0.5685203557988368, 0.6075416564846945,
             0.655037632569278, 0.6868559698939446, 0.7232371865536422, 0.7689401300034211, 0.8106416162998441,
             0.8475921997947313, 0.8753349298665755, 0.9130879233664044, 0.9382825863838522, 0.9598631542935341,
             0.9733835100923709, 0.9817037290455012, 0.9889839206294903, 0.9911939787889155, 0.9908411123600998,
             0.9908411123600998, 0.9908411123600998, 0.9908411123600998, 0.9908411123600998, 0.9908411123600998,
             0.9908411123600998, 0.9908411123600998, 0.9908411123600998, 0.9909773064203444]
        p_failure = np.interp(wind_mph, x, y, left=0.0, right=1.0)

    # HAZUS Functions - Severe
    # --------------------------

    # CECBL (Concrete Engineered Commercial Building 1 to 2 stories, HAZUS)
    elif curve == "cecbl_severe":
        x = [0.0, 62.1834262, 65.53775102, 70.21820426, 74.89865749, 79.9691485, 85.0396395, 90.11013051, 95.18062152,
             100.8145004, 105.3216035, 109.612019, 113.9024345, 118.527168, 122.4832654, 126.578662, 130.4790397,
             133.9893796, 136.5246251, 138.474814, 141.0100595, 144.1303616, 146.4705882, 148.0307393, 150.3709659,
             152.9062114, 155.4414569, 157.5866647, 159.7806271, 161.4870424, 162.8521746, 164.8511181, 166.5575334,
             167.9226656, 170.0678733, 173.968251, 177.283572, 180.4038742, 184.4992708, 187.6195729, 190.7398751,
             195.0302906, 198.5406305]
        y = [0.0, 0.004507889, 0.006517174, 0.005738064, 0.005738064, 0.005738064, 0.005738064, 0.005738064,
             0.005738064, 0.005145757, 0.006030075, 0.007856698, 0.012053582, 0.023063025, 0.047694479, 0.072249514,
             0.106622647, 0.147041578, 0.170704502, 0.205723478, 0.229565803, 0.270469114, 0.296057604, 0.330777579,
             0.365838414, 0.403494577, 0.436713568, 0.475254773, 0.513257776, 0.541991755, 0.571054634, 0.607981235,
             0.636715213, 0.663984088, 0.700634943, 0.737831853, 0.766361967, 0.799563017, 0.837839471, 0.865630238,
             0.892029291, 0.924082179, 0.948872065]
        p_failure = np.interp(wind_mph, x, y, left=0.0, right=1.0)

    # CECBM (Concrete Engineered Commercial Building 3 to 5 stories, HAZUS)
    elif curve == "cecbm_severe":
        x = [0.0, 60.0, 149.8947368, 155.0526316, 159.8421053, 165.0, 169.7894737, 174.9473684, 180.1052632,
             185.2631579, 189.6842105, 194.8421053, 199.6315789]
        y = [0.0, 0.0, 0.0, 0.010840108, 0.01897019, 0.035230352, 0.067750678, 0.113821138, 0.165311653, 0.203252033,
             0.281842818, 0.363143631, 0.471544715]
        p_failure = np.interp(wind_mph, x, y, left=0.0, right=1.0)

    # CECBH (Concrete Engineered Commercial Building 6+ stories, HAZUS)
    elif curve == "cecbh_severe":
        x = [0.0, 62.05504924, 65.41090509, 70.09349466, 74.77608422, 79.84888959, 84.92169495, 89.99450031,
             95.06730568, 100.140111, 104.8227006, 109.895506, 114.9683113, 120.0411167, 125.1139221, 130.1867274,
             134.869317, 139.9421224, 145.0149277, 150.0877331, 155.94097, 160.2333438, 164.5257176, 168.9481633,
             173.4449358, 176.6224073, 179.9392416, 183.8413995, 186.5729101, 187.9386654, 190.0848523, 192.0359313,
             193.4016866, 195.4015425, 196.5234129, 197.6940603, 199.0988372, 198.6695998]
        y = [0.0, 0.003606177, 0.005666939, 0.004966807, 0.005044231, 0.005128107, 0.005211982, 0.005295858,
             0.005379734, 0.00546361, 0.005541033, 0.005624909, 0.005708785, 0.005792661, 0.005876536, 0.005960412,
             0.006037836, 0.006121712, 0.006205587, 0.006289463, 0.005418949, 0.008962259, 0.01189791, 0.019828284,
             0.034401665, 0.062794067, 0.098657403, 0.130519864, 0.156836526, 0.19061856, 0.222770286, 0.264650738,
             0.297402283, 0.323277145, 0.365346802, 0.398309972, 0.453936627, 0.424824387]
        p_failure = np.interp(wind_mph, x, y, left=0.0, right=1.0)

    # SECBL (Steel Engineered Commercial Building 1 to 2 stories, HAZUS)
    elif curve == "secbl_severe":
        x = [0.0, 62.19394765, 65.54485344, 70.21940776, 74.8942074, 79.95857369, 85.02293998, 90.08730626, 95.15167255,
             100.7785597, 105.2804971, 109.5663053, 113.8528598, 118.1429066, 122.4345489, 126.5330245, 130.2447046,
             133.1778573, 135.7179296, 138.0672023, 140.6083338, 143.3471635, 145.8313932, 147.8481721, 150.0033994,
             152.3517492, 153.9203349, 155.8744023, 157.6406662, 159.9918299, 162.1475952, 163.6775782, 165.6729071,
             167.6324855, 170.1772567, 174.0845238, 177.4038141, 180.7243301, 185.0205122, 189.3166464, 193.6101511,
             197.3177345, 199.4667157]
        y = [0.0, 0.00521718, 0.007168241, 0.006312703, 0.006235229, 0.006151298, 0.006067368, 0.005983437, 0.005899507,
             0.005214741, 0.006023265, 0.007776414, 0.011896639, 0.027092167, 0.04734759, 0.072733455, 0.106914115,
             0.143029337, 0.168007115, 0.20562255, 0.233959424, 0.27153769, 0.295913505, 0.338039053, 0.377997879,
             0.412686192, 0.445386806, 0.465125753, 0.507004059, 0.550616498, 0.592281319, 0.62610531, 0.653153312,
             0.690370247, 0.73025029, 0.766976489, 0.792210223, 0.821331171, 0.855984489, 0.890485794, 0.916648045,
             0.937836094, 0.95798587]
        p_failure = np.interp(wind_mph, x, y, left=0.0, right=1.0)

    # SECBM (Steel Engineered Commercial Building 3 to 5 stories, HAZUS)
    elif curve == "secbm_severe":
        x = [0.0, 60.36842105, 130.7368421, 135.1578947, 139.9473684, 145.1052632, 150.2631579, 155.4210526,
             160.2105263, 165.0, 170.1578947, 175.3157895, 180.4736842, 185.6315789, 190.0526316, 195.2105263, 200]
        y = [0.0, 0.0, 0.0, 0.005420054, 0.013550136, 0.029810298, 0.059620596, 0.097560976, 0.157181572, 0.230352304,
             0.330623306, 0.447154472, 0.533875339, 0.62601626, 0.704607046, 0.756097561, 0.837398374]
        p_failure = np.interp(wind_mph, x, y, left=0.0, right=1.0)

    # SECBH (Steel Engineered Commercial Building 6+ stories, HAZUS)
    elif curve == "secbh_severe":
        x = [0.0, 60.0, 114.8947368, 119.6842105, 124.8421053, 130.0, 134.7894737, 139.9473684, 145.1052632,
             149.8947368, 155.0526316, 159.8421053, 165.0, 169.7894737, 174.9473684, 180.1052632, 184.8947368,
             189.6842105, 194.8421053, 199.6315789]
        y = [0.0, 0.0, 0.0, 0.005405405, 0.018918919, 0.051351351, 0.097297297, 0.167567568, 0.254054054, 0.351351351,
             0.445945946, 0.548648649, 0.624324324, 0.710810811, 0.786486486, 0.848648649, 0.905405405, 0.935135135,
             0.954054054, 0.962162162]
        p_failure = np.interp(wind_mph, x, y, left=0.0, right=1.0)

    # HAZUS Functions - Destruction (only 2 of the 6 building types of destruction curve that is not infinitely stiff)
    # --------------------------

    # SECBL (Steel Engineered Commercial Building 1 to 2 stories, HAZUS)
    elif curve == "secbl_destr":
        x = [140.3411247, 144.626522, 148.9131862, 153.2018429, 157.4909037, 161.7803753, 166.0710041, 170.3639131,
             174.4649887, 177.9807636, 181.6897079, 185.5934215, 189.0138903, 191.5218888, 194.3889741, 196.7357948,
             198.3024975, 199.4783153]
        y = [0.004269528, 0.004719701, 0.009187386, 0.019974509, 0.032042893, 0.045414254, 0.062455667, 0.086728602,
             0.120360139, 0.150986056, 0.176490216, 0.201947112, 0.239188939, 0.265404308, 0.297906232, 0.3277453,
             0.354473935, 0.377028643]
        p_failure = np.interp(wind_mph, x, y, left=0.0)

    # SECBM (Steel Engineered Commercial Building 3 to 5 stories, HAZUS)
    elif curve == "secbm_destr":
        x = [120.1751521, 125.1971465, 129.9269617, 134.2183378, 138.5101638, 143.0732199, 146.9340585, 150.3124673,
             152.4817256, 156.0746232, 160.3736159, 164.4772144, 167.607469, 170.15148, 172.5028261, 174.8541838,
             177.399176, 179.9442459, 182.4894926, 185.0345605, 186.8002225, 188.1740728, 190.1338831, 192.4842654,
             194.8346672, 196.9909206, 198.5608049, 199.5420634]
        y = [0.005789853, 0.004678538, 0.004912099, 0.006563319, 0.009796236, 0.017151188, 0.026020567, 0.044282351,
             0.033034997, 0.047583122, 0.076001501, 0.103179293, 0.136901133, 0.166686426, 0.204822799, 0.243000143,
             0.276233755, 0.309740503, 0.34386863, 0.377368549, 0.413534941, 0.443624096, 0.476652858, 0.511402366,
             0.546220158, 0.58417558, 0.617754025, 0.639024356]
        p_failure = np.interp(wind_mph, x, y, left=0.0)

    # =====================================#
    # Catch #
    # =====================================#
    else:
        print("Invalid fragility curve type:" + curve)

        if type(wind_mph) is np.ndarray:

            p_failure = np.zeros(len(wind_mph))
        else:
            p_failure = 0.0

    # Common return function
    return p_failure
