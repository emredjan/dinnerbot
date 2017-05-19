import os
import time
from slackclient import SlackClient
from settings import SLACK_BOT_TOKEN, BOT_ID, BOT_NAME

# initialize slack client
slack_client = SlackClient(SLACK_BOT_TOKEN)

# constants
AT_BOT = '<@' + BOT_ID + '>'
EXAMPLE_COMMAND = 'dinner'

def main():
    READ_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print('dinnerbot connected and running!')
        while True:
            for i in slack_client.rtm_read():
                if i:
                    try:
                        if i['type'] == 'message' and i['channel'].startswith('D'):
                            slack_client.api_call('chat.postMessage', channel=i['channel'], text='It somehow works!', as_user=True)
                    except:
                        pass
            '''command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:

                handle_command(command, channel)
            time.sleep(READ_DELAY)'''
    else:
        print('Connection failed. Invalid Slack token or bot ID?')

def handle_command(command, channel):
    '''
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    '''

    if command.startswith(EXAMPLE_COMMAND):
        response = 'Sure...write some more code then I can do that!'
    else:
        response = 'Not sure what you mean. Use the *' + EXAMPLE_COMMAND + \
        '* command with numbers, delimited by spaces.'

    slack_client.api_call('chat.postMessage', channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    '''
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    '''

    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
    return None, None


if __name__ == '__main__':
    main()