import os
import sys
import time
from datetime import datetime
import requests
from slackclient import SlackClient
from settings import SLACK_BOT_TOKEN, BOT_ID, BOT_NAME, GOOGLE_KEY

# initialize slack client
sc = SlackClient(SLACK_BOT_TOKEN)
sys.stdout = open('session.log', 'a')

# constants
AT_BOT = '<@' + BOT_ID + '>'

# commands
CMD_GOOGLE_PLACE = 'gp '

def main():
    READ_DELAY = 1 # 1 second delay between reading from firehose
    if sc.rtm_connect():
        print(str(datetime.now()))
        print(BOT_NAME, 'connected and running!')
        while True:
            try:
                command, channel = parse_slack_output(sc.rtm_read())
                if command and channel:
                    handle_command(command, channel)
                time.sleep(READ_DELAY)
            except KeyboardInterrupt:
                print('\nClosing ' + BOT_NAME + '...')
                sys.exit()
    else:
        print('Connection failed. Invalid Slack token or bot ID?')

def handle_command(command, channel):
    '''
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    '''
    response = ''
    message = 'Sorry, the only command I understand: *gp* _your search query_\nWhich fetches search results from google places with ratings'
    if command and command.startswith(CMD_GOOGLE_PLACE):
        search_text = command[len(CMD_GOOGLE_PLACE):]
        response = get_google_places(search_text)

        message = ''
        for i in response:
            message += i + '\n'

    sc.api_call('chat.postMessage', channel=channel, text=message, as_user=True)
    print(command, channel)

# TODO: Maybe refactor these into a class?
def get_google_places(search_text):
    '''
        Recieves a search query as argument to pass onto 
        Google Places API text search.
        Returns the results as a list.
    '''
    search_text = '+'.join(search_text.split()) # get rid of spaces and join words with '+'
    api_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=' + search_text + '&key=' + GOOGLE_KEY

    api_response = requests.get(api_url)
    api_output = api_response.json()
    # TODO: Correct the exception handling
    try:
        return [i['name'] + ': ' + str(i['rating']) for i in api_output['results']]
    except KeyError:
        return [i['name'] for i in api_output['results']]


def parse_slack_output(slack_rtm_output):
    '''
        The Slack Real Time Messaging API is an events firehose.
        This parsing function returns None unless a message is
        directed at the Bot (as a DM or @ message), based on its ID.
    '''
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            # TODO: Streamline the conditionals
            # handle DM
            if (output and
                output['type'] == 'message' and
                'text' in output and
                output['channel'].startswith('D') and
                AT_BOT not in output['text'] and
                output['user'] != BOT_ID):
                return output['text'], output['channel']
            # handle @ message
            if (output and
                output['type'] == 'message' and
                'text' in output and
                AT_BOT in output['text'] and
                output['user'] != BOT_ID):
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
    return None, None

if __name__ == '__main__':
    main()
