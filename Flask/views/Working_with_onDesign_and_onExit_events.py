import json
import os
from flask import Blueprint, request, render_template, url_for
from stimulsoft_reports import StiResult
from stimulsoft_reports.events import StiReportEventArgs
from stimulsoft_reports.report import StiReport
from stimulsoft_reports.viewer import StiViewer
from stimulsoft_reports.viewer.enums import StiToolbarDisplayMode
from stimulsoft_reports.designer import StiDesigner

Working_with_onDesign_and_onExit_events = app = Blueprint('Working_with_onDesign_and_onExit_events', __name__)


# The function will be called when saving the dashboard (both manual and automatic)
def saveReport(args: StiReportEventArgs):

    # Getting the absolute path to the dashboard file to save
    filePath = os.path.normpath(os.getcwd() + url_for('static', filename = 'reports/' + args.fileName))
    
    try:
        # Opening the file for saving, converting the dashboard to JSON and saving it
        with open(filePath, mode='w', encoding='utf-8') as file:
            jsonReport = json.dumps(args.report, indent = 4)
            file.write(jsonReport)
            file.close()
    except Exception as e:
        # In case of an error, the error message is passed to the designer
        return StiResult.getError(str(e))

    # If the save is successful, a message can be displayed
    # If the message is not required, do not return the result, or return None
    return f'The dashboard was successfully saved to a {args.fileName} file.'


@app.route('/Working_with_onDesign_and_onExit_events', methods = ['GET', 'POST'])
def index():
    # Creating a viewer object, defining JavaScript events, defining options (setting the full-screen and toolbar mode, show design button)
    viewer = StiViewer()
    viewer.onDesignReport += 'viewerDesign'
    viewer.options.appearance.fullScreenMode = True
    viewer.options.toolbar.showDesignButton = True
    viewer.options.toolbar.displayMode = StiToolbarDisplayMode.SEPARATED

    # If the request processing was successful, you need to return the result to the client side
    if viewer.processRequest(request):
        return viewer.getFrameworkResponse()
    
    # Creating a report object and loading a dashboard by URL
    report = StiReport()
    reportUrl = url_for('static', filename = 'reports/WebsiteAnalytics.mrt')
    report.loadFile(reportUrl)

    # Assigning a report object to the viewer
    viewer.report = report

    # Getting the necessary JavaScript code and visual HTML part of the viewer
    js = viewer.javascript.getHtml()
    html = viewer.getHtml()

    # Rendering an HTML template, inside which JavaScript and HTML code of the viewer are displayed
    return render_template('Working_with_onDesign_and_onExit_events.html', componentJavaScript = js, componentHtml = html)


@app.route('/Working_with_onDesign_and_onExit_events/designer', methods = ['GET', 'POST'])
def designer():
    # Creating a designer object, defining JavaScript and Python events, defining options (setting the full-screen and toolbar mode, show exit menu item)
    designer = StiDesigner()
    designer.onExit += 'designerExit'
    designer.onSaveReport += saveReport
    designer.options.appearance.fullScreenMode = True
    designer.options.toolbar.showFileMenuExit = True

    # If the request processing was successful, you need to return the result to the client side
    if designer.processRequest(request):
        return designer.getFrameworkResponse()
    
    # Creating a report object and loading a dashboard by URL
    report = StiReport()
    reportUrl = url_for('static', filename = 'reports/WebsiteAnalytics.mrt')
    report.loadFile(reportUrl)

    # Assigning a report object to the designer
    designer.report = report

    # Getting the necessary JavaScript code and visual HTML part of the designer
    js = designer.javascript.getHtml()
    html = designer.getHtml()

    # Rendering an HTML template, inside which JavaScript and HTML code of the designer are displayed
    return render_template('Working_with_onDesign_and_onExit_events.html', componentJavaScript = js, componentHtml = html)
