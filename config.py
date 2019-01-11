#######################################################################
###   Config.py:     Configuration file for Save Tweets             ###
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

############################## Twitter connection  ##############################
# https://apps.twitter.com/
consumer_key="***************************"
consumer_secret="****************************************************"
oauth_token="*************************************************"
oauth_secret="*****************************************"


################### PRINT_DEBUG=True for printing details to screen
PRINT_DEBUG=False

################### Change to your own keywords for streaming
STREAM_FILTER=['today', 'news']

################## If you want to store JSON into the output directory
# (JSON file does not include the country inference but is useful for storing the source)
SAFE_JSON=False

################## If you want to store CSV into the output directory 
# (CSV file includes also the country inference)
SAFE_CSV=True