from django import forms
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Row, Column, HTML
from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from django_summernote.widgets import SummernoteWidget

from .models import Biography
from authors.models import BiographyAuthor


class BiographyForm(forms.ModelForm):
    class Meta:
        model = Biography
        fields = [
            "title",
            "slug",
            "lifespan",
            "body",
            "authors",
            "external_links",
            "revisions",
            "primary_country",
            "secondary_country",
            "south_georgia",
            "featured",
        ]
        widgets = {
            "body": SummernoteWidget(),
            "external_links": SummernoteWidget(attrs={"summernote": {"height": "240"}}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["authors"].label = "Displayed authors"
        self.helper = FormHelper()
        self.helper.form_tag = False

        bio_id = self.instance.pk if self.instance and self.instance.pk else ""

        self.helper.layout = Layout(
            "title",
            Row(
                Column("lifespan", css_class="form-group col-md-6 mb-0"),
                Column(
                    Field(
                        "slug",
                        hx_get="/biographies/validate_slug/",
                        hx_include="#bio_id",
                        hx_target="#slug-feedback",
                        hx_trigger="keyup changed delay:500ms",
                        hx_indicator="#slug-indicator",
                    ),
                    HTML(
                        f'<input type="hidden" name="bio_id" id="bio_id" value="{bio_id}">'
                    ),
                    HTML('<div class="d-flex align-items-center mt-1">'),
                    HTML(
                        '<div id="slug-indicator" class="htmx-indicator mr-2"><i class="fa fa-spinner fa-spin text-primary"></i></div>'
                    ),
                    HTML('<div id="slug-feedback"></div>'),
                    HTML("</div>"),
                    css_class="form-group col-md-6 mb-0",
                ),
                css_class="form-row",
            ),
            Div("body", css_class="form-field-body"),
            Row(
                Column(
                    FieldWithButtons(
                        "primary_country",
                        StrictButton(
                            '<i class="fa fa-plus"></i>',
                            type="button",
                            css_class="btn-outline-secondary",
                            data_toggle="modal",
                            data_target="#addCountryModal",
                            data_field="id_primary_country",
                        ),
                    ),
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    FieldWithButtons(
                        "secondary_country",
                        StrictButton(
                            '<i class="fa fa-plus"></i>',
                            type="button",
                            css_class="btn-outline-secondary",
                            data_toggle="modal",
                            data_target="#addCountryModal",
                            data_field="id_secondary_country",
                        ),
                    ),
                    css_class="form-group col-md-6 mb-0",
                ),
                css_class="form-row",
            ),
            Row(
                Column("south_georgia", css_class="form-group col-md-6 mb-0"),
                Column("featured", css_class="form-group col-md-6 mb-0"),
                css_class="form-row mt-2 mb-3",
            ),
            Div("external_links", css_class="form-field-summernote"),
            Div("revisions", css_class="form-field-revisions"),
        )


class BiographyAuthorForm(forms.ModelForm):
    class Meta:
        model = BiographyAuthor
        fields = ["id", "author", "author_position"]
        widgets = {
            "id": forms.HiddenInput(),
            "author_position": forms.HiddenInput(attrs={"class": "author-position"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["author"].label = ""
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "id",
            FieldWithButtons(
                "author",
                StrictButton(
                    '<i class="fa fa-plus"></i>',
                    type="button",
                    css_class="btn-outline-secondary",
                    data_toggle="modal",
                    data_target="#addAuthorModal",
                    onclick="setAuthorTargetField(this)",
                ),
            ),
            "author_position",
        )

    def has_changed(self):
        changed = super().has_changed()
        if (
            changed
            and set(self.changed_data) == {"author_position"}
            and not self.data.get(self.add_prefix("author"))
        ):
            self.changed_data.remove("author_position")
            return False
        return changed


BiographyAuthorFormSet = inlineformset_factory(
    Biography, BiographyAuthor, form=BiographyAuthorForm, extra=0, can_delete=True
)
