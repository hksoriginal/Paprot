import json
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import time

from DTOs.Databases.user_feedback_dtos import UserFeedbackDTO
from Presenters.create_and_store_embeddings_presenter import \
    CreateAndStoreEmbeddingsPresenter
from Presenters.get_rag_output_presenter import GetRAGOutputPresenter
from Presenters.user_feedback_presenter import UserFeedbackPresenter

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/get_response")
async def get_bot_response(req_body: Request):
    try:
        data = await req_body.json()
        input_text = data['input_text']

        print(f"\n{input_text}\n")

        rag_presenter = GetRAGOutputPresenter()

        start = time.time()
        bot_response, source_document = rag_presenter.get_output(
            input_query=input_text)
        end = time.time()
        process_time = round(end - start, 1)

        query_result = {
            'time_taken': process_time,
            'source_document': source_document,
            'input_text': input_text,
            'similar_text': bot_response
        }

        print(query_result)

        search_result_json = json.dumps(query_result)
        return JSONResponse(content=search_result_json)

    except json.JSONDecodeError:
        return JSONResponse(
            content={'error': 'Invalid JSON format in request body'},
            status_code=400)


@app.post("/update_policies")
async def update_policy(req_body: Request):
    data = await req_body.json()
    print(data)
    try:
        data = await req_body.json()
        update_policy_flag = bool(data['update_policies'])

        if update_policy_flag:
            create_and_store_embeddings = CreateAndStoreEmbeddingsPresenter()

            start = time.time()
            message = \
                (create_and_store_embeddings.
                create_and_store_embeddings_from_policies(
                    folder_path='./../Policies'))
            end = time.time()
            process_time = end - start

            confirmation_message = {
                'message': message + f" with Processing time : "
                                     f"{round(process_time, 1)} seconds"}

            print(confirmation_message)

            return JSONResponse(content=json.dumps(confirmation_message))

    except json.JSONDecodeError:
        return JSONResponse(
            content={'error': 'Invalid JSON format in request body'},
            status_code=400)


@app.post("/store_user_feedback")
async def store_user_feedback(req_body: Request):
    record_user_feedback_presenter = UserFeedbackPresenter()

    try:
        print("FEEDBACK RECEIVED")
        data = await req_body.json()

        user_feedback_dto = UserFeedbackDTO(
            time=data['time'],
            date=data['date'],
            user_email=data['user_email'],
            user_input=data['user_input'],
            response_received=data['response_received'],
            time_taken=data['time_taken'],
            feedback=data['feedback']
        )

        message = \
            record_user_feedback_presenter.record_user_feedback_in_excel_sheet(
                user_feedback_dto=user_feedback_dto)

        print(message)

    except json.JSONDecodeError:
        return JSONResponse(
            content={'error': 'Invalid JSON format in request body'},
            status_code=400)


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
