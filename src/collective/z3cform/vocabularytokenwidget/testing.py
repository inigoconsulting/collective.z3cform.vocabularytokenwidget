from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import collective.z3cform.vocabularytokenwidget


COLLECTIVE_Z3CFORM_VOCABULARYTOKENWIDGET = PloneWithPackageLayer(
    zcml_package=collective.z3cform.vocabularytokenwidget,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.z3cform.vocabularytokenwidget:testing',
    name="COLLECTIVE_Z3CFORM_VOCABULARYTOKENWIDGET")

COLLECTIVE_Z3CFORM_VOCABULARYTOKENWIDGET_INTEGRATION = IntegrationTesting(
    bases=(COLLECTIVE_Z3CFORM_VOCABULARYTOKENWIDGET, ),
    name="COLLECTIVE_Z3CFORM_VOCABULARYTOKENWIDGET_INTEGRATION")

COLLECTIVE_Z3CFORM_VOCABULARYTOKENWIDGET_FUNCTIONAL = FunctionalTesting(
    bases=(COLLECTIVE_Z3CFORM_VOCABULARYTOKENWIDGET, ),
    name="COLLECTIVE_Z3CFORM_VOCABULARYTOKENWIDGET_FUNCTIONAL")
