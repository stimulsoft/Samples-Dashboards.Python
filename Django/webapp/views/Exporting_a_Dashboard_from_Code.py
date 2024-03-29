from django.shortcuts import render
from django.templatetags.static import static
from stimulsoft_reports.report import StiReport
from stimulsoft_reports.report.enums import StiExportFormat


def index(request):
    # Rendering an HTML template
    return render(request, 'Exporting_a_Dashboard_from_Code.html')


def export(request):
    # Creating a report object
    report = StiReport()

    # If the request processing was successful, you need to return the result to the client side
    if report.processRequest(request):
        return report.getFrameworkResponse()

    # Loading a dashboard by URL
    # This method does not load the report object on the server side, it only generates the necessary JavaScript code
    # The dashboard will be loaded into a JavaScript object on the client side
    reportUrl = static('reports/WebsiteAnalytics.mrt')
    report.loadFile(reportUrl)

    # Getting the export format passed in the GET request parameters
    requestFormat = request.GET.get('format')
    exportFormat = StiExportFormat.DOCUMENT
    if requestFormat == 'pdf':
        exportFormat = StiExportFormat.PDF
    elif requestFormat == 'excel':
        exportFormat = StiExportFormat.EXCEL
    elif requestFormat == 'html':
        exportFormat = StiExportFormat.HTML

    # Calling the dashboard export to the specified format
    # This method does not export the dashboard on the server side, it only generates the necessary JavaScript code
    # The dashboard will be exported using a JavaScript engine on the client side
    report.exportDocument(exportFormat)
    
    # Getting the necessary JavaScript code and HTML part of the dashboard engine
    js = report.javascript.getHtml()
    html = report.getHtml()

    # Rendering an HTML template, inside which JavaScript and HTML code of the dashboard are displayed
    return render(request, 'Exporting_a_Dashboard_from_Code.html', {'reportJavaScript': js, 'reportHtml': html})
