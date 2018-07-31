# Use thuis to perform a local rebuild of asciidoc files so they can be
# viewd in-tree without publishing.

from waflib import Task
from waflib.TaskGen import extension


@extension('.txt')
def run_asciidoc(self, node):
	out = node.change_ext(".html")
	if 'white-papers' in node.abspath():
		tsk = self.create_task("asciidoc_simple", node, [out])
	else:
		tsk = self.create_task("asciidoc", node, [out])
	tsk.cwd = node.parent.get_bld().abspath()


class asciidoc(Task.Task):
	color   = "BLUE"
	run_str = '${BIN_ASCIIDOC} -b html5 -a linkcss ${ASCIIDOC_FLAGS} -o ${TGT[0].name} ${SRC[0].abspath()}'
	ext_out = ".html"


class asciidoc_simple(Task.Task):
	color   = "BLUE"
	run_str = '${BIN_ASCIIDOC} -o ${TGT[0].name} ${SRC[0].abspath()}'
	ext_out = ".html"


def configure(ctx):
	ctx.find_program("asciidoc", var="BIN_ASCIIDOC", mandatory=True)


def build(ctx):
	www_source = ctx.path.ant_glob("**/*.txt")
	img_source = [x.name for x in ctx.path.ant_glob('**/*.png')] + ["asciidoc.js", "asciidoc.css", "favicon.ico"] \
		+ [x.relpath() for x in ctx.path.find_node('white-papers').ant_glob('**', excl=['**/*.txt','**/TODO'])]

	ctx(
		target	= "www",
		source	= www_source,
	)

	# Copy static data so pages can be viewed in build/
	ctx(
		features	= "subst",
		is_copy		= True,
		source		= img_source,
		target		= img_source,
	)

	ctx.install_files(ctx.env.PREFIX, img_source + [x.change_ext(".html") for x in www_source], cwd=ctx.bldnode, relative_trick=True)
