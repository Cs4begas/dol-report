from datetime import datetime
import pandas as pd
from global_constant import GLOBAL_CONSTANT
from model.report_model import ReportModel

# ... (Assume you have 'list_report_model' containing your data)

def create_excel_report(list_report_model:list[ReportModel]):

    # Extract data for the first sheet (RawReportModel)
    for report_model in list_report_model:
        # Extract data for the raw data sheet (now using raw_report_model_ip)
        raw_data = []
        for raw_model_ip in report_model.raw_report_model_ip:
            # Filter out non-SMB data if the report is an SMB report
            if "SMB" in report_model.report_title and raw_model_ip.application.upper() != "SMB":
                continue 

            raw_data.append({
                'ID': raw_model_ip.id,
                'log_date': raw_model_ip.log_date,
                'srcip': raw_model_ip.scr_ip,
                'dstport': raw_model_ip.dst_port,
                'Application': raw_model_ip.application,
                'total': raw_model_ip.total
            })

        # Create DataFrame for the raw data sheet
        df_raw = pd.DataFrame(raw_data)

        # Extract data for the pivot sheet
        pivot_data = []
        for pivot_model in report_model.report_model_ip_pivot:
            row = {'ip': pivot_model.ip}
            sorted_dates = sorted(pivot_model.date_total.keys(), key=lambda x: datetime.strptime(x, '%Y-%m-%d'))
            for date in sorted_dates:
                total = pivot_model.date_total[date]
            row[date] = total  # Add date columns dynamically

            pivot_data.append(row)  # Append row before calculating Sum_total

        df_pivot = pd.DataFrame(pivot_data)
        # Sort DataFrame by 'ip' and then by date columns
        if not df_pivot.empty:
            df_pivot['Sum_total'] = df_pivot.iloc[:, 1:-1].sum(axis=1) 

        # Create Excel writer with dynamic filename per report
        filename = f"({GLOBAL_CONSTANT.START_TIME.strftime('%Y-%m-%d')} to {GLOBAL_CONSTANT.END_TIME.strftime('%Y-%m-%d')}) {report_model.report_title}.xlsx"

        with pd.ExcelWriter(filename) as writer:
            # Write data to the raw data sheet
            df_raw.to_excel(writer, sheet_name='Raw Data', index=False)

            # Write data to the pivot sheet
            df_pivot.to_excel(writer, sheet_name='Pivot Data', index=False)

            # Auto-adjust column widths for both sheets
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                for column in worksheet.columns:
                    max_length = 0
                    column = [cell for cell in column]
                    for cell in column:
                        try: 
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                        except:
                            pass
                    adjusted_width = (max_length + 2) 
                    worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
        print(f"Excel report '{filename}' created successfully!")