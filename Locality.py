# -*- coding: utf-8 -*-
#######################################################################
###   Config.py: Locality definitions for the country inference     ###
###   Copyright: Elena Daehnhardt                                   ###
###   Contact me at: edaehn@gmail.com                               ###
#######################################################################
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



import sys
from config import PRINT_DEBUG
							
# Returns country's dimension and its strength based on the language code provided in the user profile
# Usage:
# lewis_dimension,strength,score=getDimension(country_code,lang):
# strength=0, when language is not supported by the data 
# strength=1, when language IS supported by the data
# strength=2, when language IS supported by the data and it is the first language in the list
# score - is optional


def getDimension(country_code,lang):
    """getDimension returns country's dimension and its strength based on the language code provided in the user profile.

    Args:
        country_code (str): ISO 2-digit country code.
        lang (str): ISO 2-digit language code.

    Returns:
        dimension (str): Dimension code 'LA' for linear-active, 'MA' for multi-active, and 'RE' for reactive profiles as defined in Lewis Model of Cultures
        strength (str): Equals to 2 when the language is placed as the first languege for the defined country, if it is not the first one, but listed - it equals 1, otherwise it equals to 0
        score (str): Internal code defined for the country in the model

    """
    dimension,langs,score=getLocality(country_code)
    strength=0
    if lang in langs: 
    	if langs.index(lang)==0: strength=2
    	else: strength=1

	
	return dimension,strength,score

def getCountryDimensionbyLang(language):
	"""getCountryDimensionbyLang returns country and dimension matching the specified language.
	Is used in the data collection pipeline. When country code is defined, returns dimension and languages.

	Args:
        lang (str): ISO 2-digit language code.

    Returns:
        country (str): ISO 2-digit country code.
        dimension (str): Dimension code 'LA' for linear-active, 'MA' for multi-active, and 'RE' for reactive profiles as defined in Lewis Model of Cultures
        strength (str): Equals to 2 when the language is placed as the first languege for the defined country, if it is not the first one, but listed - it equals 1, otherwise it equals to 0
        score (str): Internal code defined for the country in the model

    """
	# As a possible solution, we could acquire top two-three languages for each country in the list when the number of users from the second country 
	# was not less than 10 percent or some other treshold
	# Otherwise, we might select only one language

	# Another approach would be to comply with the information on official and native languages available at:
	# http://www.nationsonline.org/oneworld/european_languages.htm
	# Spoken languages (good list but without ISO codes):
	# http://www.infoplease.com/ipa/A0855611.html

	# However, based on majority language - it might be difficult to distinguish local population
	# out of travelers and others
	# Used info:
	# http://www.infoplease.com/ipa/A0855611.html
	# http://www.loc.gov/standards/iso639-2/php/code_list.php
	# we also did not include small minorities - as Finish-speaking in Sweden i.e.
	if language=='en': return ('US','GB'),'LA' #,('en','fr'),0   # Canada, French users=159 vs. English-speaking 3803
	if language=='fi': return 'FI','LA' #('fi','sv'),1   # Finland
	if language=='et': return 'EE','LA' #,('et','ru'),2   # Estonia
	if language=='sv': return 'SE','LA' #,('sv'),3   # Sweden
	if language=='lv': return 'LV','LA' #,('lv','ru'),4   # Latvia
	if language=='de': return ('DE','CH','AT'),'LA' #,('de'),6   # Germany
	if language=='fr': return ('LU'),'LA' #,('fr','de'),8   # Luxembourg  !!! not enough data  !!!
	if language=='cs': return 'CZ','LA' # ,('cs'),11  # Czech Republic
	if language=='nl': return 'NL','LA' # ,('nl','fy'),12  # Netherlands
	return '','MA' 
	
	
def getLocality(country_code):
	"""getLocality returns returns dimension and languages matching the specified country code.
	Is used in the data collection pipeline

	Args:
		country (str): ISO 2-digit country code.

	Returns:
		languages (tuple of strings): ISO 2-digit language codes.
		score (int): Internal country codecode.

	"""

	# As a possible solution, we could acquire top two-three languages for each country in the list when the number of users from the second country 
	# was not less than 10 percent or some other treshold
	# Otherwise, we might select only one language

	# Another approach would be to comply with the information on official and native languages available at:
	# http://www.nationsonline.org/oneworld/european_languages.htm
	# Spoken languages (good list but without ISO codes):
	# http://www.infoplease.com/ipa/A0855611.html

	# However, based on majority language - it might be difficult to distinguish local population
	# out of travelers and others
	# Used info:
	# http://www.infoplease.com/ipa/A0855611.html
	# http://www.loc.gov/standards/iso639-2/php/code_list.php
	# we also did not include small minorities - as Finish-speaking in Sweden i.e.
	if country_code=='CA': return 'LA',('en','fr'),0   # Canada, French users=159 vs. English-speaking 3803
	if country_code=='FI': return 'LA',('fi','sv'),1   # Finland
	if country_code=='EE': return 'LA',('et','ru'),2   # Estonia
	if country_code=='SE': return 'LA',('sv'),3   # Sweden
	if country_code=='LV': return 'LA',('lv','ru'),4   # Latvia
	if country_code=='GB': return 'LA',('en'),5   # U.K.
	if country_code=='DE': return 'LA',('de'),6   # Germany
	if country_code=='CH': return 'LA',('de','fr','it'),7   # Switzerland
	if country_code=='LU': return 'LA',('fr','de'),8   # Luxembourg  !!! not enough data  !!!
	if country_code=='US': return 'LA',('en','es'),9   # U.S.A.
	if country_code=='AT': return 'LA',('de','sl','hr','hu'),10  # Austria
	if country_code=='CZ': return 'LA',('cs'),11  # Czech Republic
	if country_code=='NL': return 'LA',('nl','fy'),12  # Netherlands
	if country_code=='NO': return 'LA',('no','se'),13  # Norway
	if country_code=='SI': return 'LA',('sl'),14  # Slovenia
	if country_code=='AU': return 'LA',('en'),15  # Australia
	if country_code=='DK': return 'LA',('da','fo','kl','de','en'),16  # Denmark (English is "predominant second language"
	if country_code=='IE': return 'LA',('en','ga'),17  # Ireland
	if country_code=='BE': return 'MA',('nl','fr','de'),18  # Belgium
	if country_code=='FR': return 'MA',('fr'),19  # France
	if country_code=='PL': return 'MA',('en','pl','ru'),20  # Poland
	if country_code=='LT': return 'MA',('lv','ru','lt'),21  # Lithuania
	if country_code=='BY': return 'MA',('be','ru'),22  # Belarus
	if country_code=='RU': return 'MA',('ru'),23  # Russian Federation
	if country_code=='UA': return 'MA',('uk','ru'),24  # Ukraina
	if country_code=='MK': return 'MA',('mk','sq'),25 # Macedonia
	if country_code=='AD': return 'MA',('ca','sr'),26 # ANDORRA

	if country_code=='BU': return 'MA',('bg','tr','ro'),27 # Bulgaria
	if country_code=='RO': return 'MA',('ro','hu'),28 # Romania
	if country_code=='XK': return 'MA',('sq','sr'),29 # Kosovo
	if country_code=='HU': return 'MA',('hu','ro'),30 # Hungary

	if country_code=='SK': return 'MA',('sk'),31  # Slovakia
	if country_code=='IT': return 'MA',('it'),32  # Italy
	if country_code=='PT': return 'MA',('pt'),33  # Portugal
	if country_code=='ES': return 'MA',('es','ca','gl','eu'),34  # Spain
	if country_code=='GR': return 'MA',('en','el'),35  # Greece 
	if country_code=='MT': return 'MA',('mt','en'),36  # Malta
	if country_code=='CY': return 'MA',('el','tr'),37  # Cyprus
	# http://en.wikipedia.org/wiki/Hispanic_America
	if country_code=='BO': return 'MA',('es','qu','ay'),38  # Bolivia
	if country_code=='CO': return 'MA',('es',),39  # Colombia
	if country_code=='CR': return 'MA',('es'),40  # Costa Rica
	if country_code=='CU': return 'MA',('es'),41  # Cuba
	if country_code=='DO': return 'MA',('es'),42  # Dominican Republic
	if country_code=='EC': return 'MA',('es','qu'),43  # Ecuador
	if country_code=='SV': return 'MA',('es'),44  # El Salvador
	if country_code=='GT': return 'MA',('es'),45  # Guatemala
	if country_code=='HN': return 'MA',('es'),46  # Honduras
	if country_code=='NI': return 'MA',('es'),47  # Nicaragua
	if country_code=='PA': return 'MA',('es','en'),48  # Panama
	if country_code=='PY': return 'MA',('es','gn'),49  # Paraguay
	if country_code=='PE': return 'MA',('es','qu'),50  # Peru 
	if country_code=='PR': return 'MA',(''),51  # Puerto Rico
	if country_code=='UY': return 'MA',('es','pt'),52  # Uruguay
	if country_code=='VE': return 'MA',('es'),53  # Venezuela
	# Total HA population is about 376,607,614
	if country_code=='RA': return 'MA',('es'),54  # Argentina
	if country_code=='MX': return 'MA',('es'),55  # Mexico
	if country_code=='BR': return 'MA',('pt','es','en','fr'),56  # Brazil
	if country_code=='CL': return 'MA',('es'),57  # Chile
	# http://en.wikipedia.org/wiki/Sub-saharan_africa
	if country_code=='AO': return 'MA',('pt'),58  # Angola
	if country_code=='BI': return 'MA',('fr','sw'),59  # Burundi
	if country_code=='CD': return 'MA',('fr','ln'),60  # Democratic Republic of the Congo
	if country_code=='RW': return 'MA',('rw','fr','en'),61  # Rwanda
	if country_code=='ST': return 'MA',('pt'),62  # Sao Tome and Principe
	if country_code=='CM': return 'MA',('fr','en'),63  # Cameroon
	if country_code=='CF': return 'MA',('fr'),64  # Central African Republic
	if country_code=='CG': return 'MA',('fr','ln'),65  # Congo
	if country_code=='GQ': return 'MA',('es','fr'),67  # Equatorial Guinea
	if country_code=='GA': return 'MA',('fr'),68  # Gabon
	if country_code=='KE': return 'MA',('en','sw'),69  # Kenya
	if country_code=='TZ': return 'MA',('sw','en'),70  # Tanzania
	if country_code=='UG': return 'MA',('en','lg'),71  # Uganda
	if country_code=='SD': return 'MA',('ar'),72  # Sudan
	if country_code=='SS': return 'MA',('en','ar'),73  # South Sudan
	if country_code=='DJ': return 'MA',('fr','ar','so','aa'),74  # Djibouti
	if country_code=='ER': return 'MA',('aa','ar'),75  # Eritrea
	if country_code=='ET': return 'MA',('am'),76  # Ethiopia, needs care!
	if country_code=='SO': return 'MA',('so','ar','en','it'),77  # Somalia
	if country_code=='BW': return 'MA',('tn'),78  # Botswana
	if country_code=='KM': return 'MA',('','fr','ar'),79  # Comoros
	if country_code=='LS': return 'MA',('st','en'),80  # Lesotho
	if country_code=='MG': return 'MA',('mg','fr'),81  # Madagascar
	if country_code=='MW': return 'MA',('ny','en'),82  # Malawi
	if country_code=='MU': return 'MA',('fr','en'),83  # Mauritius
	if country_code=='MZ': return 'MA',('pt'),84  # Mozambique, needs care!
	if country_code=='NA': return 'MA',('en'),85  # Namibia
	if country_code=='SC': return 'MA',(''),86  # Seychelles
	if country_code=='ZA': return 'MA',('af','en'),87  # South Africa
	if country_code=='SZ': return 'MA',(''),88  # Swaziland
	if country_code=='ZM': return 'MA',(''),89  # Zambia
	if country_code=='ZW': return 'MA',(''),90  # Zimbabwe
	if country_code=='BJ': return 'MA',(''),91  # Benin
	if country_code=='ML': return 'MA',(''),92  # Mali
	if country_code=='BF': return 'MA',(''),93  # Burkina Faso
	if country_code=='CV': return 'MA',(''),94  # Cape Verde
	if country_code=='CI': return 'MA',(''),95  # Cote d Ivoire
	if country_code=='GM': return 'MA',(''),96  # Gambia
	if country_code=='GH': return 'MA',('en'),97  # Ghana
	if country_code=='GN': return 'MA',(''),98  # Guinea
	if country_code=='GW': return 'MA',(''),99  # Guinea-Bissau
	if country_code=='LR': return 'MA',(''),100  # Liberia
	if country_code=='MR': return 'MA',(''),101  # Mauritania
	if country_code=='NE': return 'MA',(''),102  # Niger
	if country_code=='NG': return 'MA',(''),103  # Nigeria
	if country_code=='SN': return 'MA',(''),104  # Senegal
	if country_code=='SL': return 'MA',(''),105  # Sierra Leone
	if country_code=='TG': return 'MA',(''),106  # Togo
	# http://en.wikipedia.org/wiki/Sub-saharan_africa states:
	# "The population of Sub-Saharan Africa was 800 million in 2007"
	if country_code=='SA': return 'MA',(''),107  # Saudi Arabia
	# Arab countries
	if country_code=='DZ': return 'MA',(''),108  # Algeria
	if country_code=='BH': return 'MA',(''),109 # Bahrain
	if country_code=='EG': return 'MA',('ar'),110 # Egypt
	if country_code=='IQ': return 'MA',('ar','ku'),111 # Iraq
	if country_code=='JO': return 'MA',(''),112 # Jordan
	if country_code=='KW': return 'MA',(''),113 # Kuwait 
	if country_code=='LB': return 'MA',(''),114 # Lebanon
	if country_code=='LY': return 'MA',(''),115 # Libya
	if country_code=='MA': return 'MA',('ar'),116 # Morocco
	if country_code=='OM': return 'MA',(''),117 # Oman
	if country_code=='PS': return 'MA',(''),118 # Palestine
	if country_code=='QA': return 'MA',(''),119 # Qatar
	#if country_code=='SD': return 'MA',(''),120 # Sudan ---
	if country_code=='SY': return 'MA',('ar','ku'),121 # Syria
	if country_code=='TN': return 'MA',(''),122 # Tunisia
	if country_code=='AE': return 'MA',('ar','fa'),123 # United Arab Emirates
	if country_code=='YE': return 'MA',(''),124 # Yemen
	# As states http://en.wikipedia.org/wiki/Arab_countries:
	# "TOTAL  Arab League: 349,870,608"
	if country_code=='IR': return 'MA',(''),125 # Iran
	if country_code=='TR': return 'MA',('tr','ku','az'),126 # Turkey
	if country_code=='IN': return 'RE',('hi','bn','gu','ks','ml','sa','sd','or','kn','as','pa','ta','te','ur','en','id'),127 # India
	if country_code=='ID': return 'RE',('id','en','nl','jv'),128 # Indonesia
	if country_code=='MY': return 'RE',('ms','en','th','ta','te','ml','pa'),129 # Malaysia Ms was much less than 10 percent !
	if country_code=='PH': return 'RE',('es','en'),130 # Philippines
	if country_code=='KP': return 'RE',('ko'),131 # Korea, Democratic People's Republic of
	if country_code=='KR': return 'RE',('ko'),132 # Korea, Republic of
	if country_code=='TH': return 'RE',('th','km','ms'),133 # Thailand
	if country_code=='CN': return 'RE',('zh',''),134 # China
	if country_code=='VN': return 'RE',('vi','en'),135 # Vietnam
	if country_code=='JP': return 'RE',('ja'),136 # Japan
	if country_code=='TW': return 'RE',(''),137 # Taiwan, Province of China
	if country_code=='HK': return 'RE',(''),138 # Hong Kong
	if country_code=='SG': return 'RE',('en','ms','zh','ta'),139 # Singapore   
	return 'UN',(''),1000 # Undefined

				