# TheMoazin

## Producer
the service who read the details files from storage and send them in kafka

## Consumer
the service who gets the metadata from Producer and add unique id to them,<br>
loop over the locations of them and send the audio to mongodb using GridFS, <br>
use it because we can send more them 16Mb size file with it, after that send them <br>
to elasticsearch.

## Processor
the service fetch all the docs from elastic, run over them and every doc it fetches the <br>
audio data from mongodb, recognize the text from the audio add field text to the doc <br>
and assign the text to the field, calculate the BDS details and send it back to elastic.

## ServiceFastAPI
service to endpoint to receive data from elastic, got five routes:<br>
_/is_bds_ - returns all the docs who is_bds field is True<br>
_/high_thread_level_ - returns all the docs who bds_thread_level is high<br>
_/middle_thread_level_ - returns all the docs who bds_thread_level is middle<br>
_/all_logs_ - returns all the logs<br>
_/doc_logs_ - returns all the doc logs by id<br>

<br>

### BDS Details

_Precents Of BDS In Text -_ i chose to calculate it by divide the power of the <br>
hostile words in the text by the length of the text without stopwords, what means that <br>
the result give us how many times the blogger say hostile words per regular words. <br>

_Indicted Text -_ the precents i chose to set the minimum to indicted text is 15% because <br>
i think its enough hostile words from regular words to say this suppose to up red light.

_Thread_Level -_ in first place im starting from an assumption that if text not indicted the <br>
is_bds var is False, because only if the text is bd si can calculate if the thread is middle <br>
or high. <br>
i look over the docs precents and find the max value in my precents claculate pattern is 42% <br>
and the median is 15%, and the median between 15% and 42% is 23%.<br>
_so i set it like that:_ <br>
_nobne:_ less than 11%<br>
_middle:_ between 11% and 25% (i add two precents)<br>
_high:_ up than 25%


### Branches:

_Main_ - production branch <br>
_Dev_ - developing branch <br>
_Docker_ - branch that holds the docker version



