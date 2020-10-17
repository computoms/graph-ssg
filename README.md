# Graph Navigation

Graph Navigation is a small project to create a tool that can generate static html pages that are ordered as a graph of information. 

Each article generate is appended to the graph thanks to its `Parents` and `Children` articles. This provides an easy navigation as well as an easy understanding of how the articles are linked together.  

Each article, stored under the `content/` folder is name with its title in a markdown format. It contains a JSON front-matter, describing its position in the graph (Parents, Children) as well as some extra information.
