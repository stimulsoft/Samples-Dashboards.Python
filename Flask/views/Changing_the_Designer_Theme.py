from flask import Blueprint, request, url_for
from stimulsoft_reports.report import StiReport
from stimulsoft_reports.designer import StiDesigner, enums

Changing_the_Designer_Theme = app = Blueprint('Changing_the_Designer_Theme', __name__)


@app.route('/Changing_the_Designer_Theme', methods = ['GET', 'POST'])
def index():
    # Creating a designer object
    designer = StiDesigner()
    designer.javascript.appendHead('<link rel="shortcut icon" href="' + url_for('static', filename = 'favicon.ico') + '" type="image/x-icon">')

    # Defining designer options: interface theme
    designer.options.appearance.theme = enums.StiDesignerTheme.OFFICE_2022_BLACK_GREEN

    # If the request processing was successful, you need to return the result to the client side
    if designer.processRequest(request):
        return designer.getFrameworkResponse()
    
    # Creating a report object
    report = StiReport()

    # Loading a dashboard by URL
    # This method does not load the report object on the server side, it only generates the necessary JavaScript code
    # The dashboard will be loaded into a JavaScript object on the client side
    reportUrl = url_for('static', filename = 'reports/WebsiteAnalytics.mrt')
    report.loadFile(reportUrl)

    # Assigning a report object to the designer
    designer.report = report

    # Displaying the visual part of the designer as a prepared HTML page
    return designer.getFrameworkResponse()
