import settings
import os
from slackclient import SlackClient

slack_client = SlackClient(settings.SLACK_BOT_TOKEN)

if __name__ == '__main__':
    api_call = slack_client.api_call('users.list')
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == settings.BOT_NAME:
                print('Bot ID for \'' + user['name'] + '\' is ' + user.get('id'))
    else:
        print("could not find bot user with the name " + settings.BOT_NAME)