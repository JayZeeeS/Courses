import os
import re
import random
from bs4 import BeautifulSoup
import requests
import codecs
from time import sleep, strftime, localtime, time
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

LOG_FORMAT = ("\n" + ("~o" * 58) + "\n")

# Initializes your app with your bot token and socket mode handler

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Load JSON


def fetch_keywords():
    with open("conditions.json", "r") as f:
        keywords = json.load(f)
        return keywords

# Helper function that sends a messaage as a reply always.


def post_message(response, event):
    if "thread_ts" not in event:
        app.client.chat_postMessage(
            channel=event["channel"],
            thread_ts=event["ts"],
            text=response
        )
        # print(result)
        return
    app.client.chat_postMessage(
        channel=event["channel"],
        thread_ts=event["thread_ts"],
        text=response
    )
    # print(result)
    return

# Helper function to check if the message should be responded:


def checkMsg(event, json, logs=False):
    condset_id = []
    threshold = 0
    required = []
    included = []
    excluded = []
    conditions = []
    issue = ""
    ratio = False
    found = ""
    solution = ""
    logprnt = f""
    message = str(event["text"].casefold())
    for obj in json["Issue"]:
        # print("reached the issue loop")
        if logs == True:
            if "channel" in obj and "channel" in event:
                if not event["channel"] in obj["channel"]:
                    return False
        if "conditions" in obj:
            conditions = obj["conditions"]
        for condset in conditions:
            # print("reached the condset loop")
            if "condset_id" in condset:
                condset_id = condset["condset_id"]
            # print("1")
            if "threshold" in condset:
                threshold = condset["threshold"]
            # print("2")
            if "required" in condset:
                required = condset["required"]
            # print("3")
            if "included" in condset:
                included = condset["included"]
            # print("4")
            if "excluded" in condset:
                excluded = condset["excluded"]
            # print("5")
            # print(threshold)
            # print(cond)
            requiredCount = 0
            is_excluded = False
            # print("required", required)
            for req in required:
                # print("reached the required loop")
                if str(req).casefold() in message:
                    requiredCount += 1
            if requiredCount == len(required):
                keywordCount = 0
                found = ""
                for exc in excluded:
                    if exc.casefold() in message:
                        is_excluded = True
                        break
                if is_excluded:
                    break
                for inc in included:
                    # print("reached the included loop")
                    if str(inc).casefold() in message:
                        keywordCount += 1
                        if found != "":
                            found = f"{found}, {inc}"
                        else:
                            found = f"{inc}"
                ratio = keywordCount >= (len(included) * threshold)
                if "solution" in obj:
                    solution = obj["solution"]
                if "name" in obj:
                    issue = obj["name"]
                solution = solution.replace("&lt;", "<")
                solution = solution.replace("&gt;", ">")
                if ratio:
                    logprnt = f"Reached threshold: {str(ratio)} \nRatio was: {str(keywordCount / len(included))}\nThreshold is: {str(threshold)}\nIncludes keywords: {', '.join(included)}\nIssue: {str(issue)}\nIssue ID: {condset_id}\nMessage: {message}\nKeyword count: {keywordCount}\nFound keywords: {found}\nRequired keywords: {','.join(required)}\nSolution:\n{solution}\nSENT!\n{LOG_FORMAT}"
                    if logs == True:
                        logprnt = f"Message from channel {event['channel']}\nReached threshold: {str(ratio)} \nRatio was: {str(keywordCount / len(included))}\nThreshold is: {str(threshold)}\nIncludes keywords: {', '.join(included)}\nIssue: {str(issue)}\nIssue ID: {condset_id}\nMessage: {message}\nKeyword count: {keywordCount}\nFound keywords: {found}\nRequired keywords: {','.join(required)}\nSolution:\n{solution}\nSENT!\n{LOG_FORMAT}"
                        with open(f"Logs_{strftime('%d_%m_%Y', localtime())}.txt", "a") as f:
                            f.write(logprnt)
                        print(logprnt)
                    return solution
    if logs == True:
        with open(f"Logs_{strftime('%d_%m_%Y', localtime())}.txt", "a") as f:
            f.write(f"{message}\nNo match {LOG_FORMAT}")
            f.close()
    else:
        return f"{message}\nNo match {LOG_FORMAT}"
    return False


def log(channel, file, json):
    thread_count = 0
    counter = 0
    app.client.chat_postMessage(
        channel="D04FMU37QAD",
        text="Starting log."
    )
    # Initialize conversation history and cursor
    conversation_history = []
    cursor = None
    open(file, "x")
    f = codecs.open(file, "a", encoding="utf-16")
    print("Starting the history pagination and calling of API history method." + LOG_FORMAT)
    app.client.chat_postMessage(
        channel="D04FMU37QAD",
        text="Starting the history pagination and calling of API history method."
    )
    # Load conversation history using pagination
    while True:
        sleep(1.2)
        # Call conversations_history method with cursor parameter
        result = app.client.conversations_history(
            channel=channel, cursor=cursor)
        conversation_history += result["messages"]

        # Check if there are more pages of results
        if "response_metadata" in result and "next_cursor" in result["response_metadata"]:
            # Set cursor to next_cursor value
            cursor = result["response_metadata"]["next_cursor"]
        else:
            # No more pages of results
            break
    print("Starting the thread pagination and calling of API replies method." + LOG_FORMAT)
    app.client.chat_postMessage(
        channel="D04FMU37QAD",
        text="Starting the thread pagination and calling of API replies method."
    )
    # Load threads for each message in the conversation history
    for message in conversation_history:
        if "thread_ts" in message:
            # Load thread history
            thread_count += 1
            sleep(1.2)
            thread_history = app.client.conversations_replies(
                channel=channel, ts=message["thread_ts"])
            for msg in thread_history["messages"]:
                counter += 1
                solution = checkMsg(msg, json)
                if solution:
                    f.write(f"{solution}")
    app.client.chat_postMessage(
        channel="D04FMU37QAD",
        text=f"Finished Logging!\n{thread_count} threads processed\n{counter} messages processed."
    )
    return


def checkApp(app_name, json_data):
    app_list = json_data["Apps"]
    app_name = app_name.replace("Check App ".casefold(), "").strip()
    print(app_name)
    print(f"Checking data for {app_name}{LOG_FORMAT}")
    if app_name == "list please.":
        response = ""
        for app in app_list:
            if response == "":
                response = f"Here are the apps with data: \n{app['name']}, "
            else:
                response = f"{response}{app['name']}, "
        return response
    if app_name == "":
        return "Usage: Check App <App Name>"
    for app in app_list:
        if app["name"].casefold() == app_name.casefold():
            if "URLs" in app:
                return f"Here is the data relevant to {app_name.title()} found in our database:\n{app['URLs']}"
            else:
                return "Data for this app is not available."
    return f"{app_name.title()} was not found in our database."


def checkURL(site):
    response = ""
    message = set()
    contType = ""
    site = site.replace("Check URL ".casefold(), "")
    site = site.replace("<", "")
    site = site.replace(">", "")
    if "|" in site:
        site = site[:site.find("|") + 1]
    print(f"Checking URLs for {site}{LOG_FORMAT}")
    if site == "":
        return "Usage: Check URL <URL>"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        data = requests.get(site, headers=headers)
    except requests.exceptions.RequestException as e:
        print("Error: Could not establish a connection to the website. If your URL does not start with 'https://' then include it at the start.")
        return "Error: Could not establish a connection to the website. If your URL does not start with 'https://' then include it at the start."
    soup = BeautifulSoup(data.text, 'html.parser')
    sep = soup.find_all(href=re.compile("http"))
    for a in sep:
        match = re.search('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', str(a))
        if match:
            url = match.group()
            if url == site:
                continue
            try:
                sleep(random.uniform(0, 5))
                r = requests.get(url, timeout=2)
                status = r.status_code
                link = r.url
                if "Content-Type" in r.headers:
                    contType = r.headers["Content-Type"]
                if status != 200:
                    # print(f"Error: {url} returned status code {status}")
                    message.add(f"Type {contType} Code {status} URL: {url}")
                    continue
                message.add(f"Type: {contType} URL: {link}")
            except requests.exceptions.RequestException as e:
                print(f"Error: Could not establish a connection to {url}")
    for item in message:
        if response == "":
            response = f"Here are the URLs that are called by {site}, who returned code {data.status_code}:\n{item}"
        else:
            response = f"{response}\n{item}"
    return response


def checkID(id):
    response = ""
    id = id.replace(" ", "%20").strip(" \"")
    if id == "":
        return "Usage: 'Check ID <ID>'. Make sure to maintain the capitalization and spacing intact."
    print(f"Sending portal URL for ID {id.replace('%20', ' ')}{LOG_FORMAT}")
    response = f"https://portal.mbsmartservices.net/mbsmart/Admin.html?userid={id}"
    r = requests.get(response)
    if "https://portal.mbsmartservices.net/mbsmart/files/decor13.css" in r.headers:
        response = f"https://portal.mbsmartservices.net/mbsmart/Admin.html?userid=%20{id}"
    return response


# Logic starts
@app.event({"type": "message"})
@app.event({"type": "app_mention"})
def respond(event):
    # print("received")
    if "type" in event and "channel" in event and "user" in event:
        json = fetch_keywords()
        thread_ts = event.get("thread_ts", event["ts"])
        solution = ""
        message = ""
        if "text" in event:
            message = event["text"]
        else:
            print(f"Message of type {event['type']} not handled")
        if "LogMsg" in json:
            if message == json["LogMsg"]:
                print("Starting log." + LOG_FORMAT)
                log("C0238BXC141",
                    f"responseLogs_{strftime('%d_%m_%Y_%H:%M', localtime())}.txt", json)
                print("Finished logging." + LOG_FORMAT)
                return
        if "Check App".casefold() in message.casefold():
            name = message.replace(
                "Check App ".casefold(), "").strip().casefold()
            response = checkApp(name, json)
            if response != "":
                post_message(response, event)
            return
        if "Check URL".casefold() in message.casefold():
            post_message("This can take some time.", event)
            site = message.replace(
                "Check URL".casefold(), "").strip("<> ").casefold()
            response = checkURL(site)
            if response != "":
                post_message(response, event)
            else:
                post_message("Empty HTTP response", event)
            return
        if "Check ID \"".casefold() in message.casefold():
            id = message[message.find(
                "Check ID ".casefold()) + len("Check ID") + 1:].strip()
            if " \"" not in message:
                response = "Usage: 'Check ID <\"ID\">'. Make sure to maintain the spaces and cpitalization intact. Sometimes an ID will start with a space, so take that into account."
                post_message(response, event)
                return
            response = checkID(id)
            if response != "":
                post_message(response, event)
            return
        if not event["type"] == "app_mention":
            if not event["channel"] == "C04FE7YGY1Y":
                if event["user"] in json["Ignore"]:
                    print("Message was: " +
                          message + "\nIgnored" + LOG_FORMAT)
                    return
        # print("before the check")
        solution = checkMsg(event, json, True)
        # print("reached this point, woo")
    # Check if the solution has already been sent

        conversation = app.client.conversations_replies(
            channel=event["channel"], ts=thread_ts)
        if any(message["text"] == solution for message in conversation["messages"]):
            # Return without sending the solution again
            print(f"Duplicate not sent{LOG_FORMAT}")
            return

    # Send the message if ratio is true and the solution out of testing
        if solution == False:
            print(f"{message}\nNo match {LOG_FORMAT}")
            return
        post_message(solution, event)
        return
        # print("Solution sent" + LOG_FORMAT)
    print(f"Event could not be handled{LOG_FORMAT}")
    return


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
