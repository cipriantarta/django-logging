from logging import FileHandler


class InfoFileHandler(FileHandler):
    def emit(self, record):
        pass


class ErrorFileHandler(FileHandler):
    def emit(self, record):
        pass


class DebugFileHandler(FileHandler):
    def emit(self, record):
        pass
