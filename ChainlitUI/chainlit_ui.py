import os
import chainlit as cl
import json
import httpx

from user_feedback import UserFeedback
from constants import USER_EMAIL
from user_auth import AuthUser
import ast
import datetime

os.environ[
    'CHAINLIT_AUTH_SECRET'] = (
    "mVoGtl5bk*L54OQ+99E22AeM4lWfSSu:NpJzTBz-_bBASP%6pQG=Px+Pjdb=Hbv/")


@cl.password_auth_callback
def auth_callback(email: str, password: str):
    user_auth = AuthUser()
    print("AUTH: ", user_auth.check_user(email=email, password=password))
    if user_auth.check_user(email=email, password=password):
        return cl.User(
            identifier=f"{email}",
            metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None


@cl.action_callback('Not Satisfied?')
async def store_user_feedback(disagree):
    current_conversation = ast.literal_eval(disagree.value)
    request_body = {
        'date': str(datetime.datetime.now().strftime('%Y-%m-%d')),
        'time': str(datetime.datetime.now().strftime('%H:%M:%S')),
        'user_email': USER_EMAIL,
        'user_input': current_conversation[1],
        'response_received': current_conversation[0],
        'time_taken': current_conversation[2],
        'feedback': 'disagree'
    }

    api_url = "http://127.0.0.1:8000/store_user_feedback"

    async with (httpx.AsyncClient(timeout=60000, verify=False) as client):
        response = await client.post(api_url, json=request_body)

    await disagree.remove()


@cl.action_callback('Satisfied!')
async def store_user_feedback(agree):
    current_conversation = ast.literal_eval(agree.value)
    request_body = {
        'date': str(datetime.datetime.now().strftime('%Y-%m-%d')),
        'time': str(datetime.datetime.now().strftime('%H:%M:%S')),
        'user_email': USER_EMAIL,
        'user_input': current_conversation[1],
        'response_received': current_conversation[0],
        'time_taken': current_conversation[2],
        'feedback': 'agree'
    }

    api_url = "http://127.0.0.1:8000/store_user_feedback"

    async with (httpx.AsyncClient(timeout=60000, verify=False) as client):
        response = await client.post(api_url, json=request_body)

    await agree.remove()


@cl.step
async def generating():
    return "Please wait...."


@cl.on_message
async def main(message: cl.Message):
    request_body = {
        "input_text": str(message.content)
    }
    api_url = "http://127.0.0.1:8000/get_response"
    await generating()
    async with (httpx.AsyncClient(timeout=60000) as client):
        response = await client.post(api_url, json=request_body)

        if response.status_code == 200:
            json_response = json.loads(response.json())
            try:
                input_text = json_response['similar_text']
                response_text = json_response['input_text']
                time_taken = json_response['time_taken']

                actions = [
                    cl.Action(
                        name="Not Satisfied?",
                        value=f"{[input_text, response_text, time_taken]}",
                        description="Disagree with the Output"),
                    cl.Action(
                        name="Satisfied!",
                        value=f"{[input_text, response_text, time_taken]}",
                        description="Agree with the Output"),
                    cl.Action(
                        name=f"{json_response['time_taken']}s",
                        value=f"{json_response['time_taken']}s",
                        description="Time Taken by the bot")
                ]

                await (cl.Message(
                    content=json_response['similar_text'],
                    actions=actions).send())
            except KeyError:
                await cl.Message("Please ask a Relevant Query").send()
        else:
            print(f"Request failed with status code {response.status_code}")
            print(response.text)
