import os

from slackclient import SlackClient

BOT_NAME = 'botin'

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
print(os.environ.get('SLACK_BOT_TOKEN'))

if __name__ == "__main__":
    print(slack_client.api_call("api.test"))
    api_call = slack_client.api_call("users.list")
    print(api_call.get('ok'))
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print(api_call.get('error'))
        print("could not find bot user with the name " + BOT_NAME)
