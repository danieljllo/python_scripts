#! /usr/bin/env python
# This script requires python 3

"""Generate Dominoes Game
Author: Daniel Jaramillo <danieljllo@yahoo.com>

This script allows the user to generate a game of dominoes. The user
must enter the email address of all the players and the SMTP mail server
configuration (address and port) so the emails can be sent.

The user running the script can also play as he/she will not see the contents
of the generated emails.

When the script is run, each player will receive an email with the dominoes
he has to play with.

Join your friends over a video conference and also a Google Doc,
and give them all write access. Decide which player goes first and each
player can copy/paste the dominoe he wants to play from the received email
into the Google Doc.

The email contains each dominoe in the two directions it can be placed.
For example if the board currently has:
.------.------. .------.------.
|()  ()|()    | |()    |      |
|      |  ()  | |  ()  |  ()  |
|()  ()|    ()| |    ()|      |
'------'------' '------'------'

And a player has the 1-4 dominoe, he/she can choose to play it on either side
by selecting the dominoe with the desired direction from the two options in
the email.
"""

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import datetime
from typing import List

# Enter the email of the players here.
# The game can be played with 3 or 4 players
emails = ["player1@email.com",
          "player2@email.com",
          "player3@email.com"]

# Enter the email information so the emails can be sent.
sender_email = "sender@email.com"
smtp_server_address = "smtp.my-email-server.com"
smtp_server_port = 465

# List with all the dominoes availble in unicode.
# Both directions of each dominoe are provided so the player can choose
# which one to play.
dominoes = ["🁣", "🀲🀸", "🀳🀿", "🀴🁆", "🀵🁍", "🀶🁔", "🀷🁛",
            "🁫", "🀺🁀", "🀻🁇", "🀼🁎", "🀽🁕", "🀾🁜",
            "🁳", "🁂🁈", "🁃🁏", "🁄🁖", "🁅🁝",
            "🁻", "🁊🁐", "🁋🁗", "🁌🁞",
            "🂃", "🁒🁘", "🁓🁟",
            "🂋", "🁚🁠",
            "🂓"]

def select_dominoes(dominoes: List[str], order: int, num_players: int) -> str:
    """Randonly generate a set of dominoes for a player
    - If the number of players is 3, each player gets 9 dominoes,
    plus a 10th dominoe that is to be played first (all players will get it)
    - If the number of players is 4, each player gets 7 dominoes

    Keyword arguments:
    dominoes -- a list containing a shuffled full set of dominoes
    order -- the player order (player 0, 1, 2, ...)
    num_players -- the total of players (3 or 4)
    """
    dominoes_text = ""
    num_dominoes = 0
    if num_players == 3:
        num_dominoes = 9
    elif num_players == 4:
        num_dominoes = 7
    for i in range(num_dominoes):
        dominoes_text = dominoes_text + '[' +  dominoes[(order * num_dominoes) + i] + ']'
    if num_players == 3:
        dominoes_text = dominoes_text + '<<<' +  dominoes[27] + '>>>'
    return dominoes_text

def email_player(receiver_email: str, dominoes_text: str, datetime_string: str,
                 smtp_server_address: str, smtp_server_port: int,
                 sender_email: str, password: str):
    """Sends email to a player containig a set of dominoes using an SMTP server

    Keyword arguments:
    receiver_email -- the player email
    dominoes_text -- a string with the dominoes the player will play with
    datetime_string -- a string with the date/time used in the email subject
    smtp_server_address -- address of SMTP email server
        (two factor authentication (2FA) not supported)
    smtp_server_port -- port of SMTP email server
    sender_email -- email address that is used to send player emails and
        authentication with the SMTP server
    password -- password used for authentication with the SMTP server
    """

    message = MIMEMultipart("alternative")
    message["Subject"] = "Dominoe's Round " + datetime_string
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text version of your message
    prefix = """\
These are your dominoes:

"""
    text = prefix + dominoes_text

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server_address, smtp_server_port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

random.shuffle(dominoes)

datetime_string = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")

password = input("Type your mail server password and press enter:")

for i in range(len(emails)):
    dominoes_text = select_dominoes(dominoes, i, len(emails))
    email_player(emails[i], dominoes_text, datetime_string, smtp_server_address,
                    smtp_server_port, sender_email, password)
    print("Email sent to: " + emails[i])
