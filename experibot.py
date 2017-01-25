import argparse
import os
import time
from collections import namedtuple

import bot_commands as c
import command_caller as a
from slackclient import SlackClient

command_struct = namedtuple("command_struct", ["func", "description"])

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")


def bothelp(text):
    message_list = []
    text = "Here's everything I can do:"
    attach = []
    fields = []
    for key, available_command in COMMANDS.items():
        fields.append(dict(title=key, value=available_command.description))
    attach.append(dict(fields=fields))
    message_list.append((text, attach))
    return message_list


# constants
AT_BOT = "<@" + BOT_ID + "> "
COMMANDS = {"help": command_struct(bothelp, "This stuff, yeah."),
            "imdb": command_struct(c.imdb_info, "Get information on a specific movie."),
            "imdbs": command_struct(c.imdb_search, "Search information on movies."),
            "imdbtt": command_struct(c.imdb_by_code, "Get information on a movie by providing an IMDB ID.")
            }

UNABLE_TO_UNDERSTAND = "help"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(comm, chan):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = dict()
    t = "Not sure what you mean. Use the *" + UNABLE_TO_UNDERSTAND + \
        "* command for details on what I can do."
    attach = []
    received_command = comm.split(" ")[0]
    if received_command in COMMANDS.keys():
        # Implementing message list, to allow bot to send multiple messages at once
        message_list = COMMANDS[received_command].func(" ".join(comm.split(" ")[1:]))
        for (t, attach) in message_list:
            # print t, attach
            slack_client.api_call("chat.postMessage", channel=chan,
                                  text=t,
                                  attachments=attach,
                                  as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="experimental imdb slackbot with local abilities")
    parser.add_argument("--loc", choices=["local", "slack"], default="slack")
    args = vars(parser.parse_args())

    if "loc" in args.keys() and args["loc"] == "local":
        a.test_each_output()
    else:
        READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
        if slack_client.rtm_connect():
            # print("StarterBot connected and running!")
            while True:
                command, channel = parse_slack_output(slack_client.rtm_read())
                if command and channel:
                    handle_command(command, channel)
                time.sleep(READ_WEBSOCKET_DELAY)
        else:
            print("Connection failed. Invalid Slack token or bot ID?")
