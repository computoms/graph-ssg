# Graph Static Site Generator

`graph-ssg` is a small python program aimed at generating static html pages ordered in the form of a graph of articles.

Each article generated is appended to the graph thanks to its `Parents` and `Children` articles. This provides an easy navigation as well as an easy understanding of how the articles are linked together.  

Each article, is named with its title in a markdown format. It contains a JSON front-matter, describing its position in the graph (Parents, Children) as well as some extra information.

An example is available on [computoms.com](http://computoms.com).


## Usage

You can use this program by running the following command:
`python build.py -f "/path/to/settings.json"`

Before running the command, you must create a file `settings.json` that contains the following information:

```json
{
	"input": "/path/to/article/sources/",
	"output": "/path/to/output/directory/",
	"templates": "/path/to/template/directory/"
}
```

The source directory contains the articles in markdown format. In the template directory, you should create these three template files:

* `index.html`: main website page
* `map_template.html`: template page for the full-graph view of the articles
* `page_template.html`: template for an article
* `news_template.html`: template page for the news (article ordered by publication date)

The front matter of an article is a json object that is constructed as follows:

```json
{
	"Title": "Article title",
	"Abstract": "Article abstract",
	"Parents": ["Parent1", "Parent2"],
	"Children": ["Children1", "Children2"],
	"Date": "2020-04-01"
}

```

## Example

You can find an example under the `example` sub-folder of the source directory. Running `python build.py -f "./example/settings.json"` will generate the pages into the `./example/output/` directory.