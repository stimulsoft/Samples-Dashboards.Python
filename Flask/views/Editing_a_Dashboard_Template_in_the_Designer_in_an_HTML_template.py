from flask import Blueprint, request, render_template, url_for
from stimulsoft_reports.report import StiReport
from stimulsoft_reports.designer import StiDesigner

Editing_a_Dashboard_Template_in_the_Designer_in_an_HTML_template = app = Blueprint('Editing_a_Dashboard_Template_in_the_Designer_in_an_HTML_template', __name__)


@app.route('/Editing_a_Dashboard_Template_in_the_Designer_in_an_HTML_template', methods = ['GET', 'POST'])
def index():
    # Creating a designer object
    designer = StiDesigner()

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

    # Getting the necessary JavaScript code and visual HTML part of the designer
    js = designer.javascript.getHtml()
    html = designer.getHtml()

    # Rendering an HTML template, inside which JavaScript and HTML code of the designer are displayed
    return render_template('Editing_a_Dashboard_Template_in_the_Designer_in_an_HTML_template.html', designerJavaScript = js, designerHtml = html)
