#######################################################################
###   Config.py: Classifier class (to infer user countries)         ###
###   Copyright:     Elena Daehnhardt                               ###
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

from Locality import *

class Classifier:
	
	def __init__(self,table_suffix=''):
		pass
			
	def ClassifyTextToCountryDimension(self,text):
			
		country_id=self.classifier.predict([text])[0]
		
		countries = self.labels['Country']
		country=str(countries.loc[country_id][0])
		
		return country,getLocality(country)[0]

		
	def loadClassifier(self,filename):
		'''Loads a classification model from the specified file
	
		Inputs:
		filename: full filename of the classifier to be loaded
	
		Returns: classifier
		'''
		
		from sklearn.externals import joblib
		clf = joblib.load(filename)
		return clf
	

