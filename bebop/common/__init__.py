from tornado.options import define


define('port', default=5000, help='Default app port.', type=int)

define('amazon_access_key', default='', help='Amazon access key, not required.', type=str)
define('amazon_secret_key', default='', help='Amazon secret key, not required.', type=str)
define('amazon_ddb_host', default='', help='DynamoDB host, not required.', type=str)
