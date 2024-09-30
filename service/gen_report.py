import csv
from io import StringIO
import ipaddress
import re
from api.fortianalyzer_api import call_api_fortianalyzer_jsonrpc
from global_constant import GLOBAL_CONSTANT
from datetime import datetime, timedelta
from model.report_list_model_ip_pivot import ReportListModelIpPivot
from model.raw_report_model import RawReportModel
from model.report_model import ReportModel
from model.report_model_ip_pivot import ReportModelIpPivot

def get_list_of_report():
    report_dicts: dict[str, list] = GLOBAL_CONSTANT.REPORT_TYPES
    report_tid_map = {} 

    # Calculate time range (last 7 days until now)
    now = datetime.now()
    start_time = now - timedelta(days=7)
    end_time = now
    
    GLOBAL_CONSTANT.START_TIME = start_time
    GLOBAL_CONSTANT.END_TIME = end_time

    # Format dates as required by the API
    formatted_start_time = start_time.strftime('%Y-%m-%dT%H:%M:%S')
    formatted_end_time = end_time.strftime('%Y-%m-%dT%H:%M:%S')

    for _, report_list in report_dicts.items():
        for report_title in report_list:
            request_body = {
                "id": "string",  # You might need to adjust this based on API requirements
                "jsonrpc": "2.0",
                "method": "get",
                "params": [
                    {
                        "apiver": 3,
                        "sort-by": [
                            {
                                "field": "ReportName",
                                "order": "asc"
                            }
                        ],
                        "state": "generated",
                        "time-range": {
                            "end": formatted_end_time,
                            "start": formatted_start_time
                        },
                        "url": "/report/adom/root/reports/state",
                        "title": report_title
                    }
                ],
                "session": GLOBAL_CONSTANT.SESSION_ID
            }

            # Make the API call (assuming you have the 'call_api' function defined)
            response = call_api_fortianalyzer_jsonrpc(request_body)

            if response:
                response_data = response.json()
                # Extract 'tid' from the response
                try:
                    tid = response_data["result"]["data"][0]["tid"]
                    report_tid_map[report_title] = tid
                except (KeyError, IndexError):
                    print(f"Error extracting tid for report: {report_title}")
            else:
                # Handle errors if the API call fails
                print(f"Error fetching report: {report_title}")
    print(f'count of report is {report_tid_map.__len__()}')
    return report_tid_map

def get_report_data(report_tid_map: dict[str, str]):
    list_report_model: list[ReportModel] = []

    for report_title, tid in report_tid_map.items():
        request_body = {
            "id": "string",  
            "jsonrpc": "2.0",
            "method": "get",
            "params": [
                {
                    "apiver": 3,
                    "data-type": "text",
                    "format": "CSV",
                    "url": f"/report/adom/root/reports/data/{tid}"
                }
            ],
            "session": GLOBAL_CONSTANT.SESSION_ID
        }

        response = call_api_fortianalyzer_jsonrpc(request_body)

        if response:
            reportModel : ReportModel = ReportModel()
            dict_ip_pivot = {}
            response_data = response.json()
            list_report_model_pivot: list[ReportModelIpPivot] = []
            list_report_raw_model: list[RawReportModel] = []
            set_date_pivot = set()
            try:
                report_name = response_data["result"]["name"]
                csv_data = response_data["result"]["data"]
                report_list_model_ip_pivot = ReportListModelIpPivot() 
                # Parse CSV data
                csv_data = csv_data.replace('\ni2n:3\r1', '')
                csv_file = StringIO(csv_data)
                if "No matching log data for this report" in csv_data:
                    reportModel.report_model_list_ip_pivot = []
                    reportModel.raw_report_model_ip = []
                    reportModel.report_name = report_name
                    reportModel.report_title = report_title
                    list_report_model.append(reportModel)
                    print(f'Skipping {report_name}')
                    continue  # Skip to the next report
                with csv_file as f:
                    for _ in range(1):
                        f.readline()
                    reader = csv.DictReader(f)
                    # Skip the header row (assuming it's always present)
                    for row in reader:
                        if(not row['ID'].strip().isdigit()):
                            continue
                        if any(row[field] is None for field in ['ID', 'log_date', 'srcip', 'dstport', 'Application', 'total']):
                            continue  # Skip 
                        list_report_raw_model.append(RawReportModel(
                            int(row['ID']),
                            row['log_date'],
                            row['srcip'],
                            row['dstport'],
                            row['Application'],
                            int(row['total'])
                        ))
                        if row['srcip'] in dict_ip_pivot.keys():
                            data_report_pivot: ReportModelIpPivot = dict_ip_pivot[row['srcip']]
                            data_report_pivot.total += int(row['total'])  # Increment the total
                            # Update the date_total dictionary, ensuring values are added, not replaced
                            if row['log_date'] in data_report_pivot.date_total:
                                data_report_pivot.date_total[row['log_date']] += int(row['total']) 
                            else:
                                data_report_pivot.date_total[row['log_date']] = int(row['total']) 
                            set_date_pivot.add(row['log_date'])
                        else:
                            report_model_ip_pivot = ReportModelIpPivot()
                            report_model_ip_pivot.ip = row['srcip']
                            report_model_ip_pivot.total = int(row['total'])
                            report_model_ip_pivot.date_total = {row['log_date']: int(row['total'])} 
                            dict_ip_pivot[row['srcip']] = report_model_ip_pivot
                            list_report_model_pivot.append(report_model_ip_pivot)
                            set_date_pivot.add(row['log_date'])
                    
                    if(list_report_model_pivot is not None):
                        list_report_model_pivot.sort(key=lambda x: x.total, reverse=True)
                        slice_end = len(list_report_model_pivot) if len(list_report_model_pivot) < 20 else 20
                        top_ip_total = list_report_model_pivot[:slice_end]
                        if 'Branch' in report_name:
                            for ip_pivot in top_ip_total:
                                ip = ip_pivot.ip.rsplit('.', 1)[0] + ".0/24"
                                branch_name = GLOBAL_CONSTANT.IP_OFFICE_MAPPING[ip]
                                ip_pivot.subnet_ip = ip
                                ip_pivot.subnet_branch = branch_name
                            report_list_model_ip_pivot.top_20_ip_pivot = top_ip_total
                           
                    reportModel.raw_report_model_ip = list_report_raw_model
                    reportModel.report_name = report_name
                    reportModel.report_title = report_title
                    report_list_model_ip_pivot.report_model_ip_pivot = list_report_model_pivot
                    sorted_date =sorted_date = sorted(list(set_date_pivot), key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
                    report_list_model_ip_pivot.list_date = sorted_date
                    reportModel.report_model_list_ip_pivot = report_list_model_ip_pivot
                    
                    
                    list_report_model.append(reportModel)
                    
                        

            except (KeyError, IndexError):
                print(f"Error extracting data for report: {report_name}")
        else:
            print(f"Error fetching report: {report_name}")

    return list_report_model