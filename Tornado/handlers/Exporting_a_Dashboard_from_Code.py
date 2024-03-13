from tornado.web import RequestHandler
from stimulsoft_reports import StiHandler
from stimulsoft_reports.report import StiReport
from stimulsoft_reports.report.enums import StiExportFormat


class IndexHandler(RequestHandler):
    def get(self):
        # Rendering an HTML template
        self.render('Exporting_a_Dashboard_from_Code.html', reportJavaScript = '', reportHtml = '')


class ExportHandler(RequestHandler):
    def get(self):
        # Creating a report object
        report = StiReport()

        # If the request processing was successful, you need to return the result to the client side
        if report.processRequest(self.request):
            return report.getFrameworkResponse(self)

        # Loading a dashboard by URL
        # This method does not load the report object on the server side, it only generates the necessary JavaScript code
        # The dashboard will be loaded into a JavaScript object on the client side
        reportUrl = self.static_url('reports/WebsiteAnalytics.mrt')
        report.loadFile(reportUrl)

        # Getting the export format passed in the GET request parameters
        requestFormat = self.get_argument('format')
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
        return self.render('Exporting_a_Dashboard_from_Code.html', reportJavaScript = js, reportHtml = html)
    
    def post(self):
        # A separate event handler is required to process POST requests
        handler = StiHandler()
        if handler.processRequest(self.request):
            return handler.getFrameworkResponse(self)
