import model

class TestingModel:
	def __init__(self):
		self.content = []
		self.saved_content = {}

	def get_source_content(self, name):
		return self.content

	def save(self, name, content):
		self.saved_content[name] = content

	def get_articles(self, only_changed=True):
		articles = ['A', 'B', 'C']
		return [model.Article(f, self) for f in articles]



def parse_validarticle_returnsvalidtitle():
	m = TestingModel()
	m.content = ['{"Title": "TestTitle", "Abstract": "", "Parents": [], "Children": []}', 'Some content']
	a = model.Article('Test', m)
	assert(a.get_title() == 'TestTitle')

def parse_validarticle_returnsvalidparents():
	m = TestingModel()
	m.content = ['{"Title": "TestTitle", "Abstract": "", "Parents": ["Parent01", "Parent02"], "Children": []}', 'Some content']
	a = model.Article('Test', m)
	assert(len(a.get_parents()) == 2)

def parse_validarticle_returnsvalidchildren():
	m = TestingModel()
	m.content = ['{"Title": "TestTitle", "Abstract": "", "Parents": [], "Children": ["Children01"]}', 'Some content']
	a = model.Article('Test', m)
	assert(len(a.get_children()) == 1)

def parse_validarticle_returnsvalidcontent():
	m = TestingModel()
	m.content = ['{"Title": "TestTitle", "Abstract": "", "Parents": ["Parent01", "Parent02"], "Children": []}', 'Some content']
	a = model.Article('Test', m)
	assert(a.get_content() == 'Some content')

def savesource_validarticle_correctlyformatssource():
	m = TestingModel()
	m.content = ['{"Title": "TestTitle", "Abstract": "", "Parents": ["Parent01", "Parent02"], "Children": []}', 'Some content']
	a = model.Article('Test', m)
	a.save_source()
	assert(m.saved_content['Test'] == '{"Abstract": "", "Parents": ["Parent01", "Parent02"], "Children": [], "Title": "TestTitle"}\nSome content')

def model_getarticles_validsyntax():
	m = TestingModel()
	m.content = ['{"Title": "TestTitle", "Abstract": "", "Parents": ["Parent01", "Parent02"], "Children": []}', 'Some content']
	assert(len(m.get_articles()) == 3)



parse_validarticle_returnsvalidtitle()
parse_validarticle_returnsvalidparents()
parse_validarticle_returnsvalidchildren()
parse_validarticle_returnsvalidcontent()
savesource_validarticle_correctlyformatssource()
model_getarticles_validsyntax()