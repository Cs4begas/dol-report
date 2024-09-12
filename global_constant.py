import datetime


class GLOBAL_CONSTANT:
    SESSION_ID = ''
    FORTIANALYZER_URL_JSONRPC = 'https://172.16.222.101:10443/jsonrpc'
    NO_MATCHING_MESSAGE = 'No matching log data for this report'
    START_TIME:datetime 
    END_TIME:datetime
    SSH_REPORTS = [
        "RptReportCKMoo_PortSSH_Branch",
        "RptReportCKMoo_PortSSH_DOL2",
        "RptReportCKMoo_PortSSH_GC",
        "RptReportCKMoo_PortSSH_PK",
        "RptReportCKMoo_PortSSH_Server"
    ]

    TELNET_REPORTS = [
        "RptReportCKMoo_PortTelnet_Branch",
        "RptReportCKMoo_PortTelNet_DOL2",
        "RptReportCKMoo_PortTelNet_GC",
        "RptReportCKMoo_PortTelNet_PK",
        "RptReportCKMoo_PortTelNet_Server"
    ]

    SMB_REPORTS = [
        "RptReportCKMoo_PortSMB_Branch",
        "RptReportCKMoo_PortSMB_DOL2",
        "RptReportCKMoo_PortSMB_GC",
        "RptReportCKMoo_PortSMB_PK",
        "RptReportCKMoo_PortSMB_Server"
    ]

    RDP_REPORTS = [
        "RptReportCKMoo_PortRDP_Branch",
        "RptReportCKMoo_PortRDP_DOL2",
        "RptReportCKMoo_PortRDP_GC",
        "RptReportCKMoo_PortRDP_PK",
        "RptReportCKMoo_PortRDP_Server"
    ]
    
    REPORT_TYPES = {
        "SSH": SSH_REPORTS,
        "TELNET": TELNET_REPORTS,
        "SMB": SMB_REPORTS,
        "RDP": RDP_REPORTS
    }