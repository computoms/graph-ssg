from graphsitegen.build import Builder
import sys

Builder.from_args(sys.argv[1:]).run()