from waflib import Task
from waflib.TaskGen import extension


@extension('.txt')
def run_asciidoc(self, node):
	out = node.change_ext(".html")
	tsk = self.create_task("asciidoc", node, [out])
	tsk.cwd = node.parent.get_bld().abspath()


class asciidoc(Task.Task):
	color   = "BLUE"
	run_str = '${BIN_ASCIIDOC} -b html5 -a linkcss ${ASCIIDOC_FLAGS} -o ${TGT[0].name} ${SRC[0].abspath()}'
	ext_out = ".html"


def configure(ctx):
	ctx.find_program("asciidoc", var="BIN_ASCIIDOC", mandatory=True)


def build(ctx):
	www_source = ctx.path.ant_glob("*.txt")
	img_source = [x.name for x in ctx.path.ant_glob('*.png')] + ["asciidoc.css", "favicon.ico"]

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

	ctx.install_files(ctx.env.PREFIX, img_source + [x.change_ext(".html").name for x in www_source])
