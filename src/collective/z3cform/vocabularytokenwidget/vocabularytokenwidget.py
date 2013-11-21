# -*- coding: utf-8 -*-

import zope.component
import zope.interface
import zope.schema

from z3c.form import interfaces
from z3c.form import widget
from z3c.form.browser import textarea
from Products.Five.browser import BrowserView
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from collective.z3cform.vocabularytokenwidget.interfaces import IVocabularyTokenWidget
from collective.z3cform.widgets.interfaces import ILayer
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import json


class ExportVocabularyAsJSON(BrowserView):
    """Return JSON search results for jQuery Tokeninput
    for more information, see: http://loopj.com/jquery-tokeninput/#installation--setup
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.request.response.setHeader("Content-type", "application/json")
        vocab = getUtility(IVocabularyFactory,
                            name=self.request.get('vocabulary'))(self.context)
        
        if 'q' in self.request.keys():
            query = self.request['q']
            keys = [(k.value, k.title) for k in vocab if (
                        query.lower() in k.title.lower())]
        else:
            keys = []

        # we will return up to 10 tokens only
        tokens = map(self._tokenize, keys[:10])
        return json.dumps(tokens)

    def _tokenize(self, value_title):
        value, title = value_title
        if isinstance(value, str):
            value = value.decode('utf-8')
            title = title.decode('utf-8')

        return {'id': '%s' % value.replace(u"'", u"\\'"),
                'name': '%s' % title.replace(u"'", u"\\'")}


class VocabularyTokenWidget(textarea.TextAreaWidget):
    """Widget for adding new keywords and autocomplete with the ones in the
    system."""
    zope.interface.implementsOnly(IVocabularyTokenWidget)
    klass = u"vocabulary-token-widget"
    display_template = ViewPageTemplateFile('vocabularytoken_display.pt')
    input_template = ViewPageTemplateFile('vocabularytoken_input.pt')

    # JavaScript template
    js_template = u"""\
    (function($) {
        $().ready(function() {
            var newValues = '%(newtags)s';
            var oldValues = [%(oldtags)s];
            $('#%(id)s').data('klass','%(klass)s');
            vocabularyTokenInputActivate('%(id)s', newValues, oldValues);
        });
    })(jQuery);
    """
    def __init__(self, request, vocabulary=None, indexName='Subject'):
        super(VocabularyTokenWidget, self).__init__(request)
        self.vocabulary = vocabulary
        self.indexName = indexName

    def js(self):
        if not ILayer.providedBy(self.request):
            return ""
        try:
            old_values = self.field.get(self.context)
        except:
            old_values = []

        old_tags = u""
        index = 0
        if self.vocabulary:
            newtags = self.context.absolute_url() + "/json-vocabulary?vocabulary=%s" % (self.vocabulary)
        elif self.indexName:
            newtags = self.context.portal_catalog.getUniqueValuesFor(self.indexName)
        #prepopulate
        for index, value in enumerate(old_values):
            if isinstance(value, str):
                value = value.decode("utf-8")
            old_tags += u"{id: '%s', name: '%s'}" % (value.replace(
                u"'", u"\\'"), value.replace(u"'", u"\\'"))
            if index < len(old_values) - 1:
                old_tags += ", "
        result = self.js_template % dict(
            id=self.id,
            klass=self.klass,
            newtags=newtags,
            oldtags=old_tags
        )
        return result

    def render(self):
        if self.mode == interfaces.DISPLAY_MODE:
            return self.display_template(self)
        else:
            return self.input_template(self)


@zope.interface.implementer(interfaces.IFieldWidget)
def VocabularyTokenFieldWidget(field, request):
    """IFieldWidget factory for TokenInputWidget."""
    vocabulary = field.value_type.vocabularyName
    return widget.FieldWidget(field, VocabularyTokenWidget(request,
        vocabulary=vocabulary))

