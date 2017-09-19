from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = "amqp://oqocjgvc:wpDedI_G0-d_Tak-ZD35ObDlMrvr97bO@wombat.rmq.cloudamqp.com/oqocjgvc"

TEST_QUEUE_NAME = 'test'

def test_basic():
	client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)

	sentMsg = {'test': 'demo'}
	client.sendMessage(sentMsg)
	client.sleep(10)
	receivedMsg = client.getMessage()
	assert sentMsg == receivedMsg
	print "test_basic passed"


if __name__ == "__main__":
	test_basic()