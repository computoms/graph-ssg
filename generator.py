import model as modellib
import htmlutils

def generate():
	model = modellib.Model()
	html_generator = htmlutils.HtmlGenerator(model)
	articles = model.get_articles()
	print(str(len(articles)) + " articles changed.")
	for article in articles:
		html_generator.generate_article(article)

generate()