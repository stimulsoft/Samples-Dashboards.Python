from django.shortcuts import render
from django.templatetags.static import static
from stimulsoft_reports.report import StiReport
from stimulsoft_reports.designer import StiDesigner


def index(request):
	# Creating a designer object
	designer = StiDesigner()

	# If the request processing was successful, you need to return the result to the client side
	if designer.processRequest(request):
		return designer.getFrameworkResponse()
	
	# Creating a report object and loading a dashboard by URL
	report = StiReport()
	reportUrl = static('reports/WebsiteAnalytics.mrt')
	report.loadFile(reportUrl)

	# Assigning a report object to the designer
	designer.report = report

	# Getting the necessary JavaScript code and visual HTML part of the designer
	js = designer.javascript.getHtml()
	html = designer.getHtml()

	# Rendering an HTML template, inside which JavaScript and HTML code of the designer are displayed
	return render(request, 'Editing_a_Dashboard_Template_in_the_Designer_in_an_HTML_template.html', {'designerJavaScript': js, 'designerHtml': html})