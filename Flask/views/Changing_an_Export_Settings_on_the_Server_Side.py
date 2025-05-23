from flask import Blueprint, request, url_for
from stimulsoft_dashboards.export import StiPdfDashboardExportSettings
from stimulsoft_dashboards.export.enums import StiDashboardScaleMode
from stimulsoft_reports.events import StiExportEventArgs
from stimulsoft_reports.report import StiReport
from stimulsoft_reports.report.enums import StiExportFormat, StiPageOrientation
from stimulsoft_reports.viewer import StiViewer

Changing_an_Export_Settings_on_the_Server_Side = app = Blueprint('Changing_an_Export_Settings_on_the_Server_Side', __name__)


# The function will be called before exporting the dashboard
def beginExportReport(args: StiExportEventArgs):

    # You can change the file name of the exported dashboard
    args.fileName = 'MyExportedFileName.' + args.fileExtension

    # You can change export settings, the set of settings depends on the export type
    if args.format == StiExportFormat.PDF:
        settings: StiPdfDashboardExportSettings = args.settings
        settings.scaleMode = StiDashboardScaleMode.PAPER_SIZE
        settings.orientation = StiPageOrientation.LANDSCAPE


@app.route('/Changing_an_Export_Settings_on_the_Server_Side', methods = ['GET', 'POST'])
def index():
    # Creating a viewer object
    viewer = StiViewer()
    viewer.javascript.appendHead('<link rel="shortcut icon" href="' + url_for('static', filename = 'favicon.ico') + '" type="image/x-icon">')

    # Defining viewer events
    # When assigning a function name as a string, it will be called on the JavaScript client side
    # When assigning a function itself, it will be called on the Python server side
    viewer.onBeginExportReport += beginExportReport

    # If the request processing was successful, you need to return the result to the client side
    if viewer.processRequest(request):
        return viewer.getFrameworkResponse()
    
    # Creating a report object
    report = StiReport()

    # Loading a dashboard by URL
    # This method does not load the report object on the server side, it only generates the necessary JavaScript code
    # The dashboard will be loaded into a JavaScript object on the client side
    reportUrl = url_for('static', filename = 'reports/WebsiteAnalytics.mrt')
    report.loadFile(reportUrl)

    # Assigning a report object to the viewer
    viewer.report = report

    # Displaying the visual part of the viewer as a prepared HTML page
    return viewer.getFrameworkResponse()
