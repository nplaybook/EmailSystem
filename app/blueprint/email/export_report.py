import json
from math import floor
from typing import List

from flask import g, request, Response
from smtplib import SMTPResponseException
from pydantic import ValidationError

from app.schemas import ExportReportPayload
from app.models import Event
from app.blueprint.email.utils import EmailPrep, send_email_task
from app.library.orm import OrmUtils
from app.library.creds import CredUtils
from app.library.backend_scripts import ExcelFileHandler, CommonUtils
from app.library.response import SuccessResponse, ErrorResponse
from app.library.const import FILE_BASE_PATH, EXCEL_TIME_FORMAT, EXCEL_EXTENSION, MAX_FILE_SIZE


def send_export_data():
    """Export specific data and send it via email. Export means no data aggregation
    is done, just a plain record.
    
    :return: process status
    """

    try:
        payload = ExportReportPayload(**request.json)
    except ValidationError as err:
        return Response(
            json.dumps(
                ErrorResponse(message="Payload error", error=err.errors()).\
                    generate_response()
            ), 400
        )
    else:
        payload = payload.dict()
        payload["smtp"]["password"] = CredUtils.decode(payload["smtp"]["password"])

    report_table = payload.get("report")
    email_payload = payload.get("email")
    email_prep = EmailPrep(email_payload, report_table)
    excel_handler = ExcelFileHandler(report_table)
    if report_table == "event":
        # generate data
        events = g.session.query(Event).all()
        excel_files = generate_data_export_essentials(excel_handler, events)
        total_file = len(excel_files)
    else:
        NotImplementedError()

    for excel_file in excel_files:
        # protect file with password
        password = CommonUtils.generate_password()
        encrypted_file = CommonUtils.encrypt_file(FILE_BASE_PATH, excel_file, password)
        if encrypted_file:
            # generate email content
            if total_file == 1:
                email_content = email_prep.get_email_metadata(excel_file, password)
            else:
                file_index = excel_files.index(excel_file) + 1
                email_content = email_prep.get_email_metadata(excel_file, password, file_index, total_file)
            # prepare payload
            payload["email"]["email_subject"] = email_content.get("subject")
            payload["email"]["email_content"] = email_content.get("body")
            payload["email"]["email_attachment"] = encrypted_file
            payload["email"]["email_attachment_name"] = excel_file
            # send email
            try:
                send_email_task(db=g.session, payload=payload, type="html")
            except SMTPResponseException as err:
                return Response(
                    json.dumps(
                        ErrorResponse(message="Fail to send email", error=err.smtp_error.decode("utf-8")).
                            generate_response()
                    ), err.smtp_code
                )
            else:
                excel_handler.remove_excel_file(FILE_BASE_PATH, excel_file)

        return Response(
            json.dumps(
                SuccessResponse(message="Email is sent").
                    generate_response()
            ), 200
        )


def generate_data_export_essentials(handler: ExcelFileHandler, data) -> List[str]:
    """Generate filename and save excel file

    :param handle: object that will handle data generation
    :param data: data from SQLAlchemy query
    :param header: header name for the excel file
    
    :return: excel file name
    """

    # generate file and data
    file_name = handler.generate_filename(EXCEL_TIME_FORMAT, EXCEL_EXTENSION)
    header = OrmUtils.get_columns_name(data, many=True)
    excel_data = handler.format_base_data(header, data)
    handler.save_excel_file(FILE_BASE_PATH, file_name, header, excel_data)

    # check file size and split if > 10mbs per file
    file_size = CommonUtils.measure_file_size(FILE_BASE_PATH, file_name)
    if file_size >= MAX_FILE_SIZE:
        num_of_split = CommonUtils.count_split(file_size, MAX_FILE_SIZE)
        excel_files = CommonUtils.split_file(
            FILE_BASE_PATH, file_name, num_of_split, excel_data, EXCEL_EXTENSION
        )
        data_per_part = int(floor(len(excel_data)/num_of_split))
        for split, file in zip(range(num_of_split), excel_files):
            start_index, end_index = CommonUtils.get_data_index(excel_data, split, data_per_part)  
            split_data = excel_data[start_index:end_index+1]
            handler.save_excel_file(FILE_BASE_PATH, file, header, split_data)
    else:
        excel_files = [file_name]  # to list so it can be standardized if splitted

    return excel_files