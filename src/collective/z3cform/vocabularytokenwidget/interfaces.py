from zope.interface import Interface
from z3c.form import interfaces

class ILayer(Interface):
    pass

class IVocabularyTokenWidget(interfaces.ITextLinesWidget):
    """Text lines widget."""
