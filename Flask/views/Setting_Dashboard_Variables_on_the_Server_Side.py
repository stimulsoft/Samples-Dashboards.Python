from datetime import datetime
from flask import Blueprint, request, url_for
from stimulsoft_reports.events import StiVariablesEventArgs
from stimulsoft_reports.report import StiReport
from stimulsoft_reports.viewer import StiViewer

Setting_Dashboard_Variables_on_the_Server_Side = app = Blueprint('Setting_Dashboard_Variables_on_the_Server_Side', __name__)


# The function will be called before building the dashboard when preparing the values of variables
def prepareVariables(args: StiVariablesEventArgs):

    # You can set the values of the dashboard variables, the value types must match the original types
    # If the variable contained an expression, the already calculated value will be passed
    if len(args.variables) > 0:
        args.variables['Patient'].value = 'Mary Roe'
        args.variables['Observation'].value = datetime(2024, 3, 1, 0, 0, 0)
        args.variables['Visits'].value = 5


@app.route('/Setting_Dashboard_Variables_on_the_Server_Side', methods = ['GET', 'POST'])
def index():
    # Creating a viewer object and defining Python events
    viewer = StiViewer()
    viewer.onPrepareVariables += prepareVariables

    # If the request processing was successful, you need to return the result to the client side
    if viewer.processRequest(request):
        return viewer.getFrameworkResponse()
    
    # Creating a report object and loading a dashboard by URL
    report = StiReport()
    reportUrl = url_for('static', filename = 'reports/PatientHealthKPI.mrt')
    report.loadFile(reportUrl)

    # Assigning a report object to the viewer
    viewer.report = report

    # Displaying the visual part of the viewer as a prepared HTML page
    return viewer.getFrameworkResponse()
