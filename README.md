# TheMoazin

## Producer
the service who read the details files from storage and send them in kafka

## Consumer
the service who gets the metadata from Producer and add unique id to them,<br>
loop over the locations of them and send the audio to mongodb using GridFS, <br>
use it because we can send more them 16Mb size file with it, after that send them <br>
to elasticsearch.

## STT
the service fetch all the docs from elastic, run over them and every doc it fetches the <br>
audio data from mongodb, recognize the text from the audio add field text to the doc <br>
and assign the text to the field and sen dit back to elastic.

<br>

### Branches:

_Main_ - production branch <br>
_Dev_ - developing branch <br>
_Docker_ - branch that holds the docker version
