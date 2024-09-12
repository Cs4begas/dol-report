from model.raw_report_model import RawReportModel
from model.report_model_ip_pivot import ReportModelIpPivot


class ReportModel :
    report_title : str
    report_name : str
    raw_report_model_ip : list[RawReportModel]
    report_model_ip_pivot : list[ReportModelIpPivot]