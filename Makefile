# see http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Tools.DynamoDBLocal.html
dynamo:
	java -Djava.library.path=./dynamo_local/DynamoDBLocal_lib -jar DynamoDBLocal.jar --port 8010
