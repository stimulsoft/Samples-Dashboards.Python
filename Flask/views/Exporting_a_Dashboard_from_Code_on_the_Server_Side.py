from flask import Blueprint, request, render_template, url_for
from stimulsoft_reports.report import StiReport
from stimulsoft_reports.report.enums import StiEngineType, StiExportFormat

Exporting_a_Dashboard_from_Code_on_the_Server_Side = app = Blueprint('Exporting_a_Dashboard_from_Code_on_the_Server_Side', __name__)


@app.route('/Exporting_a_Dashboard_from_Code_on_the_Server_Side', methods = ['GET', 'POST'])
def index():
    # Defining the HTML page title
    title = 'Exporting a Dashboard from Code on the Server-Side'

    # Creating a report object
    report = StiReport()

    # Setting the server-side rendering mode
    report.engine = StiEngineType.SERVER_NODE_JS

    # If the request processing was successful, you need to return the result to the client side
    if report.processRequest(request):
        return report.getFrameworkResponse()
    
    # Loading a dashboard by URL
    # This method loads a dashboard file and stores it as a compressed string in an object.
    # The dashboard will be loaded from this string into a JavaScript object when using Node.js
    reportUrl = url_for('static', filename = 'reports/WebsiteAnalytics.mrt')
    report.loadFile(reportUrl, True)

    # Calling the dashboard export method. Export is also performed using Node.js engine.
    # This method will return the byte data of the exported document, or save it to a file.
    result = report.exportDocument(StiExportFormat.PDF)
    # result = report.exportDocument(StiExportFormat.PDF, filePath=url_for('static', filename = 'reports/WebsiteAnalytics.pdf'))

    if result != False:
        message = f'The exported document takes {len(result)} bytes.'
    else:
        # If there is a build error, you can display the error text.
        message = report.nodejs.error

    # Rendering an HTML template with a text message as the server response.
    return render_template('Server_Side_Message.html', title = title, message = message)
