try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

import pytest

from ckan.lib.base import render_snippet


@pytest.mark.usefixtures("with_request_context")
def test_measurement_technique_keeps_curie_link_without_live_lookup():
    curie = "http://purl.obolibrary.org/obo/CHMO_0000001"
    field = {
        "field_name": "measurement_technique",
        "display_property": "http://schema.org/measurementTechnique",
    }
    data = {
        "measurement_technique": "NMR spectroscopy",
        "measurement_technique_iri": curie,
    }

    with patch("ckanext.scheming.helpers.requests.get") as get:
        html = render_snippet(
            "scheming/display_snippets/hyperlink_mT.html",
            field=field,
            data=data,
        )

    assert 'href="{}"'.format(curie) in html
    assert "NMR spectroscopy" in html
    assert curie in html
    get.assert_not_called()
