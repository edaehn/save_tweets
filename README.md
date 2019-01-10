# Save Tweets!

## Saving Tweets into CSV and JSON files
I am often asked about Twitter data collection. In particular, how is it possible to track a set of keywords in real time?
In this Python code I am showing a possible method to user Twitter steaming API with Tweepy library.
All you need is to edit config.py and fill out your Twitter consumer key and other connection 
details which you can find out at
[https://apps.twitter.com/](https://apps.twitter.com/). Change also STREAM_FILTER variable to include your search keywords.

## Country Inference
What is the difference from other solutions? As we know, most of the Twitter users do not reveal their locations.
However, with simple machine learning techniques it is possible to infer user locations.
In this script, I provide country inference (the inferred country is added in the output CSV file).
This inference strategy (called "META" in the paper) is described in my paper [Cultural and Geolocation Aspects of Communication in Twitter](https://www.researchgate.net/publication/268279397_Cultural_and_Geolocation_Aspects_of_Communication_in_Twitter) published with my co-authors Yanguo Jing and 
Nick Taylor.

## Citation
If you like using this method, please cite my related research paper providing more details
into the realisation of the country inference used here, and some other solutions. It includes also an overview of the related works of location inference on more fine-grained level (such as state and city):

[Daehnhardt, E., Jing, Y., & Taylor, N. 2014. Cultural and geolocation aspects of 
communication in twitter. In ASE Internation Conference on Social Informatics 2014]
(https://www.researchgate.net/publication/268279397_Cultural_and_Geolocation_Aspects_of_Communication_in_Twitter)

