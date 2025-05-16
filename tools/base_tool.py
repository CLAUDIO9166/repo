class BaseTool:
    name = ""
    description = ""

    def _run(self, *args, **kwargs):
        raise NotImplementedError("Você precisa implementar o método _run().")
