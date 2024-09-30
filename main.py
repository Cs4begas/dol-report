from global_constant import GLOBAL_CONSTANT
from service.excel_service import create_excel_report
from service.file_service import directory_handle
from service.gen_report import get_list_of_report, get_report_data
from service.login import login_fotianalyzer


if __name__ == "__main__":
    login_response:dict = login_fotianalyzer()
    report_tid_maps = get_list_of_report()
    report_data_map = get_report_data(report_tid_maps)
    create_excel_report(report_data_map)
    directory_handle()
    